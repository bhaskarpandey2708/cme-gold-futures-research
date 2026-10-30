# 🛠️ CME Gold Quantitative Platform: DevOps & Deployment Guide
## Production Engineering, Automated Testing & Infrastructure Orchestration
**Documentation Standard:** Tier-1 Systematic Trading Desk Standard  
**Target Asset:** CME COMEX Continuous Gold (`GC=F`) & Micro Gold (`MGC=F`)  
**CLI Tooling:** `manage.py`, `pytest`, `docker compose`, `systemd`  

---

## 🎯 1. Overview: Production Architecture & Directory Layout

The platform enforces a strict separation between low-latency execution microservices, distributed analytical macroservices, configuration management, and automated test suites:

```text
DATABENTO_RESEARCH/
├── manage.py                          # Unified master DevOps CLI
├── Makefile                           # Developer automation targets
├── requirements.txt                   # Production dependencies (UV fast install)
├── docker-compose.yml                 # Multi-container microservices cluster
├── .env.example                       # Environment secrets template
├── .gitignore                         # Zero-leak git tracking rules
│
├── config/
│   └── settings.json                  # Centralized system, risk & fee parameters
│
├── tests/                             # Automated Test Suite (100% Passing)
│   ├── test_api_endpoints.py          # Asynchronous REST & WebSocket verification
│   ├── test_fix_gateway.py            # FIX 4.4 / iLink 3 SOH & checksum verification
│   ├── test_microstructure_engines.py # Avellaneda-Stoikov, Hawkes & Regime matrix
│   └── test_risk_engine.py            # 99% VaR, CVaR & SPAN margin stress tests
│
├── deploy/
│   ├── install_systemd.sh             # One-command Linux bare-metal installer
│   └── systemd/                       # Production Linux service unit files
│       ├── cme-harvester.service
│       ├── cme-decision-daemon.service
│       ├── cme-api-gateway.service
│       └── cme-fix-gateway.service
│
├── docker/
│   ├── Dockerfile.microservice        # Minimal sub-millisecond execution container
│   └── Dockerfile.macroservice        # Analytical container with PyTorch & models
│
├── .github/workflows/
│   ├── quant_pipeline_ci.yml          # GitHub Actions CI/CD pipeline
│   └── model_benchmark.yml            # Weekly automated model latency & pinball benchmark
│
├── scripts/                           # Core quantitative & execution engines
├── models/                            # Model weights (.pt, .pkl) and parameter registries
├── data/                              # SQLite databases, 10Y lake & harvested partitions
├── logs/                              # Real-time execution logs & JSONL streams
├── output/                            # HTML terminals, DOM dashboards & PDF/MD reports
└── docs/                              # Institutional whitepapers & specifications
```

---

## 🧪 2. Unified Master DevOps CLI (`manage.py`)

All engineering operations can be performed using the native, zero-dependency master CLI:

```bash
# 1. Run Complete Automated PyTest Suite (13 tests across all engines)
python3 manage.py test

# 2. Inspect Real-Time Quantitative Cockpit
python3 manage.py status

# 3. Verify Asynchronous REST & WebSocket Health
python3 manage.py health

# 4. Inspect Live Paper Trading Blotter & Realized PnL
python3 manage.py pnl

# 5. Inspect Top-5 Level-2 Order Book (DOM Ladder)
python3 manage.py orderbook

# 6. Execute FIX 4.4 Round-Trip Client Verification
python3 manage.py fix-test

# 7. Benchmark Scaled Foundation Transformer (0.8M to 300M+ params)
python3 manage.py benchmark

# 8. Clean Bytecode & PyTest Temporary Caches
python3 manage.py clean
```

---

## 🐳 3. Multi-Container Orchestration (`docker-compose.yml`)

The platform can be deployed as an isolated microservice mesh connected by a Redis IPC message bus:

```bash
# Spin up complete microservice mesh in detached mode
docker compose up -d

# Inspect running service health
docker compose ps

# Follow live execution daemon logs
docker compose logs -f micro-inference-engine

# Stop and gracefully terminate cluster
docker compose down
```

---

## 🐧 4. Bare-Metal Linux Service Deployment (`systemd`)

For dedicated high-frequency servers (e.g. AWS EC2 c6i, Equinix NY4 on-prem):

```bash
# Install and enable all 4 background systemd daemons
sudo bash deploy/install_systemd.sh

# Verify service statuses
sudo systemctl status cme-api-gateway.service
sudo systemctl status cme-decision-daemon.service
sudo systemctl status cme-fix-gateway.service
sudo systemctl status cme-harvester.service

# View live systemd journal logs
journalctl -u cme-decision-daemon.service -f
```

---

## 🔄 5. Continuous Integration / Continuous Deployment (CI/CD)

The GitHub Actions workflow ([`.github/workflows/quant_pipeline_ci.yml`](file:///home/ayush-pandey/DATABENTO_RESEARCH/.github/workflows/quant_pipeline_ci.yml)) automatically executes on every push and pull request:
1. **Linting & Code Quality:** Syntax validation with `ruff` and `black`.
2. **Automated Unit Testing:** Executes `pytest tests/ -v` covering FIX tags, risk metrics, and regime adaptation.
3. **Institutional Stress Checks:** Verifies that portfolio SPAN margin coverage ratio $> 1.0$ under Lehman 2008 and Covid 2020 shocks before merging.
4. **Docker Container Linting:** Verifies compose definitions via `docker compose config`.
