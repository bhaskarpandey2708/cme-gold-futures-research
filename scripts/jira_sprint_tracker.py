#!/usr/bin/env python3
"""
CME Platform Jira-Style Sprint & Epic Tracking Engine
=====================================================
Provides programmatic and CLI-based Agile Sprint management for institutional
quantitative engineering, tracking Epics, User Stories, Story Points, and Status.

Usage:
  python3 scripts/jira_sprint_tracker.py board           # Display ASCII Kanban Board
  python3 scripts/jira_sprint_tracker.py status          # Summary metrics & completion %
  python3 scripts/jira_sprint_tracker.py start <key>     # Set story to IN_PROGRESS
  python3 scripts/jira_sprint_tracker.py test <key>      # Set story to QA_TESTING
  python3 scripts/jira_sprint_tracker.py done <key>      # Set story to DONE
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any

BASE_DIR = Path(__file__).resolve().parent.parent
BOARD_FILE = BASE_DIR / "config" / "jira_sprint_board.json"

# ANSI Colors
C_GOLD = "\033[38;5;220m"
C_BLUE = "\033[38;5;75m"
C_GREEN = "\033[38;5;82m"
C_YELLOW = "\033[38;5;226m"
C_MUTED = "\033[38;5;244m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"


class JiraSprintTracker:
    def __init__(self, board_path: Path = BOARD_FILE):
        self.board_path = board_path
        self.data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.board_path.exists():
            raise FileNotFoundError(f"Jira board configuration not found at {self.board_path}")
        with open(self.board_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self):
        with open(self.board_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def print_status(self):
        stories = self.data.get("stories", [])
        total_pts = sum(s.get("points", 0) for s in stories)
        done_pts = sum(s.get("points", 0) for s in stories if s.get("status") == "DONE")
        in_prog_pts = sum(s.get("points", 0) for s in stories if s.get("status") in ("IN_PROGRESS", "QA_TESTING"))
        ready_pts = sum(s.get("points", 0) for s in stories if s.get("status") == "READY")

        pct = (done_pts / total_pts * 100.0) if total_pts > 0 else 0.0

        print(f"\n{C_BOLD}{C_GOLD}══════════════════════════════════════════════════════════════════════════════════════{C_RESET}")
        print(f"{C_BOLD} 📋 JIRA SPRINT TRACKER: {self.data.get('sprint_name')}{C_RESET}")
        print(f"{C_BOLD}{C_GOLD}══════════════════════════════════════════════════════════════════════════════════════{C_RESET}")
        print(f" Goal: {self.data.get('sprint_goal')}")
        print(f" Cadence: {self.data.get('sprint_cadence')}")
        print(f" Velocity / Progress: {C_GREEN}{C_BOLD}{done_pts}/{total_pts} Story Points ({pct:.1f}% Complete){C_RESET}")
        print(f" Status Breakdown: [READY: {ready_pts} pts] | [IN_PROGRESS: {in_prog_pts} pts] | [DONE: {done_pts} pts]\n")

        print(f"{C_BOLD}▶ EPICS BREAKDOWN:{C_RESET}")
        epics = self.data.get("epics", [])
        for e in epics:
            e_stories = [s for s in stories if s.get("epic") == e["id"]]
            e_done = sum(s.get("points", 0) for s in e_stories if s.get("status") == "DONE")
            e_total = sum(s.get("points", 0) for s in e_stories)
            e_pct = (e_done / e_total * 100.0) if e_total > 0 else 0.0
            print(f"  • {C_BLUE}{e['id']} [{e['key']}]{C_RESET}: {e['title']:<48} "
                  f"({e_done}/{e_total} pts | {C_GREEN if e_pct==100 else C_YELLOW}{e_pct:>5.1f}%{C_RESET})")
        print("")

    def print_board(self):
        self.print_status()
        stories = self.data.get("stories", [])
        columns = ["READY", "IN_PROGRESS", "QA_TESTING", "DONE"]

        print(f"{C_BOLD}┌───────────────────┬───────────────────┬───────────────────┬───────────────────┐{C_RESET}")
        print(f"{C_BOLD}│    READY (TODO)   │    IN PROGRESS    │    QA / TESTING   │     DONE (100%)   │{C_RESET}")
        print(f"{C_BOLD}├───────────────────┼───────────────────┼───────────────────┼───────────────────┤{C_RESET}")

        col_stories = {c: [s for s in stories if s.get("status") == c] for c in columns}
        max_rows = max(len(col_stories[c]) for c in columns)

        for r in range(max_rows):
            row_cells = []
            for c in columns:
                if r < len(col_stories[c]):
                    s = col_stories[c][r]
                    cell_text = f"[{s['key']}] {s['points']}p {s['title'][:10]}"
                    row_cells.append(f"{cell_text:<19}")
                else:
                    row_cells.append(f"{' ': <19}")
            print(f"│ {row_cells[0]} │ {row_cells[1]} │ {row_cells[2]} │ {row_cells[3]} │")
        print(f"{C_BOLD}└───────────────────┴───────────────────┴───────────────────┴───────────────────┘{C_RESET}\n")

    def update_status(self, story_key: str, new_status: str):
        found = False
        for s in self.data.get("stories", []):
            if s.get("key").upper() == story_key.upper():
                old_status = s.get("status")
                s["status"] = new_status.upper()
                found = True
                print(f"[✓] Updated {s['key']} ({s['title']}): {old_status} ──► {C_GREEN}{s['status']}{C_RESET}")
                break
        if not found:
            print(f"[!] Story key '{story_key}' not found on active sprint board.")
        else:
            self._save()


def main():
    parser = argparse.ArgumentParser(description="Jira Sprint & Epic Tracker CLI")
    parser.add_argument("command", choices=["board", "status", "start", "test", "done"], help="Command")
    parser.add_argument("key", nargs="?", default="", help="Story Key (e.g. CME-101)")
    args = parser.parse_args()

    tracker = JiraSprintTracker()
    if args.command == "status":
        tracker.print_status()
    elif args.command == "board":
        tracker.print_board()
    elif args.command == "start":
        tracker.update_status(args.key, "IN_PROGRESS")
    elif args.command == "test":
        tracker.update_status(args.key, "QA_TESTING")
    elif args.command == "done":
        tracker.update_status(args.key, "DONE")


if __name__ == "__main__":
    main()
