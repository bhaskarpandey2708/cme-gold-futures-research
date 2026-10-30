#!/usr/bin/env python3
"""
Kaggle Free GPU Headless Cloud Orchestrator
===========================================
Submits model training jobs to Kaggle's free NVIDIA Tesla T4 / P100 GPUs (73 GB RAM, 30 hrs/wk).
Monitors kernel execution status, and downloads trained checkpoints back to local disk.

Usage:
  python3 scripts/kaggle_runner.py --push
  python3 scripts/kaggle_runner.py --status
  python3 scripts/kaggle_runner.py --output
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
KAGGLE_DEPLOY_DIR = BASE_DIR / "deploy" / "kaggle"
MODELS_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "output"


def check_kaggle_creds():
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    has_env = os.getenv("KAGGLE_USERNAME") and os.getenv("KAGGLE_KEY")
    if not kaggle_json.exists() and not has_env:
        print("\n" + "=" * 75)
        print("⚠️  KAGGLE CREDENTIALS NOT FOUND")
        print("=" * 75)
        print("To enable 30 hours/week of free headless GPU compute from your terminal:")
        print("1. Go to https://www.kaggle.com/settings -> Click 'Create New Token'")
        print("2. It will download 'kaggle.json'.")
        print("3. Move it to: ~/.kaggle/kaggle.json")
        print("   mkdir -p ~/.kaggle && mv ~/Downloads/kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json")
        print("=" * 75)
        return False
    return True


def push_kernel():
    if not check_kaggle_creds():
        return
    print(f"[*] Pushing GPU training job from {KAGGLE_DEPLOY_DIR} to Kaggle Cloud...")
    cmd = ["kaggle", "kernels", "push", "-p", str(KAGGLE_DEPLOY_DIR)]
    res = subprocess.run(cmd)
    if res.returncode == 0:
        print("✅ Successfully submitted job to Kaggle GPU cluster!")
        print("   Monitor with: python3 scripts/kaggle_runner.py --status")


def check_status():
    if not check_kaggle_creds():
        return
    meta_file = KAGGLE_DEPLOY_DIR / "kernel-metadata.json"
    if not meta_file.exists():
        print("[!] kernel-metadata.json not found.")
        return
    meta = json.loads(meta_file.read_text())
    kernel_id = meta["id"]
    print(f"[*] Checking execution status for: {kernel_id}...")
    subprocess.run(["kaggle", "kernels", "status", kernel_id])


def pull_output():
    if not check_kaggle_creds():
        return
    meta_file = KAGGLE_DEPLOY_DIR / "kernel-metadata.json"
    meta = json.loads(meta_file.read_text())
    kernel_id = meta["id"]
    print(f"[*] Downloading trained model checkpoints from: {kernel_id} -> models/...")
    cmd = ["kaggle", "kernels", "output", kernel_id, "-p", str(MODELS_DIR)]
    subprocess.run(cmd)
    print("✅ Download completed.")


def main():
    parser = argparse.ArgumentParser(description="Kaggle Free GPU Orchestrator")
    parser.add_argument("--push", action="store_true", help="Submit training job to Kaggle GPU")
    parser.add_argument("--status", action="store_true", help="Check status of running Kaggle kernel")
    parser.add_argument("--output", action="store_true", help="Download trained checkpoints from Kaggle")

    args = parser.parse_args()

    if args.push:
        push_kernel()
    elif args.status:
        check_status()
    elif args.output:
        pull_output()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
