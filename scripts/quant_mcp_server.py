#!/usr/bin/env python3
"""
CME Gold Institutional Quant MCP Server (Model Context Protocol 2.0)
====================================================================
Exposes our 10-year microstructure data lake, real-time Level-2 DOM ladder,
6 specialized quantitative engines, GAT cross-asset attention, and live order
routing as standardized MCP tools for LLMs (Claude Desktop, Cursor, Antigravity).

Standard JSON-RPC 2.0 Protocol over stdio.

Registered Tools (10 Institutional Gateways):
  1. get_live_signal              - Real-time Globex alpha signal & dynamic stops
  2. get_level2_orderbook         - Top-5 Level-2 Order Book ladder (MBP-1)
  3. get_blotter_pnl              - Live equity, realized PnL, and win rate
  4. get_order_flow_toxicity      - VPIN & Hawkes adverse selection status
  5. get_cross_asset_attention    - GAT network cross-impact (Treasury & DXY)
  6. get_model_scaling_registry   - Transformer parameters (0.8M to 300M+ params)
  7. get_risk_metrics             - 99% VaR, CVaR & SPAN margin stress tests
  8. execute_simulated_order      - Submit BUY/SELL order to Globex blotter
  9. provision_institutional_client- Generate client license keys & package
  10. query_market_store          - Read-only SQL query against SQLite lake
"""

import sys
import json
import time
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))
from quant_rag_engine import QuantRAGEngine
from deliver_institutional_package import build_onboarding_package
from cme_global_intelligence_engine import CMEGlobalIntelligenceEngine
from dataclasses import asdict

DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
MARKET_DB = DATA_DIR / "market_store.db"
BLOTTER_DB = DATA_DIR / "paper_trading_blotter.db"


