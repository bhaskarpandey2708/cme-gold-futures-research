#!/usr/bin/env python3
"""
Enterprise Real-Time Decision & Risk Daemon
===========================================
Continuously monitors freshly harvested CME Gold microstructure ticks,
evaluates Stacking Meta-Alpha & Deep Learning probability distributions,
computes Fractional Kelly sizing and CME FIFO queue fill targets,
and logs real-time institutional trade execution decisions (BUY/SELL/HOLD).

Generates:
  • logs/live_decisions.jsonl (Structured decision feed)
  • output/enterprise_decision_terminal.html (Live browser monitor)

Usage:
  python3 scripts/run_enterprise_decision_daemon.py --interval 10 --once
  python3 scripts/run_enterprise_decision_daemon.py --interval 10 --daemon
"""

import os
import sys
import time
import json
import argparse
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent.parent
GDRIVE_DIR = BASE_DIR
DATA_DIR = BASE_DIR / "data"
HARVEST_DIR = DATA_DIR / "harvested"
LOGS_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "output"

LOGS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DECISIONS_LOG = LOGS_DIR / "live_decisions.jsonl"
TERMINAL_HTML = OUTPUT_DIR / "enterprise_decision_terminal.html"

# Import Enterprise Decision Engine, Alert Dispatcher & Paper Blotter
sys.path.append(str(BASE_DIR / "scripts"))
from enterprise_decision_system import EnterpriseDecisionSystem
from trading_alert_dispatcher import TradingAlertDispatcher
from paper_trading_simulator import PaperTradingSimulator


class EnterpriseDecisionDaemon:
    def __init__(self, check_interval: int = 15, capital: float = 250_000.0):
        self.interval = check_interval
        self.engine = EnterpriseDecisionSystem(max_capital=capital, max_risk_per_trade=0.015)
        self.blotter = PaperTradingSimulator(initial_capital=capital, restore_state=True)
        self.dispatcher = TradingAlertDispatcher()
        self.last_processed_file = None
        self.total_decisions = 0
        self.last_gdrive_sync = 0.0

    def get_latest_harvest_file(self) -> Path:
        """Finds the most recent parquet batch from today's partition."""
        if not HARVEST_DIR.exists():
            return None
        today_dirs = sorted(list(HARVEST_DIR.glob("202*")), reverse=True)
        if not today_dirs:
            return None
        p_files = sorted(list(today_dirs[0].glob("gold_mbp1_*.parquet")), key=lambda p: p.stat().st_mtime, reverse=True)
        # Exclude features files if looking for raw
        raw_files = [f for f in p_files if "features" not in f.name]
        return raw_files[0] if raw_files else (p_files[0] if p_files else None)

    def evaluate_latest_batch(self):
        latest_file = self.get_latest_harvest_file()
        if not latest_file or not latest_file.exists():
            print("[!] No harvested parquet batches found to evaluate.")
            return

        print(f"[*] Ingesting latest market batch: {latest_file.name} ({latest_file.stat().st_size / 1024:.1f} KB)")
        try:
            df = pd.read_parquet(latest_file)
            if df.empty:
                return

            # Grab top 5 most recent book snapshots
            books = df[df["action"] == "B"] if "action" in df.columns else df
            if books.empty:
                books = df

            latest_row = books.iloc[-1]
            snapshot = {
                "bid_px_00": float(latest_row.get("bid_px_00", 2724.80)),
                "ask_px_00": float(latest_row.get("ask_px_00", 2724.90)),
                "bid_sz_00": float(latest_row.get("bid_sz_00", 25.0)),
                "ask_sz_00": float(latest_row.get("ask_sz_00", 20.0)),
            }

            decision = self.engine.generate_trade_decision(snapshot, regime_vol=0.14)
            decision["source_file"] = latest_file.name
            decision["evaluated_at"] = datetime.now(timezone.utc).isoformat()

            # Append to decisions log
            with open(DECISIONS_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(decision) + "\n")

            self.total_decisions += 1
            print(f"[✓] Decision #{self.total_decisions}: [{decision['decision']}] "
                  f"Price: ${decision['target_price']:.2f} | "
                  f"Conviction: {decision['alpha_signals']['conviction']} "
                  f"(Alpha: {decision['alpha_signals']['alpha_score']:+.2f})")

            # Dispatch Institutional Alert if BUY or SELL
            signal_payload = {
                "timestamp": decision["evaluated_at"],
                "primary_action": decision["decision"],
                "target_price": decision["target_price"],
                "conviction": decision["alpha_signals"]["conviction"],
                "composite_alpha": decision["alpha_signals"]["alpha_score"],
                "suggested_contracts": decision.get("sizing", {}).get("contracts", 1) if decision.get("sizing") else 1,
                "stop_loss": decision.get("stop_loss", 0.0),
                "take_profit": decision.get("take_profit", 0.0)
            }
            self.dispatcher.dispatch_alert(signal_payload)

            # Ingest into Live Paper Trading Blotter
            try:
                self.blotter.process_decision(decision)
                if self.total_decisions % 5 == 0:
                    report_text = self.blotter.generate_blotter_report()
                    (OUTPUT_DIR / "PAPER_TRADING_BLOTTER_REPORT.md").write_text(report_text, encoding="utf-8")
            except Exception as be:
                print(f"[!] Blotter execution error: {be}")

            # Update HTML Terminal Dashboard
            self.render_terminal_dashboard(decision)

        except Exception as e:
            print(f"[!] Error evaluating market batch: {e}")

    def render_terminal_dashboard(self, latest_decision: dict):
        action_color = "#00E676" if latest_decision["decision"] == "BUY" else ("#FF5252" if latest_decision["decision"] == "SELL" else "#FFD600")
        alpha = latest_decision["alpha_signals"]
        micro = latest_decision["microstructure_state"]
        sizing = latest_decision.get("sizing") or {}

        stop_loss_str = f"${latest_decision['stop_loss']:.2f}" if latest_decision.get('stop_loss') is not None else "N/A (Holding)"
        take_profit_str = f"${latest_decision['take_profit']:.2f}" if latest_decision.get('take_profit') is not None else "N/A (Holding)"
        rr_str = f"{latest_decision['risk_reward_ratio']:.2f} : 1" if latest_decision.get('risk_reward_ratio') is not None else "N/A"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="10">
