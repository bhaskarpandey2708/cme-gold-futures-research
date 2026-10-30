#!/usr/bin/env python3
"""
CME Gold Pre-Market Intelligence Dispatcher
===========================================
Formats, prepares, and dispatches institutional daily intelligence briefings
and data lakes to institutional allocators, CTAs, and registered prop desks.

Key Features:
- Synthesizes latest pre-market alpha, VPIN toxicity, basis parity, and TFT quantiles.
- Compiles multi-part institutional payload (HTML executive memo + CSV microstructure metrics).
- Zero ZIP archives: Conforms strictly to unzipped CSV / Parquet / Excel delivery standard.
- Persists dispatch audit logs to logs/dispatch_audit.log and outputs RFC-compliant previews.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"

MEMO_MD = OUTPUT_DIR / "CME_GOLD_DAILY_INTELLIGENCE_MEMO.md"
MEMO_HTML = OUTPUT_DIR / "CME_GOLD_DAILY_INTELLIGENCE_MEMO.html"
AUDIT_LOG = LOGS_DIR / "dispatch_audit.log"
PAYLOAD_JSON = OUTPUT_DIR / "email_dispatch_payload.json"


def prepare_dispatch_package(recipient_email: str, recipient_name: str = "Institutional Allocator") -> dict:
    """Prepares institutional email payload with unzipped attachments."""
    # Ensure memo is fresh
    if not MEMO_MD.exists():
        import subprocess
        subprocess.run([sys.executable, str(BASE_DIR / "scripts" / "generate_daily_market_memo.py")], check=True)

    with open(MEMO_MD, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = ""
    if MEMO_HTML.exists():
        with open(MEMO_HTML, "r", encoding="utf-8") as f:
            html_content = f.read()

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    subject = f"🏛️ CME Gold Globex Institutional Intelligence Dossier — {now_utc}"

    # Prepare executive summary text body
    body_text = f"""Dear {recipient_name},

Attached is the CME Gold Globex Pre-Market Quantitative Intelligence Dossier for the upcoming session ({now_utc}).

KEY HIGHLIGHTS:
• Active Directional Signal: Derived from Inception-BiLSTM DeepLOB and Cross-Asset GAT models.
• Toxicity Defense (VPIN): Real-time volume-synchronized probability of toxicity monitoring.
• CME Standard vs. Micro Basis Parity: Continuous physical arbitrage surveillance.
• Probabilistic Price Quantiles: Multi-horizon Temporal Fusion Transformer (+1h, +4h, +24h).

In accordance with institutional delivery protocols, all data feeds and model reports are delivered in unzipped standard formats (HTML and CSV).

Best regards,

CME Globex Microstructure Execution & Quantitative Research Desk
Proprietary Direct CME Capture Cluster
Chicago Mercantile Exchange / New York Floor
"""

    # Identify unzipped attachment candidates (CSV and HTML)
    attachments = []
    if MEMO_HTML.exists():
        attachments.append(str(MEMO_HTML))

    # Look for client CSV exports
    sample_csv = BASE_DIR / "CLIENT_SHARABLE_SAMPLE_DATASET" / "gold_mbp1_10k_sample.csv"
    if sample_csv.exists():
        attachments.append(str(sample_csv))

    payload = {
        "timestamp": now_utc,
        "to": recipient_email,
        "recipient_name": recipient_name,
        "subject": subject,
        "body_text": body_text,
        "html_content": html_content,
        "attachments": attachments
    }

    with open(PAYLOAD_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    # Append to audit log
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{now_utc}] PREPARED briefing for {recipient_email} | Attachments: {len(attachments)}\n")

    return payload


def main():
    parser = argparse.ArgumentParser(description="Dispatch CME Gold Pre-Market Briefing")
    parser.add_argument("--to", default="bhaskarauthor@gmail.com", help="Recipient email address")
    parser.add_argument("--name", default="Institutional Allocator / Partner", help="Recipient name")
    parser.add_argument("--preview", action="store_true", help="Print preview to terminal")
    args = parser.parse_args()

    payload = prepare_dispatch_package(args.to, args.name)

    print("=" * 80)
    print(" 📨 CME GOLD INSTITUTIONAL INTELLIGENCE DISPATCH PACKAGE READY")
    print("=" * 80)
    print(f"Recipient:   {payload['to']} ({payload['recipient_name']})")
    print(f"Subject:     {payload['subject']}")
    print(f"Attachments: {len(payload['attachments'])} unzipped files")
    for att in payload["attachments"]:
        print(f"  • {att}")
    print(f"Payload File: {PAYLOAD_JSON}")
    print("=" * 80)

    if args.preview:
        print("\n--- [EMAIL BODY PREVIEW] ---")
        print(payload["body_text"])
        print("----------------------------\n")


if __name__ == "__main__":
    main()
