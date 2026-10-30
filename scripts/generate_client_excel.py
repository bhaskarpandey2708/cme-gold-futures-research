#!/usr/bin/env python3
"""
Generate Master Institutional Multi-Tab Excel Workbook for Client Delivery
==========================================================================
Builds 'CME_Gold_Futures_7Day_Client_Accuracy_Pack.xlsx' containing:
1. Cover & Executive Methodology Summary
2. Day-Level CME Settlements & Volatilities (7 Days)
3. 1-Hour Continuous Globex Bars (168 Hours)
4. 1-Minute Intraday Continuous Bars with VWAP (9,660 Minutes)
5. 1-Second Continuous Market Depth & Spread (High-Frequency Series)
6. Sub-Second MBP-1 Level 2 Order Book & Trades with 16 Alpha Features
"""

import os
import pandas as pd
from pathlib import Path
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SRC_DIR = Path("/home/ayush-pandey/DATABENTO_RESEARCH/CLIENT_DELIVERY_7DAYS")
OUT_XLSX = SRC_DIR / "CME_Gold_Futures_7Day_Client_Accuracy_Pack.xlsx"
GDRIVE_DIR = Path("/home/ayush-pandey/GoogleDrive/Databento_Gold_Futures_Research/CLIENT_DELIVERY_7DAYS")

print("[*] Loading CSV datasets for multi-sheet Excel generation...")
df_daily = pd.read_csv(SRC_DIR / "01_CME_Gold_Daily_Recent_7Days.csv")
df_1h = pd.read_csv(SRC_DIR / "02_CME_Gold_1Hour_Recent_7Days.csv")
df_1m = pd.read_csv(SRC_DIR / "03_CME_Gold_1Minute_Recent_7Days.csv")
df_1s = pd.read_csv(SRC_DIR / "04_CME_Gold_1Second_Recent_7Days.csv")
df_mbp1 = pd.read_csv(SRC_DIR / "05_CME_Gold_MBP1_OrderBook_and_Trades_Recent.csv")

# Create Summary Sheet
df_summary = pd.DataFrame([
    {"Temporal Tier": "Daily (Macro)", "Record Count": len(df_daily), "Resolution": "1 Day / Session", "Key Metrics": "CME Globex Settlement, High, Low, Parkinson, Garman-Klass, Rogers-Satchell Volatilities"},
    {"Temporal Tier": "1-Hour Continuous", "Record Count": len(df_1h), "Resolution": "60 Minutes (Unbroken)", "Key Metrics": "OHLCV, 24-hr Rolling Annualized Volatility, Rogers-Satchell Drift, Dollar Volume"},
    {"Temporal Tier": "1-Minute Intraday", "Record Count": len(df_1m), "Resolution": "60 Seconds", "Key Metrics": "OHLCV, Intraday Volume, VWAP (Volume-Weighted Average Price)"},
    {"Temporal Tier": "1-Second Continuous", "Record Count": len(df_1s), "Resolution": "1 Second", "Key Metrics": "High-Frequency OHLCV, CME Globex $0.10 Top-of-Book Spread Modeling, Bid/Ask Depth"},
    {"Temporal Tier": "MBP-1 Sub-Second L2", "Record Count": len(df_mbp1), "Resolution": "Tick-by-Tick Depth & Trades", "Key Metrics": "1:1 Databento MDP 3.0 Schema, OBI, Micro-Price, CVD, VPIN Flow Toxicity, Triple Barrier Labels"}
])

print(f"[*] Writing Excel workbook to {OUT_XLSX}...")
with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as writer:
    df_summary.to_excel(writer, sheet_name="Executive_Summary", index=False)
    df_daily.to_excel(writer, sheet_name="01_Daily_Settlements", index=False)
    df_1h.to_excel(writer, sheet_name="02_Hourly_Continuous", index=False)
    df_1m.to_excel(writer, sheet_name="03_1Minute_Continuous", index=False)
    # Write top 25,000 rows of 1-second for fast opening and responsiveness
    df_1s.iloc[:25000].to_excel(writer, sheet_name="04_1Second_Sample_25k", index=False)
    df_mbp1.to_excel(writer, sheet_name="05_MBP1_OrderBook_Trades", index=False)

    # Style header rows
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

    for sheetname in writer.sheets:
        ws = writer.sheets[sheetname]
        for col_idx in range(1, ws.max_column + 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
            # Auto width
            col_letter = get_column_letter(col_idx)
            max_len = max([len(str(ws.cell(row=r, column=col_idx).value or '')) for r in range(1, min(ws.max_row, 50) + 1)])
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

print(f"[✓] Successfully generated Excel workbook: {OUT_XLSX} ({OUT_XLSX.stat().st_size / (1024*1024):.2f} MB)")

# Copy to Google Drive
if GDRIVE_DIR.exists():
    import shutil
    gdrive_out = GDRIVE_DIR / OUT_XLSX.name
    shutil.copy2(OUT_XLSX, gdrive_out)
    shutil.copy2(OUT_XLSX, Path("/home/ayush-pandey/GoogleDrive/Databento_Gold_Futures_Research/SHARE_PACKAGE") / OUT_XLSX.name)
    print(f"[✓] Mirrored Excel workbook to Google Drive: {gdrive_out}")
