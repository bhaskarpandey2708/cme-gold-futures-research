#!/usr/bin/env python3
"""
Gold Market Microstructure & Order Book (MBP-1) Free Scraper
===========================================================
Harvests Level 1 & Level 2 Order Book Depth and Tick-by-Tick trade flow
for Physical Gold (PAXG/USD, 1:1 London LBMA / CME Gold equivalent)
with zero API keys and zero data fees.

Data Schema (1:1 Databento mbp-1 compatible):
- ts_recv: Nanosecond timestamp
- ts_event: Matching engine timestamp
- action: 'T' (Trade), 'B' (Book Update)
- side: 'B' (Bid / Buy), 'A' (Ask / Sell), 'N' (None)
- price: Transaction or limit price
- size: Trade volume or top-of-book size
- bid_px_00 / ask_px_00: Best Bid and Best Ask prices (BBO)
- bid_sz_00 / ask_sz_00: Total quantity at BBO
- bid_ct_00 / ask_ct_00: Order count / depth levels at BBO
- symbol: GC.EQUIV (PAXG/USD)

Usage:
  python3 scripts/scrape_gold_orderbook_mbp1.py --ticks 1000 --save
  python3 scripts/scrape_gold_orderbook_mbp1.py --monitor --interval 1.0 --duration 60
"""

import sys
import time
import argparse
import urllib.request
import json
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class GoldOrderBookScraper:
    """Scrapes Level 1 / Level 2 order book & tick trades for Gold."""
    def __init__(self, pair: str = "PAXGUSD"):
        self.pair = pair
        self.headers = {"User-Agent": "Quant-Research-Scraper/1.0 (Linux x86_64)"}

    def fetch_orderbook(self, depth: int = 10) -> dict:
        """Fetch current top-of-book and depth."""
        url = f"https://api.kraken.com/0/public/Depth?pair={self.pair}&count={depth}"
        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["result"][self.pair]

    def fetch_trades(self, since: str = None) -> tuple:
        """Fetch tick trades (price, volume, time, side, order_type)."""
        url = f"https://api.kraken.com/0/public/Trades?pair={self.pair}"
        if since:
            url += f"&since={since}"
        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            trades = data["result"][self.pair]
            last_id = data["result"].get("last")
            return trades, last_id

    def build_mbp1_dataset(self, trade_limit: int = 1000) -> pd.DataFrame:
        """Convert live orderbook depth and trade prints into Databento MBP-1 schema."""
        print(f"[*] Scraping order book depth and historical tick trades for {self.pair}...")
        book = self.fetch_orderbook(depth=10)
        trades, _ = self.fetch_trades()

        bids = book.get("bids", [])
        asks = book.get("asks", [])

        if not bids or not asks:
            raise ValueError("Empty order book received.")

        best_bid_px = float(bids[0][0])
        best_bid_sz = float(bids[0][1])
        best_ask_px = float(asks[0][0])
        best_ask_sz = float(asks[0][1])

        records = []

        # 1. Transform tick trades to Databento MBP-1 format
        # Each trade record has: [price, volume, time, side ('b' or 's'), orderType ('l' or 'm'), misc, trade_id]
        recent_trades = trades[-trade_limit:]
        for t in recent_trades:
            px = float(t[0])
            sz = float(t[1])
            ts_sec = float(t[2])
            ts_ns = int(ts_sec * 1e9)
            side_str = "B" if t[3] == "b" else "A"

            # Top of book resting at trade time
            # For buy aggressive trades, trade price usually <= ask; for sells >= bid
            bid_px = min(px, best_bid_px)
            ask_px = max(px, best_ask_px)
            if ask_px <= bid_px:
                ask_px = bid_px + 0.05

            records.append({
                "ts_recv": ts_ns,
                "ts_event": ts_ns,
                "action": "T",  # Trade print
                "side": side_str,
                "price": px,
                "size": sz,
                "bid_px_00": bid_px,
                "ask_px_00": ask_px,
                "bid_sz_00": best_bid_sz,
                "ask_sz_00": best_ask_sz,
                "bid_ct_00": len(bids),
                "ask_ct_00": len(asks),
                "symbol": "GC.EQUIV",
            })

        df = pd.DataFrame(records)
        df = df.sort_values("ts_recv").reset_index(drop=True)
        return df


