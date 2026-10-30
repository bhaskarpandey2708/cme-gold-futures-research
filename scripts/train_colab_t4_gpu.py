"""
CME Gold Deep Order Book BiLSTM-Attention Neural Network
========================================================
GPU-Accelerated High-Frequency Microstructure Alpha Engine
Trained on Google Colab NVIDIA Tesla T4 GPU (16GB VRAM)

Features:
- Sequence modeling (T=20 ticks historical depth context)
- Bidirectional LSTM with Multi-Head Self-Attention
- Mixed Precision (FP16) on NVIDIA Tensor Cores
- Predicts forward mid-price direction (5-tick horizon)
"""

import os
import sys
import time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# Check GPU Hardware
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("=" * 70)
print("🚀 CME GOLD DEEP ORDER BOOK GPU TRAINING (NVIDIA T4)")
print("=" * 70)
print(f"PyTorch Version:  {torch.__version__}")
print(f"Compute Device:   {device}")
if torch.cuda.is_available():
    print(f"GPU Model:        {torch.cuda.get_device_name(0)}")
    print(f"Total VRAM:       {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
print("-" * 70)

# 1. Feature Engineering
print("[*] Loading and engineering microstructure features...")
from pathlib import Path
candidate_paths = [
    Path("/content/GC_sample_mbp1.parquet"),
    Path(__file__).resolve().parent.parent / "data" / "GC_sample_mbp1.parquet",
    Path("data/GC_sample_mbp1.parquet"),
    Path("GC_sample_mbp1.parquet")
]
data_path = None
for cp in candidate_paths:
    if cp.exists():
        data_path = str(cp)
        break

if not data_path:
    raise FileNotFoundError("Could not find GC_sample_mbp1.parquet in candidate locations.")

print(f"[✓] Using dataset: {data_path}")
df = pd.read_parquet(data_path)
mid = (df["bid_px_00"] + df["ask_px_00"]) / 2.0
tot_sz = df["bid_sz_00"] + df["ask_sz_00"]

obi = np.where(tot_sz > 0, (df["bid_sz_00"] - df["ask_sz_00"]) / tot_sz, 0.0)
micro = np.where(tot_sz > 0, (df["bid_sz_00"] * df["ask_px_00"] + df["ask_sz_00"] * df["bid_px_00"]) / tot_sz, mid)
micro_spread = micro - mid
spread_bps = ((df["ask_px_00"] - df["bid_px_00"]) / mid) * 10000.0
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

# Target: 5-tick forward direction
horizon = 5
fwd_ret = ((mid.shift(-horizon) - mid) / mid).values
labels = np.where(fwd_ret > 0, 1.0, 0.0)

# Build Sliding Sequence Windows (T=20 ticks context)
T_SEQ = 20
X_seq = []
y_seq = []

for i in range(T_SEQ, len(norm_features) - horizon):
    X_seq.append(norm_features[i - T_SEQ:i])
    y_seq.append(labels[i])

X_arr = np.array(X_seq, dtype=np.float32)
y_arr = np.array(y_seq, dtype=np.float32)

print(f"[✓] Created {len(X_arr):,} temporal sequences (Window: {T_SEQ} ticks, Features: {X_arr.shape[2]})")

# Train/Test Split (80/20 chronological - NO shuffling to prevent lookahead)
split_idx = int(len(X_arr) * 0.8)
X_train, y_train = X_arr[:split_idx], y_arr[:split_idx]
X_test, y_test = X_arr[split_idx:], y_arr[split_idx:]

class OrderBookDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X)
        self.y = torch.tensor(y).unsqueeze(1)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

train_loader = DataLoader(OrderBookDataset(X_train, y_train), batch_size=64, shuffle=False)
test_loader = DataLoader(OrderBookDataset(X_test, y_test), batch_size=64, shuffle=False)

# 2. Deep BiLSTM-Attention Neural Network Architecture
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
        pooled = attn_out[:, -1, :]  # Take last attention-weighted temporal state
        out = self.fc(pooled)
        return out

model = DeepOrderBookNet(input_dim=X_arr.shape[2], hidden_dim=64, num_layers=2).to(device)
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=15)

print(f"\n🧠 Model Parameters: {sum(p.numel() for p in model.parameters()):,}")
print("[*] Launching GPU training on Tesla T4...")

# 3. Training Loop with Mixed Precision
epochs = 12
scaler = torch.amp.GradScaler('cuda') if torch.cuda.is_available() else None

start_time = time.time()
best_acc = 0.0

for epoch in range(1, epochs + 1):
    model.train()
    total_loss = 0.0

    for batch_X, batch_y in train_loader:
        batch_X, batch_y = batch_X.to(device), batch_y.to(device)
        optimizer.zero_grad()

        if torch.cuda.is_available():
            with torch.amp.autocast('cuda'):
                preds = model(batch_X)
                loss = criterion(preds, batch_y)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            preds = model(batch_X)
            loss = criterion(preds, batch_y)
            loss.backward()
            optimizer.step()

        total_loss += loss.item()

    scheduler.step()

    # Evaluation on Out-of-Sample Test Set
    model.eval()
    test_correct = 0
    test_total = 0

    with torch.no_grad():
        for batch_X, batch_y in test_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            preds = model(batch_X)
            predicted_labels = (torch.sigmoid(preds) > 0.5).float()
            test_correct += (predicted_labels == batch_y).sum().item()
            test_total += batch_y.size(0)

    test_acc = (test_correct / test_total) * 100.0 if test_total > 0 else 0.0
    if test_acc > best_acc:
        best_acc = test_acc
        out_models = Path(__file__).resolve().parent.parent / "models"
        out_models.mkdir(parents=True, exist_ok=True)
        torch.save(model.state_dict(), str(out_models / "gold_orderbook_t4_model.pt"))
        if Path("/content").exists():
            torch.save(model.state_dict(), "/content/gold_orderbook_t4_model.pt")

    avg_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch:02d}/{epochs:02d} | Train Loss: {avg_loss:.4f} | Out-of-Sample Accuracy: {test_acc:.2f}% | Best: {best_acc:.2f}%")

duration = time.time() - start_time
print("\n" + "=" * 70)
print("🏁 GPU TRAINING COMPLETED")
print("=" * 70)
print(f"Total Training Time:    {duration:.2f} seconds")
print(f"Peak Out-of-Sample Acc: {best_acc:.2f}%")
print(f"Saved Checkpoint:       models/gold_orderbook_t4_model.pt (and /content/ if Colab)")
print("=" * 70)
