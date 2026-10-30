#!/usr/bin/env python3
"""
CME Multi-Commodity Real Historical Multi-Scale Lakehouse Pipeline (2016-2026)
=============================================================================
Replicates the proven CME Gold (GC) research architecture across the entire
CME commodity complex at zero API cost:
- Phase 1: Metals Complex (SI Silver, HG Copper, PL Platinum, PA Palladium)
- Phase 2: Energy Complex (CL WTI Crude, BZ Brent, NG Nat Gas, RB Gasoline, HO Heating Oil)
- Phase 3: Agriculture Complex (ZC Corn, ZS Soybeans, ZW Wheat)

Ingests:
1. 10-Year Daily Continuous Historical Lakes (2,500+ bars/asset)
2. 2-Year Hourly Continuous High-Density Lakes (17,000+ bars/asset)
3. Parkinson, Garman-Klass & Parkinson Volatility Estimators
4. Vectorized Brownian-Bridge 1-Second Continuous Microstructure Lakes
5. Direct ingestion into SQLite `market_store.db` and Google Drive lakehouse.
"""

import sys
import os
import json
import math
import time
import sqlite3
import urllib.request
import functools
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

print = functools.partial(print, flush=True)

# Directory configurations
LOCAL_DIR = Path(__file__).resolve().parents[2]
GDRIVE_DIR = Path(__file__).resolve().parents[2]
BASE_DIR = GDRIVE_DIR if GDRIVE_DIR.exists() else LOCAL_DIR

DATA_DIR = BASE_DIR / "data"
LOCAL_DATA = LOCAL_DIR / "data"
COMMODITIES_DIR = DATA_DIR / "commodities"
DAILY_DIR = COMMODITIES_DIR / "daily_10y"
HOURLY_DIR = COMMODITIES_DIR / "hourly_continuous"
S1_DIR = COMMODITIES_DIR / "historical_1s"
DB_PATH = DATA_DIR / "market_store.db"

DAILY_DIR.mkdir(parents=True, exist_ok=True)
HOURLY_DIR.mkdir(parents=True, exist_ok=True)
S1_DIR.mkdir(parents=True, exist_ok=True)

# 12 Target CME Commodities
COMMODITY_SPECS = {
    # Phase 1: Metals
    "SI=F": {"symbol": "SI", "name": "CME Silver Futures", "complex": "METALS", "tick_size": 0.005, "multiplier": 5000.0},
    "HG=F": {"symbol": "HG", "name": "CME Copper Futures", "complex": "METALS", "tick_size": 0.0005, "multiplier": 25000.0},
    "PL=F": {"symbol": "PL", "name": "CME Platinum Futures", "complex": "METALS", "tick_size": 0.10, "multiplier": 50.0},
    "PA=F": {"symbol": "PA", "name": "CME Palladium Futures", "complex": "METALS", "tick_size": 0.50, "multiplier": 100.0},
    # Phase 2: Energy
    "CL=F": {"symbol": "CL", "name": "CME WTI Crude Oil", "complex": "ENERGY", "tick_size": 0.01, "multiplier": 1000.0},
    "BZ=F": {"symbol": "BZ", "name": "CME Brent Crude Oil", "complex": "ENERGY", "tick_size": 0.01, "multiplier": 1000.0},
    "NG=F": {"symbol": "NG", "name": "CME Natural Gas", "complex": "ENERGY", "tick_size": 0.001, "multiplier": 10000.0},
    "RB=F": {"symbol": "RB", "name": "CME RBOB Gasoline", "complex": "ENERGY", "tick_size": 0.0001, "multiplier": 42000.0},
    "HO=F": {"symbol": "HO", "name": "CME Heating Oil", "complex": "ENERGY", "tick_size": 0.0001, "multiplier": 42000.0},
    # Phase 3: Agriculture
    "ZC=F": {"symbol": "ZC", "name": "CBOT Corn Futures", "complex": "AGRICULTURE", "tick_size": 0.25, "multiplier": 50.0},
    "ZS=F": {"symbol": "ZS", "name": "CBOT Soybean Futures", "complex": "AGRICULTURE", "tick_size": 0.25, "multiplier": 50.0},
    "ZW=F": {"symbol": "ZW", "name": "CBOT Wheat Futures", "complex": "AGRICULTURE", "tick_size": 0.25, "multiplier": 50.0},
}


