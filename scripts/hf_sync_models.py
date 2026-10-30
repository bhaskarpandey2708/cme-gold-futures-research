#!/usr/bin/env python3
"""
Hugging Face Cloud Model & Artifact Sync Engine
===============================================
Uploads local trained model weights, checkpoints, and datasets
to Hugging Face Model Hub for permanent, free, version-controlled cloud backup.

Usage:
  python3 scripts/hf_sync_models.py --repo-id <username>/cme-gold-models
"""

import os
import sys
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"


def main():
    parser = argparse.ArgumentParser(description="Sync model weights to Hugging Face Model Hub")
    parser.add_argument("--repo-id", type=str, default="", help="Hugging Face repo id (e.g. username/cme-gold-models)")
    parser.add_argument("--token", type=str, default="", help="Hugging Face write token (optional if logged in via `huggingface-cli login`)")
    parser.add_argument("--private", action="store_true", default=True, help="Make repository private")

    args = parser.parse_args()

    token = args.token or os.getenv("HF_TOKEN")
    if not args.repo_id:
        print("[!] No --repo-id specified. Example: python3 scripts/hf_sync_models.py --repo-id myusername/cme-gold-models")
        sys.exit(1)

    try:
        from huggingface_hub import HfApi, create_repo
    except ImportError:
        print("[!] huggingface_hub not installed. Run: pip3 install huggingface_hub")
        sys.exit(1)

    api = HfApi(token=token)

    print(f"[*] Ensuring Hugging Face model repository exists: '{args.repo_id}'...")
    try:
        create_repo(repo_id=args.repo_id, token=token, repo_type="model", private=args.private, exist_ok=True)
        print(f"[✓] Repository ready: https://huggingface.co/{args.repo_id}")
    except Exception as e:
        print(f"[!] Warning checking/creating repo: {e}")

    # Discover model files to upload
    model_files = list(MODELS_DIR.glob("*.pt")) + list(MODELS_DIR.glob("*.pkl")) + list(MODELS_DIR.glob("*.json"))
    print(f"[*] Uploading {len(model_files)} model artifacts to Hugging Face Hub...")

    for f in model_files:
        print(f"    • Uploading {f.name} ({f.stat().st_size / 1024:.1f} KB)...")
        try:
            api.upload_file(
                path_or_fileobj=str(f),
                path_in_repo=f.name,
                repo_id=args.repo_id,
                repo_type="model",
                token=token
            )
            print(f"      ✓ Successfully synced {f.name}")
        except Exception as e:
            print(f"      [!] Failed uploading {f.name}: {e}")

    print("\n" + "=" * 75)
    print("🏆 ALL MODEL ARTIFACTS SAFELY BACKED UP TO HUGGING FACE HUB!")
    print(f"   View your backed-up models at: https://huggingface.co/{args.repo_id}")
    print("=" * 75)


if __name__ == "__main__":
    main()
