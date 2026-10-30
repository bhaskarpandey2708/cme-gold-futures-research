#!/usr/bin/env python3
"""
Apex Multi-Commodity Platform: Automated Full Walkthrough Video & Screen Capture
==============================================================================
Records a smooth 1080p 60fps walkthrough video and captures high-resolution screenshots
of all 10 platform views, converting the recording to MP4 and an animated GIF preview.
"""

import sys
import time
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
SCREENS_DIR = OUTPUT_DIR / "screens"
VIDEO_DIR = OUTPUT_DIR / "walkthrough_video"

SCREENS_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

LIVE_URL = "https://cme-multi-commodity-cockpit.onrender.com"

def run_walkthrough():
    print("=" * 75)
    print(" 🎬 APEX MULTI-COMMODITY PLATFORM: RECORDING HIGH-DEF WALKTHROUGH")
    print(f"    Target URL: {LIVE_URL}")
    print(f"    Screens Directory: {SCREENS_DIR}")
    print(f"    Video Directory:   {VIDEO_DIR}")
    print("=" * 75)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(VIDEO_DIR),
            record_video_size={"width": 1920, "height": 1080}
        )
        page = context.new_page()

        # Step 1: Master Cockpit Load
        print("▶ Step 1: Loading Master Multi-Commodity Cockpit...")
        page.goto(LIVE_URL, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2500)
        page.screenshot(path=str(SCREENS_DIR / "01_master_cockpit_gold_view.png"), full_page=False)
        print("   ✅ Captured: 01_master_cockpit_gold_view.png")

        # Step 2: Switch to Silver (SI)
        print("▶ Step 2: Switching to Silver (SI)...")
        page.click("text=SI (Silver)")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(SCREENS_DIR / "02_silver_depth_view.png"), full_page=False)
        print("   ✅ Captured: 02_silver_depth_view.png")

        # Step 3: Switch to Crude Oil (CL)
        print("▶ Step 3: Switching to Crude Oil (CL)...")
        page.click("text=CL (Crude WTI)")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(SCREENS_DIR / "03_crude_oil_view.png"), full_page=False)
        print("   ✅ Captured: 03_crude_oil_view.png")

        # Step 4: Switch to Natural Gas (NG)
        print("▶ Step 4: Switching to Natural Gas (NG)...")
        page.click("text=NG (NatGas)")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(SCREENS_DIR / "04_natural_gas_view.png"), full_page=False)
        print("   ✅ Captured: 04_natural_gas_view.png")

        # Step 5: Switch back to Gold and Route Canary Order
        print("▶ Step 5: Routing Canary Order on CME Globex FIX Gateway...")
        page.click("text=GC (Gold)")
        page.wait_for_timeout(1000)
        page.select_option("#broker-select", "CME_GLOBEX_FIX_9800")
        page.fill("#order-qty", "10")
        page.fill("#order-px", "4002.50")
        page.click("#btn-fire-order")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(SCREENS_DIR / "05_canary_order_router_view.png"), full_page=False)
        print("   ✅ Captured: 05_canary_order_router_view.png")

        # Step 6: Open Allocator Lead Modal and Fill Details
        print("▶ Step 6: Opening Institutional Allocator Intake Modal...")
        page.click("button:has-text('Request Pilot & Tearsheet')")
        page.wait_for_timeout(1000)
        page.fill("#lead-name", "James Sterling")
        page.fill("#lead-email", "j.sterling@meridian-funds.com")
        page.fill("#lead-org", "Meridian Global Macro Fund")
        page.select_option("#lead-role", "Institutional Allocator")
        page.select_option("#lead-interest", "SMA Mandate ($1M - $5M Institutional)")
        page.fill("#lead-notes", "Requesting complete 10-Year Tearsheet and SMA pilot onboarding details for Q4 2026.")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(SCREENS_DIR / "06_lead_intake_modal_view.png"), full_page=False)
        print("   ✅ Captured: 06_lead_intake_modal_view.png")

        # Step 7: Submit Lead Form and Capture Provisioned Credentials
        print("▶ Step 7: Provisioning Pilot Credentials & Tearsheet Access...")
        page.click("button:has-text('Submit Request & Provision Pilot Credentials')")
        page.wait_for_timeout(2000)
        page.screenshot(path=str(SCREENS_DIR / "07_lead_provisioned_success_view.png"), full_page=False)
        print("   ✅ Captured: 07_lead_provisioned_success_view.png")
        page.click("button:has-text('Done')")
        page.wait_for_timeout(800)

        # Step 8: Open Pre-Market Daily Intelligence Memo Modal
        print("▶ Step 8: Opening Pre-Market Daily Intelligence Memo...")
        page.click("button:has-text('Pre-Market Memo')")
        page.wait_for_timeout(2500)
        page.screenshot(path=str(SCREENS_DIR / "08_premarket_memo_modal_view.png"), full_page=False)
        print("   ✅ Captured: 08_premarket_memo_modal_view.png")
        page.click("#memoModalBackdrop .modal-close")
        page.wait_for_timeout(800)

        # Step 9: Open Feedback Modal
        print("▶ Step 9: Opening Visitor Feedback Modal...")
        page.click(".floating-fab")
        page.wait_for_timeout(1000)
        page.fill("#fb-name", "Dr. Aris Thorne")
        page.fill("#fb-email", "thorne@oxford-quant.ac.uk")
        page.select_option("#fb-type", "Feature Request")
        page.fill("#fb-msg", "Superb execution latency (0.19ms) and Level-2 DOM queue dynamics. Would love to see cross-asset volatility smile integration.")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(SCREENS_DIR / "09_feedback_modal_view.png"), full_page=False)
        print("   ✅ Captured: 09_feedback_modal_view.png")
        page.click("#feedbackModalBackdrop .modal-close")
        page.wait_for_timeout(800)

        # Step 10: OpenAPI Swagger Documentation View
        print("▶ Step 10: Navigating to OpenAPI Swagger 3.0 Documentation...")
        page.goto(f"{LIVE_URL}/docs", wait_until="networkidle", timeout=20000)
        page.wait_for_timeout(2000)
        page.screenshot(path=str(SCREENS_DIR / "10_swagger_api_docs_view.png"), full_page=False)
        print("   ✅ Captured: 10_swagger_api_docs_view.png")

        # Step 11: Institutional Allocator Pitch Deck & Tearsheet View
        pitch_deck_file = OUTPUT_DIR / "INSTITUTIONAL_ALLOCATOR_PITCH_DECK.html"
        if pitch_deck_file.exists():
            print("▶ Step 11: Capturing Institutional Pitch Deck & Tearsheet View...")
            page.goto(f"file://{pitch_deck_file.resolve()}", wait_until="load")
            page.wait_for_timeout(1500)
            page.screenshot(path=str(SCREENS_DIR / "11_allocator_pitch_deck_view.png"), full_page=False)
            print("   ✅ Captured: 11_allocator_pitch_deck_view.png")

        # Finalize Video Recording
        print("▶ Finalizing Video Recording...")
        context.close()
        browser.close()

    # Locate and Convert Video with FFmpeg
    raw_webms = list(VIDEO_DIR.glob("*.webm"))
    if raw_webms:
        latest_webm = sorted(raw_webms, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        mp4_path = VIDEO_DIR / "apex_cockpit_full_walkthrough.mp4"
        gif_path = VIDEO_DIR / "apex_cockpit_preview.gif"

        print(f"▶ Encoding MP4 from raw capture ({latest_webm.name})...")
        cmd_mp4 = [
            "ffmpeg", "-y", "-i", str(latest_webm),
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(mp4_path)
        ]
        subprocess.run(cmd_mp4, check=True)
        print(f"   🎉 MP4 Video Generated: {mp4_path} ({mp4_path.stat().st_size / 1024:.1f} KB)")

        print("▶ Generating High-Quality Animated GIF Preview...")
        cmd_gif = [
            "ffmpeg", "-y", "-i", str(mp4_path),
            "-vf", "fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            "-loop", "0",
            str(gif_path)
        ]
        subprocess.run(cmd_gif, check=True)
        print(f"   🎉 Animated GIF Generated: {gif_path} ({gif_path.stat().st_size / 1024:.1f} KB)")

    print("=" * 75)
    print(" ✅ ALL SCREENSHOTS, HIGH-DEF MP4 VIDEO, AND GIF GENERATED SUCCESSFULLY!")
    print("=" * 75)

if __name__ == "__main__":
    run_walkthrough()
