#!/usr/bin/env python3
"""
CME Gold 1-Second Data Lake Fast Query Utility
==============================================
Fast columnar scanning of the 205,259,940 1-second continuous bars.

Usage:
  python3 scripts/query_1s_lake.py --year 2024 --limit 10
  python3 scripts/query_1s_lake.py --stats
"""

import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import pyarrow.parquet as pq

BASE_DIR = Path(__file__).resolve().parent.parent
S1_DIR = Path("/home/ayush-pandey/DATABENTO_RESEARCH/data/historical_1s")
if not S1_DIR.exists():
    S1_DIR = Path("/home/ayush-pandey/GoogleDrive/Databento_Gold_Futures_Research/data/historical_1s")


def main():
    parser = argparse.ArgumentParser(description="Query 1-Second Gold Data Lake")
    parser.add_argument("--year", type=int, default=2026, help="Target year partition (2017-2026)")
    parser.add_argument("--limit", type=int, default=5, help="Number of bars to display")
    parser.add_argument("--stats", action="store_true", help="Display all partition sizes & totals")
    args = parser.parse_args()

    files = sorted(list(S1_DIR.glob("gold_1s_*.parquet")))
    if not files:
        print(f"❌ No 1-second parquet partitions found in {S1_DIR}")
        return

    if args.stats:
        print("=" * 70)
        print(" ⚡ CME GOLD 1-SECOND CONTINUOUS DATA LAKE AUDIT (2017–2026)")
        print("=" * 70)
        total_rows = 0
        total_size = 0.0
        for f in files:
            meta = pq.read_metadata(f)
            rows = meta.num_rows
            size_mb = f.stat().st_size / (1024 * 1024)
            total_rows += rows
            total_size += size_mb
            print(f"📁 {f.name:<24} | Rows: {rows:>11,} | Size: {size_mb:>6.1f} MB")
        print("-" * 70)
        print(f"🏆 TOTAL: {total_rows:,} continuous 1-second bars | {total_size:.1f} MB (~{total_size/1024:.2f} GB)")
        print("=" * 70)
        return

    target_file = S1_DIR / f"gold_1s_{args.year}.parquet"
    if not target_file.exists():
        print(f"❌ Partition for year {args.year} not found at {target_file}")
        return

    # Sub-second fast batch read
    pf = pq.ParquetFile(target_file)
    batch = next(pf.iter_batches(batch_size=args.limit))
    df = batch.to_pandas()
    df["ts_event"] = pd.to_datetime(df["epoch_s"], unit="s", utc=True).dt.strftime("%Y-%m-%d %H:%M:%S+00:00")
    print(f"\n[*] Sample {args.limit} continuous 1-second bars from partition {args.year}:")
    cols = ["ts_event", "epoch_s", "open", "high", "low", "close", "volume", "spread"]
    print(df[cols].to_string(index=False))


if __name__ == "__main__":
    main()
