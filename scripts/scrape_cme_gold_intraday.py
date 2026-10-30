#!/usr/bin/env python3
"""
CME Gold Futures (GC) Free Intraday Scraper
===========================================
Scrapes high-frequency intraday data for CME COMEX Gold Futures (GC=F, MGC=F)
from public financial backends with zero API fees, no authentication required.

Features:
- Fetches 1-minute, 2-minute, 5-minute, 15-minute, 1-hour intraday bars.
- Extracts Open, High, Low, Close, Volume, and nanosecond/microsecond timestamps.
- Computes high-frequency microstructure metrics:
    * Corwin-Schultz Bid-Ask Spread Estimator (from High/Low pairs)
    * Realized Intraday Volatility
    * Volume Weighted Average Price (VWAP)
- Exports directly to Parquet and CSV in data/ directory.

Usage:
  python3 scripts/scrape_cme_gold_intraday.py --symbol GC=F --interval 1m --range 7d
  python3 scripts/scrape_cme_gold_intraday.py --symbol MGC=F --interval 5m --range 30d
"""

import sys
import argparse
import urllib.request
import urllib.error
import http.cookiejar
import json
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class YahooSession:
    """Manages Yahoo Finance authenticated session cookies and crumbs."""
    def __init__(self):
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        self.crumb = None
        self._authenticate()

    def _authenticate(self):
        """Fetch session cookie from fc.yahoo.com and extract API crumb."""
        try:
            # 1. Obtain A3 cookie
            try:
                self.opener.open(urllib.request.Request("https://fc.yahoo.com", headers=self.headers), timeout=6)
            except urllib.error.HTTPError:
                pass  # Sets the A3 session cookie even on 404

            # 2. Extract crumb
            crumb_req = urllib.request.Request("https://query2.finance.yahoo.com/v1/test/getcrumb", headers=self.headers)
            crumb_resp = self.opener.open(crumb_req, timeout=6)
            self.crumb = crumb_resp.read().decode("utf-8").strip()
            print(f"[✓] Yahoo Session Authenticated (Crumb: {self.crumb})")
        except Exception as e:
            print(f"[!] Warning acquiring crumb: {e}. Will attempt fallback direct query.")

    def get_chart_json(self, symbol: str, interval: str, range_str: str) -> dict:
        """Fetch chart data with crumb."""
        crumb_param = f"&crumb={self.crumb}" if self.crumb else ""
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval={interval}&range={range_str}{crumb_param}"
        req = urllib.request.Request(url, headers=self.headers)
        with self.opener.open(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))


def fetch_yahoo_intraday(symbol: str = "GC=F", interval: str = "1m", range_str: str = "7d") -> tuple:
    """Fetch high-frequency intraday bars for CME Gold Futures."""
    session = YahooSession()
    print(f"[*] Querying zero-cost endpoint for {symbol} (interval: {interval}, range: {range_str})...")

    try:
        data = session.get_chart_json(symbol, interval, range_str)
    except Exception as e:
        print(f"[!] Error fetching data: {e}")
        sys.exit(1)

    result = data["chart"]["result"][0]
    meta = result.get("meta", {})
    timestamps = result.get("timestamp", [])
    quotes = result.get("indicators", {}).get("quote", [{}])[0]

    if not timestamps or not quotes:
        print(f"[!] No price bars returned for symbol {symbol}")
        sys.exit(1)

    df = pd.DataFrame({
        "ts_event": [datetime.fromtimestamp(ts, tz=timezone.utc) for ts in timestamps],
        "open": quotes.get("open", []),
        "high": quotes.get("high", []),
        "low": quotes.get("low", []),
        "close": quotes.get("close", []),
        "volume": quotes.get("volume", []),
    })

    # Drop nulls (e.g. market closure pauses)
    df = df.dropna().reset_index(drop=True)
    df["symbol"] = symbol
    df["currency"] = meta.get("currency", "USD")

    print(f"[✓] Successfully scraped {len(df):,} intraday bars for {symbol}")
    return df, meta


