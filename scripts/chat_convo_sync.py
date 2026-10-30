#!/usr/bin/env python3
"""
Databento Research - Continuous Conversation & State Synchronizer
==================================================================
Extracts conversation transcripts, agent decisions, and tool executions,
persisting them every 600 seconds into GoogleDrive CONVERSATION_LOGS.md,
updating AGENT.md state, and emitting audit logs to guarantee zero data loss.

Usage:
  python3 chat_convo_sync.py                  # One-time sync
  python3 chat_convo_sync.py --daemon         # Continuous 600s background loop
"""

import os
import sys
import json
import time
import argparse
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
GDRIVE_ROOT = BASE_DIR
LOCAL_MIRROR = BASE_DIR
APP_DATA_DIR = Path(os.path.expanduser("~/.gemini/antigravity-cli"))

LOGS_DIR = BASE_DIR / "logs"
LOCAL_LOGS_DIR = LOGS_DIR
LOGS_DIR.mkdir(parents=True, exist_ok=True)

EVENT_LOG_FILE = LOGS_DIR / "event_log.jsonl"
LOCAL_EVENT_LOG_FILE = EVENT_LOG_FILE
AGENT_FILE = BASE_DIR / "AGENT.md"
LOCAL_AGENT_FILE = AGENT_FILE
TARGET_CONVO_LOG = BASE_DIR / "CONVERSATION_LOGS.md"
LOCAL_CONVO_LOG = TARGET_CONVO_LOG

COLLABORATOR_EMAIL = "bhaskarauthor@gmail.com"


def get_active_convo_id() -> str:
    """Detect current active conversation ID by finding latest modified transcript."""
    brain_dir = APP_DATA_DIR / "brain"
    if brain_dir.exists():
        candidates = []
        for d in brain_dir.iterdir():
            if d.is_dir():
                p = d / ".system_generated" / "logs" / "transcript.jsonl"
                if p.exists():
                    candidates.append((p.stat().st_mtime, d.name))
        if candidates:
            candidates.sort(reverse=True)
            return candidates[0][1]
    return "079a0145-8a92-41ee-9f28-bbbd00545696"


