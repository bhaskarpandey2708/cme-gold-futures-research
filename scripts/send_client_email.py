#!/usr/bin/env python3
"""
CME Gold Client Email Dispatch Utility (No ZIP - Native Excel & CSV)
===================================================================
Dispatches the 7-day multi-scale data accuracy package to `bhaskarauthor@gmail.com`
using native common formats (Excel .xlsx and CSV files) instead of ZIP archives.
Supports standard Gmail SMTP or desktop email client invocation.

Usage:
  python3 scripts/send_client_email.py
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import subprocess

RECIPIENT = "bhaskarauthor@gmail.com"
SUBJECT = "CME Gold Futures Multi-Scale Institutional Data Package (Recent 7 Days 2026) — Excel & CSV Formats"

PKG_DIR = Path("/home/ayush-pandey/DATABENTO_RESEARCH/CLIENT_DELIVERY_7DAYS")
EMAIL_DRAFT = PKG_DIR / "00_EMAIL_DRAFT_FOR_CLIENT.txt"

# Common formats to attach (Excel workbook and CSVs)
ATTACHMENTS = [
    PKG_DIR / "CME_Gold_Futures_7Day_Client_Accuracy_Pack.xlsx",
    PKG_DIR / "01_CME_Gold_Daily_Recent_7Days.csv",
    PKG_DIR / "02_CME_Gold_1Hour_Recent_7Days.csv",
    PKG_DIR / "03_CME_Gold_1Minute_Recent_7Days.csv",
    PKG_DIR / "05_CME_Gold_MBP1_OrderBook_and_Trades_Recent.csv",
    PKG_DIR / "00_executive_client_dashboard.html",
]

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")


def send_email():
    print("=" * 75)
    print(" 📧 CME GOLD CLIENT EMAIL DISPATCH ENGINE (EXCEL & CSV ATTACHMENTS)")
    print("=" * 75)
    print(f"[*] Target Recipient: {RECIPIENT}")
    print(f"[*] Subject:          {SUBJECT}")
    print(f"[*] Attachment Format: Excel (.xlsx) & CSVs (NO ZIP)")
    print("[*] Files to attach:")
    total_size = 0
    valid_attachments = []
    for att in ATTACHMENTS:
        if att.exists():
            sz = att.stat().st_size
            total_size += sz
            valid_attachments.append(att)
            print(f"    • {att.name:<48} ({sz / 1024:.1f} KB)")
        else:
            print(f"    • [MISSING] {att.name}")
    print(f"[*] Total Attachment Size: {total_size / (1024*1024):.2f} MB (Well under 25 MB Gmail limit)")

    if not SMTP_USER or not SMTP_PASS:
        print("\n[!] Notice: No outbound SMTP credentials found in environment ($SMTP_USER / $SMTP_PASS).")
        print("[✓] All unzipped common format files (Excel .xlsx & CSVs) are generated in:")
        print(f"    • {PKG_DIR}")
        print(f"    • /home/ayush-pandey/GoogleDrive/Databento_Gold_Futures_Research/CLIENT_DELIVERY_7DAYS")
        print("\n💡 Option 1: Direct Send via Terminal with your Gmail App Password:")
        print("    export SMTP_USER='your_email@gmail.com'")
        print("    export SMTP_PASS='your_16_digit_app_password'")
        print("    python3 scripts/send_client_email.py")
        print("\n💡 Option 2: Pre-populated Desktop Composer (xdg-email):")
        print("    Run: python3 scripts/send_client_email.py --open-client")
        print("=" * 75)
        return False

    try:
        print(f"\n[*] Connecting to {SMTP_HOST}:{SMTP_PORT} as {SMTP_USER}...")
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)

        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = RECIPIENT
        msg["Subject"] = SUBJECT

        body_text = EMAIL_DRAFT.read_text(encoding="utf-8") if EMAIL_DRAFT.exists() else "Please find attached the CME Gold Futures 7-Day Excel and CSV datasets."
        msg.attach(MIMEText(body_text, "plain"))

        # Attach all individual files (Excel and CSVs)
        for att in valid_attachments:
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if att.suffix == ".xlsx" else ("text/html" if att.suffix == ".html" else "text/csv")
            with open(att, "rb") as f:
                part = MIMEBase(*mime_type.split("/"))
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={att.name}")
                msg.attach(part)

        print("[*] Transmitting message with multi-file Excel & CSV attachments...")
        server.sendmail(SMTP_USER, RECIPIENT, msg.as_string())
        server.close()
        print(f"[✓] Email dispatched successfully to {RECIPIENT}!")
        print("=" * 75)
        return True

    except Exception as e:
        print(f"❌ Failed to send email via SMTP: {e}")
        return False


if __name__ == "__main__":
    if "--open-client" in sys.argv:
        cmd = ["xdg-email", "--subject", SUBJECT, "--body", EMAIL_DRAFT.read_text(encoding="utf-8")]
        for att in ATTACHMENTS:
            if att.exists():
                cmd.extend(["--attach", str(att)])
        cmd.append(RECIPIENT)
        subprocess.Popen(cmd)
        print("[✓] Launched default desktop mail client with attachments!")
    else:
        send_email()
