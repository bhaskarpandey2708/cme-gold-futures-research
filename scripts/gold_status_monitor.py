#!/usr/bin/env python3
"""
CME Gold Quantitative Microstructure Suite - Unified Status Monitor
====================================================================
Prints an institutional real-time terminal dashboard of all daemons,
order book partition activity, SQLite lakes, paper blotter PnL,
and live alpha execution signals.
"""

import os
import sys
import json
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent.parent
GDRIVE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
BLOTTER_DB = DATA_DIR / "paper_trading_blotter.db"
DECISIONS_LOG = LOGS_DIR / "live_decisions.jsonl"
MARKET_DB = DATA_DIR / "market_store.db"

# ANSI Colors
CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
BOLD = "\033[1m"
RESET = "\033[0m"


def check_daemon_process(pattern: str) -> dict:
    try:
        res = subprocess.run(["pgrep", "-f", pattern], stdout=subprocess.PIPE, text=True)
        pids = [p.strip() for p in res.stdout.strip().split("\n") if p.strip()]
        if not pids:
            return {"status": "STOPPED", "pid": "-", "cpu": "-", "mem": "-", "etime": "-"}
        pid = pids[0]
        ps_res = subprocess.run(["ps", "-p", pid, "-o", "%cpu,rss,etime", "--no-headers"], stdout=subprocess.PIPE, text=True)
        parts = ps_res.stdout.strip().split()
        if len(parts) >= 3:
            cpu, rss_kb, etime = parts[0], float(parts[1]), parts[2]
            return {"status": "ACTIVE", "pid": pid, "cpu": f"{cpu}%", "mem": f"{rss_kb/1024:.1f} MB", "etime": etime}
        return {"status": "ACTIVE", "pid": pid, "cpu": "-", "mem": "-", "etime": "-"}
    except Exception:
        return {"status": "ERROR", "pid": "-", "cpu": "-", "mem": "-", "etime": "-"}


def print_banner():
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"{CYAN}╔══════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║     🥇 CME GOLD FUTURES RESEARCH — UNIFIED QUANTITATIVE COCKPIT             ║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════════════════════════════════════════════╝{RESET}")
    print(f" Timestamp: {BOLD}{now_utc}{RESET} | Market: CME COMEX Globex GC=F\n")


def print_daemons():
    print(f"{BOLD}▶ 1. ACTIVE PRODUCTION DAEMONS{RESET}")
    print("-" * 80)
    print(f"{'DAEMON NAME':<25} {'STATUS':<10} {'PID':<8} {'CPU':<8} {'MEM':<10} {'UPTIME':<12}")
    print("-" * 80)
    daemons = [
        ("Continuous Harvester", "harvest_continuous_gold.py"),
        ("Google Drive Sync", "chat_convo_sync.py"),
        ("Enterprise Decision", "run_enterprise_decision_daemon.py"),
        ("Async REST API (8085)", "quant_api_server.py"),
    ]
    for name, pattern in daemons:
        info = check_daemon_process(pattern)
        st_color = GREEN if info["status"] == "ACTIVE" else RED
        print(f"{name:<25} {st_color}{info['status']:<10}{RESET} {info['pid']:<8} {info['cpu']:<8} {info['mem']:<10} {info['etime']:<12}")
    print("-" * 80 + "\n")


def print_harvest_activity():
    print(f"{BOLD}▶ 2. RECENT HARVEST ACTIVITY (Partitioned Buffers){RESET}")
    print("-" * 80)
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_dir = GDRIVE_DIR / "data" / "harvested" / today_str
    if not today_dir.exists():
        today_dir = DATA_DIR / "harvested" / today_str

    if today_dir.exists():
        files = sorted(list(today_dir.glob("gold_mbp1_*.parquet")), key=lambda p: p.stat().st_mtime, reverse=True)[:5]
        print(f" Partition: {CYAN}{today_dir}{RESET}")
        for f in files:
            sz_kb = f.stat().st_size / 1024
            mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%H:%M:%S")
            print(f"   • {f.name:<38} Size: {sz_kb:6.1f} KB   Time: {mtime}")
    else:
        print(f" {YELLOW}Waiting for today's partition flushes...{RESET}")
    print()


