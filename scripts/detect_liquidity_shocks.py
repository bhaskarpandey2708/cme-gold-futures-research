#!/usr/bin/env python3
"""
CME Gold Market Liquidity Shock & Order Flow Toxicity Detector
==============================================================
Identifies high-frequency microstructure anomalies:
1. Spread Blowouts (Spread > 2.5x rolling mean)
2. Book Depth Flash Vacuums (Queue sizes < 25% rolling mean)
3. Volume-Synchronized Probability of Toxicity (VPIN)
4. Institutional Aggressive Sweeps (Multi-tick consecutive taker bursts)

Usage:
  python3 scripts/detect_liquidity_shocks.py --input data/GC_sample_mbp1.parquet
  python3 scripts/detect_liquidity_shocks.py --input data/gold_mbp1_scraped_20261022_173140.parquet
"""

import sys
import argparse
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


def calculate_vpin(df: pd.DataFrame, bucket_volume: float = 50.0, n_buckets: int = 10) -> float:
    """Compute Volume-Synchronized Probability of Toxicity (VPIN)."""
    if "side" not in df.columns or "size" not in df.columns:
        return 0.0

    trades = df[df["action"] == "T"].copy()
    if trades.empty:
        return 0.0

    bucket_imbalances = []
    curr_buy = 0.0
    curr_sell = 0.0
    curr_vol = 0.0

    for _, row in trades.iterrows():
        sz = float(row["size"])
        side = row["side"]
        if side == "B":
            curr_buy += sz
        elif side == "A":
            curr_sell += sz
        curr_vol += sz

        if curr_vol >= bucket_volume:
            imbalance = abs(curr_buy - curr_sell)
            bucket_imbalances.append(imbalance)
            curr_buy = 0.0
            curr_sell = 0.0
            curr_vol = 0.0

    if len(bucket_imbalances) < 2:
        return 0.0

    recent_imbalances = bucket_imbalances[-n_buckets:]
    vpin = sum(recent_imbalances) / (len(recent_imbalances) * bucket_volume)
    return float(min(vpin, 1.0))


def detect_shocks(df: pd.DataFrame, spread_multiplier: float = 2.5, depth_fraction: float = 0.25) -> tuple:
    """Scan order book events for microstructural liquidity shocks."""
    df = df.copy().reset_index(drop=True)

    df["spread"] = df["ask_px_00"] - df["bid_px_00"]
    df["total_depth"] = df["bid_sz_00"] + df["ask_sz_00"]

    rolling_spread = df["spread"].rolling(50, min_periods=10).mean()
    rolling_depth = df["total_depth"].rolling(50, min_periods=10).mean()

    # 1. Spread Blowout Events
    spread_blowouts = df[df["spread"] > (rolling_spread * spread_multiplier)].copy()

    # 2. Flash Queue Vacuums (Liquidity Holes)
    depth_vacuums = df[df["total_depth"] < (rolling_depth * depth_fraction)].copy()

    # 3. Aggressive Sweeps (3+ consecutive trades on same side)
    sweeps = []
    if "action" in df.columns and "side" in df.columns:
        trades = df[df["action"] == "T"].copy()
        consec_side = None
        consec_count = 0
        sweep_vol = 0.0
        start_ts = None

        for _, tr in trades.iterrows():
            side = tr["side"]
            if side in ("B", "A"):
                if side == consec_side:
                    consec_count += 1
                    sweep_vol += float(tr["size"])
                else:
                    if consec_count >= 3:
                        sweeps.append({
                            "ts": start_ts,
                            "side": "BUY_SWEEP" if consec_side == "B" else "SELL_SWEEP",
                            "consecutive_trades": consec_count,
                            "total_volume": sweep_vol,
                        })
                    consec_side = side
                    consec_count = 1
                    sweep_vol = float(tr["size"])
                    start_ts = tr.get("ts_recv")

        if consec_count >= 3:
            sweeps.append({
                "ts": start_ts,
                "side": "BUY_SWEEP" if consec_side == "B" else "SELL_SWEEP",
                "consecutive_trades": consec_count,
                "total_volume": sweep_vol,
            })

    # VPIN Calculation
    vpin = calculate_vpin(df)

    metrics = {
        "total_events": len(df),
        "avg_spread": float(df["spread"].mean()),
        "max_spread": float(df["spread"].max()),
        "spread_blowouts_count": len(spread_blowouts),
        "depth_vacuums_count": len(depth_vacuums),
        "aggressive_sweeps_count": len(sweeps),
        "vpin_toxicity": vpin,
        "sweeps": sweeps,
    }

    return metrics, spread_blowouts, depth_vacuums