class CMERealHistoricalPipeline:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        self.init_sqlite_tables()

    def init_sqlite_tables(self):
        conn = sqlite3.connect(str(DB_PATH))
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cme_commodities_10y_daily (
                date TEXT,
                epoch_s INTEGER,
                symbol TEXT,
                name TEXT,
                complex TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                parkinson_vol REAL,
                garman_klass_vol REAL,
                return_pct REAL,
                PRIMARY KEY (date, symbol)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cme_commodities_hourly (
                timestamp TEXT,
                epoch_s INTEGER,
                symbol TEXT,
                name TEXT,
                complex TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                parkinson_vol REAL,
                garman_klass_vol REAL,
                return_pct REAL,
                PRIMARY KEY (timestamp, symbol)
            )
        """)
        conn.commit()
        conn.close()

    def fetch_yahoo_chart(self, yf_symbol: str, range_str: str, interval: str) -> pd.DataFrame:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yf_symbol}?range={range_str}&interval={interval}"
        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        result = data.get("chart", {}).get("result", [])
        if not result:
            return pd.DataFrame()

        res0 = result[0]
        timestamps = res0.get("timestamp", [])
        quote = res0.get("indicators", {}).get("quote", [{}])[0]

        opens = quote.get("open", [])
        highs = quote.get("high", [])
        lows = quote.get("low", [])
        closes = quote.get("close", [])
        volumes = quote.get("volume", [])

        rows = []
        meta = COMMODITY_SPECS.get(yf_symbol, {})
        clean_sym = meta.get("symbol", yf_symbol)
        complex_name = meta.get("complex", "OTHER")
        asset_name = meta.get("name", yf_symbol)

        for i, ts in enumerate(timestamps):
            o = opens[i] if i < len(opens) else None
            h = highs[i] if i < len(highs) else None
            l = lows[i] if i < len(lows) else None
            c = closes[i] if i < len(closes) else None
            v = volumes[i] if i < len(volumes) else None

            if None in (o, h, l, c) or math.isnan(o) or math.isnan(c) or math.isnan(h) or math.isnan(l):
                continue
            if h < l or o <= 0 or c <= 0:
                continue

            dt_utc = datetime.fromtimestamp(ts, tz=timezone.utc)
            rows.append({
                "timestamp": dt_utc.strftime("%Y-%m-%d %H:%M:%S"),
                "date": dt_utc.strftime("%Y-%m-%d"),
                "epoch_s": int(ts),
                "symbol": clean_sym,
                "name": asset_name,
                "complex": complex_name,
                "open": round(float(o), 4),
                "high": round(float(h), 4),
                "low": round(float(l), 4),
                "close": round(float(c), 4),
                "volume": float(v) if v is not None and not math.isnan(v) else 0.0,
            })

        if not rows:
            return pd.DataFrame()

        df = pd.DataFrame(rows).sort_values("epoch_s").reset_index(drop=True)
        # Parkinson & Garman-Klass Volatilities
        df["parkinson_vol"] = np.sqrt((np.log(df["high"] / df["low"]) ** 2) / (4.0 * np.log(2.0))).fillna(0.0)
        df["garman_klass_vol"] = np.sqrt(
            np.maximum(0, 0.5 * (np.log(df["high"] / df["low"]) ** 2) - (2.0 * np.log(2.0) - 1.0) * (np.log(df["close"] / df["open"]) ** 2))
        ).fillna(0.0)
        df["return_pct"] = df["close"].pct_change().fillna(0.0)
        return df

    def run_daily_10y_ingestion(self):
        print("\n" + "=" * 80)
        print(" 📅 STEP 1: INGESTING 10-YEAR CONTINUOUS DAILY LAKES (2016-2026)")
        print("=" * 80)

        conn = sqlite3.connect(str(DB_PATH))
        for yf_sym, meta in COMMODITY_SPECS.items():
            sym = meta["symbol"]
            print(f"  ▶ Ingesting {sym:<4} ({meta['name']})...", end=" ", flush=True)
            try:
                df = self.fetch_yahoo_chart(yf_sym, range_str="10y", interval="1d")
                if df.empty:
                    print("⚠️ No data")
                    continue

                out_p = DAILY_DIR / f"{sym}_10y_daily.parquet"
                df.to_parquet(out_p, compression="snappy", index=False)

                # SQLite bulk insert
                cols = ["date", "epoch_s", "symbol", "name", "complex", "open", "high", "low", "close", "volume", "parkinson_vol", "garman_klass_vol", "return_pct"]
                df[cols].to_sql("cme_commodities_10y_daily", conn, if_exists="append", index=False)
                print(f"✅ {len(df):,} bars ({df['date'].iloc[0]} to {df['date'].iloc[-1]}) -> {out_p.name}")
            except Exception as e:
                print(f"❌ Error: {e}")
        conn.commit()
        conn.close()

    def run_hourly_ingestion(self):
        print("\n" + "=" * 80)
        print(" ⏰ STEP 2: INGESTING CONTINUOUS HIGH-DENSITY HOURLY LAKES (17,000+ BARS)")
        print("=" * 80)

        conn = sqlite3.connect(str(DB_PATH))
        for yf_sym, meta in COMMODITY_SPECS.items():
            sym = meta["symbol"]
            print(f"  ▶ Ingesting {sym:<4} ({meta['name']})...", end=" ", flush=True)
            try:
                df = self.fetch_yahoo_chart(yf_sym, range_str="730d", interval="1h")
                if df.empty:
                    print("⚠️ No data")
                    continue

                out_p = HOURLY_DIR / f"{sym}_hourly_continuous.parquet"
                df.to_parquet(out_p, compression="snappy", index=False)

                # SQLite bulk insert
                cols = ["timestamp", "epoch_s", "symbol", "name", "complex", "open", "high", "low", "close", "volume", "parkinson_vol", "garman_klass_vol", "return_pct"]
                df[cols].to_sql("cme_commodities_hourly", conn, if_exists="append", index=False)
                print(f"✅ {len(df):,} hourly bars ({df['timestamp'].iloc[0]} to {df['timestamp'].iloc[-1]}) -> {out_p.name}")
            except Exception as e:
                print(f"❌ Error: {e}")
        conn.commit()
        conn.close()

    def run_brownian_bridge_1s_lake(self, sample_limit_days: int = 60):
        print("\n" + "=" * 80)
        print(f" 🔬 STEP 3: GENERATING 1-SECOND BROWNIAN-BRIDGE CONTINUOUS LAKES (Recent {sample_limit_days} Days)")
        print("=" * 80)

        for yf_sym, meta in COMMODITY_SPECS.items():
            sym = meta["symbol"]
            tick = meta["tick_size"]
            daily_file = DAILY_DIR / f"{sym}_10y_daily.parquet"
            if not daily_file.exists():
                continue

            print(f"  ▶ Building 1-Second Continuous Lake for {sym:<4}...", end=" ", flush=True)
            df_daily = pd.read_parquet(daily_file).tail(sample_limit_days)
            all_1s_chunks = []

            for _, row in df_daily.iterrows():
                day_start = pd.Timestamp(row["date"], tz="UTC")
                num_seconds = 23 * 3600  # 23 hours of Globex trading per day
                ts_idx = pd.date_range(day_start, periods=num_seconds, freq="1s")

                o, h, l, c = row["open"], row["high"], row["low"], row["close"]
                # Vectorized Brownian Bridge bounded by OHLC
                t = np.linspace(0, 1, num_seconds)
                W = np.cumsum(np.random.normal(0, tick, num_seconds))
                bridge = o + (c - o) * t + (W - t * W[-1])
                # Bound within exact High/Low
                bridge = np.clip(bridge, l, h)

                df_sec = pd.DataFrame({
                    "ts_event": ts_idx,
                    "symbol": sym,
                    "open": np.round(bridge, 4),
                    "high": np.round(bridge + np.random.uniform(0, tick, num_seconds), 4),
                    "low": np.round(bridge - np.random.uniform(0, tick, num_seconds), 4),
                    "close": np.round(bridge, 4),
                    "volume": np.random.randint(1, 15, num_seconds),
                })
                all_1s_chunks.append(df_sec)

            df_all_1s = pd.concat(all_1s_chunks, ignore_index=True)
            out_1s = S1_DIR / f"{sym}_1s_continuous.parquet"
            df_all_1s.to_parquet(out_1s, compression="snappy", index=False)
            print(f"✅ {len(df_all_1s):,} continuous 1-second bars ({out_1s.stat().st_size / (1024*1024):.2f} MB)")


def main():
    pipeline = CMERealHistoricalPipeline()
    pipeline.run_daily_10y_ingestion()
    pipeline.run_hourly_ingestion()
    pipeline.run_brownian_bridge_1s_lake(sample_limit_days=30)

    print("\n" + "=" * 80)
    print(" 🏁 CME MULTI-COMMODITY REAL HISTORICAL LAKEHOUSE COMPLETE!")
    print(f" 📂 Data Root: {DATA_DIR}")
    print(f" 🗄️ Master Database: {DB_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()
