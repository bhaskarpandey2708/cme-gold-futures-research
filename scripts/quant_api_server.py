#!/usr/bin/env python3
"""
CME Gold Institutional Async REST API Server, WebSocket Gateway & Live Web Cockpit
===================================================================================
Production asynchronous HTTP/JSON API server built with aiohttp,
providing programmatic REST endpoints, native bidirectional WebSocket streaming (/ws/live),
and a real-time Level-2 DOM web cockpit for algorithmic trading desks and institutional clients.

Endpoints:
  GET  /                     - Master Real-Time Web Cockpit (HTML/JS + WebSocket DOM)
  GET  /ws/live              - Native Bidirectional WebSocket stream (Sub-Second Book & Signals)
  GET  /api/v1/health        - System health & active daemons status
  GET  /api/v1/signal        - Live execution decision, dynamic stops & Kelly sizing
  GET  /api/v1/orderbook     - Top-5 Level-2 Order Book ladder (MBP-1)
  GET  /api/v1/pnl           - Live paper blotter equity, net PnL, and win rate
  GET  /api/v1/vpin          - Rolling order flow toxicity & Hawkes shield
  GET  /api/v1/basis         - CME Gold vs Micro Basis arbitrage & OU half-life
  GET  /api/v1/risk          - 99% VaR, Expected Shortfall & SPAN margin stress
  GET  /api/v1/models/scaling- Parameter scaling matrix (0.8M to 300M+ params)
  POST /api/v1/lead          - Instant institutional client onboarding & token issuance
  POST /api/v1/ask           - Natural language QuantRAG query answering
  POST /api/v1/query         - Read-only SQLite query interface

Usage:
  python3 scripts/quant_api_server.py --port 8085
"""

import sys
import json
import sqlite3
import asyncio
import argparse
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import asdict
import aiohttp
from aiohttp import web

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "scripts"))
from quant_rag_engine import QuantRAGEngine
from deliver_institutional_package import build_onboarding_package
from cme_global_intelligence_engine import CMEGlobalIntelligenceEngine
from multiscale_data_engine import MultiScaleDataEngine

DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
MODELS_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "output"
MARKET_DB = DATA_DIR / "market_store.db"
DECISIONS_LOG = LOGS_DIR / "live_decisions.jsonl"


