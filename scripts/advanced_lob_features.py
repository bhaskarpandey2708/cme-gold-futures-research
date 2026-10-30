#!/usr/bin/env python3
"""
CME Gold Advanced LOB Feature Engineering & Triple Barrier Labeling Engine
=========================================================================
Institutional-grade feature engineering for high-frequency microstructure prediction:
- Multi-dimensional Limit Order Book (LOB) geometry
- Order Count Imbalance (OCI) and Average Depth per Participant
- Volume-Synchronized Probability of Toxicity (VPIN)
- Cumulative Volume Delta (CVD) multi-scale signatures
- Marcos López de Prado's Triple Barrier Labeling (dynamic volatility barriers)

Outputs:
- Enriched dataset with normalized feature vectors and triple-barrier target labels.
- Stores output directly on Google Drive to maintain zero local storage overhead.
"""

import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
GDRIVE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = GDRIVE_DIR / "data" if GDRIVE_DIR.exists() else BASE_DIR / "data"
OUTPUT_DIR = GDRIVE_DIR / "output" if GDRIVE_DIR.exists() else BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def compute_advanced_microstructure_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer institutional-grade microstructure feature set from MBP-1 order book data."""
    df = df.copy()

    # 1. Core Price Geometry
    df["mid"] = (df["bid_px_00"] + df["ask_px_00"]) / 2.0
    df["spread"] = df["ask_px_00"] - df["bid_px_00"]
    df["spread_bps"] = (df["spread"] / df["mid"]) * 10000.0
    df["spread_vol_20"] = df["spread_bps"].rolling(20).std().fillna(0.0)

    # 2. Book Depth & Queue Imbalance
    tot_sz = df["bid_sz_00"] + df["ask_sz_00"]
    df["obi"] = np.where(tot_sz > 0, (df["bid_sz_00"] - df["ask_sz_00"]) / tot_sz, 0.0)
    df["queue_ratio"] = np.log((df["bid_sz_00"] + 1e-4) / (df["ask_sz_00"] + 1e-4))
    df["d_obi_3"] = df["obi"].diff(3).fillna(0.0)
    df["d_obi_10"] = df["obi"].diff(10).fillna(0.0)

    # 3. Micro-Price Elasticity
    df["micro_price"] = np.where(
        tot_sz > 0,
        (df["bid_sz_00"] * df["ask_px_00"] + df["ask_sz_00"] * df["bid_px_00"]) / tot_sz,
        df["mid"]
    )
    df["micro_spread_bps"] = ((df["micro_price"] - df["mid"]) / df["mid"]) * 10000.0

    # 4. Order Count Imbalance (OCI) & Institutional Block Profiling
    tot_ct = df["bid_ct_00"] + df["ask_ct_00"]
    df["oci"] = np.where(tot_ct > 0, (df["bid_ct_00"] - df["ask_ct_00"]) / tot_ct, 0.0)
    df["avg_bid_size"] = np.where(df["bid_ct_00"] > 0, df["bid_sz_00"] / df["bid_ct_00"], df["bid_sz_00"])
    df["avg_ask_size"] = np.where(df["ask_ct_00"] > 0, df["ask_sz_00"] / df["ask_ct_00"], df["ask_sz_00"])
    df["size_per_order_skew"] = np.log((df["avg_bid_size"] + 1e-4) / (df["avg_ask_size"] + 1e-4))

    # 5. Trade Flow & Flow Toxicity (VPIN & CVD)
    trade_signs = np.where(df["side"] == "B", 1, np.where(df["side"] == "A", -1, 0))
    trade_vol = df["size"].fillna(0.0)
    df["signed_vol"] = trade_signs * trade_vol
    df["cvd_10"] = df["signed_vol"].rolling(10).sum().fillna(0.0)
    df["cvd_50"] = df["signed_vol"].rolling(50).sum().fillna(0.0)

    # VPIN: Order flow toxicity proxy over 30-tick rolling bucket
    abs_signed_vol = df["signed_vol"].abs().rolling(30).sum()
    sum_vol = trade_vol.rolling(30).sum()
    df["vpin_30"] = np.nan_to_num(np.where(sum_vol > 0, abs_signed_vol / sum_vol, 0.0), nan=0.0)

    # 6. Realized Volatility & Multi-Horizon Momentum
    ret_1 = df["mid"].pct_change().fillna(0.0)
    df["vol_20"] = ret_1.rolling(20).std().fillna(0.0) * 10000.0
    df["vol_50"] = ret_1.rolling(50).std().fillna(0.0) * 10000.0
    df["mom_5"] = (df["mid"] - df["mid"].shift(5)).fillna(0.0) / (df["vol_20"] + 1e-5)
    df["mom_15"] = (df["mid"] - df["mid"].shift(15)).fillna(0.0) / (df["vol_50"] + 1e-5)

    return df


def apply_triple_barrier_labeling(df: pd.DataFrame, pt_mult: float = 1.0, sl_mult: float = 1.0, max_ticks: int = 20) -> pd.DataFrame:
    """
    Marcos López de Prado's Triple Barrier Labeling Method:
    - Upper Barrier (Profit Target): mid_t * (1 + pt_mult * sigma_t) -> Label: +1 (BUY)
    - Lower Barrier (Stop Loss):     mid_t * (1 - sl_mult * sigma_t) -> Label: -1 (SELL)
    - Vertical Barrier (Time Exit):  max_ticks forward                -> Label: sign of mid_t+max - mid_t
    """
    df = df.copy()
    n = len(df)
    labels = np.zeros(n, dtype=np.float32)
    barrier_hit = []

    mid = df["mid"].values
    vol = df["vol_20"].values / 10000.0  # Volatility in fractional return

    for i in range(n - max_ticks):
        entry_mid = mid[i]
        curr_vol = max(vol[i], 0.0001)  # Minimum volatility floor of 1 bps

        upper_barrier = entry_mid * (1.0 + pt_mult * curr_vol)
        lower_barrier = entry_mid * (1.0 - sl_mult * curr_vol)

        hit = 0  # 0 = timeout, 1 = profit target hit first, -1 = stop loss hit first
        hit_tick = max_ticks

        for t in range(1, max_ticks + 1):
            future_mid = mid[i + t]
            if future_mid >= upper_barrier:
                hit = 1
                hit_tick = t
                break
            elif future_mid <= lower_barrier:
                hit = -1
                hit_tick = t
                break

        if hit == 0:
            # Vertical barrier timeout: label based on directional sign at expiration
            ret_at_timeout = (mid[i + max_ticks] - entry_mid) / entry_mid
            if ret_at_timeout > 0.00005:  # > 0.5 bps
                hit = 1
            elif ret_at_timeout < -0.00005:
                hit = -1
            else:
                hit = 0

        labels[i] = hit
        barrier_hit.append(hit_tick)

    # Pad remaining tail
    barrier_hit.extend([0] * max_ticks)

    df["tb_label"] = labels
    df["tb_hit_tick"] = barrier_hit

    # Binary labels for neural classification: 1 = BUY, 0 = SELL/FLAT
    df["tb_target_buy"] = np.where(df["tb_label"] == 1, 1.0, 0.0)
    df["tb_target_direction"] = np.where(df["tb_label"] == 1, 1.0, np.where(df["tb_label"] == -1, 0.0, 0.5))

    return df


def get_feature_columns() -> list:
    """Return list of institutional predictive feature column names."""
    return [
        "obi", "queue_ratio", "d_obi_3", "d_obi_10",
        "micro_spread_bps", "spread_bps", "spread_vol_20",
        "oci", "size_per_order_skew",
        "cvd_10", "cvd_50", "vpin_30",
        "vol_20", "vol_50", "mom_5", "mom_15"
    ]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Advanced LOB Feature Engineering")
    parser.add_argument("--input", type=str, default=None, help="Path to input parquet file")
    parser.add_argument("--output", type=str, default=None, help="Path to output parquet file")
    args = parser.parse_args()

    print("=" * 70)
    print("🔬 ADVANCED MICROSTRUCTURE FEATURE ENGINEERING & TRIPLE BARRIER LABELING")
    print("=" * 70)

    # Find dataset
    if args.input:
        dataset_path = Path(args.input)
    else:
        dataset_path = DATA_DIR / "GC_sample_mbp1.parquet"
        if not dataset_path.exists():
            parquets = list(DATA_DIR.glob("*.parquet"))
            if parquets:
                dataset_path = parquets[0]
            else:
                print("❌ No parquet dataset found.")
                sys.exit(1)

    print(f"[*] Processing dataset: {dataset_path}")
    raw_df = pd.read_parquet(dataset_path)
    print(f"[*] Input records: {len(raw_df):,}")

    enriched_df = compute_advanced_microstructure_features(raw_df)
    labeled_df = apply_triple_barrier_labeling(enriched_df, pt_mult=1.0, sl_mult=1.0, max_ticks=20)

    feature_cols = get_feature_columns()
    print(f"[✓] Successfully engineered {len(feature_cols)} advanced microstructure features:")
    for col in feature_cols:
        print(f"    • {col:<20} | mean: {labeled_df[col].mean():>8.4f} | std: {labeled_df[col].std():>8.4f}")

    print("\n📊 Triple Barrier Label Distribution:")
    tb_dist = labeled_df["tb_label"].value_counts(normalize=True) * 100.0
    for label_val, pct in tb_dist.items():
        name = "BUY (+1)" if label_val == 1 else "SELL (-1)" if label_val == -1 else "FLAT/TIMEOUT (0)"
        print(f"    • {name:<18}: {pct:>6.2f}%")

    if args.output:
        out_file = Path(args.output)
    else:
        out_file = DATA_DIR / f"{dataset_path.stem}_advanced_features.parquet"

    out_file.parent.mkdir(parents=True, exist_ok=True)
    labeled_df.to_parquet(out_file)
    print(f"\n[✓] Persisted advanced feature dataset: {out_file}")
    print(f"    File Size: {out_file.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