def generate_shock_report(input_file: Path, metrics: dict) -> Path:
    """Generate Markdown Liquidity Shock Report."""
    timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_file = OUTPUT_DIR / f"LIQUIDITY_SHOCK_REPORT_{input_file.stem}_{timestamp_str}.md"

    vpin = metrics["vpin_toxicity"]
    toxicity_level = "🚨 HIGH (Informed Trading Surge)" if vpin > 0.50 else "🟡 MODERATE" if vpin > 0.25 else "🟢 LOW (Balanced Market Flow)"

    md = [
        "# ⚡ CME Gold Market Liquidity Shock & Toxicity Report",
        f"\n**Target Dataset:** `{input_file.name}`  ",
        f"**Audit Date:** `{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}`  ",
        "**Microstructure Focus:** Spread Blowouts, Flash Depth Vacuums, & VPIN Toxicity  ",
        "\n---",
        "\n## 📊 1. Liquidity Stress Indicators\n",
        "| Microstructure Metric | Mined Value | Baseline Benchmark | Risk Status |",
        "| :--- | :---: | :---: | :---: |",
        f"| **Average Bid-Ask Spread** | `${metrics['avg_spread']:.4f}` | $0.10 - $0.35 | Normal |",
        f"| **Maximum Spread Spike** | `${metrics['max_spread']:.4f}` | < $1.00 | {'🚨 Stretched' if metrics['max_spread'] > 1.0 else 'Normal'} |",
        f"| **Spread Blowouts (>2.5x Mean)** | `{metrics['spread_blowouts_count']}` events | 0 | {'⚠️ Anomalies Detected' if metrics['spread_blowouts_count'] > 0 else 'Stable'} |",
        f"| **Depth Vacuums (<25% Mean)** | `{metrics['depth_vacuums_count']}` events | 0 | {'⚠️ Thin Liquidity' if metrics['depth_vacuums_count'] > 0 else 'Healthy'} |",
        f"| **Aggressive Trade Sweeps** | `{metrics['aggressive_sweeps_count']}` sweeps | Normal | Active Flow |",
        f"| **VPIN Flow Toxicity** | `{vpin:.4f}` | < 0.35 | {toxicity_level} |",
        "\n---",
        "\n## 🌊 2. Recent Institutional Sweeps\n",
        "| Sweep Timestamp (ns) | Sweep Direction | Trade Chain Count | Total Sweep Volume |",
        "| :--- | :---: | :---: | :---: |",
    ]

    for sw in metrics.get("sweeps", [])[:10]:
        md.append(f"| `{sw['ts']}` | **`{sw['side']}`** | `{sw['consecutive_trades']}` trades | `{sw['total_volume']:.2f}` units |")

    if not metrics.get("sweeps"):
        md.append("| *None detected in sample* | --- | --- | --- |")

    md.extend([
        "\n---",
        "\n## 🧠 3. Microstructure Risk Management Insights",
        "- **Adverse Selection Protection:** When VPIN exceeds 0.35 or spread blowouts occur, market-making algorithms should widen quoted bid-ask spreads or reduce resting size.",
        "- **Execution Slippage Avoidance:** Institutional sweeps indicate aggressive taker orders consuming multiple queue layers; market orders during these periods incur elevated slippage friction.",
        "\n---",
        "*Generated automatically by Databento CME Gold Quantitative Toxicity Engine.*"
    ])

    report_file.write_text("\n".join(md), encoding="utf-8")
    return report_file


def main():
    parser = argparse.ArgumentParser(description="Detect Market Liquidity Shocks & Flow Toxicity")
    parser.add_argument("--input", type=str, default=str(DATA_DIR / "GC_sample_mbp1.parquet"), help="Path to input MBP-1 dataset")
    args = parser.parse_args()

    input_path = Path(args.input)
    print("=" * 70)
    print("⚡ CME GOLD LIQUIDITY SHOCK & TOXICITY DETECTOR")
    print("=" * 70)
    print(f"Dataset: {input_path.name}")

    df = pd.read_parquet(input_path) if input_path.suffix == ".parquet" else pd.read_csv(input_path)
    metrics, blowouts, vacuums = detect_shocks(df)

    report_path = generate_shock_report(input_path, metrics)

    print("\n" + "=" * 70)
    print("📊 LIQUIDITY SHOCK AUDIT SUMMARY")
    print("=" * 70)
    print(f"Total Events Scanned:    {metrics['total_events']:,}")
    print(f"Spread Blowouts (>2.5x): {metrics['spread_blowouts_count']} events")
    print(f"Depth Vacuums (<25%):    {metrics['depth_vacuums_count']} events")
    print(f"Aggressive Sweeps:       {metrics['aggressive_sweeps_count']} sweeps")
    print(f"VPIN Flow Toxicity:      {metrics['vpin_toxicity']:.4f}")
    print(f"Audit Report:            {report_path}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
