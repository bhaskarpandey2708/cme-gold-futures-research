#!/usr/bin/env python3
"""
CME Gold Platform - Parallel Production Daemons Orchestrator
============================================================
Launches and manages the 5 core institutional quantitative daemons in parallel:
  1. Continuous Harvester       (scripts/harvest_continuous_gold.py)
  2. Google Drive Delta Sync    (scripts/chat_convo_sync.py --daemon --interval 600)
  3. Enterprise Decision Daemon (scripts/run_enterprise_decision_daemon.py --interval 15 --daemon)
  4. Async REST & WebSocket API (scripts/quant_api_server.py --port 8085)
  5. CME FIX 4.4 Gateway        (scripts/fix_protocol_gateway.py --port 9800 --daemon)
"""

import os
import sys
import time
import subprocess
import signal
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PYTHON = sys.executable
LOGS_DIR = BASE_DIR / "logs"
PID_DIR = LOGS_DIR / "pids"

LOGS_DIR.mkdir(parents=True, exist_ok=True)
PID_DIR.mkdir(parents=True, exist_ok=True)

DAEMONS = [
    {
        "name": "Continuous Harvester",
        "script": "harvest_continuous_gold.py",
        "args": ["--interval", "5.0", "--flush-minutes", "10"],
        "log": LOGS_DIR / "harvester_daemon.log",
        "pid_file": PID_DIR / "harvester.pid",
    },
    {
        "name": "Google Drive Sync (600s)",
        "script": "chat_convo_sync.py",
        "args": ["--daemon", "--interval", "600"],
        "log": LOGS_DIR / "sync_daemon.log",
        "pid_file": PID_DIR / "sync.pid",
    },
    {
        "name": "Enterprise Decision Daemon",
        "script": "run_enterprise_decision_daemon.py",
        "args": ["--interval", "15", "--daemon"],
        "log": LOGS_DIR / "decision_daemon.log",
        "pid_file": PID_DIR / "decision.pid",
    },
    {
        "name": "Async REST & WebSocket (8085)",
        "script": "quant_api_server.py",
        "args": ["--port", "8085"],
        "log": LOGS_DIR / "api_gateway.log",
        "pid_file": PID_DIR / "api_server.pid",
    },
    {
        "name": "CME FIX 4.4 Gateway (9800)",
        "script": "fix_protocol_gateway.py",
        "args": ["--port", "9800", "--daemon"],
        "log": LOGS_DIR / "fix_gateway.log",
        "pid_file": PID_DIR / "fix_gateway.pid",
    },
    {
        "name": "600-Min Watchdog Supervisor",
        "script": "watchdog_600m_daemon.py",
        "args": ["--duration-mins", "600", "--interval-sec", "600"],
        "log": LOGS_DIR / "watchdog_600m.log",
        "pid_file": PID_DIR / "watchdog.pid",
    },
    {
        "name": "Unified Quant Cockpit (8090)",
        "script": "unified_quant_cockpit_server.py",
        "args": [],
        "log": LOGS_DIR / "unified_cockpit.log",
        "pid_file": PID_DIR / "unified_cockpit.pid",
    },
    {
        "name": "1-Year Multi-Schema Downloader & GDrive Archiver",
        "script": "pipeline/full_1year_multi_schema_pipeline.py",
        "args": ["--daemon", "--batch", "1", "--interval", "10"],
        "log": LOGS_DIR / "all_schemas_1year_stream.log",
        "pid_file": PID_DIR / "all_schemas_1year.pid",
    },
    {
        "name": "CME Commodities 1-Year Multi-Schema Downloader",
        "script": "pipeline/cme_all_commodities_1year_pipeline.py",
        "args": ["--daemon", "--batch", "1", "--interval", "5"],
        "log": LOGS_DIR / "all_commodities_1year_stream.log",
        "pid_file": PID_DIR / "all_commodities_1year.pid",
    },
]


def is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def stop_daemons():
    print("🛑 Stopping all active platform daemons...")
    stopped_count = 0
    # Stop by pattern match to be thorough
    patterns = [
        "harvest_continuous_gold.py",
        "chat_convo_sync.py",
        "run_enterprise_decision_daemon.py",
        "quant_api_server.py",
        "fix_protocol_gateway.py",
        "watchdog_600m_daemon.py",
        "download_in_parts_to_gdrive.py",
        "full_1year_multi_schema_pipeline.py",
    ]
    for pattern in patterns:
        try:
            res = subprocess.run(["pgrep", "-f", pattern], stdout=subprocess.PIPE, text=True)
            pids = [int(p.strip()) for p in res.stdout.strip().split("\n") if p.strip()]
            for pid in pids:
                if pid != os.getpid():
                    os.kill(pid, signal.SIGTERM)
                    stopped_count += 1
        except Exception:
            pass
    time.sleep(1)
    print(f"✅ Stopped {stopped_count} daemon process(es).")


def start_daemons():
    print("=" * 80)
    print(" 🚀 CME GOLD QUANTITATIVE PLATFORM — LAUNCHING PARALLEL PRODUCTION DAEMONS")
    print("=" * 80)

    # First clean up any orphans
    stop_daemons()

    started = []
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BASE_DIR / "scripts")

    for d in DAEMONS:
        log_f = open(d["log"], "a", encoding="utf-8")
        cmd = [str(PYTHON), "-u", str(BASE_DIR / "scripts" / d["script"])] + d["args"]
        proc = subprocess.Popen(
            cmd,
            stdout=log_f,
            stderr=subprocess.STDOUT,
            cwd=str(BASE_DIR),
            env=env,
            start_new_session=True,
        )
        d["pid_file"].write_text(str(proc.pid))
        started.append((d["name"], proc.pid, d["log"]))
        print(f"  • {d['name']:<32} [PID {proc.pid}] -> {d['log'].name}")

    print("\n⏳ Verifying daemon initialization (waiting 3s)...")
    time.sleep(3)

    # Check status
    print("-" * 80)
    print(f"{'DAEMON NAME':<32} {'PID':<10} {'STATUS':<15} {'HEALTH'}")
    print("-" * 80)
    all_ok = True
    for name, pid, log_p in started:
        active = is_running(pid)
        st = "🟢 RUNNING" if active else "🔴 FAILED"
        if not active:
            all_ok = False
        print(f"{name:<32} {pid:<10} {st:<15} Log: {log_p.name}")
    print("-" * 80)

    if all_ok:
        print("✅ All 5 institutional daemons are successfully running in parallel!")
    else:
        print("⚠️ Some daemons failed to initialize. Check logs in logs/")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stop":
        stop_daemons()
    else:
        start_daemons()