def print_market_db():
    print(f"{BOLD}▶ 3. SQLITE MASTER STORE & 10-YEAR LAKES{RESET}")
    print("-" * 80)
    target_db = GDRIVE_DIR / "data" / "market_store.db"
    if not target_db.exists():
        target_db = MARKET_DB

    if target_db.exists():
        sz_mb = target_db.stat().st_size / (1024 * 1024)
        print(f" Store Path: {CYAN}{target_db}{RESET} ({sz_mb:.1f} MB)")
        try:
            conn = sqlite3.connect(f"file:{target_db}?mode=ro", uri=True)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [r[0] for r in cur.fetchall() if not r[0].startswith("sqlite_")]
            for t in sorted(tables):
                cur.execute(f"SELECT COUNT(*) FROM {t}")
                cnt = cur.fetchone()[0]
                print(f"   • Table [{t}]: {cnt:,} rows")
            conn.close()
        except Exception as e:
            print(f"   Database query notice: {e}")
    else:
        print(f" {RED}Database not found at {target_db}{RESET}")
    print()


def print_blotter():
    print(f"{BOLD}▶ 4. LIVE GLOBEX PAPER TRADING BLOTTER{RESET}")
    print("-" * 80)
    if BLOTTER_DB.exists():
        try:
            conn = sqlite3.connect(BLOTTER_DB)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*), SUM(net_pnl) FROM blotter_positions WHERE status LIKE 'CLOSED%'")
            row = cur.fetchone()
            trades = row[0] or 0
            pnl = row[1] or 0.0

            cur.execute("SELECT COUNT(*) FROM blotter_positions WHERE status LIKE 'CLOSED%' AND net_pnl > 0")
            wins = cur.fetchone()[0] or 0
            wr = (wins / trades * 100) if trades > 0 else 0.0

            cur.execute("SELECT total_equity, cash_balance, open_contracts FROM blotter_equity_snapshots ORDER BY snapshot_time DESC LIMIT 1")
            eq_row = cur.fetchone()
            equity = eq_row[0] if eq_row else 250_000.0
            pos = eq_row[2] if eq_row else 0

            pnl_col = GREEN if pnl >= 0 else RED
            print(f"   • Total Account Equity:   {BOLD}${equity:,.2f}{RESET} (Base: $250,000.00)")
            print(f"   • Cumulative Realized PnL: {pnl_col}{BOLD}${pnl:+,.2f}{RESET} (Net of Globex fees)")
            print(f"   • Executed Trades:        {trades} closed positions (Win Rate: {BOLD}{wr:.1f}%{RESET})")
            print(f"   • Current Globex Position: {pos:+d} GC Contract(s)")
            conn.close()
        except Exception as e:
            print(f"   Blotter notice: {e}")
    else:
        print(f" {YELLOW}Blotter database initializing...{RESET}")
    print()


def print_latest_decision():
    print(f"{BOLD}▶ 5. LATEST LIVE ALPHA DECISION SIGNAL{RESET}")
    print("-" * 80)
    if DECISIONS_LOG.exists():
        try:
            with open(DECISIONS_LOG, "r") as f:
                lines = [l.strip() for l in f if l.strip()]
            if lines:
                d = json.loads(lines[-1])
                act = d.get("decision", "HOLD")
                col = GREEN if act == "BUY" else (RED if act == "SELL" else YELLOW)
                alpha = d.get("alpha_signals", {})
                sl = f"${d['stop_loss']:.2f}" if d.get("stop_loss") else "N/A"
                tp = f"${d['take_profit']:.2f}" if d.get("take_profit") else "N/A"
                print(f"   • Primary Signal:         {col}{BOLD}[{act}]{RESET} @ ${d.get('target_price', 0):.2f}")
                print(f"   • Alpha Conviction:       {alpha.get('alpha_score', 0):+.2f} ({alpha.get('conviction', 'MEDIUM')})")
                print(f"   • Dynamic Risk Targets:   Stop: {sl} | Target: {tp}")
                print(f"   • Evaluated Batch:        {d.get('source_file')} ({d.get('evaluated_at')})")
        except Exception as e:
            print(f"   Decision log notice: {e}")
    print("=" * 80)
    print(f"{BOLD}💡 Quick Commands:{RESET}")
    print(f"  • Status Monitor:   {GREEN}gold-status{RESET} (or: python3 scripts/gold_status_monitor.py)")
    print(f"  • Live Watch:       {GREEN}watch -n 5 gold-status{RESET}")
    print(f"  • Paper Blotter:    {GREEN}python3 scripts/paper_trading_simulator.py{RESET}")
    print(f"  • Risk Tearsheet:   {GREEN}python3 scripts/generate_institutional_risk_tearsheet.py{RESET}")
    print("=" * 80)


if __name__ == "__main__":
    print_banner()
    print_daemons()
    print_harvest_activity()
    print_market_db()
    print_blotter()
    print_latest_decision()
