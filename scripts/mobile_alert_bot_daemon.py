#!/usr/bin/env python3
"""
Apex Institutional Mobile Alert Bot Daemon
Zero-dependency multi-channel notification engine (Telegram, Discord, Slack, WhatsApp, REST).
Dispatches instant push notifications to mobile devices when allocators request pilot access,
simulate $50M prime mandates, or trip SEC 15c3-5 risk boundaries.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime

LEAD_LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "lead_alerts.jsonl")

def format_telegram_message(lead):
    name = lead.get("name", "Unknown Allocator")
    org = lead.get("org", "Institutional Fund")
    email = lead.get("email", "N/A")
    capacity = lead.get("capital_capacity", "$50M Prime Mandate")
    notes = lead.get("notes", "Requested institutional pilot access")
    source = lead.get("source", "Live Production Web Cockpit")
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    wa_text = urllib.parse.quote(f"Hello {name}, this is the Apex Institutional Allocator Desk regarding your pilot request for {org}.")
    wa_url = f"https://wa.me/919470778244?text={wa_text}"
    
    msg = (
        f"🚨 <b>APEX CME GLOBEX — NEW ALLOCATOR LEAD</b>\n\n"
        f"👤 <b>Name:</b> {name}\n"
        f"🏢 <b>Institution:</b> {org}\n"
        f"📧 <b>Email:</b> <code>{email}</code>\n"
        f"💼 <b>Prime Capacity:</b> <b>{capacity}</b>\n"
        f"📝 <b>Mandate Notes:</b> {notes}\n"
        f"🌐 <b>Source:</b> {source}\n"
        f"⏱ <b>Timestamp:</b> {timestamp}\n\n"
        f"📲 <a href='{wa_url}'><b>1-Tap WhatsApp Desk Reply</b></a> | "
        f"<a href='https://cme-multi-commodity-cockpit.onrender.com'><b>Open Live Cockpit</b></a>"
    )
    return msg

def format_discord_payload(lead):
    name = lead.get("name", "Unknown Allocator")
    org = lead.get("org", "Institutional Fund")
    email = lead.get("email", "N/A")
    capacity = lead.get("capital_capacity", "$50M Prime Mandate")
    notes = lead.get("notes", "Requested institutional pilot access")
    source = lead.get("source", "Live Production Web Cockpit")
    
    return {
        "username": "Apex Institutional Desk Bot",
        "avatar_url": "https://cme-multi-commodity-cockpit.onrender.com/favicon.ico",
        "embeds": [{
            "title": "🚨 New Institutional Allocator Lead Received",
            "description": f"**{name}** from **{org}** has requested institutional pilot access.",
            "color": 165807, # Sky Blue (#0284c7)
            "fields": [
                {"name": "Institution", "value": org, "inline": True},
                {"name": "Capacity Target", "value": capacity, "inline": True},
                {"name": "Email", "value": f"`{email}`", "inline": True},
                {"name": "Mandate Notes", "value": notes, "inline": False},
                {"name": "Source / Channel", "value": source, "inline": True},
                {"name": "Direct Desk Action", "value": "[WhatsApp +91 9470778244](https://wa.me/919470778244)", "inline": True}
            ],
            "footer": {"text": "Apex CME Globex Autonomous Execution Platform"},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }]
    }

def dispatch_to_telegram(token, chat_id, message_html):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message_html,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200, resp.read().decode('utf-8')
    except Exception as e:
        return False, str(e)

def dispatch_to_discord(webhook_url, payload_dict):
    data = json.dumps(payload_dict).encode('utf-8')
    req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': 'ApexBot/1.0'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status in (200, 204), f"Status {resp.status}"
    except Exception as e:
        return False, str(e)

def dispatch_to_generic_webhook(webhook_url, payload_dict):
    data = json.dumps(payload_dict).encode('utf-8')
    req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status in (200, 201, 202, 204), f"Status {resp.status}"
    except Exception as e:
        return False, str(e)

def broadcast_lead(lead):
    results = {}
    
    # 1. Telegram Dispatch
    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    tg_chat = os.environ.get("TELEGRAM_CHAT_ID")
    if tg_token and tg_chat:
        tg_ok, tg_resp = dispatch_to_telegram(tg_token, tg_chat, format_telegram_message(lead))
        results["telegram"] = {"success": tg_ok, "response": tg_resp}
    else:
        results["telegram"] = {"configured": False, "note": "Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID"}
        
    # 2. Discord Dispatch
    discord_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if discord_url:
        dc_ok, dc_resp = dispatch_to_discord(discord_url, format_discord_payload(lead))
        results["discord"] = {"success": dc_ok, "response": dc_resp}
    else:
        results["discord"] = {"configured": False, "note": "Set DISCORD_WEBHOOK_URL"}
        
    # 3. Generic Alert Webhook (Slack / Custom REST)
    alert_url = os.environ.get("ALERT_WEBHOOK_URL")
    if alert_url and alert_url != discord_url:
        gen_ok, gen_resp = dispatch_to_generic_webhook(alert_url, {
            "event": "INSTITUTIONAL_LEAD",
            "lead": lead,
            "dispatched_at": datetime.utcnow().isoformat() + "Z"
        })
        results["webhook"] = {"success": gen_ok, "response": gen_resp}
    else:
        results["webhook"] = {"configured": bool(alert_url)}

    # Always log locally
    print(f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}] Broadcasted lead for {lead.get('name')} ({lead.get('org')}) -> {results}")
    return results

def run_test():
    test_lead = {
        "name": "Sarah Jenkins (Managing Director)",
        "org": "Citadel Securities Macro Fund",
        "email": "sjenkins@citadelsecurities.com",
        "capital_capacity": "$50M Prime SMA",
        "notes": "Exploring CME Globex Gold Microstructure Alpha & FIX 4.4 Gateway",
        "source": "CLI Verification Daemon Test"
    }
    print("Simulating test institutional lead dispatch...")
    res = broadcast_lead(test_lead)
    print("\n--- Test Dispatch Results ---")
    print(json.dumps(res, indent=2))
    print("\nFormatted Telegram HTML Preview:\n" + format_telegram_message(test_lead))

def run_daemon(poll_interval=2.0):
    print(f"Starting Apex Mobile Alert Bot Daemon. Monitoring: {LEAD_LOG_FILE}")
    last_pos = 0
    if os.path.exists(LEAD_LOG_FILE):
        last_pos = os.path.getsize(LEAD_LOG_FILE)
        
    while True:
        try:
            if os.path.exists(LEAD_LOG_FILE):
                curr_size = os.path.getsize(LEAD_LOG_FILE)
                if curr_size > last_pos:
                    with open(LEAD_LOG_FILE, 'r') as f:
                        f.seek(last_pos)
                        new_lines = f.readlines()
                        last_pos = f.tell()
                    for line in new_lines:
                        line = line.strip()
                        if line:
                            try:
                                lead_data = json.loads(line)
                                broadcast_lead(lead_data)
                            except Exception as parse_err:
                                print(f"Error parsing log line: {parse_err}")
                elif curr_size < last_pos:
                    last_pos = curr_size
            time.sleep(poll_interval)
        except KeyboardInterrupt:
            print("\nShutting down Mobile Alert Bot Daemon.")
            break
        except Exception as e:
            print(f"Daemon error: {e}")
            time.sleep(poll_interval)

if __name__ == "__main__":
    if "--test" in sys.argv:
        run_test()
    elif "--daemon" in sys.argv:
        run_daemon()
    else:
        print("Usage:")
        print("  python scripts/mobile_alert_bot_daemon.py --test    # Test dispatch formatting")
        print("  python scripts/mobile_alert_bot_daemon.py --daemon  # Run persistent monitoring daemon")
