#!/usr/bin/env python3
"""
CME Gold Platform - 600-Minute Autonomous Watchdog & Telemetry Daemon
=====================================================================
Enforces the 600-Minute Overnight Execution Rule and 600-Second Sync Heartbeat:
  • Runs for a target duration of 600 minutes (10 hours)
  • Wakes up every 600 seconds (10 minutes)
  • Inspects health of all 5 parallel production daemons
  • Auto-restarts any dropped daemon immediately
  • Queries and logs live blotter PnL, equity, and market state
  • Maintains audit trail in logs/watchdog_600m.log and event_log.jsonl
"""

import os
import sys
import time
import json
import argparse
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PYTHON = BASE_DIR / ".venv" / "bin" / "python3"
LOGS_DIR = BASE_DIR / "logs"
WATCHDOG_LOG = LOGS_DIR / "watchdog_600m.log"
EVENT_LOG = LOGS_DIR / "event_log.jsonl"

DAEMONS = [
    ("Continuous Harvester", "harvest_continuous_gold.py", ["--interval", "5.0", "--flush-minutes", "10"], "harvester_daemon.log"),
    ("Google Drive Sync", "chat_convo_sync.py", ["--daemon", "--interval", "600"], "sync_daemon.log"),
    ("Enterprise Decision", "run_enterprise_decision_daemon.py", ["--interval", "15", "--daemon"], "decision_daemon.log"),
    ("Async REST API", "quant_api_server.py", ["--port", "8085"], "api_gateway.log"),
    ("CME FIX Gateway", "fix_protocol_gateway.py", ["--port", "9800", "--daemon"], "fix_gateway.log"),
]


def log_message(msg: str):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{now}] {msg}"
    print(line)
    with open(WATCHDOG_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def is_pattern_running(pattern: str) -> bool:
    try:
        res = subprocess.run(["pgrep", "-f", pattern], stdout=subprocess.PIPE, text=True)
        pids = [p.strip() for p in res.stdout.strip().split("\n") if p.strip()]
        return len(pids) > 0
    except Exception:
        return False


def revive_daemon(name: str, script: str, args: list, log_file: str):
    log_p = LOGS_DIR / log_file
    log_f = open(log_p, "a", encoding="utf-8")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BASE_DIR / "scripts")
    cmd = [str(PYTHON), "-u", str(BASE_DIR / "scripts" / script)] + args
    proc = subprocess.Popen(cmd, stdout=log_f, stderr=subprocess.STDOUT, cwd=str(BASE_DIR), env=env, start_new_session=True)
    log_message(f"⚠️ [REVIVED] {name} (Script: {script}) restarted with PID {proc.pid}")


def get_pnl_summary() -> dict:
    try:
        req = urllib.request.urlopen("http://localhost:8085/api/v1/pnl", timeout=3)
        return json.loads(req.read().decode())
    except Exception:
        return {}


def run_watchdog(total_duration_mins: int = 600, cycle_interval_sec: int = 600):
    start_time = time.time()
    end_time = start_time + (total_duration_mins * 60)
    cycle = 0

    log_message("=" * 75)
    log_message(" 🛡️ CME GOLD 600-MINUTE AUTONOMOUS SUPERVISOR WATCHDOG ACTIVE")
    log_message(f"    Total Target Duration: {total_duration_mins} mins ({total_duration_mins/60:.1f} hours)")
    log_message(f"    Audit Cycle Interval:  {cycle_interval_sec} seconds (10 mins)")
    log_message(f"    Managed Daemons:       {len(DAEMONS)} parallel services")
    log_message("=" * 75)

    while time.time() < end_time:
        cycle += 1
        elapsed_mins = (time.time() - start_time) / 60.0
        remaining_mins = max(0.0, total_duration_mins - elapsed_mins)

        log_message(f"\n--- [Cycle #{cycle}] Elapsed: {elapsed_mins:.1f}m | Remaining: {remaining_mins:.1f}m ---")

        # 1. Inspect and revive daemons
        statuses = {}
        for name, script, args, log_file in DAEMONS:
            active = is_pattern_running(script)
            statuses[name] = active
            if not active:
                revive_daemon(name, script, args, log_file)
            else:
                log_message(f"  • {name:<25}: 🟢 ACTIVE")

        # 2. Query blotter
        pnl_data = get_pnl_summary()
        equity = pnl_data.get("total_equity", "N/A")
        realized = pnl_data.get("realized_pnl", "N/A")
        trades = pnl_data.get("total_trades", "N/A")
        win_rate = pnl_data.get("win_rate_pct", "N/A")

        log_message(f"  • Blotter Status: Equity=${equity} | Realized PnL=${realized} | Trades={trades} (Win Rate: {win_rate}%)")

        # Sleep for next cycle or remaining time
        sleep_time = min(cycle_interval_sec, max(1, int(end_time - time.time())))
        if sleep_time > 0:
            time.sleep(sleep_time)

    log_message("=" * 75)
    log_message(f" ✅ 600-MINUTE WATCHDOG RUN COMPLETED SUCCESSFULLY AFTER {cycle} CYCLES.")
    log_message("=" * 75)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="600-Minute Autonomous Watchdog Daemon")
    parser.add_argument("--duration-mins", type=int, default=600, help="Total watchdog duration in minutes (default: 600)")
    parser.add_argument("--interval-sec", type=int, default=600, help="Heartbeat interval in seconds (default: 600)")
    parser.add_argument("--daemon", action="store_true", help="Run detached as background daemon")
    args = parser.parse_args()

    run_watchdog(args.duration_mins, args.interval_sec)