<title>Enterprise Quantitative Decision Terminal — CME Gold Futures</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #0b0e14; color: #e6edf3; margin: 0; padding: 24px; }}
  .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #21262d; padding-bottom: 16px; margin-bottom: 24px; }}
  .badge {{ background: #1f6feb22; color: #58a6ff; border: 1px solid #1f6feb; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 24px; }}
  .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; }}
  .metric-label {{ font-size: 12px; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }}
  .metric-val {{ font-size: 26px; font-weight: 700; }}
  .signal-box {{ background: #161b22; border: 2px solid {action_color}; border-radius: 8px; padding: 24px; text-align: center; margin-bottom: 24px; }}
  .signal-title {{ font-size: 14px; color: #8b949e; text-transform: uppercase; margin-bottom: 8px; }}
  .signal-action {{ font-size: 48px; font-weight: 900; color: {action_color}; letter-spacing: 2px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
  th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #21262d; font-size: 13px; }}
  th {{ color: #8b949e; }}
</style>
</head>
<body>
  <div class="header">
    <div>
      <h2 style="margin: 0; font-size: 20px;">⚡ CME Gold Futures — Enterprise Decision Terminal</h2>
      <div style="font-size: 12px; color: #8b949e; margin-top: 4px;">Live Microstructure Decision Engine • Auto-Refreshes Every 10s</div>
    </div>
    <div class="badge">ACTIVE STREAMING</div>
  </div>

  <div class="signal-box">
    <div class="signal-title">Real-Time Execution Signal</div>
    <div class="signal-action">{latest_decision['decision']}</div>
    <div style="color: #8b949e; font-size: 14px; margin-top: 8px;">
      Order Type: <strong style="color: #fff;">{latest_decision['order_type']}</strong> | Target Price: <strong style="color: #fff;">${latest_decision['target_price']:.2f}</strong> | Conviction: <strong style="color: #fff;">{alpha['conviction']}</strong>
    </div>
  </div>

  <div class="grid">
    <div class="card">
      <div class="metric-label">Microstructure Mid Price</div>
      <div class="metric-val">${micro['mid_price']:.2f}</div>
      <div style="font-size: 12px; color: #8b949e; margin-top: 4px;">Spread: ${micro['spread_usd']:.2f} (Top-of-Book)</div>
    </div>
    <div class="card">
      <div class="metric-label">Order Book Imbalance (OBI)</div>
      <div class="metric-val" style="color: {'#00E676' if micro['obi'] > 0 else '#FF5252'};">{micro['obi']:+.4f}</div>
      <div style="font-size: 12px; color: #8b949e; margin-top: 4px;">Micro Drift: {micro['micro_drift_bps']:+.2f} bps</div>
    </div>
    <div class="card">
      <div class="metric-label">Model Alpha Score</div>
      <div class="metric-val" style="color: {action_color};">{alpha['alpha_score']:+.2f}</div>
      <div style="font-size: 12px; color: #8b949e; margin-top: 4px;">P(Up): {alpha['p_up']:.1%} | P(Down): {alpha['p_down']:.1%}</div>
    </div>
    <div class="card">
      <div class="metric-label">Fractional Kelly Sizing</div>
      <div class="metric-val">{sizing.get('contracts_to_trade', 0)} Contracts</div>
      <div style="font-size: 12px; color: #8b949e; margin-top: 4px;">Notional: ${sizing.get('notional_value', 0):,.2f} | Risk: ${sizing.get('max_dollar_risk', 0):,.2f}</div>
    </div>
  </div>

  <div class="grid">
    <div class="card">
      <div class="metric-label">Simulated Account Equity</div>
      <div class="metric-val" style="color: #58a6ff;">${self.blotter.get_total_equity(latest_decision['target_price']):,.2f}</div>
      <div style="font-size: 12px; color: #8b949e; margin-top: 4px;">Initial Capital: $250,000.00</div>
    </div>
    <div class="card">
      <div class="metric-label">Cumulative Realized PnL</div>
      <div class="metric-val" style="color: {'#00E676' if self.blotter.realized_pnl >= 0 else '#FF5252'};">${self.blotter.realized_pnl:+,.2f}</div>
      <div style="font-size: 12px; color: #8b949e; margin-top: 4px;">Net of $2.15/ct exchange fees</div>
    </div>
    <div class="card">
      <div class="metric-label">Execution Win Rate</div>
      <div class="metric-val">{(self.blotter.winning_trades / max(1, self.blotter.total_trades) * 100):.1f}%</div>
      <div style="font-size: 12px; color: #8b949e; margin-top: 4px;">{self.blotter.total_trades} Closed Trades ({self.blotter.winning_trades}W / {self.blotter.losing_trades}L)</div>
    </div>
    <div class="card">
      <div class="metric-label">Active Globex Position</div>
      <div class="metric-val">{self.blotter.current_position:+d} Contracts</div>
      <div style="font-size: 12px; color: #8b949e; margin-top: 4px;">Margin Used: ${abs(self.blotter.current_position) * 9900:,.2f}</div>
    </div>
  </div>

  <div class="card">
    <h3 style="margin-top: 0; font-size: 15px;">📋 Risk & Dynamic Barrier Targets</h3>
    <table>
      <tr><th>Parameter</th><th>Value</th><th>Institutional Rationale</th></tr>
      <tr><td>Target Execution Price</td><td>${latest_decision['target_price']:.2f}</td><td>Top-of-Book CME Globex queue entry</td></tr>
      <tr><td>Stop Loss Level</td><td>{stop_loss_str}</td><td>Dynamic 2.5x spread + 8-tick barrier boundary</td></tr>
      <tr><td>Take Profit Target</td><td>{take_profit_str}</td><td>Dynamic 4.5x spread profit expansion target</td></tr>
      <tr><td>Risk / Reward Ratio</td><td>{rr_str}</td><td>Positive expectancy threshold requirement</td></tr>
      <tr><td>Evaluated Batch File</td><td>{latest_decision.get('source_file')}</td><td>Streaming partitioned Parquet buffer</td></tr>
    </table>
  </div>
</body>
</html>
"""
        TERMINAL_HTML.write_text(html, encoding="utf-8")
        # Throttle Google Drive updates to once every 5 minutes or on active BUY/SELL signals
        now_ts = time.time()
        is_signal = latest_decision.get("primary_action") in ("BUY", "SELL")
        if GDRIVE_DIR.exists() and (is_signal or (now_ts - self.last_gdrive_sync >= 300)):
            gdrive_term = GDRIVE_DIR / "output" / "enterprise_decision_terminal.html"
            try:
                gdrive_term.parent.mkdir(parents=True, exist_ok=True)
                gdrive_term.write_text(html, encoding="utf-8")
                self.last_gdrive_sync = now_ts
            except Exception:
                pass


def main():
    parser = argparse.ArgumentParser(description="Enterprise Decision Daemon")
    parser.add_argument("--interval", type=int, default=15, help="Check interval in seconds")
    parser.add_argument("--once", action="store_true", help="Execute single evaluation and exit")
    parser.add_argument("--daemon", action="store_true", help="Run continuously in background")
    args = parser.parse_args()

    daemon = EnterpriseDecisionDaemon(check_interval=args.interval)
    print("=" * 70)
    print(" 🏛️  ENTERPRISE DECISION DAEMON INITIALIZING")
    print("=" * 70)

    if args.once or not args.daemon:
        daemon.evaluate_latest_batch()
    else:
        print(f"[*] Running decision daemon every {args.interval} seconds (Press Ctrl+C to stop)...")
        while True:
            daemon.evaluate_latest_batch()
            time.sleep(args.interval)


if __name__ == "__main__":
    main()