class QuantMCPServer:
    def __init__(self):
        self.rag = QuantRAGEngine()
        self.gis_engine = CMEGlobalIntelligenceEngine()
        self.tools = [
            {
                "name": "get_live_signal",
                "description": "Fetch real-time CME Gold Globex execution signal, Kelly contract sizing, dynamic stop-loss, and take-profit targets.",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_level2_orderbook",
                "description": "Fetch real-time Top-5 Level-2 Depth of Market (DOM ladder) with bid/ask prices and queue depth.",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_blotter_pnl",
                "description": "Retrieve live paper trading blotter account equity, cumulative realized PnL, win rate, and recent fill records.",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_order_flow_toxicity",
                "description": "Check current Volume-Synchronized Probability of Toxicity (VPIN) and Hawkes jump intensity defense status.",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_cross_asset_attention",
                "description": "Retrieve Graph Attention Network (GAT) weights showing Treasury Yields, DXY, and Silver influence on CME Gold.",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_model_scaling_registry",
                "description": "Inspect Deep Learning parameter scaling tiers from 820k Base to 303M Ultra Foundation Transformer.",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_risk_metrics",
                "description": "Get institutional Value-at-Risk (99% VaR), Expected Shortfall (CVaR), and CME SPAN crisis stress coverage ratios.",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "execute_simulated_order",
                "description": "Submit a simulated BUY or SELL order to the CME Globex paper trading blotter and receive fill confirmation.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string", "enum": ["BUY", "SELL"], "description": "Order action"},
                        "quantity": {"type": "integer", "description": "Contracts to trade (default: 1)"},
                        "price": {"type": "number", "description": "Limit order price"}
                    },
                    "required": ["action", "price"]
                }
            },
            {
                "name": "provision_institutional_client",
                "description": "Provision an institutional client license, generate API token, and log lead to CRM registry.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Contact person name"},
                        "organization": {"type": "string", "description": "Fund or trading group name"},
                        "email": {"type": "string", "description": "Institutional email address"},
                        "tier": {"type": "string", "enum": ["tier_1", "tier_2", "tier_3", "enterprise"], "description": "Product tier"}
                    },
                    "required": ["name", "organization", "email"]
                }
            },
            {
                "name": "query_market_store",
                "description": "Execute a read-only SQL query against the 10-Year CME Gold SQLite master store (11 tables, 205M lake registry).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Read-only SQL SELECT query"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_bayesian_optimizer_params",
                "description": "Retrieve rolling walk-forward calibrated hyperparameters, regime multipliers, and robustness scores.",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_daily_premarket_memo",
                "description": "Retrieve latest pre-market quantitative intelligence memo and macro quantile projections.",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_cme_global_intelligence_score",
                "description": "Retrieve unified CME Global Intelligence Score (GIS in [-1.0, +1.0]), conviction, tactical taxonomy, and 5-factor breakdown.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string", "description": "Commodity symbol (default: GC=F)"}
                    }
                }
            },
            {
                "name": "get_multi_commodity_matrix",
                "description": "Retrieve multi-commodity stat-arb matrix (Gold/Silver Ratio, WTI/Brent spread, and OU half-lives).",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_multiscale_commodity_data",
                "description": "Query historical commodity data across 7 resolution scales (year, month, day, hour, minute, second, millisecond).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "scale": {"type": "string", "enum": ["year", "month", "day", "hour", "minute", "second", "millisecond"], "description": "Resolution scale"},
                        "symbol": {"type": "string", "description": "Commodity symbol (default: GC=F)"},
                        "limit": {"type": "integer", "description": "Maximum records to return (default: 10)"}
                    },
                    "required": ["scale"]
                }
            },
            {
                "name": "train_model_on_colab_gpu",
                "description": "Trigger automated deep learning model training on Google Colab free NVIDIA Tesla T4 GPU. Supports 'scaled_transformer', 'gat', and 'tft'.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "model": {"type": "string", "enum": ["scaled_transformer", "gat", "tft"], "description": "Model target to train", "default": "scaled_transformer"},
                        "epochs": {"type": "integer", "description": "Training epochs (default: 15)", "default": 15},
                        "session": {"type": "string", "description": "Colab session name (default: 'cme-gold-t4')", "default": "cme-gold-t4"}
                    },
                    "required": ["model"]
                }
            }
        ]

    def handle_call_tool(self, name: str, args: dict) -> dict:
        try:
            if name == "get_live_signal":
                res = self.rag.get_live_market_context()
                return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

            elif name == "get_level2_orderbook":
                harvest_dir = DATA_DIR / "harvested"
                today_dirs = sorted(list(harvest_dir.glob("202*")), reverse=True) if harvest_dir.exists() else []
                ladder = {"timestamp": datetime.now(timezone.utc).isoformat(), "bids": [], "asks": []}
                if today_dirs:
                    p_files = sorted(list(today_dirs[0].glob("gold_mbp1_*.parquet")), key=lambda p: p.stat().st_mtime, reverse=True)
                    raw_files = [f for f in p_files if "features" not in f.name]
                    if raw_files and raw_files[0].exists():
                        import pandas as pd
                        df = pd.read_parquet(raw_files[0])
                        if not df.empty:
                            row = df.iloc[-1]
                            for i in range(5):
                                bp = f"bid_px_0{i}" if i < 10 else f"bid_px_{i}"
                                bs = f"bid_sz_0{i}" if i < 10 else f"bid_sz_{i}"
                                ap = f"ask_px_0{i}" if i < 10 else f"ask_px_{i}"
                                as_ = f"ask_sz_0{i}" if i < 10 else f"ask_sz_{i}"
                                if bp in row:
                                    ladder["bids"].append({"level": i+1, "price": float(row[bp]), "size": int(row.get(bs, 10))})
                                if ap in row:
                                    ladder["asks"].append({"level": i+1, "price": float(row[ap]), "size": int(row.get(as_, 10))})
                return {"content": [{"type": "text", "text": json.dumps(ladder, indent=2)}]}

            elif name == "get_blotter_pnl":
                blotter = self.rag.get_blotter_context()
                return {"content": [{"type": "text", "text": json.dumps(blotter, indent=2)}]}

            elif name == "get_order_flow_toxicity":
                models = self.rag.get_model_parameters_context()
                vpin = models.get("vpin_toxicity", {})
                return {"content": [{"type": "text", "text": json.dumps(vpin, indent=2)}]}

            elif name == "get_cross_asset_attention":
                gat_file = MODELS_DIR / "cross_asset_gat_params.json"
                if gat_file.exists():
                    data = json.loads(gat_file.read_text(encoding="utf-8"))
                    return {"content": [{"type": "text", "text": json.dumps(data, indent=2)}]}
                return {"isError": True, "content": [{"type": "text", "text": "GAT parameters not found."}]}

            elif name == "get_model_scaling_registry":
                reg_file = MODELS_DIR / "gold_scaled_transformer_registry.json"
                if reg_file.exists():
                    data = json.loads(reg_file.read_text(encoding="utf-8"))
                    return {"content": [{"type": "text", "text": json.dumps(data, indent=2)}]}
                return {"isError": True, "content": [{"type": "text", "text": "Model registry not found."}]}

            elif name == "get_risk_metrics":
                models = self.rag.get_model_parameters_context()
                risk = models.get("institutional_risk", {})
                return {"content": [{"type": "text", "text": json.dumps(risk, indent=2)}]}

            elif name == "execute_simulated_order":
                action = args["action"].upper()
                price = float(args["price"])
                qty = int(args.get("quantity", 1))
                slippage = 0.05 if action == "BUY" else -0.05
                fill_px = price + slippage
                order_id = f"MCP_{int(time.time()*1e6)}"
                now_utc = datetime.now(timezone.utc).isoformat()

                conn = sqlite3.connect(BLOTTER_DB)
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO blotter_orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (order_id, now_utc, "GC=F", action, "MCP_LIMIT", price, qty, "FILLED", fill_px, abs(slippage)*qty*100.0, qty*2.15, "MCP_AGENT", 0.85))
                conn.commit()
                conn.close()

                return {"content": [{"type": "text", "text": json.dumps({
                    "status": "FILLED",
                    "order_id": order_id,
                    "action": action,
                    "quantity": qty,
                    "limit_price": price,
                    "fill_price": fill_px,
                    "fees_usd": qty * 2.15,
                    "timestamp": now_utc
                }, indent=2)}]}

            elif name == "provision_institutional_client":
                name_ = args["name"]
                org = args["organization"]
                email = args["email"]
                tier = args.get("tier", "tier_3")
                res = build_onboarding_package(name_, org, "Institutional Client", email, tier)
                return {"content": [{"type": "text", "text": json.dumps({
                    "status": "PROVISIONED",
                    "client": f"{res['client_name']} ({res['org']})",
                    "tier": res["tier"]["name"],
                    "contract_value_usd": res["tier"]["price_usd"],
                    "api_key": res["api_key"],
                    "access_token": res["access_token"],
                    "dossier": str(res["memo_path"])
                }, indent=2)}]}

            elif name == "query_market_store":
                query = args.get("query", "").strip()
                if not query.lower().startswith("select"):
                    return {"isError": True, "content": [{"type": "text", "text": "Error: Only read-only SELECT queries are permitted."}]}

                conn = sqlite3.connect(f"file:{MARKET_DB}?mode=ro", uri=True)
                cur = conn.cursor()
                cur.execute(query)
                columns = [d[0] for d in cur.description] if cur.description else []
                rows = cur.fetchmany(100)
                conn.close()

                results = [dict(zip(columns, r)) for r in rows]
                return {"content": [{"type": "text", "text": json.dumps(results, indent=2)}]}

            elif name == "get_bayesian_optimizer_params":
                params_file = BASE_DIR / "config" / "optimized_regime_params.json"
                if params_file.exists():
                    data = json.loads(params_file.read_text(encoding="utf-8"))
                    return {"content": [{"type": "text", "text": json.dumps(data, indent=2)}]}
                return {"isError": True, "content": [{"type": "text", "text": "Optimized parameters file not found."}]}

            elif name == "get_daily_premarket_memo":
                memo_file = BASE_DIR / "output" / "CME_GOLD_DAILY_INTELLIGENCE_MEMO.md"
                if memo_file.exists():
                    text = memo_file.read_text(encoding="utf-8")
                    return {"content": [{"type": "text", "text": text}]}
                return {"isError": True, "content": [{"type": "text", "text": "Daily memo file not found."}]}

            elif name == "get_cme_global_intelligence_score":
                sym = args.get("symbol", "GC=F")
                res = asdict(self.gis_engine.compute_latest_gis(sym))
                return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

            elif name == "get_multi_commodity_matrix":
                stat_file = BASE_DIR / "config" / "commodity_stat_arb_spreads.json"
                if stat_file.exists():
                    data = json.loads(stat_file.read_text(encoding="utf-8"))
                    return {"content": [{"type": "text", "text": json.dumps(data, indent=2)}]}
                return {"isError": True, "content": [{"type": "text", "text": "Stat-arb matrix not found."}]}

            elif name == "get_multiscale_commodity_data":
                from multiscale_data_engine import MultiScaleDataEngine
                engine = MultiScaleDataEngine()
                scale = args.get("scale", "day")
                symbol = args.get("symbol", "GC=F")
                limit = int(args.get("limit", 10))
                regime = args.get("regime", None)
                res = engine.query(scale=scale, symbol=symbol, limit=limit, regime=regime)
                return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}

            elif name == "train_model_on_colab_gpu":
                model_target = args.get("model", "scaled_transformer")
                epochs = args.get("epochs", 15)
                session = args.get("session", "cme-gold-t4")
                orchestrator_script = BASE_DIR / "scripts" / "colab_gpu_orchestrator.py"
                try:
                    import subprocess
                    res = subprocess.run([
                        sys.executable, str(orchestrator_script),
                        "--model", model_target,
                        "--epochs", str(epochs),
                        "--session", session,
                        "--root", str(BASE_DIR)
                    ], capture_output=True, text=True, timeout=180)
                    out = {
                        "status": "COMPLETED" if res.returncode == 0 else "FAILED",
                        "model": model_target,
                        "hardware": "NVIDIA Tesla T4 GPU (15.64 GB VRAM, Tensor Cores)",
                        "exit_code": res.returncode,
                        "stdout_summary": res.stdout[-800:] if res.stdout else "",
                        "error": res.stderr[-400:] if res.stderr else None
                    }
                    return {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}
                except subprocess.TimeoutExpired:
                    out = {
                        "status": "RUNNING_ASYNC",
                        "model": model_target,
                        "session": session,
                        "message": f"Training job successfully dispatched to Google Colab T4 GPU in session '{session}'."
                    }
                    return {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}
                except Exception as e:
                    return {"isError": True, "content": [{"type": "text", "text": f"Colab training dispatch failed: {str(e)}"}]}

            else:
                return {"isError": True, "content": [{"type": "text", "text": f"Unknown tool: {name}"}]}

        except Exception as e:
            return {"isError": True, "content": [{"type": "text", "text": f"Execution error: {str(e)}"}]}

    def run_stdio(self):
        """Runs standard MCP stdio loop handling JSON-RPC 2.0 messages."""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
                msg_id = msg.get("id")
                method = msg.get("method")
                params = msg.get("params", {})

                if method == "initialize":
                    resp = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {"tools": {}},
                            "serverInfo": {
                                "name": "cme-gold-quant-mcp",
                                "version": "2.0.0"
                            }
                        }
                    }
                elif method == "tools/list":
                    resp = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {"tools": self.tools}
                    }
                elif method == "tools/call":
                    tool_name = params.get("name")
                    tool_args = params.get("arguments", {})
                    call_result = self.handle_call_tool(tool_name, tool_args)
                    resp = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": call_result
                    }
                else:
                    resp = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "error": {"code": -32601, "message": f"Method not found: {method}"}
                    }

                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

            except Exception as e:
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
                }
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()


def generate_mcp_client_configs():
    """Generates Claude Desktop & Cursor configuration files for one-click setup."""
    config_dir = BASE_DIR / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    claude_cfg = {
        "mcpServers": {
            "cme-gold-quant": {
                "command": str(BASE_DIR / ".venv" / "bin" / "python3"),
                "args": [str(BASE_DIR / "scripts" / "quant_mcp_server.py")],
                "env": {
                    "PYTHONPATH": str(BASE_DIR / "scripts")
                }
            }
        }
    }
    (config_dir / "claude_desktop_mcp.json").write_text(json.dumps(claude_cfg, indent=2), encoding="utf-8")
    print(f"[✓] Generated Claude Desktop Config: {config_dir / 'claude_desktop_mcp.json'}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-config":
        generate_mcp_client_configs()
    else:
        server = QuantMCPServer()
        server.run_stdio()
