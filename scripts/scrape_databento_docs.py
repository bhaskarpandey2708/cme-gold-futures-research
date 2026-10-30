#!/usr/bin/env python3
"""
Databento Documentation & Schema Scraper
Scrapes and mines schema definitions, field dictionaries, and dataset specs from databento.com
and converts them into structured Markdown files for offline research.
"""

import os
import sys
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
from config import DOCS_DIR

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

PAGES_TO_SCRAPE = [
    {
        "name": "01_MBP1_SCHEMA_SPEC.md",
        "url": "https://databento.com/docs/schemas-and-data-formats/mbp-1",
        "topic": "Market by Price (MBP-1) Level 1 Specification",
    },
    {
        "name": "02_MBP10_SCHEMA_SPEC.md",
        "url": "https://databento.com/docs/schemas-and-data-formats/mbp-10",
        "topic": "Market by Price (MBP-10) Level 2 Specification",
    },
    {
        "name": "03_MBO_SCHEMA_SPEC.md",
        "url": "https://databento.com/docs/schemas-and-data-formats/mbo",
        "topic": "Market by Order (MBO) Tick-level Specification",
    },
    {
        "name": "04_TRADES_SCHEMA_SPEC.md",
        "url": "https://databento.com/docs/schemas-and-data-formats/trades",
        "topic": "Trades Schema Specification",
    },
    {
        "name": "05_CME_GLOBEX_MDP3_DATASET.md",
        "url": "https://databento.com/docs/datasets/glbx-mdp3",
        "topic": "CME Globex MDP 3.0 Dataset & Futures Coverage",
    },
    {
        "name": "06_SYMBOLOGY_STANDARDS.md",
        "url": "https://databento.com/docs/standards-and-conventions/symbology",
        "topic": "Databento Symbology Standards (Continuous, Parent, Raw)",
    },
    {
        "name": "07_HISTORICAL_API_REFERENCE.md",
        "url": "https://databento.com/docs/api-reference-historical",
        "topic": "Historical API Reference & Endpoints",
    },
]


def table_to_markdown(table):
    """Convert an HTML table into a clean GitHub Flavored Markdown table."""
    rows = table.find_all("tr")
    if not rows:
        return ""

    md_table = []
    headers = []
    
    # Process header
    th_cells = rows[0].find_all(["th", "td"])
    for th in th_cells:
        headers.append(th.get_text(separator=" ", strip=True).replace("\n", " "))
    
    if not headers:
        return ""
        
    md_table.append("| " + " | ".join(headers) + " |")
    md_table.append("| " + " | ".join(["---"] * len(headers)) + " |")

    # Process data rows
    for row in rows[1:]:
        td_cells = row.find_all("td")
        if not td_cells:
            continue
        row_vals = [td.get_text(separator=" ", strip=True).replace("\n", " ").replace("|", "\\|") for td in td_cells]
        # Pad or trim to match header length
        if len(row_vals) < len(headers):
            row_vals += [""] * (len(headers) - len(row_vals))
        elif len(row_vals) > len(headers):
            row_vals = row_vals[:len(headers)]
        md_table.append("| " + " | ".join(row_vals) + " |")

    return "\n".join(md_table) + "\n\n"


def parse_page_to_markdown(html_content, title, url):
    """Parse HTML content into structured Markdown text."""
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Extract main content container
    content = soup.find("main") or soup.find("article") or soup.find("div", {"id": "content"}) or soup.body
    if not content:
        return f"# {title}\n\nSource: {url}\n\nCould not extract main content."

    md_lines = [
        f"# {title}",
        f"\n> **Source:** [{url}]({url})",
        f"> **Archived For:** Financial Market Research & Algorithmic Trading Systems\n",
        "---\n",
    ]

    for element in content.descendants:
        if element.name in ["h1", "h2", "h3", "h4"]:
            level = int(element.name[1])
            text = element.get_text(strip=True)
            if text:
                md_lines.append(f"{'#' * level} {text}\n")
        elif element.name == "p":
            text = element.get_text(strip=True)
            if text and len(text) > 10:
                md_lines.append(f"{text}\n")
        elif element.name == "pre":
            code = element.get_text()
            md_lines.append(f"```python\n{code.strip()}\n```\n")
        elif element.name == "table":
            table_md = table_to_markdown(element)
            if table_md:
                md_lines.append(table_md)

    # Clean up excessive duplicate newlines
    cleaned = re.sub(r"\n{3,}", "\n\n", "\n".join(md_lines))
    return cleaned


def scrape_all():
    """Scrape and mine all specified Databento documentation pages."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"🚀 Starting Databento Documentation & Schema Mining...")
    print(f"📁 Destination Folder: {DOCS_DIR}\n")

    catalog = [
        "# Databento Research Knowledge Base",
        "\nThis directory contains mined schema references, field definitions, and protocol specifications from Databento.\n",
        "| Document | Topic | Source URL |",
        "| :--- | :--- | :--- |",
    ]

    for page in PAGES_TO_SCRAPE:
        print(f"⏳ Mining: {page['topic']} ({page['url']})...")
        try:
            resp = requests.get(page["url"], headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                md_content = parse_page_to_markdown(resp.text, page["topic"], page["url"])
                out_path = DOCS_DIR / page["name"]
                out_path.write_text(md_content, encoding="utf-8")
                print(f"   ✅ Saved: {out_path.name} ({len(md_content)} bytes)")
                catalog.append(f"| [{page['name']}](file://{out_path}) | {page['topic']} | [Link]({page['url']}) |")
            else:
                print(f"   ⚠️ Failed: HTTP {resp.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    # Write Catalog
    catalog_path = DOCS_DIR / "INDEX.md"
    catalog_path.write_text("\n".join(catalog), encoding="utf-8")
    print(f"\n🎉 Mining Complete! Index created at: {catalog_path}")


if __name__ == "__main__":
    scrape_all()
