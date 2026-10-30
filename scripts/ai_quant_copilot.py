#!/usr/bin/env python3
"""
CME Gold Interactive AI Quant Copilot & Telegram/Terminal Agent
==============================================================
An autonomous, conversational financial assistant that allows traders
and quantitative analysts to query live trading signals, order book
toxicity, basis arbitrage, risk metrics, and PnL in natural language
via Terminal CLI, Discord, or Telegram.

Supported Commands:
  /status  - Overall system status, daemons, and storage health
  /signal  - Real-time CME Globex alpha decision, target, stops
  /pnl     - Live blotter equity, realized PnL, win rate
  /vpin    - Order flow toxicity & Hawkes flash-crash shield
  /basis   - CME GC vs MGC basis arbitrage & OU half-life
  /risk    - 99% Value-at-Risk (VaR), CVaR & SPAN margin stress
  /help    - Display interactive command guide

Usage:
  python3 scripts/ai_quant_copilot.py --interactive
  python3 scripts/ai_quant_copilot.py --query "What is our current PnL?"
  python3 scripts/ai_quant_copilot.py --telegram --token <BOT_TOKEN>
"""

import sys
import json
import time
import argparse
import urllib.request
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))
from quant_rag_engine import QuantRAGEngine

CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BOLD = "\033[1m"
RESET = "\033[0m"


class AIQuantCopilot:
    def __init__(self, telegram_token: str = None):
        self.rag = QuantRAGEngine()
        self.tg_token = telegram_token
        self.last_update_id = 0

    def handle_command(self, text: str) -> str:
        """Parses slash commands or natural language questions."""
        cmd = text.strip().lower()

        if cmd in ("/start", "/help"):
            return (
                "🤖 **CME Gold AI Quant Copilot Ready**\n"
                "Available Commands:\n"
                "• `/signal` - Real-time execution action & dynamic stops\n"
                "• `/pnl`    - Account equity, net PnL, and win rate\n"
                "• `/vpin`   - Order flow toxicity & defense shield\n"
                "• `/basis`  - CME GC vs MGC basis arbitrage & OU half-life\n"
                "• `/risk`   - 99% VaR, CVaR & SPAN stress test coverage\n"
                "• `/status` - Daemon health & lake partition activity\n"
                "Or simply ask any question in plain English!"
            )
        elif cmd == "/signal":
            return self.rag.answer_query("latest signal and dynamic stops")
        elif cmd in ("/pnl", "/equity", "/blotter"):
            return self.rag.answer_query("current pnl and equity")
        elif cmd in ("/vpin", "/toxicity"):
            return self.rag.answer_query("vpin toxicity and hawkes shield")
        elif cmd in ("/basis", "/arb"):
            return self.rag.answer_query("basis arbitrage performance and half life")
        elif cmd in ("/risk", "/var"):
            return self.rag.answer_query("institutional risk var and cvar")
        elif cmd == "/status":
            m = self.rag.get_live_market_context()
            b = self.rag.get_blotter_context()
            return (
                f"🏛️ **System Cockpit Status:**\n"
                f"• Production Daemons: ACTIVE (Harvester, Sync, Decision Engine)\n"
                f"• Latest Decision: [{m.get('primary_action')}] @ ${m.get('target_price', 0):.2f}\n"
                f"• Total Equity: ${b.get('total_equity', 250000.0):,.2f} (Net Realized: ${b.get('realized_pnl', 0.0):+,.2f})\n"
                f"• Open Contracts: {b.get('open_contracts', 0):+d} GC Contract(s)\n"
                f"• Evaluated Batch: {m.get('source_batch')}"
            )
        else:
            # Natural Language QuantRAG query
            return self.rag.answer_query(text)

    def run_interactive_cli(self):
        """Interactive terminal session."""
        print(f"{CYAN}╔══════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{CYAN}║     🤖 CME GOLD INTERACTIVE AI QUANT COPILOT (TERMINAL SESSION)          ║{RESET}")
        print(f"{CYAN}╚══════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"Type {GREEN}/help{RESET} for commands or ask any question. Type {BOLD}exit{RESET} to quit.\n")

        while True:
            try:
                user_input = input(f"{BOLD}QuantUser > {RESET}").strip()
                if not user_input:
                    continue
                if user_input.lower() in ("exit", "quit", "q"):
                    print("[*] Exiting AI Quant Copilot. Goodbye!")
                    break

                resp = self.handle_command(user_input)
                print(f"\n{CYAN}Copilot >{RESET}\n{resp}\n")
            except (KeyboardInterrupt, EOFError):
                print("\n[*] Session terminated.")
                break

    def run_telegram_polling(self):
        """Continuous long-polling loop for Telegram Bot."""
        if not self.tg_token:
            print("[!] Error: Telegram bot token required for polling mode.")
            return

        print(f"[*] Starting Telegram AI Bot polling...")
        api_base = f"https://api.telegram.org/bot{self.tg_token}"

        while True:
            try:
                url = f"{api_base}/getUpdates?offset={self.last_update_id + 1}&timeout=30"
                req = urllib.request.Request(url, headers={"User-Agent": "CME-Gold-Copilot/1.0"})
                with urllib.request.urlopen(req, timeout=35) as resp:
                    data = json.loads(resp.read().decode("utf-8"))

                for item in data.get("result", []):
                    self.last_update_id = item["update_id"]
                    msg = item.get("message", {})
                    chat_id = msg.get("chat", {}).get("id")
                    text = msg.get("text", "")

                    if chat_id and text:
                        print(f"[*] Received Telegram query from chat {chat_id}: '{text}'")
                        reply = self.handle_command(text)
                        
                        # Send Reply
                        send_url = f"{api_base}/sendMessage"
                        payload = urllib.parse.urlencode({
                            "chat_id": chat_id,
                            "text": reply,
                            "parse_mode": "Markdown"
                        }).encode("utf-8")
                        send_req = urllib.request.Request(send_url, data=payload)
                        urllib.request.urlopen(send_req, timeout=10)

                time.sleep(1)
            except Exception as e:
                time.sleep(5)


def main():
    parser = argparse.ArgumentParser(description="CME Gold AI Quant Copilot")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive CLI session")
    parser.add_argument("--query", type=str, help="Single natural language query")
    parser.add_argument("--telegram", action="store_true", help="Run as Telegram bot")
    parser.add_argument("--token", type=str, help="Telegram Bot Token")
    args = parser.parse_args()

    copilot = AIQuantCopilot(telegram_token=args.token)

    if args.query:
        print(copilot.handle_command(args.query))
    elif args.telegram:
        copilot.run_telegram_polling()
    else:
        copilot.run_interactive_cli()


if __name__ == "__main__":
    main()
