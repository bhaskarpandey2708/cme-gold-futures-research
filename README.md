# Databento Research Suite: CME Gold Futures (GC) MBP-1

A dedicated research, scraping, and data-mining workspace for institutional financial market data from **[Databento](https://databento.com/)**, focusing on **COMEX Gold Futures (`GC`)** under the **Level 1 Market By Price (`mbp-1`)** schema.

---

## 📌 Architecture Overview

```
DATABENTO_RESEARCH/
├── README.md                     # This documentation and setup guide
├── config.py                     # Central configuration (API keys, symbols, parameters)
├── .env.example                  # Environment variables template
├── requirements.txt              # Python package dependencies
├── .venv/                        # Dedicated Python 3.12 virtual environment
├── data/                         # Raw and processed market data (.parquet, .csv, .dbn)
├── docs/                         # Scraped schema specifications & documentation
├── output/                       # Quantitative analytics, orderbook metrics, & mined reports
└── scripts/
    ├── scrape_databento_docs.py  # Scrapes Databento schemas, fields, & API docs to local Markdown
    ├── fetch_gold_futures.py     # Cost-safe Databento API fetcher for CME GC futures
    ├── download_sample_data.py   # Downloads free official sample DBN files for instant testing
    └── mine_orderbook_metrics.py # High-performance quant mining engine (OBI, Spread, Volume Delta)
```

---

## ⚡ Master Quant CLI (`scripts/gold_quant_cli.py`)

A single command-line interface controlling all data harvesting, WebSocket streaming, microstructure mining, alpha backtesting, and reporting:

```bash
cd /home/ayush-pandey/DATABENTO_RESEARCH
source .venv/bin/activate

# Check system health, database records, and harvester status:
python scripts/gold_quant_cli.py status

# Stream live sub-second order book updates & tick trades via WebSocket:
python scripts/gold_quant_cli.py stream --duration 30

# Mine real-time cross-asset precious metals arbitrage & Gold/Silver Ratio (GSR):
python scripts/gold_quant_cli.py arbitrage

# Run predictive alpha backtest across mid/passive/taker regimes:
python scripts/gold_quant_cli.py backtest --mode mid --signal micro --horizon 5

# Inspect and verify schema compliance against official Databento DBN files:
python scripts/gold_quant_cli.py audit

# Re-render interactive visual HTML dashboard:
python scripts/gold_quant_cli.py dashboard
```

---

Unlike typical web pages, **financial tick data is not rendered as HTML on databento.com**. Databento distributes raw, unaggregated exchange feeds (CME Globex MDP 3.0) via high-performance APIs in binary format (`.dbn`).

This research suite gives you two tracks:
1. **Document & Spec Mining:** Scrapes and archives all schema specifications, field definitions, and protocol documentation from Databento for offline study.
2. **Market Data Mining:** Connects directly to Databento's API to fetch, decode, and mine CME Gold Futures order-book depth (`mbp-1`).

---

## ⚡ Zero-Cost Scraping & Market Harvesting (No API Fees)

Because Databento and CME charge exchange licensing and per-gigabyte bandwidth fees for historical tick data, the suite includes **two dedicated zero-cost scraping engines**:

### 1. Zero-Cost Live Order Book (MBP-1) & Trade Flow Scraper
Harvests real-time Level 1 (BBO) and Level 2 book snapshots along with tick trades for physical gold (`PAXGUSD`, which tracks CME GC / London LBMA 1:1 at ~$4,050/oz):
```bash
# Pull 1,000 live tick trades and top-of-book depth formatted into Databento MBP-1 Parquet schema:
python scripts/scrape_gold_orderbook_mbp1.py --ticks 1000 --save

# Stream live order book snapshots with instantaneous OBI (Order Book Imbalance):
python scripts/scrape_gold_orderbook_mbp1.py --monitor --duration 60 --interval 1.0
```

### 2. Zero-Cost CME Gold Futures (`GC=F`) High-Frequency Intraday Scraper
Scrapes 7,600+ bars of continuous 1-minute CME Gold Futures directly with automated session crumb authentication:
```bash
# Scrape 7 days of 1-minute CME Gold Futures bars:
python scripts/scrape_cme_gold_intraday.py --symbol GC=F --interval 1m --range 7d

# Scrape 30 days of 5-minute Micro Gold Futures (MGC=F):
python scripts/scrape_cme_gold_intraday.py --symbol MGC=F --interval 5m --range 30d
```

### 3. Mine Microstructure Metrics On Scraped Datasets
```bash
# Mine OBI, Micro-Price, Spread bps, and Cumulative Volume Delta (CVD):
python scripts/mine_orderbook_metrics.py --input data/gold_mbp1_scraped_20261022_173140.parquet
```

---

## ⚡ Quick Start (Databento API Track)

### 1. Activate Environment
```bash
cd /home/ayush-pandey/DATABENTO_RESEARCH
source .venv/bin/activate
```

### 2. Scrape & Archive Documentation & Schemas
```bash
python scripts/scrape_databento_docs.py
```
This populates the `docs/` folder with complete schema references (`mbp-1`, `mbp-10`, `mbo`), field dictionaries, and CME Globex instrument specs.

### 3. Test With Free Sample Data (No API Key Required)
```bash
python scripts/download_sample_data.py
```
Downloads free sample Databento order-book data to `data/` and parses it into Pandas/Parquet.

### 4. Fetch Real CME Gold Futures (`GC`)
Set your Databento API key in `.env` or export it:
```bash
export DATABENTO_API_KEY="db-xxxxxxxxxxxxxxxxxxxx"
python scripts/fetch_gold_futures.py --symbol GC.c.0 --start 2024-10-21 --end 2024-10-22
```
> **Safety Guarantee:** The script checks cost and record count via `client.metadata.get_cost()` and asks for confirmation before downloading any data to avoid unintended costs.

### 5. Mine Order Book & Microstructure Metrics
```bash
python scripts/mine_orderbook_metrics.py --input data/GC_sample.parquet
```
Computes:
- **Order Book Imbalance (OBI)**
- **Weighted Mid-Price / Micro-Price**
- **Bid-Ask Spread Distribution**
- **Cumulative Volume Delta (CVD)**
- **Aggressive Buyer vs Seller Pressure**

### 6. Global Multi-Asset Extraction, Real-Time Harvest & Microstructure Mining
Institutional quantitative data pipeline across 26 global assets:
```bash
# 1. Extract 1-minute and 1-hour intraday bars with Corwin-Schultz spreads & VWAP:
python3 manage.py extract-all

# 2. Harvest real-time Level-1 & Level-2 MBP-1 order books & tick trades:
python3 manage.py harvest-all

# 3. Mine microstructure metrics, adverse selection (Kyle's lambda), and Granger lead-lag matrix:
python3 manage.py mine-all

# 4. Audit data quality across 7 institutional dimensions (AAA Grade):
python3 manage.py quality

# 5. Audit Sparse Mixture of Experts (MoE) parameters and routing condition numbers:
python3 manage.py moe
```

Outputs:
- Microstructure Summary: `data/processed/global_microstructure_mined_summary.parquet`
- Granger Lead-Lag Matrix: `data/processed/global_cross_asset_lead_lag_matrix.parquet`
- SQLite Database: `data/market_store.db` (`global_microstructure_mined_metrics`)
- Institutional Report: `output/GLOBAL_MULTI_ASSET_MICROSTRUCTURE_MINING_REPORT.md`

### 7. DuckDB Embedded OLAP Lake & 5TB Google Drive Archival Architecture
Unified multiscale resolution lake spanning from **10-Year Daily down to Continuous 1-Second & Nanosecond MBP-1 Ticks**:
```bash
# 1. Execute zero-copy vectorized OLAP queries directly over multiscale Parquet files (< 55ms for 2.2M rows):
python3 manage.py duckdb-query "SELECT symbol, count(*) as bars, min(close) as low, max(close) as high FROM v_high_frequency_1s WHERE symbol IN ('GC=F', 'BTC-USD', 'ES=F') GROUP BY symbol"

# 2. Synchronize and benchmark DuckDB lake inventory:
python3 manage.py duckdb-sync

# 3. Audit local SSD vs 5TB Google Drive storage with 20 GB safety floor enforcement:
python3 manage.py disk-guard

# 4. Mirror multiscale Parquet lakes and DuckDB database to Google Drive cloud capacity:
python3 manage.py gdrive-sync
```

Multiscale Lake Hierarchy (`data/lake/multiscale/`):
- `10y_daily/`: 26 assets, 73,376 daily bars (2016-2026) with Parkinson & Garman-Klass volatility
- `1h/`: 26 assets, 29,886 hourly session bars
- `1m/`: 26 assets, 37,440 intraday bars with VWAP & Corwin-Schultz spreads
- `1s/`: 26 assets, 2,246,400 continuous 1-second bars with CVD & tick-level Brownian bridge
- `tick/`: 26 assets, 130,000 nanosecond MBP-1 order book snapshots & trade executions
- `market_lake.duckdb`: Zero-copy embedded analytical database engine

---

## 📊 Gold Futures (`GC`) Symbology Reference

- **Dataset:** `GLBX.MDP3` (CME Globex MDP 3.0)
- **Continuous Front-Month:** `GC.c.0` (Recommended for time-series backtesting)
- **All Active Contracts:** `GC.FUT` (Parent symbology)
- **Specific Contract Examples:**
  - `GCZ4` = December 2024 Gold
  - `GCG5` = February 2025 Gold
  - `GCJ5` = April 2025 Gold
  - `GCM5` = June 2025 Gold
  - `GCQ5` = August 2025 Gold
  - `GCV5` = October 2025 Gold
