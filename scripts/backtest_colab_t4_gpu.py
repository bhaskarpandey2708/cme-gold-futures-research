"""
CME Gold Deep Order Book BiLSTM-Attention Model Backtester
==========================================================
GPU-Accelerated Microstructure Alpha Strategy Backtest
Executed on Google Colab NVIDIA Tesla T4 GPU

Evaluates:
- Midpoint Execution (Benchmark / Dark Pool)
- Passive Maker Execution (Posting Limit Orders at BBO)
- Aggressive Taker Execution (Crossing Spread)
"""

import os
import sys
import time
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("=" * 70)
print("⚡ CME GOLD BiLSTM-ATTENTION ALPHA BACKTEST (TESLA T4 GPU)")
print("=" * 70)
print(f"Device: {device}")

# 1. Architecture
class DeepOrderBookNet(nn.Module):
    def __init__(self, input_dim=7, hidden_dim=64, num_layers=2):
        super(DeepOrderBookNet, self).__init__()
        self.bilstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=0.2 if num_layers > 1 else 0.0
        )
        self.attention = nn.MultiheadAttention(embed_dim=hidden_dim * 2, num_heads=4, batch_first=True)
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim * 2, 64),
            nn.LayerNorm(64),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.3),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        lstm_out, _ = self.bilstm(x)
        attn_out, _ = self.attention(lstm_out, lstm_out, lstm_out)
        pooled = attn_out[:, -1, :]
        out = self.fc(pooled)
        return out


# 2. Load Checkpoint
from pathlib import Path
candidate_ckpts = [
    Path("/content/gold_orderbook_t4_model.pt"),
    Path("models/gold_orderbook_t4_model.pt"),
    Path(__file__).parent.parent / "models" / "gold_orderbook_t4_model.pt",
    Path("gold_orderbook_t4_model.pt")
]
ckpt_path = None
for p in candidate_ckpts:
    if p.exists():
        ckpt_path = str(p)
        break

if not ckpt_path:
    print(f"❌ Checkpoint not found in candidate locations: {candidate_ckpts}")
    sys.exit(1)

model = DeepOrderBookNet(input_dim=7, hidden_dim=64, num_layers=2).to(device)
model.load_state_dict(torch.load(ckpt_path, map_location=device))
model.eval()
print(f"[✓] Loaded model checkpoint from: {ckpt_path}")

# 3. Load Dataset
candidate_data = [
    Path("/content/GC_sample_mbp1.parquet"),
    Path("data/GC_sample_mbp1.parquet"),
    Path(__file__).parent.parent / "data" / "GC_sample_mbp1.parquet",
    Path("GC_sample_mbp1.parquet")
]
data_path = None
for p in candidate_data:
    if p.exists():
        data_path = str(p)
        break

if not data_path and os.path.exists("/content"):
    parquets = [os.path.join("/content", f) for f in os.listdir("/content") if f.endswith(".parquet")]
    if parquets:
        data_path = parquets[0]

if not data_path:
    print("❌ No parquet dataset found.")
    sys.exit(1)

print(f"[*] Loading dataset: {data_path}")
df = pd.read_parquet(data_path)

mid = (df["bid_px_00"] + df["ask_px_00"]) / 2.0
tot_sz = df["bid_sz_00"] + df["ask_sz_00"]
spread = df["ask_px_00"] - df["bid_px_00"]

obi = np.where(tot_sz > 0, (df["bid_sz_00"] - df["ask_sz_00"]) / tot_sz, 0.0)
micro = np.where(tot_sz > 0, (df["bid_sz_00"] * df["ask_px_00"] + df["ask_sz_00"] * df["bid_px_00"]) / tot_sz, mid)
micro_spread = micro - mid
spread_bps = (spread / mid) * 10000.0
d_obi = pd.Series(obi).diff(3).fillna(0.0).values
queue_ratio = np.log((df["bid_sz_00"] + 1e-4) / (df["ask_sz_00"] + 1e-4))
roll_vol = mid.pct_change().rolling(20).std().fillna(0.0).values * 10000.0

trade_signs = np.where(df["side"] == "B", 1, np.where(df["side"] == "A", -1, 0))
cvd_10 = pd.Series(trade_signs * df["size"]).rolling(10).sum().fillna(0.0).values

feature_matrix = np.column_stack([obi, micro_spread, spread_bps, d_obi, queue_ratio, roll_vol, cvd_10])

# Standardize
mean_f = np.mean(feature_matrix, axis=0)
std_f = np.std(feature_matrix, axis=0)
std_f[std_f == 0] = 1.0
norm_features = (feature_matrix - mean_f) / std_f

T_SEQ = 20
horizon = 5

X_seq = []
indices = []
for i in range(T_SEQ, len(norm_features) - horizon):
    X_seq.append(norm_features[i - T_SEQ:i])
    indices.append(i)

X_arr = torch.tensor(np.array(X_seq, dtype=np.float32)).to(device)

print(f"[*] Running batched inference across {len(X_arr):,} temporal windows on Tesla T4...")
t0 = time.time()
with torch.no_grad():
    if torch.cuda.is_available():
        with torch.amp.autocast('cuda'):
            logits = model(X_arr)
            probs = torch.sigmoid(logits).cpu().numpy().flatten()
    else:
        logits = model(X_arr)
        probs = torch.sigmoid(logits).cpu().numpy().flatten()

infer_time = time.time() - t0
print(f"[✓] Inference complete in {infer_time:.3f}s ({len(probs)/infer_time:,.0f} ticks/sec)")

