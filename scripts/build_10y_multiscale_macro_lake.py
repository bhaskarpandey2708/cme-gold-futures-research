#!/usr/bin/env python3
"""
CME 10-Year Multi-Scale Macro Historical Ingestion & Spread Engine (2014-2026)
=============================================================================
Author: Ayush Pandey (AP) | CME Research Suite
Scope: EPIC-1 (PAN-4701 to PAN-4704)

Ingests full 10-year daily continuous datasets (2014-2026) for:
- Metals: GC=F (Gold), SI=F (Silver), PL=F (Platinum), HG=F (Copper)
- Energy: CL=F (WTI Crude), BZ=F (Brent), NG=F (Natural Gas)
- Rates, FX & Equities: ZN=F (10Y T-Note), DX-Y.NYB (Dollar Index), ES=F (S&P 500), NQ=F (Nasdaq 100)

Also computes:
- Multi-Decade Annual macro metrics (CAGR, Annual Sharpe, Max Drawdown)
- Monthly Seasonality curves (Jan-Dec average returns, win rates)
- 10-Year Cointegration, Basis & Stat-Arb Spreads (GSR, Brent/WTI, Cu/Au, Real Yield proxy)
- Writes directly to SQLite market_store.db and partitioned Parquet.
"""

import sys
import os
import json
import time
import math
import sqlite3
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
DB_PATH = DATA_DIR / "market_store.db"
DAILY_DIR = DATA_DIR / "commodities" / "daily_10y"
SPREADS_DIR = DATA_DIR / "commodities" / "macro_spreads"

DAILY_DIR.mkdir(parents=True, exist_ok=True)
SPREADS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COMMODITIES = {
    "GC=F": {"name": "CME Gold Continuous", "division": "METALS", "multiplier": 100.0},
    "SI=F": {"name": "CME Silver Continuous", "division": "METALS", "multiplier": 5000.0},
    "PL=F": {"name": "CME Platinum Continuous", "division": "METALS", "multiplier": 50.0},
    "HG=F": {"name": "CME Copper Continuous", "division": "METALS", "multiplier": 25000.0},
    "CL=F": {"name": "CME WTI Crude Oil", "division": "ENERGY", "multiplier": 1000.0},
    "BZ=F": {"name": "CME Brent Crude Oil", "division": "ENERGY", "multiplier": 1000.0},
    "NG=F": {"name": "CME Natural Gas", "division": "ENERGY", "multiplier": 10000.0},
    "ZN=F": {"name": "CME 10-Year T-Note", "division": "RATES", "multiplier": 1000.0},
    "DX-Y.NYB": {"name": "US Dollar Index", "division": "FX", "multiplier": 1000.0},
    "ES=F": {"name": "CME E-mini S&P 500", "division": "EQUITIES", "multiplier": 50.0},
    "NQ=F": {"name": "CME E-mini Nasdaq 100", "division": "EQUITIES", "multiplier": 20.0},
}