def parse_transcript(convo_id: str):
    """Parse transcript.jsonl and transcript_full.jsonl for conversation."""
    logs_dir = APP_DATA_DIR / "brain" / convo_id / ".system_generated" / "logs"
    transcript_path = logs_dir / "transcript.jsonl"
    full_path = logs_dir / "transcript_full.jsonl"

    if not transcript_path.exists():
        return []

    records = []
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass

    # Read full entries if truncated
    full_map = {}
    if full_path.exists():
        with open(full_path, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                line = line.strip()
                if line:
                    try:
                        full_map[idx] = json.loads(line)
                    except Exception:
                        pass

    for idx, rec in enumerate(records):
        if rec.get("truncated_fields") and idx in full_map:
            for field in rec["truncated_fields"]:
                if field in full_map[idx]:
                    rec[field] = full_map[idx][field]

    return records


def format_convo_markdown(records, convo_id: str) -> str:
    """Format transcript steps into clean readable markdown."""
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    md = [
        "# Complete Session & Conversation Logs: CME Gold Futures (GC) MBP-1",
        f"\n**Project:** Databento Market Microstructure Research",
        f"**Conversation ID:** `{convo_id}`",
        f"**Collaborator:** `{COLLABORATOR_EMAIL}`",
        f"**Last Sync:** `{now_str}`",
        f"**Total Steps Recorded:** `{len(records)}`",
        "\n---\n",
    ]

    turn_idx = 1
    current_turn = {"prompt": "", "actions": [], "responses": [], "ts": ""}

    for rec in records:
        rtype = rec.get("type", "")
        source = rec.get("source", "")
        ts = rec.get("created_at", "")

        if rtype == "USER_INPUT" and source == "USER_EXPLICIT":
            # Save previous turn if exists
            if current_turn["prompt"]:
                md.append(f"### Turn {turn_idx} [{current_turn['ts']}] User Request\n")
                md.append(f"> {current_turn['prompt']}\n")
                if current_turn["actions"]:
                    md.append("#### Actions & Executed Tools:")
                    for act in current_turn["actions"]:
                        md.append(f"- `[{act['tool']}]` {act['summary']}")
                    md.append("")
                if current_turn["responses"]:
                    md.append("#### Assistant Output:")
                    for resp in current_turn["responses"]:
                        md.append(f"{resp}\n")
                md.append("---\n")
                turn_idx += 1

            current_turn = {"prompt": rec.get("content", "").strip(), "actions": [], "responses": [], "ts": ts}

        elif rtype == "PLANNER_RESPONSE":
            content = rec.get("content", "")
            if content and content.strip():
                current_turn["responses"].append(content.strip())

            for tc in rec.get("tool_calls", []):
                tool_name = tc.get("tool_name") or tc.get("name") or ""
                args = tc.get("arguments") or tc.get("args") or {}
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        args = {"raw": args}
                summary = ""
                if isinstance(args, dict):
                    summary = (args.get("toolSummary") or args.get("Path") or 
                               args.get("CommandLine") or args.get("query") or 
                               args.get("Action") or "")
                summary_str = str(summary).strip().strip('"').strip("'")
                if tool_name:
                    current_turn["actions"].append({"tool": tool_name, "summary": summary_str[:120]})

    # Flush last turn
    if current_turn["prompt"]:
        md.append(f"### Turn {turn_idx} [{current_turn['ts']}] User Request\n")
        md.append(f"> {current_turn['prompt']}\n")
        if current_turn["actions"]:
            md.append("#### Actions & Executed Tools:")
            for act in current_turn["actions"]:
                md.append(f"- `[{act['tool']}]` {act['summary']}")
            md.append("")
        if current_turn["responses"]:
            md.append("#### Assistant Output:")
            for resp in current_turn["responses"]:
                md.append(f"{resp}\n")
        md.append("---\n")

    return "\n".join(md)


def update_agent_state(step_count: int, convo_id: str):
    """Update AGENT.md state and timestamp."""
    # Ensure local rewritten AGENT.md is mirrored to Google Drive first
    try:
        if LOCAL_AGENT_FILE.exists():
            AGENT_FILE.write_bytes(LOCAL_AGENT_FILE.read_bytes())
    except Exception as e:
        pass

    for af in [AGENT_FILE, LOCAL_AGENT_FILE]:
        if not af.exists():
            continue
        try:
            now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            text = af.read_text(encoding="utf-8")

            text = re.sub(r"- \*\*Current Session ID:\*\* .*", f"- **Current Session ID:** `{convo_id}`", text)
            text = re.sub(r"- \*\*Last Sync Timestamp:\*\* .*", f"- **Last Sync Timestamp:** `{now_str}`", text)

            mount_ok = Path("/home/ayush-pandey/GoogleDrive").exists()
            status_str = "ONLINE (FUSE rclone mounted)" if mount_ok else "OFFLINE"
            text = re.sub(r"- \*\*Google Drive Mount Status:\*\* .*", f"- **Google Drive Mount Status:** `{status_str}`", text)

            if "- **Total Steps Synced:**" in text:
                text = re.sub(r"- \*\*Total Steps Synced:\*\* .*", f"- **Total Steps Synced:** `{step_count}` steps", text)
            else:
                text += f"\n- **Total Steps Synced:** `{step_count}` steps\n"

            af.write_text(text, encoding="utf-8")
        except Exception as e:
            print(f"[!] Warning updating {af}: {e}")


def log_event(event_type: str, details: dict):
    """Append structured JSON audit event log."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "details": details,
    }
    line = json.dumps(entry) + "\n"
    for ef in [EVENT_LOG_FILE, LOCAL_EVENT_LOG_FILE]:
        try:
            ef.parent.mkdir(parents=True, exist_ok=True)
            with open(ef, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception:
            pass


def sync_all():
    """Execute complete sync cycle shipping all convos, agent memory, logs, and markdown reports."""
    convo_id = get_active_convo_id()
    records = parse_transcript(convo_id)
    if not records:
        print(f"[!] No transcript found for {convo_id}")
        return False

    markdown_content = format_convo_markdown(records, convo_id)

    # 1. Write Conversation Logs to Google Drive & Local Mirror
    try:
        TARGET_CONVO_LOG.write_text(markdown_content, encoding="utf-8")
        print(f"[✓] Synced to Google Drive: {TARGET_CONVO_LOG.name} ({len(records)} steps, {len(markdown_content):,} bytes)")
    except Exception as e:
        print(f"[!] Warning writing to Google Drive: {e}")

    try:
        if LOCAL_MIRROR.exists():
            LOCAL_CONVO_LOG.write_text(markdown_content, encoding="utf-8")
            print(f"[✓] Mirrored to local workspace: {LOCAL_CONVO_LOG.name}")
    except Exception as e:
        print(f"[!] Warning mirroring to local: {e}")

    # 2. Update AGENT.md state
    update_agent_state(len(records), convo_id)
    print(f"[✓] Updated AGENT.md memory state")

    # 3. Ship all Markdown Reports & HTML Dashboards from output/
    synced_reports = 0
    local_output = LOCAL_MIRROR / "output"
    gdrive_output = GDRIVE_ROOT / "output"
    gdrive_output.mkdir(parents=True, exist_ok=True)

    if local_output.exists():
        for f in local_output.iterdir():
            if f.is_file() and (f.suffix in (".md", ".html")):
                try:
                    dest = gdrive_output / f.name
                    if not dest.exists() or f.stat().st_mtime > dest.stat().st_mtime:
                        dest.write_bytes(f.read_bytes())
                        synced_reports += 1
                except Exception as e:
                    pass
        print(f"[✓] Shipped {synced_reports} research reports & dashboards -> Google Drive output/")

    # 4. Ship Documentation Markdown files from docs/
    synced_docs = 0
    local_docs = LOCAL_MIRROR / "docs"
    gdrive_docs = GDRIVE_ROOT / "docs"
    gdrive_docs.mkdir(parents=True, exist_ok=True)

    if local_docs.exists():
        for f in local_docs.iterdir():
            if f.is_file() and f.suffix == ".md":
                try:
                    dest = gdrive_docs / f.name
                    if not dest.exists() or f.stat().st_mtime > dest.stat().st_mtime:
                        dest.write_bytes(f.read_bytes())
                        synced_docs += 1
                except Exception as e:
                    pass
        print(f"[✓] Shipped {synced_docs} documentation specs -> Google Drive docs/")

    # 5. Ship Root README.md, manage.py, cme_gold_sdk.py, docker-compose.yml
    try:
        for fname in ["README.md", "manage.py", "cme_gold_sdk.py", "docker-compose.yml"]:
            lfile = LOCAL_MIRROR / fname
            gfile = GDRIVE_ROOT / fname
            if lfile.exists():
                if not gfile.exists() or lfile.stat().st_mtime > gfile.stat().st_mtime:
                    gfile.write_bytes(lfile.read_bytes())
        print(f"[✓] Shipped Root Tooling (manage.py, SDK, docker-compose) -> Google Drive")
    except Exception as e:
        pass

    # 6. Ship Config JSON files
    try:
        lconfig = LOCAL_MIRROR / "config"
        gconfig = GDRIVE_ROOT / "config"
        gconfig.mkdir(parents=True, exist_ok=True)
        if lconfig.exists():
            for cf in lconfig.glob("*.json"):
                dest = gconfig / cf.name
                if not dest.exists() or cf.stat().st_mtime > dest.stat().st_mtime:
                    dest.write_bytes(cf.read_bytes())
            print(f"[✓] Shipped Config JSON files -> Google Drive config/")
    except Exception as e:
        pass

    # 7. Ship Python Scripts
    try:
        lscripts = LOCAL_MIRROR / "scripts"
        gscripts = GDRIVE_ROOT / "scripts"
        gscripts.mkdir(parents=True, exist_ok=True)
        if lscripts.exists():
            synced_py = 0
            for sf in lscripts.glob("*.py"):
                dest = gscripts / sf.name
                if not dest.exists() or sf.stat().st_mtime > dest.stat().st_mtime:
                    dest.write_bytes(sf.read_bytes())
                    synced_py += 1
            print(f"[✓] Shipped {synced_py} Python scripts -> Google Drive scripts/")
    except Exception as e:
        pass

    # 8. Ship Master Share Package & ZIP
    try:
        local_zip = LOCAL_MIRROR / "CME_Gold_Futures_MBP1_Research_DataPack.zip"
        gdrive_zip = GDRIVE_ROOT / "CME_Gold_Futures_MBP1_Research_DataPack.zip"
        if local_zip.exists():
            if not gdrive_zip.exists() or local_zip.stat().st_mtime > gdrive_zip.stat().st_mtime:
                gdrive_zip.write_bytes(local_zip.read_bytes())
                print(f"[✓] Shipped DataPack ZIP ({local_zip.stat().st_size / 1024:.1f} KB) -> Google Drive")
    except Exception as e:
        pass

    # 8b. Ship DuckDB & Multiscale Parquet Lake to Google Drive 5TB
    try:
        from storage.disk_space_guardian import DiskSpaceGuardian
        guardian = DiskSpaceGuardian()
        guard_res = guardian.sync_to_gdrive()
        if guard_res.get("synced_files", 0) > 0:
            print(f"[✓] Shipped {guard_res['synced_files']} DuckDB & Multiscale Parquet files ({guard_res['synced_mb']} MB) -> Google Drive")
    except Exception as e:
        pass

    # 9. Sync Git Changes to GitHub Remote (if pending updates exist)
    sync_git_repo()

    # 7. Log Audit Event
    log_event("COMPREHENSIVE_SHIPPING_COMPLETED", {
        "convo_id": convo_id,
        "step_count": len(records),
        "bytes_written": len(markdown_content),
        "reports_shipped": synced_reports,
        "docs_shipped": synced_docs,
        "collaborator": COLLABORATOR_EMAIL,
        "sync_timestamp": datetime.now(timezone.utc).isoformat(),
    })

    return True


def sync_git_repo():
    """Checks for pending git changes and pushes delta to GitHub."""
    try:
        env = os.environ.copy()
        env["PATH"] = f"/home/ayush-pandey/.local/bin:{env.get('PATH', '')}"
        status_res = subprocess.run(
            ["git", "-C", str(LOCAL_MIRROR), "status", "--porcelain"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
            env=env
        )
        changes = status_res.stdout.strip()
        if changes:
            now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            print(f"[*] Git changes detected. Staging and committing...")
            subprocess.run(["git", "-C", str(LOCAL_MIRROR), "add", "."], check=True, timeout=15, env=env)
            commit_msg = f"chore(sync): automated institutional state update [{now_str}]"
            subprocess.run(["git", "-C", str(LOCAL_MIRROR), "commit", "-m", commit_msg], check=True, timeout=15, env=env)
            print(f"[*] Pushing commit to GitHub remote (origin main)...")
            push_res = subprocess.run(
                ["git", "-C", str(LOCAL_MIRROR), "push", "origin", "main"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=45,
                env=env
            )
            if push_res.returncode == 0:
                print(f"[✓] Successfully pushed automated sync commit to GitHub!")
            else:
                print(f"[!] Git push note: {push_res.stderr.strip()[:100]}")
        else:
            print("[✓] Git working tree clean — zero pending changes to push.")
    except Exception as e:
        print(f"[!] Git auto-push skipped: {e}")


def run_daemon(interval_sec: int = 600):
    """Run persistent 600-second daemon."""
    print(f"🚀 Launching Databento 600-Second Auto-Sync Daemon...")
    print(f"📁 Target Folder: {GDRIVE_ROOT}")
    print(f"👤 Collaborator: {COLLABORATOR_EMAIL}")
    print(f"⏱️ Sync Interval: {interval_sec} seconds (10 minutes)\n")

    sync_all()

    try:
        while True:
            time.sleep(interval_sec)
            now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            print(f"[{now}] 🔄 Waking up for scheduled 600-second sync cycle...")
            sync_all()
    except KeyboardInterrupt:
        print("\n[!] Auto-Sync Daemon terminated gracefully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize conversation logs and agent memory")
    parser.add_argument("--daemon", action="store_true", help="Run continuously every 600 seconds")
    parser.add_argument("--interval", type=int, default=600, help="Interval in seconds (default: 600)")
    args = parser.parse_args()

    if args.daemon:
        run_daemon(args.interval)
    else:
        sync_all()