def compute_microstructure_intraday(df: pd.DataFrame) -> pd.DataFrame:
    """Compute High-Frequency Spread & Microstructure metrics."""
    # 1. Bar VWAP = (High + Low + Close) / 3 * Volume / Volume
    typical_price = (df["high"] + df["low"] + df["close"]) / 3.0
    df["typical_price"] = typical_price
    df["dollar_volume"] = typical_price * df["volume"]
    cum_vol = df["volume"].cumsum()
    cum_dollar = df["dollar_volume"].cumsum()
    df["vwap"] = np.where(cum_vol > 0, cum_dollar / cum_vol, typical_price)

    # 2. Corwin-Schultz High-Low Spread Estimator (Microstructure standard for tick-less data)
    # Estimates effective bid-ask spread from 2-consecutive high-low price ratios
    high = df["high"].values
    low = df["low"].values
    spreads = [np.nan]

    for i in range(1, len(df)):
        h1, l1 = high[i-1], low[i-1]
        h2, l2 = high[i], low[i]
        if l1 <= 0 or l2 <= 0 or h1 <= 0 or h2 <= 0:
            spreads.append(np.nan)
            continue

        gamma = (np.log(max(h1, h2) / min(l1, l2))) ** 2
        beta = (np.log(h1 / l1)) ** 2 + (np.log(h2 / l2)) ** 2
        alpha = (np.sqrt(2 * beta) - np.sqrt(beta)) / (3 - 2 * np.sqrt(2)) - np.sqrt(gamma / (3 - 2 * np.sqrt(2)))

        if alpha > 0:
            s = 2 * (np.exp(alpha) - 1) / (1 + np.exp(alpha))
            spreads.append(s * df["close"].iloc[i])
        else:
            spreads.append(0.0)

    df["est_bid_ask_spread"] = spreads
    df["est_spread_bps"] = (df["est_bid_ask_spread"] / df["close"]) * 10000.0

    # 3. Log returns & Realized Volatility (rolling 30 bars)
    df["log_ret"] = np.log(df["close"] / df["close"].shift(1))
    df["realized_vol_30"] = df["log_ret"].rolling(30).std() * np.sqrt(252 * 1440) * 100.0  # Annualized %

    return df


def main():
    parser = argparse.ArgumentParser(description="Scrape CME Gold Futures Intraday Market Data")
    parser.add_argument("--symbol", type=str, default="GC=F", help="Ticker (GC=F for continuous Gold, MGC=F for Micro Gold)")
    parser.add_argument("--interval", type=str, default="1m", choices=["1m", "2m", "5m", "15m", "30m", "60m", "1d"], help="Bar interval")
    parser.add_argument("--range", type=str, default="7d", help="Data range (e.g., 1d, 5d, 7d, 30d, 60d)")
    parser.add_argument("--format", type=str, default="parquet", choices=["parquet", "csv", "both"], help="Export format")
    args = parser.parse_args()

    clean_sym = args.symbol.replace("=", "_")
    timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    df, meta = fetch_yahoo_intraday(args.symbol, args.interval, args.range)
    df = compute_microstructure_intraday(df)

    # Save data
    parquet_path = DATA_DIR / f"CME_{clean_sym}_{args.interval}_{args.range}_{timestamp_str}.parquet"
    csv_path = DATA_DIR / f"CME_{clean_sym}_{args.interval}_{args.range}_{timestamp_str}.csv"

    if args.format in ("parquet", "both"):
        df.to_parquet(parquet_path, index=False)
        print(f"[✓] Saved Parquet: {parquet_path} ({parquet_path.stat().st_size:,} bytes)")

    if args.format in ("csv", "both"):
        df.to_csv(csv_path, index=False)
        print(f"[✓] Saved CSV: {csv_path} ({csv_path.stat().st_size:,} bytes)")

    # Print summary report
    print("\n" + "=" * 70)
    print(f"📊 CME GOLD FUTURES ({args.symbol}) INTRADAY RESEARCH SUMMARY")
    print("=" * 70)
    print(f"Total Bars Scraped:        {len(df):,}")
    print(f"First Bar Time:            {df['ts_event'].min()}")
    print(f"Last Bar Time:             {df['ts_event'].max()}")
    print(f"Latest Price:              ${df['close'].iloc[-1]:.2f}")
    print(f"High / Low Range:          ${df['low'].min():.2f} - ${df['high'].max():.2f}")
    print(f"Average Estimated Spread:  ${df['est_bid_ask_spread'].dropna().mean():.4f} ({df['est_spread_bps'].dropna().mean():.2f} bps)")
    print(f"Average Realized Vol (30): {df['realized_vol_30'].dropna().mean():.2f}%")
    print(f"Total Traded Volume:       {int(df['volume'].sum()):,} contracts")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