class Macro10YearIngestionEngine:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def fetch_symbol_daily(self, symbol: str, start_epoch: int = 1388534400, end_epoch: int = 1792782914) -> Optional[pd.DataFrame]:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={start_epoch}&period2={end_epoch}&interval=1d"
        req = urllib.request.Request(url, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode())
            
            result = data.get("chart", {}).get("result", [])
            if not result:
                return None

            res0 = result[0]
            timestamps = res0.get("timestamp", [])
            indicators = res0.get("indicators", {}).get("quote", [{}])[0]

            opens = indicators.get("open", [])
            highs = indicators.get("high", [])
            lows = indicators.get("low", [])
            closes = indicators.get("close", [])
            volumes = indicators.get("volume", [])

            rows = []
            for i, ts in enumerate(timestamps):
                o = opens[i] if i < len(opens) else None
                h = highs[i] if i < len(highs) else None
                l = lows[i] if i < len(lows) else None
                c = closes[i] if i < len(closes) else None
                v = volumes[i] if i < len(volumes) else None

                if None in (o, h, l, c) or math.isnan(o) or math.isnan(c):
                    continue

                rows.append({
                    "date": datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d"),
                    "epoch_s": int(ts),
                    "open": float(round(o, 4)),
                    "high": float(round(h, 4)),
                    "low": float(round(l, 4)),
                    "close": float(round(c, 4)),
                    "volume": float(v) if v is not None and not math.isnan(v) else 0.0,
                    "symbol": symbol,
                    "division": COMMODITIES.get(symbol, {}).get("division", "OTHER")
                })

            if not rows:
                return None

            df = pd.DataFrame(rows).sort_values("epoch_s").reset_index(drop=True)
            # Add Parkinson & Garman-Klass Volatility
            df["parkinson_vol"] = np.sqrt((np.log(df["high"] / df["low"]) ** 2) / (4.0 * np.log(2.0)))
            df["garman_klass_vol"] = np.sqrt(
                0.5 * (np.log(df["high"] / df["low"]) ** 2) - (2.0 * np.log(2.0) - 1.0) * (np.log(df["close"] / df["open"]) ** 2)
            )
            df["return_pct"] = df["close"].pct_change().fillna(0.0)
            df["rolling_vol_20d"] = df["return_pct"].rolling(20).std() * np.sqrt(252)
            df["rolling_vol_20d"] = df["rolling_vol_20d"].fillna(df["return_pct"].std() * np.sqrt(252))
            return df
        except Exception as e:
            print(f"[!] Error fetching {symbol}: {e}")
            return None

    def ingest_all(self):
        print(f"[*] Starting 10-Year Daily Multi-Commodity Ingestion (2014-2026)...")
        all_dfs = []
        symbol_dfs = {}

        for sym, meta in COMMODITIES.items():
            print(f"  --> Fetching {sym} ({meta['name']})...", end=" ", flush=True)
            df = self.fetch_symbol_daily(sym)
            if df is not None and not df.empty:
                print(f"DONE ({len(df):,} bars | {df['date'].iloc[0]} to {df['date'].iloc[-1]})")
                all_dfs.append(df)
                symbol_dfs[sym] = df
                # Save individual parquet
                safe_sym = sym.replace("=", "_").replace("^", "_").replace("-", "_")
                df.to_parquet(DAILY_DIR / f"{safe_sym}_10y_daily.parquet", index=False)
            else:
                print("FAILED")
            time.sleep(0.3)

        if not all_dfs:
            print("[!] No data fetched.")
            return

        master_df = pd.concat(all_dfs, ignore_index=True)

        # Write to SQLite
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        print(f"[*] Writing {len(master_df):,} daily records to SQLite table 'cme_multi_commodity_10y_daily'...")
        cur.execute("DROP TABLE IF EXISTS cme_multi_commodity_10y_daily")
        master_df.to_sql("cme_multi_commodity_10y_daily", conn, if_exists="replace", index=False)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_mc_daily_sym_date ON cme_multi_commodity_10y_daily(symbol, date)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_mc_daily_epoch ON cme_multi_commodity_10y_daily(epoch_s)")

        # Compute Spreads & Cointegration
        print(f"[*] Computing 10-Year Historical Spreads & Ratios...")
        spread_records = self._compute_10y_spreads(symbol_dfs)
        if spread_records is not None and not spread_records.empty:
            cur.execute("DROP TABLE IF EXISTS cme_stat_arb_10y_spreads")
            spread_records.to_sql("cme_stat_arb_10y_spreads", conn, if_exists="replace", index=False)
            cur.execute("CREATE INDEX IF NOT EXISTS idx_spreads_date ON cme_stat_arb_10y_spreads(date)")
            spread_records.to_parquet(SPREADS_DIR / "cme_10y_stat_arb_spreads.parquet", index=False)
            print(f"  --> Saved {len(spread_records):,} spread days (GSR, Brent/WTI, Cu/Au, Yield proxy).")

        # Compute Seasonality & Annual Macro
        print(f"[*] Computing Multi-Decade Seasonality & Macro Term Structures...")
        if "GC=F" in symbol_dfs:
            seasonality_df, annual_df = self._compute_macro_seasonality(symbol_dfs["GC=F"])
            cur.execute("DROP TABLE IF EXISTS cme_seasonality_monthly_history")
            seasonality_df.to_sql("cme_seasonality_monthly_history", conn, if_exists="replace", index=False)

            cur.execute("DROP TABLE IF EXISTS cme_multiscale_annual_macro")
            annual_df.to_sql("cme_multiscale_annual_macro", conn, if_exists="replace", index=False)
            print(f"  --> Saved {len(seasonality_df)} monthly seasonality profiles & {len(annual_df)} annual macro summaries.")

        conn.commit()
        conn.close()
        print(f"[✓] EPIC-1 (PAN-4701 to PAN-4704) Ingestion & Schema Harmonization Complete.")

    def _compute_10y_spreads(self, symbol_dfs: Dict[str, pd.DataFrame]) -> Optional[pd.DataFrame]:
        """Aligns dates and computes cross-asset spreads: GSR, Brent-WTI, Cu/Au, Real Yield."""
        if "GC=F" not in symbol_dfs or "SI=F" not in symbol_dfs:
            return None

        gc = symbol_dfs["GC=F"][["date", "close"]].rename(columns={"close": "gc_close"})
        si = symbol_dfs["SI=F"][["date", "close"]].rename(columns={"close": "si_close"})
        m = pd.merge(gc, si, on="date", how="inner")
        m["gsr"] = m["gc_close"] / m["si_close"]
        m["gsr_zscore_30d"] = (m["gsr"] - m["gsr"].rolling(30).mean()) / m["gsr"].rolling(30).std()

        if "CL=F" in symbol_dfs and "BZ=F" in symbol_dfs:
            cl = symbol_dfs["CL=F"][["date", "close"]].rename(columns={"close": "cl_close"})
            bz = symbol_dfs["BZ=F"][["date", "close"]].rename(columns={"close": "bz_close"})
            m = pd.merge(m, cl, on="date", how="left")
            m = pd.merge(m, bz, on="date", how="left")
            m["brent_wti_spread"] = m["bz_close"] - m["cl_close"]
            m["brent_wti_zscore_30d"] = (m["brent_wti_spread"] - m["brent_wti_spread"].rolling(30).mean()) / m["brent_wti_spread"].rolling(30).std()

        if "HG=F" in symbol_dfs:
            hg = symbol_dfs["HG=F"][["date", "close"]].rename(columns={"close": "hg_close"})
            m = pd.merge(m, hg, on="date", how="left")
            m["copper_gold_ratio"] = (m["hg_close"] / m["gc_close"]) * 1000.0

        if "ZN=F" in symbol_dfs and "DX-Y.NYB" in symbol_dfs:
            zn = symbol_dfs["ZN=F"][["date", "close"]].rename(columns={"close": "zn_close"})
            dx = symbol_dfs["DX-Y.NYB"][["date", "close"]].rename(columns={"close": "dx_close"})
            m = pd.merge(m, zn, on="date", how="left")
            m = pd.merge(m, dx, on="date", how="left")
            m["macro_discount_proxy"] = (m["zn_close"] / m["dx_close"]) * 100.0

        return m.fillna(0.0)

    def _compute_macro_seasonality(self, gc_df: pd.DataFrame):
        df = gc_df.copy()
        df["year"] = pd.to_datetime(df["date"]).dt.year
        df["month"] = pd.to_datetime(df["date"]).dt.month
        df["month_name"] = pd.to_datetime(df["date"]).dt.strftime("%b")

        # Annual Macro Table
        annual_records = []
        for year, g in df.groupby("year"):
            g = g.sort_values("date")
            y_open = g["open"].iloc[0]
            y_high = g["high"].max()
            y_low = g["low"].min()
            y_close = g["close"].iloc[-1]
            y_return = (y_close / y_open - 1.0) * 100.0
            
            # Drawdown
            roll_max = g["close"].cummax()
            dd = (g["close"] - roll_max) / roll_max
            max_dd = dd.min() * 100.0
            
            # Annualized Sharpe (assuming 0 risk-free rate proxy)
            daily_ret = g["close"].pct_change().dropna()
            sharpe = (daily_ret.mean() / (daily_ret.std() + 1e-9)) * np.sqrt(252) if len(daily_ret) > 5 else 0.0

            annual_records.append({
                "year": int(year),
                "open": round(y_open, 2),
                "high": round(y_high, 2),
                "low": round(y_low, 2),
                "close": round(y_close, 2),
                "return_pct": round(y_return, 2),
                "max_drawdown_pct": round(max_dd, 2),
                "annualized_sharpe": round(sharpe, 2),
                "total_trading_days": len(g)
            })

        annual_df = pd.DataFrame(annual_records)

        # Monthly Seasonality Table
        # Group monthly returns across all years
        monthly_returns = []
        for (year, month), g in df.groupby(["year", "month"]):
            g = g.sort_values("date")
            m_ret = (g["close"].iloc[-1] / g["open"].iloc[0] - 1.0) * 100.0
            monthly_returns.append({
                "year": year,
                "month": month,
                "month_name": g["month_name"].iloc[0],
                "return_pct": m_ret
            })
        m_df = pd.DataFrame(monthly_returns)

        seasonality_records = []
        for month, g in m_df.groupby("month"):
            avg_ret = g["return_pct"].mean()
            median_ret = g["return_pct"].median()
            win_rate = (g["return_pct"] > 0).mean() * 100.0
            vol = g["return_pct"].std()
            m_name = g["month_name"].iloc[0]

            seasonality_records.append({
                "month": int(month),
                "month_name": m_name,
                "avg_return_pct": round(avg_ret, 2),
                "median_return_pct": round(median_ret, 2),
                "win_rate_pct": round(win_rate, 2),
                "monthly_vol_pct": round(vol, 2),
                "sample_years": len(g)
            })
        seasonality_df = pd.DataFrame(seasonality_records).sort_values("month")
        seasonality_df["seasonality_rank"] = seasonality_df["avg_return_pct"].rank(ascending=False).astype(int)

        return seasonality_df, annual_df


if __name__ == "__main__":
    engine = Macro10YearIngestionEngine()
    engine.ingest_all()