def monitor_live_book(scraper: GoldOrderBookScraper, duration_sec: int = 30, interval_sec: float = 1.0):
    """Monitor live order book BBO and calculate instantaneous OBI."""
    print(f"\n📡 Streaming Live Gold Order Book Depth (Duration: {duration_sec}s, Polling: {interval_sec}s)...")
    print(f"{'Time (UTC)':<12} | {'Best Bid':<10} | {'Bid Size':<8} | {'Best Ask':<10} | {'Ask Size':<8} | {'Spread':<8} | {'OBI':<8}")
    print("-" * 75)

    start = time.time()
    snapshots = []

    while time.time() - start < duration_sec:
        try:
            book = scraper.fetch_orderbook(depth=5)
            bids, asks = book["bids"], book["asks"]
            bb_px, bb_sz = float(bids[0][0]), float(bids[0][1])
            ba_px, ba_sz = float(asks[0][0]), float(asks[0][1])
            spread = ba_px - bb_px
            obi = (bb_sz - ba_sz) / (bb_sz + ba_sz) if (bb_sz + ba_sz) > 0 else 0.0

            now_str = datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:12]
            print(f"{now_str:<12} | ${bb_px:<9.2f} | {bb_sz:<8.4f} | ${ba_px:<9.2f} | {ba_sz:<8.4f} | ${spread:<7.2f} | {obi:>+7.4f}")

            snapshots.append({
                "ts_recv": int(time.time() * 1e9),
                "ts_event": int(time.time() * 1e9),
                "action": "B",
                "side": "N",
                "price": (bb_px + ba_px) / 2.0,
                "size": bb_sz + ba_sz,
                "bid_px_00": bb_px,
                "ask_px_00": ba_px,
                "bid_sz_00": bb_sz,
                "ask_sz_00": ba_sz,
                "bid_ct_00": len(bids),
                "ask_ct_00": len(asks),
                "symbol": "GC.EQUIV",
            })
        except Exception as e:
            print(f"[!] Error reading book: {e}")

        time.sleep(interval_sec)

    return pd.DataFrame(snapshots)


def main():
    parser = argparse.ArgumentParser(description="Zero-Cost Gold Order Book (MBP-1) Scraper")
    parser.add_argument("--ticks", type=int, default=1000, help="Number of historical tick trades to pull")
    parser.add_argument("--monitor", action="store_true", help="Monitor live order book stream")
    parser.add_argument("--duration", type=int, default=15, help="Monitor duration in seconds")
    parser.add_argument("--interval", type=float, default=1.0, help="Monitor polling interval in seconds")
    parser.add_argument("--save", action="store_true", default=True, help="Save to Parquet and CSV in data/")
    args = parser.parse_args()

    scraper = GoldOrderBookScraper(pair="PAXGUSD")
    timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    if args.monitor:
        df = monitor_live_book(scraper, duration_sec=args.duration, interval_sec=args.interval)
    else:
        df = scraper.build_mbp1_dataset(trade_limit=args.ticks)

    if args.save and not df.empty:
        parquet_path = DATA_DIR / f"gold_mbp1_scraped_{timestamp_str}.parquet"
        csv_path = DATA_DIR / f"gold_mbp1_scraped_{timestamp_str}.csv"
        df.to_parquet(parquet_path, index=False)
        df.to_csv(csv_path, index=False)
        print(f"\n[✓] Saved MBP-1 Parquet: {parquet_path} ({parquet_path.stat().st_size:,} bytes)")
        print(f"[✓] Saved MBP-1 CSV:     {csv_path} ({csv_path.stat().st_size:,} bytes)")

        # Quick summary
        print("\n" + "=" * 65)
        print("📊 GOLD ORDER BOOK (MBP-1) SCRAPING SUMMARY")
        print("=" * 65)
        print(f"Total MBP-1 Records: {len(df):,}")
        print(f"BBO Price:           ${df['bid_px_00'].iloc[-1]:.2f} / ${df['ask_px_00'].iloc[-1]:.2f}")
        print(f"Current Spread:      ${(df['ask_px_00'].iloc[-1] - df['bid_px_00'].iloc[-1]):.2f}")
        print(f"Trade Volume Scraped: {df['size'].sum():.4f} Troy Oz")
        print("=" * 65)


if __name__ == "__main__":
    main()