class QuantAPIServer:
    def __init__(self):
        self.rag = QuantRAGEngine()
        self.gis_engine = CMEGlobalIntelligenceEngine()
        self.multiscale_engine = MultiScaleDataEngine()
        self.app = web.Application()
        self.active_websockets = set()
        self._setup_routes()
        self.app.on_startup.append(self.start_background_tasks)
        self.app.on_cleanup.append(self.cleanup_background_tasks)

    def _setup_routes(self):
        self.app.router.add_get("/", self.handle_web_cockpit)
        self.app.router.add_get("/docs", self.handle_swagger_docs)
        self.app.router.add_get("/api/v1/openapi.json", self.handle_openapi_spec)
        self.app.router.add_get("/ws/live", self.handle_websocket)
        self.app.router.add_get("/api/v1/health", self.handle_health)
        self.app.router.add_get("/api/v1/signal", self.handle_signal)
        self.app.router.add_get("/api/v1/gis", self.handle_gis)
        self.app.router.add_get("/api/v1/multiscale/hierarchy", self.handle_multiscale_hierarchy)
        self.app.router.add_get("/api/v1/multiscale", self.handle_multiscale_query)
        self.app.router.add_get("/api/v1/orderbook", self.handle_orderbook)
        self.app.router.add_get("/api/v1/depth10", self.handle_depth10)
        self.app.router.add_get("/api/v1/mbo/queue", self.handle_mbo_queue)
        self.app.router.add_get("/api/v1/tensor/deeplob", self.handle_deeplob_tensor)
        self.app.router.add_get("/api/v1/pnl", self.handle_pnl)
        self.app.router.add_get("/api/v1/vpin", self.handle_vpin)
        self.app.router.add_get("/api/v1/basis", self.handle_basis)
        self.app.router.add_get("/api/v1/risk", self.handle_risk)
        self.app.router.add_get("/api/v1/models/scaling", self.handle_scaling)
        self.app.router.add_get("/api/v1/optimizer", self.handle_optimizer)
        self.app.router.add_get("/api/v1/memo", self.handle_memo)
        self.app.router.add_post("/api/v1/lead", self.handle_lead)
        self.app.router.add_post("/api/v1/ask", self.handle_ask)
        self.app.router.add_post("/api/v1/query", self.handle_query)

    async def start_background_tasks(self, app):
        app["broadcaster"] = asyncio.create_task(self._broadcaster_loop())

    async def cleanup_background_tasks(self, app):
        app["broadcaster"].cancel()
        await asyncio.gather(app["broadcaster"], return_exceptions=True)

    def _build_live_stream_payload(self) -> dict:
        signal = self.rag.get_live_market_context()
        pnl = self.rag.get_blotter_context()
        
        # Order book ladder
        ladder = {"bids": [], "asks": []}
        harvest_dir = DATA_DIR / "harvested"
        today_dirs = sorted(list(harvest_dir.glob("202*")), reverse=True) if harvest_dir.exists() else []
        if today_dirs:
            p_files = sorted(list(today_dirs[0].glob("gold_mbp1_*.parquet")), key=lambda p: p.stat().st_mtime, reverse=True)
            raw_files = [f for f in p_files if "features" not in f.name]
            if raw_files and raw_files[0].exists():
                try:
                    import pandas as pd
                    df = pd.read_parquet(raw_files[0])
                    if not df.empty:
                        last_row = df.iloc[-1]
                        for i in range(5):
                            bp_col = f"bid_px_0{i}" if i < 10 else f"bid_px_{i}"
                            bs_col = f"bid_sz_0{i}" if i < 10 else f"bid_sz_{i}"
                            ap_col = f"ask_px_0{i}" if i < 10 else f"ask_px_{i}"
                            as_col = f"ask_sz_0{i}" if i < 10 else f"ask_sz_{i}"
                            if bp_col in last_row:
                                ladder["bids"].append({"level": i+1, "price": float(last_row[bp_col]), "size": int(last_row.get(bs_col, 10))})
                            if ap_col in last_row:
                                ladder["asks"].append({"level": i+1, "price": float(last_row[ap_col]), "size": int(last_row.get(as_col, 10))})
                except Exception:
                    pass

        return {
            "type": "TICK_UPDATE",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "signal": signal,
            "gis": asdict(self.gis_engine.compute_latest_gis("GC=F")),
            "pnl": pnl,
            "orderbook": ladder
        }

    async def _broadcaster_loop(self):
        while True:
            try:
                await asyncio.sleep(1.0)
                if self.active_websockets:
                    payload = self._build_live_stream_payload()
                    dead = set()
                    for ws in self.active_websockets:
                        try:
                            await ws.send_json(payload)
                        except Exception:
                            dead.add(ws)
                    self.active_websockets -= dead
            except asyncio.CancelledError:
                break
            except Exception as e:
                await asyncio.sleep(1.0)

    async def handle_websocket(self, request):
        ws = web.WebSocketResponse(heartbeat=15.0)
        await ws.prepare(request)
        self.active_websockets.add(ws)
        try:
            # Immediate snapshot on connect
            await ws.send_json(self._build_live_stream_payload())
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == "ping":
                        await ws.send_str("pong")
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
        finally:
            self.active_websockets.discard(ws)
        return ws

    async def handle_health(self, request):
        return web.json_response({
            "status": "ONLINE",
            "server": "CME Gold Institutional Quant API & WebSocket Gateway",
            "version": "2.0.0-PROD",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target_asset": "CME COMEX Continuous Gold Futures (GC=F)",
            "engines_active": 6,
            "active_ws_clients": len(self.active_websockets)
        })

    async def handle_signal(self, request):
        ctx = self.rag.get_live_market_context()
        return web.json_response(ctx)

    async def handle_gis(self, request):
        symbol = request.query.get("symbol", "GC=F")
        decision = self.gis_engine.compute_latest_gis(symbol)
        return web.json_response(asdict(decision))

    async def handle_multiscale_hierarchy(self, request):
        hierarchy = self.multiscale_engine.get_scale_hierarchy()
        return web.json_response(hierarchy)

    async def handle_multiscale_query(self, request):
        scale = request.query.get("scale", "day")
        symbol = request.query.get("symbol", "GC=F")
        limit = int(request.query.get("limit", 100))
        regime = request.query.get("regime", None)
        result = self.multiscale_engine.query(scale=scale, symbol=symbol, limit=limit, regime=regime)
        return web.json_response(result)

    async def handle_orderbook(self, request):
        payload = self._build_live_stream_payload()
        return web.json_response(payload["orderbook"])

    async def handle_depth10(self, request):
        try:
            import duckdb
            conn = duckdb.connect(str(DATA_DIR / "market_lake.duckdb"), read_only=True)
            df = conn.execute("SELECT * FROM v_mbp10_depth LIMIT 1").df()
            conn.close()
            if df.empty:
                return web.json_response({"error": "No MBP-10 data available"}, status=404)
            row = df.iloc[0]
            bids = [{"level": i, "price": float(row[f"bid_px_{i:02d}"]), "size": int(row[f"bid_sz_{i:02d}"]), "count": int(row[f"bid_ct_{i:02d}"])} for i in range(10)]
            asks = [{"level": i, "price": float(row[f"ask_px_{i:02d}"]), "size": int(row[f"ask_sz_{i:02d}"]), "count": int(row[f"ask_ct_{i:02d}"])} for i in range(10)]
            return web.json_response({
                "symbol": str(row["symbol"]),
                "ts_recv": str(row["ts_recv"]),
                "spread": round(float(row["ask_px_00"] - row["bid_px_00"]), 2),
                "levels": 10,
                "bids": bids,
                "asks": asks,
            })
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def handle_mbo_queue(self, request):
        try:
            import duckdb
            import pandas as pd
            limit = int(request.query.get("limit", 20))
            conn = duckdb.connect(str(DATA_DIR / "market_lake.duckdb"), read_only=True)
            df = conn.execute(f"SELECT * FROM v_mbo_queues ORDER BY ts_recv DESC LIMIT {limit}").df()
            conn.close()
            events = df.to_dict(orient="records")
            for ev in events:
                for k, v in ev.items():
                    if isinstance(v, (pd.Timestamp, datetime)):
                        ev[k] = v.isoformat()
            return web.json_response({
                "schema": "mbo",
                "count": len(events),
                "events": events
            })
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def handle_deeplob_tensor(self, request):
        try:
            from deeplob_tensor_adapter import DeepLOBTensorAdapter
            adapter = DeepLOBTensorAdapter()
            pq_path = DATA_DIR / "databento_GLBX_MDP3_GCZ6_mbp-10.parquet"
            if not pq_path.exists():
                return web.json_response({"error": "MBP-10 parquet required for tensor adapter"}, status=404)
            tensors, mids = adapter.extract_batch_from_parquet(pq_path, step=25)
            return web.json_response({
                "model_target": "DeepLOB CNN-BiLSTM",
                "tensor_shape": list(tensors.shape),
                "batch_size": tensors.shape[0],
                "channels": tensors.shape[1],
                "sequence_window": tensors.shape[2],
                "feature_dimension": tensors.shape[3],
                "mean_normalized_price": round(float(tensors[:, :, :, 0].mean().item()), 4),
                "mean_normalized_size": round(float(tensors[:, :, :, 1].mean().item()), 4),
            })
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def handle_pnl(self, request):
        ctx = self.rag.get_blotter_context()
        return web.json_response(ctx)

    async def handle_vpin(self, request):
        models = self.rag.get_model_parameters_context()
        return web.json_response(models.get("vpin_toxicity", {}))

    async def handle_basis(self, request):
        models = self.rag.get_model_parameters_context()
        return web.json_response(models.get("metals_stat_arb", {}))

    async def handle_risk(self, request):
        models = self.rag.get_model_parameters_context()
        return web.json_response(models.get("institutional_risk", {}))

    async def handle_scaling(self, request):
        reg_file = MODELS_DIR / "gold_scaled_transformer_registry.json"
        if reg_file.exists():
            data = json.loads(reg_file.read_text(encoding="utf-8"))
            return web.json_response(data)
        return web.json_response({"error": "Registry not found"}, status=404)

    async def handle_optimizer(self, request):
        opt_file = BASE_DIR / "config" / "optimized_regime_params.json"
        if opt_file.exists():
            data = json.loads(opt_file.read_text(encoding="utf-8"))
            return web.json_response(data)
        return web.json_response({"error": "Optimizer calibrations not found"}, status=404)

    async def handle_memo(self, request):
        memo_md = OUTPUT_DIR / "CME_GOLD_DAILY_INTELLIGENCE_MEMO.md"
        memo_html = OUTPUT_DIR / "CME_GOLD_DAILY_INTELLIGENCE_MEMO.html"
        md_text = memo_md.read_text(encoding="utf-8") if memo_md.exists() else ""
        html_text = memo_html.read_text(encoding="utf-8") if memo_html.exists() else ""
        return web.json_response({
            "status": "AVAILABLE",
            "markdown": md_text,
            "html": html_text,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    async def handle_lead(self, request):
        try:
            data = await request.json()
            name = data.get("name", "Institutional Allocator")
            org = data.get("org", "Quantitative Trading Group")
            role = data.get("role", "Head of Quantitative Trading")
            email = data.get("email", "").strip()
            tier = data.get("tier", "tier_3")
            if not email:
                return web.json_response({"error": "Missing 'email' field."}, status=400)
            res = build_onboarding_package(name, org, role, email, tier)
            return web.json_response({
                "status": "PROVISIONED",
                "client_name": res["client_name"],
                "organization": res["org"],
                "tier": res["tier"]["name"],
                "contract_value_usd": res["tier"]["price_usd"],
                "api_key": res["api_key"],
                "access_token": res["access_token"],
                "onboarding_dossier": str(res["memo_path"]),
                "attachments_ready": len(res["attachments"])
            })
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def handle_ask(self, request):
        try:
            data = await request.json()
            query = data.get("query", "")
            if not query:
                return web.json_response({"error": "Missing 'query' field"}, status=400)
            answer = self.rag.answer_query(query)
            return web.json_response({"query": query, "answer": answer, "timestamp": datetime.now(timezone.utc).isoformat()})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def handle_query(self, request):
        try:
            data = await request.json()
            sql = data.get("query", "").strip()
            if not sql.lower().startswith("select"):
                return web.json_response({"error": "Only read-only SELECT queries are permitted."}, status=403)

            conn = sqlite3.connect(f"file:{MARKET_DB}?mode=ro", uri=True)
            cur = conn.cursor()
            cur.execute(sql)
            columns = [d[0] for d in cur.description] if cur.description else []
            rows = cur.fetchmany(100)
            conn.close()

            results = [dict(zip(columns, r)) for r in rows]
            return web.json_response({"row_count": len(results), "rows": results})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def handle_swagger_docs(self, request):
        html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>CME Gold Institutional API — Interactive OpenAPI Documentation</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.11.0/swagger-ui.min.css">
  <style>
    body { margin: 0; background: #070a11; font-family: sans-serif; }
    .swagger-ui .topbar { display: none; }
    .swagger-ui { filter: invert(88%) hue-rotate(180deg); }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.11.0/swagger-ui-bundle.min.js"></script>
  <script>
    window.onload = function() {
      SwaggerUIBundle({
        url: "/api/v1/openapi.json",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [SwaggerUIBundle.presets.apis],
        layout: "BaseLayout"
      });
    };
  </script>
</body>
</html>
"""
        return web.Response(text=html, content_type="text/html")

    async def handle_openapi_spec(self, request):
        spec = {
            "openapi": "3.0.3",
            "info": {
                "title": "CME Gold Futures Institutional Quantitative API",
                "version": "2.5.0-PROD",
                "description": "High-frequency microstructure data, real-time alpha decisions, Level-2 DOM ladder, and risk governance endpoints for CME COMEX Continuous Gold (`GC=F`) & Micro Gold (`MGC=F`).",
                "contact": {"name": "Institutional Quantitative Desk", "email": "bhaskarauthor@gmail.com"}
            },
            "servers": [{"url": "http://localhost:8085", "description": "Local Cluster Gateway"}],
            "paths": {
                "/api/v1/health": {
                    "get": {
                        "summary": "System Health Status",
                        "responses": {"200": {"description": "Server health status and active engines"}}
                    }
                },
                "/api/v1/signal": {
                    "get": {
                        "summary": "Live Microstructure Alpha Signal",
                        "responses": {"200": {"description": "Action, target price, dynamic stops, conviction"}}
                    }
                },
                "/api/v1/gis": {
                    "get": {
                        "summary": "CME Global Intelligence Score (GIS)",
                        "responses": {"200": {"description": "Unified scalar score in [-1.0, +1.0], tactical taxonomy, and factor breakdown"}}
                    }
                },
                "/api/v1/multiscale/hierarchy": {
                    "get": {
                        "summary": "Multi-Scale 7-Tier Catalog Hierarchy",
                        "responses": {"200": {"description": "Full catalog of 7 resolution tiers (Year, Month, Day, Hour, Minute, Second, Millisecond)"}}
                    }
                },
                "/api/v1/multiscale": {
                    "get": {
                        "summary": "Unified Multi-Scale Historical Market Data Query",
                        "parameters": [
                            {"name": "scale", "in": "query", "schema": {"type": "string", "enum": ["year", "month", "day", "hour", "minute", "second", "millisecond"]}},
                            {"name": "symbol", "in": "query", "schema": {"type": "string", "default": "GC=F"}},
                            {"name": "limit", "in": "query", "schema": {"type": "integer", "default": 100}}
                        ],
                        "responses": {"200": {"description": "Historical bars or microstructure snapshots with sub-millisecond retrieval latency"}}
                    }
                },
                "/api/v1/orderbook": {
                    "get": {
                        "summary": "Top-5 Level-2 Order Book (DOM)",
                        "responses": {"200": {"description": "Bid and Ask price ladder with queue depth"}}
                    }
                },
                "/api/v1/pnl": {
                    "get": {
                        "summary": "Live Paper Trading Blotter Status",
                        "responses": {"200": {"description": "Total equity, net PnL, win rate, closed executions"}}
                    }
                },
                "/api/v1/vpin": {
                    "get": {
                        "summary": "VPIN Toxicity & Hawkes Status",
                        "responses": {"200": {"description": "Volume-synchronized toxicity and quote pull boundary"}}
                    }
                },
                "/api/v1/basis": {
                    "get": {
                        "summary": "Metals Cointegration & Basis Parity",
                        "responses": {"200": {"description": "Standard vs Micro Gold basis and OU half-life"}}
                    }
                },
                "/api/v1/risk": {
                    "get": {
                        "summary": "Institutional Risk & Crisis Stress Tests",
                        "responses": {"200": {"description": "99% VaR, CVaR, and Lehman/Covid margin coverage"}}
                    }
                },
                "/api/v1/models/scaling": {
                    "get": {
                        "summary": "Deep Learning Parameter Scaling Matrix",
                        "responses": {"200": {"description": "Transformer parameter tiers (0.8M to 300M+ params)"}}
                    }
                },
                "/api/v1/optimizer": {
                    "get": {
                        "summary": "Bayesian Walk-Forward Hyperparameter Calibrations",
                        "responses": {"200": {"description": "Optimal conviction, VPIN barrier, and regime-adaptive multipliers"}}
                    }
                },
                "/api/v1/memo": {
                    "get": {
                        "summary": "Daily Pre-Market Quantitative Intelligence Memo",
                        "responses": {"200": {"description": "Latest markdown and HTML executive intelligence briefing"}}
                    }
                },
                "/api/v1/lead": {
                    "post": {
                        "summary": "Client Onboarding & License Token Issuance",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "org": {"type": "string"},
                                            "email": {"type": "string"},
                                            "tier": {"type": "string", "enum": ["tier_1", "tier_2", "tier_3", "enterprise"]}
                                        },
                                        "required": ["name", "org", "email"]
                                    }
                                }
                            }
                        },
                        "responses": {"200": {"description": "Provisioned client credentials and package download links"}}
                    }
                },
                "/api/v1/ask": {
                    "post": {
                        "summary": "Natural Language QuantRAG Intelligence Query",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {"query": {"type": "string"}},
                                        "required": ["query"]
                                    }
                                }
                            }
                        },
                        "responses": {"200": {"description": "100% numerically grounded AI Quant response"}}
                    }
                }
            }
        }
        return web.json_response(spec)

    async def handle_web_cockpit(self, request):
        template_path = BASE_DIR / "templates" / "institutional_cockpit.html"
        if template_path.exists():
            html = template_path.read_text(encoding="utf-8")
            return web.Response(text=html, content_type="text/html")
        return web.Response(text="<h1>Institutional Cockpit Template Not Found</h1>", content_type="text/html")


def main():
    parser = argparse.ArgumentParser(description="CME Gold Institutional Quant API & WebSocket Server")
    default_port = int(os.getenv("PORT", 8085))
    parser.add_argument("--port", type=int, default=default_port, help="Port to listen on (default: 8085)")
    args = parser.parse_args()

    server = QuantAPIServer()
    print("=" * 75)
    print(f" 🚀 CME GOLD ASYNC REST API & WEBSOCKET GATEWAY STARTING ON PORT {args.port}")
    print(f"    Web Cockpit: http://localhost:{args.port}/")
    print(f"    WebSocket:   ws://localhost:{args.port}/ws/live")
    print(f"    REST Base:   http://localhost:{args.port}/api/v1/")
    print("=" * 75)
    web.run_app(server.app, host="0.0.0.0", port=args.port, print=None)


if __name__ == "__main__":
    main()
