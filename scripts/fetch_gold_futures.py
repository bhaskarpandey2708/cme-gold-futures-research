#!/usr/bin/env python3
"""
Production Databento CME Gold Futures (GC) Data Fetcher
Connects to Databento API, checks cost & record size before downloading,
and exports high-resolution MBP-1 data to Parquet/CSV.
"""

import os
import sys
import argparse
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
from config import DATA_DIR, DEFAULT_DATASET, DEFAULT_SYMBOL, DEFAULT_SCHEMA, DEFAULT_STYPE_IN

try:
    import databento as db
    import pandas as pd
except ImportError:
    print("❌ Error: Databento or Pandas is not installed. Run 'pip install -r requirements.txt'")
    sys.exit(1)


def fetch_databento_gold(
    api_key: str,
    dataset: str = DEFAULT_DATASET,
    symbol: str = DEFAULT_SYMBOL,
    schema: str = DEFAULT_SCHEMA,
    stype_in: str = DEFAULT_STYPE_IN,
    start: str = "2024-10-21T13:30:00",
    end: str = "2024-10-21T14:30:00",
    output_format: str = "parquet",
    force_download: bool = False,
):
    """
    Safely fetch CME Gold Futures data from Databento with cost verification.
    """
    if not api_key:
        api_key = os.getenv("DATABENTO_API_KEY", "")

    if not api_key or api_key == "your-databento-api-key-here":
        print("\n⚠️  No valid DATABENTO_API_KEY provided.")
        print("Please obtain an API key from https://databento.com/portal/keys")
        print("Set it using: export DATABENTO_API_KEY='db-...' or pass --key\n")
        return None

    print("\n" + "=" * 60)
    print("💎 DATABENTO CME GOLD FUTURES (GC) FETCH ENGINE")
    print("=" * 60)
    print(f"Dataset:       {dataset}")
    print(f"Symbol:        {symbol}")
    print(f"Schema:        {schema}")
    print(f"Start (UTC):   {start}")
    print(f"End (UTC):     {end}")
    print(f"Output Format: {output_format}")
    print("=" * 60)

    client = db.Historical(key=api_key)

    # 1. Safety Check: Verify Cost & Billable Size First!
    print("🔍 Estimating query size and cost via Databento Metadata API...")
    try:
        cost = client.metadata.get_cost(
            dataset=dataset,
            symbols=[symbol],
            schema=schema,
            start=start,
            end=end,
            stype_in=stype_in,
        )
        billable_size = client.metadata.get_billable_size(
            dataset=dataset,
            symbols=[symbol],
            schema=schema,
            start=start,
            end=end,
            stype_in=stype_in,
        )
        print(f"   💰 Estimated Cost:     ${cost:.4f} USD")
        print(f"   📦 Estimated Size:     {billable_size / (1024 * 1024):.2f} MB")
    except Exception as e:
        print(f"   ⚠️ Metadata cost check returned: {e}")
        cost = 0.0

    if cost > 5.0 and not force_download:
        confirm = input(f"⚠️ Query cost exceeds $5.00 (${cost:.2f}). Proceed? [y/N]: ")
        if confirm.lower() != "y":
            print("🛑 Query cancelled by user.")
            return None

    # 2. Fetch Data
    print("\n⬇️ Fetching timeseries data from Databento...")
    try:
        data = client.timeseries.get_range(
            dataset=dataset,
            symbols=[symbol],
            schema=schema,
            start=start,
            end=end,
            stype_in=stype_in,
        )
        df = data.to_df()
        print(f"✅ Downloaded {len(df):,} records successfully!")

        clean_sym = symbol.replace(".", "_")
        clean_start = start.split("T")[0]
        filename = f"{dataset}_{clean_sym}_{schema}_{clean_start}.{output_format}"
        out_path = DATA_DIR / filename

        if output_format == "parquet":
            df.to_parquet(out_path, index=False)
        else:
            df.to_csv(out_path, index=False)

        print(f"💾 Saved to: {out_path} ({out_path.stat().st_size / (1024 * 1024):.2f} MB)")
        return out_path

    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch CME Gold Futures MBP-1 data from Databento")
    parser.add_argument("--key", type=str, default="", help="Databento API key")
    parser.add_argument("--dataset", type=str, default=DEFAULT_DATASET, help="Dataset identifier")
    parser.add_argument("--symbol", type=str, default=DEFAULT_SYMBOL, help="Symbol (e.g. GC.c.0, GC.FUT, GCZ4)")
    parser.add_argument("--schema", type=str, default=DEFAULT_SCHEMA, help="Schema (e.g. mbp-1, mbp-10, trades)")
    parser.add_argument("--start", type=str, default="2024-10-21T13:30:00", help="Start UTC timestamp")
    parser.add_argument("--end", type=str, default="2024-10-21T14:30:00", help="End UTC timestamp")
    parser.add_argument("--format", type=str, default="parquet", choices=["parquet", "csv"], help="Output format")
    parser.add_argument("--yes", action="store_true", help="Skip cost confirmation prompt")

    args = parser.parse_args()
    fetch_databento_gold(
        api_key=args.key,
        dataset=args.dataset,
        symbol=args.symbol,
        schema=args.schema,
        start=args.start,
        end=args.end,
        output_format=args.format,
        force_download=args.yes,
    )
