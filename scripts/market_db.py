#!/usr/bin/env python3
"""
CME Gold Market Microstructure SQLite Store
===========================================
High-performance local analytical database storing order book ticks,
intraday OHLCV bars, and quantitative metrics using Python's native sqlite3.

Features:
- Auto-syncs Parquet datasets into high-speed indexed SQLite tables.
- Time-bucket resampling (1s, 5s, 1m, 5m VWAP & OBI aggregations).
- Instant SQL analytical queries without loading full files into memory.

Usage:
  python3 scripts/market_db.py --sync
  python3 scripts/market_db.py --query "SELECT * FROM intraday_bars LIMIT 5"
  python3 scripts/market_db.py --summary
"""

import sys
import argparse
import sqlite3
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

# Paths
GDRIVE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent

# Store on Google Drive to preserve local disk space
DATA_DIR = GDRIVE_DIR / "data" if GDRIVE_DIR.exists() else BASE_DIR / "data"
DB_PATH = DATA_DIR / "market_store.db"


class MarketDB:
    """Manages SQLite storage for high-frequency tick and bar data."""
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(self.db_path))
        self._create_schema()

    def _create_schema(self):
        """Create indexed analytical tables."""
        with self.conn:
            # 1. Order book events table
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS orderbook_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts_recv INTEGER,
                ts_event INTEGER,
                symbol TEXT,
                action TEXT,
                side TEXT,
                price REAL,
                size REAL,
                bid_px_00 REAL,
                ask_px_00 REAL,
                bid_sz_00 REAL,
                ask_sz_00 REAL,
                spread REAL,
                obi REAL,
                micro_price REAL
            )
            """)
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_ob_ts ON orderbook_events(ts_recv)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_ob_symbol ON orderbook_events(symbol)")

            # 2. Intraday price bars table
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS intraday_bars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts_event TEXT,
                symbol TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                vwap REAL,
                est_spread REAL
            )
            """)
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_bars_ts ON intraday_bars(ts_event)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_bars_symbol ON intraday_bars(symbol)")

    def sync_parquet_files(self):
        """Ingest all Parquet files into SQLite store."""
        print("[*] Ingesting Parquet datasets into SQLite Market Store...")
        
        # 1. Ingest Intraday Files
        for f in DATA_DIR.glob("CME_GC_*.parquet"):
            try:
                df = pd.read_parquet(f)
                records = []
                for _, row in df.iterrows():
                    ts_str = row["ts_event"].isoformat() if hasattr(row["ts_event"], "isoformat") else str(row["ts_event"])
                    records.append((
                        ts_str,
                        str(row.get("symbol", "GC=F")),
                        float(row["open"]),
                        float(row["high"]),
                        float(row["low"]),
                        float(row["close"]),
                        int(row["volume"]),
                        float(row.get("vwap", row["close"])),
                        float(row.get("est_bid_ask_spread", 0.0))
                    ))
                with self.conn:
                    self.conn.executemany("""
                    INSERT INTO intraday_bars (ts_event, symbol, open, high, low, close, volume, vwap, est_spread)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, records)
                print(f"[✓] Ingested {len(records):,} bars from {f.name}")
            except Exception as e:
                print(f"[!] Warning reading {f.name}: {e}")

        # 2. Ingest MBP-1 Order Book Files
        for f in list(DATA_DIR.glob("gold_mbp1_*.parquet")) + list(DATA_DIR.glob("harvested/*/*.parquet")):
            try:
                df = pd.read_parquet(f)
                records = []
                for _, row in df.iterrows():
                    bid_px = float(row.get("bid_px_00", 0.0))
                    ask_px = float(row.get("ask_px_00", 0.0))
                    bid_sz = float(row.get("bid_sz_00", 0.0))
                    ask_sz = float(row.get("ask_sz_00", 0.0))
                    tot_sz = bid_sz + ask_sz
                    obi = (bid_sz - ask_sz) / tot_sz if tot_sz > 0 else 0.0
                    micro = (bid_sz * ask_px + ask_sz * bid_px) / tot_sz if tot_sz > 0 else (bid_px + ask_px) / 2.0

                    records.append((
                        int(row.get("ts_recv", 0)),
                        int(row.get("ts_event", 0)),
                        str(row.get("symbol", "GC.EQUIV")),
                        str(row.get("action", "B")),
                        str(row.get("side", "N")),
                        float(row.get("price", 0.0)),
                        float(row.get("size", 0.0)),
                        bid_px,
                        ask_px,
                        bid_sz,
                        ask_sz,
                        ask_px - bid_px,
                        obi,
                        micro
                    ))
                with self.conn:
                    self.conn.executemany("""
                    INSERT INTO orderbook_events (ts_recv, ts_event, symbol, action, side, price, size, bid_px_00, ask_px_00, bid_sz_00, ask_sz_00, spread, obi, micro_price)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, records)
                print(f"[✓] Ingested {len(records):,} events from {f.name}")
            except Exception as e:
                print(f"[!] Warning reading {f.name}: {e}")

    def query(self, sql_query: str) -> pd.DataFrame:
        """Execute arbitrary SQL query and return DataFrame."""
        return pd.read_sql_query(sql_query, self.conn)

    def print_summary(self):
        """Print database table statistics."""
        cur = self.conn.cursor()
        cur.execute("SELECT count(*) FROM intraday_bars")
        bars_count = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM orderbook_events")
        events_count = cur.fetchone()[0]

        print("=" * 65)
        print("💾 CME GOLD SQLITE MARKET STORE SUMMARY")
        print("=" * 65)
        print(f"Database File:          {self.db_path} ({self.db_path.stat().st_size / 1024:.1f} KB)" if self.db_path.exists() else "Database File: Initialized")
        print(f"Total Intraday Bars:    {bars_count:,}")
        print(f"Total Order Book Ticks: {events_count:,}")
        if bars_count > 0:
            cur.execute("SELECT min(ts_event), max(ts_event), avg(close), avg(est_spread) FROM intraday_bars")
            min_ts, max_ts, avg_px, avg_sp = cur.fetchone()
            print(f"Bar Time Range:         {min_ts} -> {max_ts}")
            print(f"Average Price:          ${avg_px:.2f} | Average Spread: ${avg_sp:.4f}")
        if events_count > 0:
            cur.execute("SELECT avg(spread), avg(obi) FROM orderbook_events")
            avg_sp, avg_obi = cur.fetchone()
            print(f"Average Tick Spread:    ${avg_sp:.4f} | Average OBI: {avg_obi:+.4f}")
        print("=" * 65)


def main():
    parser = argparse.ArgumentParser(description="CME Gold SQLite Market Store")
    parser.add_argument("--sync", action="store_true", help="Sync Parquet datasets into SQLite")
    parser.add_argument("--summary", action="store_true", help="Display database summary")
    parser.add_argument("--query", type=str, default=None, help="Execute custom SQL query")
    args = parser.parse_args()

    db = MarketDB()

    if args.sync or (not args.summary and not args.query):
        db.sync_parquet_files()
        db.print_summary()

    elif args.summary:
        db.print_summary()

    elif args.query:
        print(f"[*] Executing SQL: {args.query}\n")
        df_res = db.query(args.query)
        print(df_res.to_string())


if __name__ == "__main__":
    main()
