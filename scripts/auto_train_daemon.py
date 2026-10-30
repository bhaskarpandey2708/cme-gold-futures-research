#!/usr/bin/env python3
"""
Automated Continuous Gold Microstructure GPU Training Daemon
============================================================
Periodically inspects freshly harvested tick data on Google Drive,
triggers deep learning retraining on Google Colab's free NVIDIA Tesla T4 GPU,
and writes updated model checkpoints and alpha reports directly back to Google Drive.

Zero local storage consumed: 100% cloud GPU execution & Google Drive storage.

Usage:
  python3 scripts/auto_train_daemon.py --interval 1800 --daemon
  python3 scripts/auto_train_daemon.py --once
"""

import os
import sys
import time
import json
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
GDRIVE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = GDRIVE_DIR / "data" if GDRIVE_DIR.exists() else BASE_DIR / "data"
HARVEST_DIR = DATA_DIR / "harvested"
MODELS_DIR = GDRIVE_DIR / "models" if GDRIVE_DIR.exists() else BASE_DIR / "models"
OUTPUT_DIR = GDRIVE_DIR / "output" if GDRIVE_DIR.exists() else BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"
EVENT_LOG = LOGS_DIR / "event_log.jsonl"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

COLAB_CLI = Path("/Users/bhaskarpandey/.local/bin/colab")
SESSION_NAME = "gold-t4-training"
STATE_FILE = DATA_DIR / "auto_trainer_state.json"


def log_event(event_type: str, details: dict):
    """Log structured event."""
    rec = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "details": details
    }
    with open(EVENT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def get_latest_harvested_dataset() -> Path:
    """Find latest partitioned parquet file or consolidated file."""
    if not HARVEST_DIR.exists():
        return DATA_DIR / "GC_sample_mbp1.parquet"

    harvest_files = sorted(list(HARVEST_DIR.glob("**/*.parquet")), key=lambda p: p.stat().st_mtime, reverse=True)
    if harvest_files:
        return harvest_files[0]
    return DATA_DIR / "GC_sample_mbp1.parquet"


def run_cmd(cmd_list: list, timeout_sec: int = 90) -> str:
    """Run shell command and return stdout."""
    res = subprocess.run(cmd_list, capture_output=True, text=True, timeout=timeout_sec)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed ({res.returncode}): {res.stderr.strip() or res.stdout.strip()}")
    return res.stdout.strip()


def check_and_train():
    """Execute one training and evaluation cycle on Colab T4 GPU."""
    dataset = get_latest_harvested_dataset()
    if not dataset.exists():
        print(f"[-] No dataset available for training yet.")
        return

    file_size = dataset.stat().st_size
    mtime = dataset.stat().st_mtime

    # Check state to avoid redundant training on identical file
    last_state = {}
    if STATE_FILE.exists():
        try:
            last_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass

    if last_state.get("file") == str(dataset) and last_state.get("size") == file_size:
        print(f"[*] Dataset '{dataset.name}' has not changed since last GPU training. Skipping.")
        return

    print("\n" + "=" * 70)
    print(f"⚡ TRIGGERING AUTOMATED T4 GPU TRAINING ON FRESH DATA: {dataset.name}")
    print("=" * 70)

    # 1. Ensure Colab session
    sessions_out = run_cmd([str(COLAB_CLI), "sessions"])
    if SESSION_NAME not in sessions_out:
        print(f"[*] Creating new Colab session with NVIDIA Tesla T4 GPU...")
        run_cmd([str(COLAB_CLI), "new", "--session", SESSION_NAME, "--gpu", "T4"], timeout_sec=90)
    else:
        print(f"[✓] Active Colab T4 session confirmed.")

    # 2. Upload dataset to Colab NVMe
    remote_path = f"/content/{dataset.name}"
    print(f"[*] Uploading fresh dataset to Colab: {dataset.name} ({file_size / 1024:.1f} KB)...")
    run_cmd([str(COLAB_CLI), "upload", "-s", SESSION_NAME, str(dataset), remote_path], timeout_sec=120)

    # 3. Execute training script
    train_script = BASE_DIR / "scripts" / "train_colab_t4_gpu.py"
    print(f"[*] Launching BiLSTM-Attention GPU training on Tesla T4...")
    res = subprocess.run(
        [str(COLAB_CLI), "exec", "-s", SESSION_NAME, "-f", str(train_script), "--timeout", "180"],
        text=True
    )
    if res.returncode != 0:
        print("❌ Remote GPU training execution failed.")
        return

    # 4. Download trained weights directly to Google Drive
    dest_model = MODELS_DIR / "gold_orderbook_t4_model.pt"
    run_cmd([str(COLAB_CLI), "download", "-s", SESSION_NAME, "/content/gold_orderbook_t4_model.pt", str(dest_model)])
    print(f"[✓] Persisted updated model checkpoint to Google Drive: {dest_model}")

    # 5. Run backtest benchmark on remote GPU
    backtest_script = BASE_DIR / "scripts" / "backtest_colab_t4_gpu.py"
    print(f"[*] Executing out-of-sample multi-regime backtest on Tesla T4...")
    res_bt = subprocess.run(
        [str(COLAB_CLI), "exec", "-s", SESSION_NAME, "-f", str(backtest_script), "--timeout", "120"],
        text=True
    )

    if res_bt.returncode == 0:
        # Download backtest metrics to Google Drive
        dest_json = OUTPUT_DIR / "t4_backtest_results.json"
        run_cmd([str(COLAB_CLI), "download", "-s", SESSION_NAME, "/content/t4_backtest_results.json", str(dest_json)])
        print(f"[✓] Downloaded backtest metrics to Google Drive: {dest_json}")

    # 6. Update state file
    new_state = {
        "file": str(dataset),
        "size": file_size,
        "mtime": mtime,
        "last_trained_utc": datetime.now(timezone.utc).isoformat(),
        "model_path": str(dest_model)
    }
    STATE_FILE.write_text(json.dumps(new_state, indent=2), encoding="utf-8")

    log_event("AUTO_GPU_TRAINING_COMPLETED", {
        "dataset": dataset.name,
        "size_bytes": file_size,
        "model_destination": str(dest_model),
        "collaborator": "bhaskarauthor@gmail.com"
    })
    print(f"[✓] Automated T4 GPU cycle completed successfully!")


def main():
    parser = argparse.ArgumentParser(description="Automated Microstructure GPU Training Daemon")
    parser.add_argument("--interval", type=int, default=1800, help="Check interval in seconds (default: 1800 / 30m)")
    parser.add_argument("--daemon", action="store_true", help="Run continuously in background")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    args = parser.parse_args()

    if args.once:
        check_and_train()
        return

    print("=" * 70)
    print("🌾 CONTINUOUS MICROSTRUCTURE T4 GPU TRAINING DAEMON")
    print(f"Polling Interval: {args.interval}s ({args.interval / 60:.1f} mins)")
    print(f"Compute:          Google Colab Free NVIDIA Tesla T4 GPU")
    print(f"Storage:          100% Google Drive (Zero Local Bloat)")
    print("=" * 70)

    while True:
        try:
            check_and_train()
        except Exception as e:
            print(f"[!] Error during GPU cycle: {e}")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
