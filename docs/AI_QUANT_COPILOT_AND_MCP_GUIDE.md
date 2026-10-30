# 🤖 CME Gold AI Quant Copilot & Model Context Protocol (MCP) Server
## Institutional Guide for AI Agents, RAG Pipelines, and Telegram Integration

This guide documents how to integrate our 10-year microstructure data lake, SQLite master store, and 6 quantitative decision engines into:
1. **Interactive AI Quant Copilot** (Terminal CLI & Telegram Bot)
2. **QuantRAG Engine** (Hallucination-free numerical retrieval)
3. **Quant MCP Server** (Standard Model Context Protocol for Claude Desktop, Cursor, and Antigravity)

---

## 🛠️ 1. The CME Gold Quant MCP Server

The MCP server runs standard JSON-RPC 2.0 over `stdio`, allowing any modern LLM to call our quantitative engines autonomously.

### Available MCP Tools:
| Tool Name | Parameters | Institutional Output |
| :--- | :--- | :--- |
| `get_live_signal` | None | Real-time action (`BUY`/`SELL`/`HOLD`), entry target, stop-loss, take-profit, and Kelly contract sizing. |
| `get_order_flow_toxicity` | None | Rolling VPIN, Hawkes jump intensity, and automated circuit breaker defense status. |
| `get_basis_arbitrage` | None | CME Standard (`GC`) vs. Micro (`MGC`) Gold Basis, ADF cointegration, and Ornstein-Uhlenbeck mean-reversion half-life. |
| `get_blotter_pnl` | None | Live paper trading blotter account equity, cumulative realized PnL, win rate, and recent closed executions. |
| `get_risk_metrics` | None | 99% Value-at-Risk (VaR), Expected Shortfall (CVaR), and CME SPAN crisis stress coverage ratios. |
| `query_market_store` | `query: str` | Read-only SQL query against the 10-year SQLite master store (11 tables, 205M lake partition registry). |

### Integration with Claude Desktop (`claude_desktop_config.json`):
Add the following block to your Claude Desktop configuration:
```json
{
  "mcpServers": {
    "cme-gold-quant": {
      "command": "/home/ayush-pandey/DATABENTO_RESEARCH/.venv/bin/python3",
      "args": [
        "/home/ayush-pandey/DATABENTO_RESEARCH/scripts/quant_mcp_server.py"
      ]
    }
  }
}
```

---

## 📱 2. Interactive AI Quant Copilot (CLI & Telegram)

Traders and analysts can query their portfolio and market microstructure in plain English or via slash commands.

### Interactive CLI Session:
```bash
/home/ayush-pandey/DATABENTO_RESEARCH/.venv/bin/python3 /home/ayush-pandey/DATABENTO_RESEARCH/scripts/ai_quant_copilot.py --interactive
```

### Direct Script Query:
```bash
/home/ayush-pandey/DATABENTO_RESEARCH/.venv/bin/python3 /home/ayush-pandey/DATABENTO_RESEARCH/scripts/ai_quant_copilot.py --query "What is our current PnL and open position?"
```

### Supported Commands:
- `/signal` ➔ Real-time execution action, price, and dynamic stops.
- `/pnl`    ➔ Live blotter account equity, net PnL, and win rate.
- `/vpin`   ➔ Rolling order flow toxicity and quote cancellation shield.
- `/basis`  ➔ CME Gold Standard vs. Micro Basis arbitrage spread and OU half-life.
- `/risk`   ➔ 99% VaR, Expected Shortfall, and SPAN crisis stress coverage.
- `/status` ➔ Full production daemon health and lake partition activity.

### Telegram Bot Deployment:
Run the copilot in continuous Telegram polling mode:
```bash
/home/ayush-pandey/DATABENTO_RESEARCH/.venv/bin/python3 /home/ayush-pandey/DATABENTO_RESEARCH/scripts/ai_quant_copilot.py --telegram --token "YOUR_TELEGRAM_BOT_TOKEN"
```

---

## 🔍 3. QuantRAG: Grounded Numerical Retrieval Architecture

Standard LLMs suffer from severe mathematical hallucinations when discussing pricing and portfolio state. **QuantRAG** bridges this gap:

```
┌────────────────────────────────────────────────────────┐
│                   USER PROMPT / QUERY                  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                   QuantRAG RETRIEVER                   │
├───────────────────────────┬────────────────────────────┤
│ SQLite Lake (205M Events) │ Live Decisions Log (JSONL) │
│ Models Store (Parameters) │ Paper Blotter DB (Fills)   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│            VERIFIED DETERMINISTIC CONTEXT              │
│  (Exact prices, PnL, VaR, stops - 0% Hallucination)   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                   LLM REASONING CORE                   │
│           (Claude 3.5 Sonnet / GPT-4o / Llama-3)       │
└────────────────────────────────────────────────────────┘
```

The QuantRAG pipeline guarantees that every numerical figure returned to the user is grounded directly in our SQLite database, parquet lake, or live decision stream.