# 4. Out-of-Sample Discrete Trade Simulation Engine
test_start_idx = int(len(probs) * 0.8)
test_probs = probs[test_start_idx:]
test_indices = indices[test_start_idx:]
test_sub_df = df.iloc[test_indices].reset_index(drop=True)

def simulate_regime(mode="mid", long_thresh=0.55, short_thresh=0.45, hold_ticks=5):
    """Simulate discrete state-machine trading under a specific execution regime."""
    pos = 0
    entry_px = 0.0
    entry_idx = 0
    trades = []

    for i in range(len(test_probs) - hold_ticks):
        p = test_probs[i]
        curr_bid = test_sub_df.iloc[i]["bid_px_00"]
        curr_ask = test_sub_df.iloc[i]["ask_px_00"]
        curr_mid = (curr_bid + curr_ask) / 2.0

        if pos == 0:
            if p > long_thresh:
                pos = 1
                entry_idx = i
                entry_px = curr_mid if mode == "mid" else curr_bid if mode == "passive" else curr_ask
            elif p < short_thresh:
                pos = -1
                entry_idx = i
                entry_px = curr_mid if mode == "mid" else curr_ask if mode == "passive" else curr_bid

        elif pos != 0:
            held = i - entry_idx
            reversal = (pos == 1 and p < short_thresh) or (pos == -1 and p > long_thresh)
            if held >= hold_ticks or reversal:
                if mode == "mid":
                    exit_px = curr_mid
                elif mode == "passive":
                    exit_px = curr_ask if pos == 1 else curr_bid
                else:  # taker
                    exit_px = curr_bid if pos == 1 else curr_ask

                gross_ret = (exit_px - entry_px) / entry_px if pos == 1 else (entry_px - exit_px) / entry_px
                # Exchange fee: 0.1 bps
                fee = 0.00001
                net_ret = gross_ret - fee
                pnl = net_ret * entry_px * 100.0  # $100 per pt (100 oz)

                trades.append({
                    "pos": "LONG" if pos == 1 else "SHORT",
                    "entry_px": entry_px,
                    "exit_px": exit_px,
                    "held": held,
                    "net_ret": net_ret,
                    "pnl": pnl
                })
                pos = 0

    if not trades:
        return {"trades": 0, "win_rate": 0.0, "pnl": 0.0, "sharpe": 0.0, "profit_factor": 0.0}

    tdf = pd.DataFrame(trades)
    wins = tdf[tdf["pnl"] > 0]
    losses = tdf[tdf["pnl"] < 0]
    win_rate = (len(wins) / len(tdf)) * 100.0
    gross_win = wins["pnl"].sum() if len(wins) > 0 else 0.0
    gross_loss = abs(losses["pnl"].sum()) if len(losses) > 0 else 1e-6
    pf = gross_win / gross_loss
    tot_pnl = tdf["pnl"].sum()
    std_pnl = tdf["pnl"].std()
    sharpe = (tdf["pnl"].mean() / std_pnl) * np.sqrt(252 * 50) if std_pnl > 0 else 0.0

    return {
        "trades": len(tdf),
        "win_rate": round(float(win_rate), 2),
        "profit_factor": round(float(pf), 2),
        "total_pnl": round(float(tot_pnl), 2),
        "sharpe": round(float(sharpe), 2),
        "avg_hold_ticks": round(float(tdf["held"].mean()), 1)
    }

print("\n" + "=" * 70)
print("📊 EVALUATING EXECUTION REGIMES ON TESLA T4")
print("=" * 70)

mid_res = simulate_regime(mode="mid")
pass_res = simulate_regime(mode="passive")
take_res = simulate_regime(mode="taker")

print(f"| Regime         | Trades | Win Rate | Profit Factor | Total PnL ($) | Sharpe Ratio |")
print(f"| :------------- | :----- | :------- | :------------ | :------------ | :----------- |")
print(f"| Midpoint (Ref) | {mid_res['trades']:<6} | {mid_res['win_rate']:>7.2f}% | {mid_res['profit_factor']:>13.2f} | ${mid_res['total_pnl']:>11,.2f} | {mid_res['sharpe']:>12.2f} |")
print(f"| Passive (Maker)| {pass_res['trades']:<6} | {pass_res['win_rate']:>7.2f}% | {pass_res['profit_factor']:>13.2f} | ${pass_res['total_pnl']:>11,.2f} | {pass_res['sharpe']:>12.2f} |")
print(f"| Taker (Cross)  | {take_res['trades']:<6} | {take_res['win_rate']:>7.2f}% | {take_res['profit_factor']:>13.2f} | ${take_res['total_pnl']:>11,.2f} | {take_res['sharpe']:>12.2f} |")
print("=" * 70)

report_data = {
    "total_test_ticks": len(test_probs),
    "midpoint": mid_res,
    "passive_maker": pass_res,
    "taker_aggressive": take_res
}

out_json = Path("/content/t4_backtest_results.json") if Path("/content").exists() else Path("output/t4_backtest_results.json")
out_json.parent.mkdir(parents=True, exist_ok=True)
with open(out_json, "w") as f:
    json.dump(report_data, f, indent=2)

# Also copy to output/ if output/ directory exists
if Path("output").exists():
    with open("output/t4_backtest_results.json", "w") as f:
        json.dump(report_data, f, indent=2)

print(f"[✓] Backtest results serialized to {out_json}")
