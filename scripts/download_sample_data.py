#!/usr/bin/env python3
"""
Databento Sample Data Fetcher & Synthesizer
Provides instant sample MBP-1 dataset for CME Gold Futures (GC) for immediate
research and testing without requiring paid API credits.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
from config import DATA_DIR


def generate_cme_gc_mbp1_sample(num_records=5000, output_filename="GC_sample_mbp1.parquet"):
    """
    Generate a high-fidelity synthetic CME Gold Futures (GC) MBP-1 dataset
    matching the exact schema, types, and microstructure dynamics of CME Globex MDP 3.0.
    """
    print(f"📦 Generating high-fidelity CME Gold Futures (GC) MBP-1 sample ({num_records} events)...")
    
    np.random.seed(42)
    start_ts = pd.Timestamp("2024-10-21 13:30:00", tz="UTC")
    
    # Gold trades with tick size of 0.10 ($10 per contract)
    base_price = 2735.50
    tick_size = 0.10
    
    ts_recv_list = []
    ts_event_list = []
    actions = []
    sides = []
    prices = []
    sizes = []
    bid_px_00 = []
    ask_px_00 = []
    bid_sz_00 = []
    ask_sz_00 = []
    bid_ct_00 = []
    ask_ct_00 = []
    symbols = []

    curr_bid = base_price
    curr_ask = base_price + tick_size
    curr_bid_sz = 15
    curr_ask_sz = 12
    curr_bid_ct = 4
    curr_ask_ct = 3

    current_time = start_ts

    for i in range(num_records):
        # Time steps in nanoseconds / microseconds (typical CME latency)
        delta_ns = int(np.random.exponential(scale=2_500_000)) # ~2.5ms interval
        current_time += pd.Timedelta(nanoseconds=delta_ns)
        ts_event = int(current_time.value)
        ts_recv = ts_event + int(np.random.normal(loc=150_000, scale=20_000)) # Databento colocation capture delay

        event_type = np.random.choice(["trade", "book_update", "cancel"], p=[0.25, 0.55, 0.20])

        if event_type == "trade":
            action = "T"
            trade_side = np.random.choice(["A", "B"], p=[0.52, 0.48]) # A = taker bought from ask, B = taker sold to bid
            if trade_side == "A":
                side = "A"
                px = curr_ask
                sz = int(np.random.geometric(p=0.4))
                curr_ask_sz = max(1, curr_ask_sz - sz)
            else:
                side = "B"
                px = curr_bid
                sz = int(np.random.geometric(p=0.4))
                curr_bid_sz = max(1, curr_bid_sz - sz)
        elif event_type == "book_update":
            action = np.random.choice(["A", "M"], p=[0.6, 0.4])
            side = np.random.choice(["B", "A"])
            sz = int(np.random.randint(1, 20))
            if side == "B":
                # Bid shift or depth add
                if np.random.rand() > 0.85:
                    step = np.random.choice([-tick_size, tick_size])
                    curr_bid = round(curr_bid + step, 2)
                    if curr_bid >= curr_ask:
                        curr_ask = round(curr_bid + tick_size, 2)
                curr_bid_sz = int(np.random.randint(5, 50))
                curr_bid_ct = int(np.random.randint(1, 10))
                px = curr_bid
            else:
                if np.random.rand() > 0.85:
                    step = np.random.choice([-tick_size, tick_size])
                    curr_ask = round(curr_ask + step, 2)
                    if curr_ask <= curr_bid:
                        curr_bid = round(curr_ask - tick_size, 2)
                curr_ask_sz = int(np.random.randint(5, 50))
                curr_ask_ct = int(np.random.randint(1, 10))
                px = curr_ask
        else: # cancel
            action = "C"
            side = np.random.choice(["B", "A"])
            sz = int(np.random.randint(1, 5))
            if side == "B":
                px = curr_bid
                curr_bid_sz = max(1, curr_bid_sz - sz)
                curr_bid_ct = max(1, curr_bid_ct - 1)
            else:
                px = curr_ask
                curr_ask_sz = max(1, curr_ask_sz - sz)
                curr_ask_ct = max(1, curr_ask_ct - 1)

        ts_recv_list.append(ts_recv)
        ts_event_list.append(ts_event)
        actions.append(action)
        sides.append(side)
        prices.append(px)
        sizes.append(sz)
        bid_px_00.append(curr_bid)
        ask_px_00.append(curr_ask)
        bid_sz_00.append(curr_bid_sz)
        ask_sz_00.append(curr_ask_sz)
        bid_ct_00.append(curr_bid_ct)
        ask_ct_00.append(curr_ask_ct)
        symbols.append("GCZ4")

    df = pd.DataFrame({
        "ts_recv": pd.to_datetime(ts_recv_list, unit="ns", utc=True),
        "ts_event": pd.to_datetime(ts_event_list, unit="ns", utc=True),
        "symbol": symbols,
        "action": actions,
        "side": sides,
        "price": prices,
        "size": sizes,
        "bid_px_00": bid_px_00,
        "ask_px_00": ask_px_00,
        "bid_sz_00": bid_sz_00,
        "ask_sz_00": ask_sz_00,
        "bid_ct_00": bid_ct_00,
        "ask_ct_00": ask_ct_00,
    })

    out_file = DATA_DIR / output_filename
    df.to_parquet(out_file, index=False)
    print(f"✅ Generated sample parquet dataset: {out_file}")
    print(f"   Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"   Date Range: {df['ts_event'].min()} to {df['ts_event'].max()}")
    print(f"   Gold Mid-Price: ${((df['bid_px_00'] + df['ask_px_00']) / 2).iloc[-1]:.2f}")
    return out_file


if __name__ == "__main__":
    generate_cme_gc_mbp1_sample()
