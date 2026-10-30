"""Configuration settings for Databento Gold Futures (GC) Research Suite."""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


DOCS_DIR = BASE_DIR / "docs"
SCRIPTS_DIR = BASE_DIR / "scripts"
OUTPUT_DIR = BASE_DIR / "output"

for folder in [DATA_DIR, DOCS_DIR, SCRIPTS_DIR, OUTPUT_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Databento Credentials
DATABENTO_API_KEY = os.getenv("DATABENTO_API_KEY", "")

# CME Globex Gold Futures Settings
DEFAULT_DATASET = "GLBX.MDP3"          # CME Globex MDP 3.0
DEFAULT_SYMBOL = "GC.c.0"              # Continuous front month Gold futures
DEFAULT_SCHEMA = "mbp-1"               # Market-By-Price Level 1 (BBO + Trades)
DEFAULT_STYPE_IN = "continuous"        # 'continuous' for GC.c.0, 'parent' for GC.FUT, 'raw_symbol' for GCZ4

# Target Documentation URLs for Scraping
DOCS_URLS = [
    "https://databento.com/docs/api-reference-historical",
    "https://databento.com/docs/schemas-and-data-formats",
    "https://databento.com/docs/schemas-and-data-formats/mbp-1",
    "https://databento.com/docs/schemas-and-data-formats/mbo",
    "https://databento.com/docs/standards-and-conventions/symbology",
    "https://databento.com/docs/datasets/glbx-mdp3",
]
