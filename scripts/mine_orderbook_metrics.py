#!/usr/bin/env python3
"""
High-Frequency Order Book & Microstructure Mining Engine
Processes Databento MBP-1 Gold Futures (GC) data to calculate:
- Order Book Imbalance (OBI)
- Volume-Weighted Micro-Price
- Bid-Ask Spread Dynamics
- Cumulative Volume Delta (CVD) & Trade Flow Pressure
- High-Frequency Volatility and Liquidity Metrics
"""

import sys
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
from config import DATA_DIR, OUTPUT_DIR


def mine_mbp1_data(input_file: Path):
    """Run quantitative mining pipeline on MBP-1 dataset."""
    print("\n" + "=" * 65)
    print("🔬 DATABENTO MBP-1 MARKET MICROSTRUCTURE MINER")
    print("=" * 65)
    print(f"Reading: {input_file.name}...")

    if input_file.suffix == ".parquet":
        df = pd.read_parquet(input_file)
    elif input_file.suffix == ".csv":
        df = pd.read_csv(input_file)
    else:
        raise ValueError(f"Unsupported format: {input_file.suffix}. Expected .parquet or .csv")

    total_records = len(df)
    print(f"Loaded:  {total_records:,} events")

    # 1. Basic Mid-Price & Spread
    mid_price = (df["bid_px_00"] + df["ask_px_00"]) / 2.0
    spread = df["ask_px_00"] - df["bid_px_00"]
    spread_bps = (spread / mid_price) * 10000.0

    # 2. Order Book Imbalance (OBI)
    # OBI = (bid_sz - ask_sz) / (bid_sz + ask_sz)
    total_l1_depth = df["bid_sz_00"] + df["ask_sz_00"]
    obi = np.where(total_l1_depth > 0, (df["bid_sz_00"] - df["ask_sz_00"]) / total_l1_depth, 0.0)

    # 3. Micro-Price (Volume Weighted Top-of-Book Price)
    # micro_px = (bid_px * ask_sz + ask_px * bid_sz) / (bid_sz + ask_sz)
    micro_price = np.where(
        total_l1_depth > 0,
        (df["bid_px_00"] * df["ask_sz_00"] + df["ask_px_00"] * df["bid_sz_00"]) / total_l1_depth,
        mid_price
    )

    # 4. Trade Analysis & Volume Delta
    trades_mask = df["action"] == "T"
    trades_df = df[trades_mask].copy()
    
    total_trades = len(trades_df)
    buy_trades = trades_df[trades_df["side"] == "A"]
    sell_trades = trades_df[trades_df["side"] == "B"]
    
    buy_volume = buy_trades["size"].sum() if not buy_trades.empty else 0
    sell_volume = sell_trades["size"].sum() if not sell_trades.empty else 0
    net_volume_delta = buy_volume - sell_volume
    total_traded_volume = buy_volume + sell_volume

    # 5. Compile Results
    results = {
        "Dataset File": input_file.name,
        "Total Events": total_records,
        "Total Trades Executed": total_trades,
        "Trade Event Ratio": f"{(total_trades / total_records * 100):.2f}%",
        "Total Volume Traded (Contracts)": int(total_traded_volume),
        "Aggressive Buy Volume": int(buy_volume),
        "Aggressive Sell Volume": int(sell_volume),
        "Net Volume Delta (CVD)": int(net_volume_delta),
        "Buy/Sell Volume Ratio": f"{(buy_volume / sell_volume):.3f}" if sell_volume > 0 else "N/A",
        "Starting Mid-Price ($)": f"${mid_price.iloc[0]:.2f}",
        "Ending Mid-Price ($)": f"${mid_price.iloc[-1]:.2f}",
        "Max Price Observed ($)": f"${df['price'].max():.2f}",
        "Min Price Observed ($)": f"${df['price'].min():.2f}",
        "Average Bid-Ask Spread ($)": f"${spread.mean():.4f}",
        "Average Spread in Basis Points": f"{spread_bps.mean():.2f} bps",
        "Average Order Book Imbalance (OBI)": f"{obi.mean():+.4f} (range: -1 to +1)",
        "Average Bid Queue Size": f"{df['bid_sz_00'].mean():.1f} contracts",
        "Average Ask Queue Size": f"{df['ask_sz_00'].mean():.1f} contracts",
    }

    # Print Summary to CLI
    print("\n" + "-" * 65)
    print("📊 MINED QUANTITATIVE METRICS")
    print("-" * 65)
    for k, v in results.items():
        print(f"  • {k:<36}: {v}")
    print("-" * 65)

    # 6. Save Markdown Report & Enriched DataFrame
    report_filename = f"MINING_REPORT_{input_file.stem}.md"
    report_path = OUTPUT_DIR / report_filename

    md_report = [
        f"# Market Microstructure Research Report: {input_file.stem}",
        f"\n**Mined At:** {pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"**Input Dataset:** `{input_file.name}`",
        "\n## 📈 Key Microstructure Indicators\n",
        "| Metric | Mined Value | Description |",
        "| :--- | :--- | :--- |",
    ]

    for k, v in results.items():
        md_report.append(f"| **{k}** | `{v}` | Quant metric |")

    md_report.extend([
        "\n## 🧠 Algorithmic Research Takeaways",
        f"- **Order Book Pressure:** Average OBI is `{obi.mean():+.4f}`. {'Strong buy pressure' if obi.mean() > 0.05 else 'Strong sell pressure' if obi.mean() < -0.05 else 'Balanced market equilibrium'}.",
        f"- **Order Flow Delta:** Cumulative Volume Delta is `{net_volume_delta:+,.2f}` units. {'Buyers dominated market orders' if net_volume_delta > 0 else 'Sellers dominated market orders'}.",
        f"- **Liquidity Friction:** Average spread is `{spread.mean():.4f}` (~`{spread_bps.mean():.2f}` bps), indicating {'tight liquidity' if spread.mean() <= 0.15 else 'wide liquidity gap'}.",
        "\n---",
        "*Generated automatically by Databento Research Mining Engine.*"
    ])

    report_path.write_text("\n".join(md_report), encoding="utf-8")
    print(f"\n✅ Research Report generated: {report_path}")

    # Save Enriched Dataset with Micro-Price and OBI columns
    df_enriched = df.copy()
    df_enriched["mid_price"] = mid_price
    df_enriched["micro_price"] = micro_price
    df_enriched["spread"] = spread
    df_enriched["obi"] = obi
    
    enriched_path = OUTPUT_DIR / f"{input_file.stem}_enriched.parquet"
    df_enriched.to_parquet(enriched_path, index=False)
    print(f"💾 Enriched Dataset saved with OBI & Micro-Price: {enriched_path}")
    return report_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mine MBP-1 Order Book Metrics")
    parser.add_argument("--input", type=str, default=str(DATA_DIR / "GC_sample_mbp1.parquet"), help="Path to input parquet/csv")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"⚠️ Input file not found: {input_path}")
        print("Generating synthetic CME GC MBP-1 sample dataset first...")
        from download_sample_data import generate_cme_gc_mbp1_sample
        input_path = generate_cme_gc_mbp1_sample()

    mine_mbp1_data(input_path)
