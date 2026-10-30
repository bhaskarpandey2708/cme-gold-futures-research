#!/usr/bin/env python3
"""
Institutional Client Trial & API Key Auto-Provisioning Engine
=============================================================
Automates client onboarding, API key issuance, rate limit governance,
and client-ready quickstart package generation for institutional allocators.

Usage:
  python3 scripts/provision_client_trial.py --client "Apex Capital" --email "allocator@apex.com" --tier tier_1_pro_quant
"""

import os
import sys
import time
import json
import uuid
import secrets
import sqlite3
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "client_licensing.db"
OUTPUT_DIR = BASE_DIR / "output" / "client_packages"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def init_licensing_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS institutional_licenses (
            license_id TEXT PRIMARY KEY,
            client_name TEXT NOT NULL,
            contact_email TEXT NOT NULL,
            tier_id TEXT NOT NULL,
            api_key TEXT UNIQUE NOT NULL,
            rate_limit_rps INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            status TEXT NOT NULL,
            features_json TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def provision_client(client_name: str, contact_email: str, tier_id: str, duration_days: int = 30) -> dict:
    init_licensing_db()
    
    # Load catalog
    catalog_path = BASE_DIR / "client_packages" / "COMMERCIAL_PRICING_CATALOG.json"
    tiers = {}
    if catalog_path.exists():
        with open(catalog_path, "r") as f:
            data = json.load(f)
            tiers = {t["tier_id"]: t for t in data.get("tiers", [])}

    tier_info = tiers.get(tier_id, {
        "display_name": tier_id.replace("_", " ").title(),
        "rate_limit_req_sec": 25,
        "features": ["Standard Market Feeds", "REST API Access"]
    })

    license_id = f"LIC_{uuid.uuid4().hex[:8].upper()}"
    raw_secret = secrets.token_urlsafe(32)
    api_key = f"apx_{tier_id[:4]}_{raw_secret}"

    now = datetime.now(timezone.utc)
    expires = now + timedelta(days=duration_days)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO institutional_licenses 
        (license_id, client_name, contact_email, tier_id, api_key, rate_limit_rps, created_at, expires_at, status, features_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?)
    """, (
        license_id, client_name, contact_email, tier_id, api_key,
        tier_info.get("rate_limit_req_sec", 25),
        now.isoformat(), expires.isoformat(),
        json.dumps(tier_info.get("features", []))
    ))
    conn.commit()
    conn.close()

    # Generate Onboarding Dossier
    client_slug = client_name.lower().replace(" ", "_").replace(".", "")
    client_dir = OUTPUT_DIR / client_slug
    client_dir.mkdir(parents=True, exist_ok=True)

    dossier_md = f"""# 🏛️ Institutional Quantitative Suite: Client Onboarding Dossier
## Welcome, {client_name}!

- **License ID:** `{license_id}`
- **Subscription Tier:** `{tier_info.get('display_name')}`
- **Contact:** `{contact_email}`
- **Active API Key:** `{api_key}`
- **Rate Limit Ceiling:** `{tier_info.get('rate_limit_req_sec', 25)} requests / second`
- **Validity Period:** `{now.strftime('%Y-%m-%d')} to {expires.strftime('%Y-%m-%d')}` (`{duration_days}` Days Trial)

---

### 🚀 Quickstart Python Client SDK

```python
import urllib.request
import json

API_KEY = "{api_key}"
BASE_URL = "http://127.0.0.1:8090"  # or cloud gateway endpoint

req = urllib.request.Request(f"{{BASE_URL}}/api/v1/cockpit/snapshot")
req.add_header("X-API-KEY", API_KEY)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    print("Live CME Gold Equity:", data["cme_gold"]["pnl"]["total_equity"])
    print("Live NIFTY Micro-Price:", data["india_hft"]["depth"]["last_price"])
    print("PatchTST AI Signal:", data["india_hft"]["patchtst"]["multi_horizon_alpha"]["horizon_1_scalp_5s"]["action"])
```

### 📋 Entitled Platform Capabilities:
"""
    for f_item in tier_info.get("features", []):
        dossier_md += f"- [x] {f_item}\n"

    dossier_path = client_dir / "ONBOARDING_DOSSIER.md"
    with open(dossier_path, "w") as f:
        f.write(dossier_md)

    payload = {
        "license_id": license_id,
        "client_name": client_name,
        "contact_email": contact_email,
        "tier": tier_info.get("display_name"),
        "api_key": api_key,
        "rate_limit_rps": tier_info.get("rate_limit_req_sec", 25),
        "created_at": now.isoformat(),
        "expires_at": expires.isoformat(),
        "onboarding_dossier": str(dossier_path)
    }

    with open(client_dir / "license_credentials.json", "w") as f:
        json.dump(payload, f, indent=2)

    return payload


def main():
    parser = argparse.ArgumentParser(description="Provision Institutional Trial License")
    parser.add_argument("--client", type=str, required=True, help="Institutional client name")
    parser.add_argument("--email", type=str, required=True, help="Client contact email")
    parser.add_argument("--tier", type=str, default="tier_1_pro_quant", choices=[
        "tier_1_pro_quant", "tier_2_wealth_advisor_ria", "tier_3_wealthtech_broker_api", "tier_4_family_office_institutional"
    ], help="Target subscription tier")
    parser.add_argument("--duration", type=int, default=30, help="Trial duration in days (default: 30)")

    args = parser.parse_args()
    res = provision_client(args.client, args.email, args.tier, args.duration)
    print("=" * 78)
    print("✅ INSTITUTIONAL CLIENT LICENSE SUCCESSFULLY PROVISIONED!")
    print("=" * 78)
    print(json.dumps(res, indent=2))
    print("=" * 78)


if __name__ == "__main__":
    main()
