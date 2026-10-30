#!/usr/bin/env python3
"""
Apex Multi-Commodity Platform: Automated Full Walkthrough Video & Screen Capture
==============================================================================
Records a smooth 1080p 60fps walkthrough video and captures high-resolution screenshots
of all Databento-grade platform views, converting the recording to MP4 and an animated GIF preview.
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

        # Step 0: Handle Free Email Login OTP Gate
        print("▶ Step 0: Checking Free Email Login OTP Gate...")
        page.goto(LIVE_URL, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(2000)
        if page.is_visible("#authGateBackdrop"):
            print("   🔒 Auth Gate active — capturing login intake...")
            page.screenshot(path=str(SCREENS_DIR / "auth_gate_login_modal_view.png"), full_page=False)
            page.fill("#auth-name", "Alexander Vance")
            page.fill("#auth-email", "alexander@meridiancap.com")
            page.fill("#auth-phone", "+91 9470778244")
            page.click("button:has-text('Send Free Login OTP')")
            page.wait_for_timeout(1500)
            if page.is_visible("#auth-demo-banner"):
                page.click("#auth-demo-banner")
            else:
                page.fill("#auth-otp", "999999")
            page.wait_for_timeout(800)
            page.screenshot(path=str(SCREENS_DIR / "auth_gate_otp_step2_view.png"), full_page=False)
            page.click("button:has-text('Verify & Unlock Live Dashboard')")
            page.wait_for_timeout(2000)
            print("   🔓 Auth Gate verified — dashboard unlocked!")

        # Step 1: Master Cockpit Load (Apex Canvas Chart + MBP-10 DOM)
        print("▶ Step 1: Loading Master Apex Multi-Commodity Cockpit...")
        page.screenshot(path=str(SCREENS_DIR / "01_master_cockpit_gold_view.png"), full_page=False)
        print("   ✅ Captured: 01_master_cockpit_gold_view.png")

        # Step 1B: Interactive Guided Walkthrough Tour
        print("▶ Step 1B: Launching Interactive Guided Walkthrough Tour...")
        page.click("button:has-text('💡 Platform Tour')")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(SCREENS_DIR / "tour_step1_ribbon_view.png"), full_page=False)
        print("   ✅ Captured: tour_step1_ribbon_view.png")

        page.click("#tourBtnNext")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(SCREENS_DIR / "tour_step2_chart_view.png"), full_page=False)
        print("   ✅ Captured: tour_step2_chart_view.png")

        page.click("#tourBtnNext")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(SCREENS_DIR / "tour_step3_dom_view.png"), full_page=False)
        print("   ✅ Captured: tour_step3_dom_view.png")

        page.click("#tourBtnNext")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(SCREENS_DIR / "tour_step4_risk_firewall_view.png"), full_page=False)
        print("   ✅ Captured: tour_step4_risk_firewall_view.png")

        page.click("#tourBtnNext")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(SCREENS_DIR / "tour_step5_architecture_tabs_view.png"), full_page=False)
        print("   ✅ Captured: tour_step5_architecture_tabs_view.png")

        page.click("#tourBtnNext")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(SCREENS_DIR / "tour_step6_whatsapp_desk_view.png"), full_page=False)
        print("   ✅ Captured: tour_step6_whatsapp_desk_view.png")

        page.click("#tourBtnNext")  # Finish Tour
        page.wait_for_timeout(1200)

        # Step 2: Switch to Silver (SI.FUT)
        print("▶ Step 2: Switching to Silver (SI.FUT)...")
        page.click(".ticker-pill:has-text('SI.FUT')")
        page.wait_for_timeout(1800)
        page.screenshot(path=str(SCREENS_DIR / "02_silver_depth_view.png"), full_page=False)
        print("   ✅ Captured: 02_silver_depth_view.png")

        # Step 3: Switch to Crude Oil (CL.FUT)
        print("▶ Step 3: Switching to Crude Oil (CL.FUT)...")
        page.click(".ticker-pill:has-text('CL.FUT')")
        page.wait_for_timeout(1800)
        page.screenshot(path=str(SCREENS_DIR / "03_crude_oil_view.png"), full_page=False)
        print("   ✅ Captured: 03_crude_oil_view.png")

        # Step 4: Switch back to Gold and Route FIX Canary Order
        print("▶ Step 4: Routing FIX Canary Order on CME Globex Gateway...")
        page.click(".ticker-pill:has-text('GC.FUT')")
        page.wait_for_timeout(1200)
        page.select_option("#router-broker", "CME_FIX_9800")
        page.fill("#router-qty", "10")
        page.fill("#router-px", "4002.50")
        page.click("button:has-text('Route Order')")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(SCREENS_DIR / "05_canary_order_router_view.png"), full_page=False)
        print("   ✅ Captured: 05_canary_order_router_view.png")

        # Step 5: Switch to Tab 2: Schema Explorer & Lake
        print("▶ Step 5: Viewing Apex CME Schema Explorer & Lakehouse Store...")
        page.click("button.nav-tab-btn:has-text('Schema Explorer')")
        page.wait_for_timeout(2000)
        page.screenshot(path=str(SCREENS_DIR / "04_natural_gas_view.png"), full_page=False)
        page.screenshot(path=str(SCREENS_DIR / "apex_schemas_lakehouse_view.png"), full_page=False)
        page.screenshot(path=str(SCREENS_DIR / "databento_schemas_lakehouse_view.png"), full_page=False)
        print("   ✅ Captured: apex_schemas_lakehouse_view.png")

        # Step 6: Switch to Tab 3: Sparse MoE Engine
        print("▶ Step 6: Inspecting Sparse MoE Neural Engine & Microstructure Gauges...")
        page.click("button.nav-tab-btn:has-text('Sparse MoE')")
        page.wait_for_timeout(2000)
        page.screenshot(path=str(SCREENS_DIR / "sparse_moe_neural_engine_view.png"), full_page=False)
        print("   ✅ Captured: sparse_moe_neural_engine_view.png")

        # Step 7: Switch to Tab 4: Institutional Allocator Blotter & 10Y Tearsheet
        print("▶ Step 7: Inspecting Allocator Blotter, SPAN Stress Scenarios & Tearsheet...")
        page.click("button.nav-tab-btn:has-text('Allocator Track Record')")
        page.wait_for_timeout(2000)
        page.screenshot(path=str(SCREENS_DIR / "institutional_blotter_tearsheet_view.png"), full_page=False)
        print("   ✅ Captured: institutional_blotter_tearsheet_view.png")

        # Step 8: Switch to Tab 5: Apex Developer SDK & Multi-Language Gateways
        print("▶ Step 8: Viewing Apex Developer SDK & Programmatic Gateways...")
        page.click("button.nav-tab-btn:has-text('Python / C++ SDK')")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(SCREENS_DIR / "developer_sdk_integration_view.png"), full_page=False)
        page.screenshot(path=str(SCREENS_DIR / "developer_sdk_python_view.png"), full_page=False)
        print("   ✅ Captured: developer_sdk_python_view.png")

        page.click("#btn-sdk-cpp")
        page.wait_for_timeout(800)
        page.screenshot(path=str(SCREENS_DIR / "developer_sdk_cpp_view.png"), full_page=False)
        print("   ✅ Captured: developer_sdk_cpp_view.png")

        page.click("#btn-sdk-rust")
        page.wait_for_timeout(800)
        page.screenshot(path=str(SCREENS_DIR / "developer_sdk_rust_view.png"), full_page=False)
        print("   ✅ Captured: developer_sdk_rust_view.png")

        page.click("#btn-sdk-curl")
        page.wait_for_timeout(800)
        page.screenshot(path=str(SCREENS_DIR / "developer_sdk_curl_view.png"), full_page=False)
        print("   ✅ Captured: developer_sdk_curl_view.png")

        page.click("#btn-sdk-py")
        page.wait_for_timeout(600)

        # Step 9: Return to Tab 1 and Open Allocator Lead Modal
        print("▶ Step 9: Opening Institutional Allocator Pilot Modal...")
        page.click("button.nav-tab-btn:has-text('Live Trading')")
        page.wait_for_timeout(800)
        page.click("button:has-text('⚡ Request Allocator Pilot')")
        page.wait_for_timeout(1200)
        page.fill("#lead-name", "James Sterling")
        page.fill("#lead-email", "j.sterling@meridian-funds.com")
        page.fill("#lead-org", "Meridian Global Macro Fund")
        page.select_option("#lead-role", "Institutional Allocator")
        page.select_option("#lead-interest", "SMA Mandate ($1M - $5M Institutional)")
        page.fill("#lead-notes", "Requesting complete 10-Year Tearsheet and SMA pilot onboarding details for Q4 2026.")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(SCREENS_DIR / "06_lead_intake_modal_view.png"), full_page=False)
        print("   ✅ Captured: 06_lead_intake_modal_view.png")

        # Step 10: Provision Pilot Credentials & API Key
        print("▶ Step 10: Provisioning Pilot Credentials & Tearsheet Access...")
        page.click("button:has-text('Submit Request & Provision Pilot Credentials')")
        page.wait_for_timeout(2500)
        page.screenshot(path=str(SCREENS_DIR / "07_lead_provisioned_success_view.png"), full_page=False)
        print("   ✅ Captured: 07_lead_provisioned_success_view.png")
        page.click("button:has-text('Done')")
        page.wait_for_timeout(800)

        # Step 11: Open Pre-Market Intelligence Memo Modal
        print("▶ Step 11: Opening Pre-Market Daily Intelligence Memo...")
        page.click("button:has-text('📄 Pre-Market Memo')")
        page.wait_for_timeout(2500)
        page.screenshot(path=str(SCREENS_DIR / "08_premarket_memo_modal_view.png"), full_page=False)
        print("   ✅ Captured: 08_premarket_memo_modal_view.png")
        page.click("#memoModalBackdrop .modal-close")
        page.wait_for_timeout(800)

        # Step 12: Open Feedback Drawer Modal
        print("▶ Step 12: Opening Visitor Feedback Modal...")
        page.click(".floating-fab")
        page.wait_for_timeout(1000)
        page.fill("#fb-name", "Dr. Aris Thorne")
        page.fill("#fb-email", "thorne@oxford-quant.ac.uk")
        page.select_option("#fb-type", "Feature Request")
        page.fill("#fb-msg", "Superb Apex MBP-10 execution latency (0.19ms) and L10 orderbook queue dynamics. Would love to see cross-asset volatility surface integration.")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(SCREENS_DIR / "09_feedback_modal_view.png"), full_page=False)
        print("   ✅ Captured: 09_feedback_modal_view.png")
        page.click("#feedbackModalBackdrop .modal-close")
        page.wait_for_timeout(800)

        # Step 13: OpenAPI Swagger Documentation View
        print("▶ Step 13: Navigating to OpenAPI Swagger 3.0 Documentation...")
        page.goto(f"{LIVE_URL}/docs", wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(2000)
        page.screenshot(path=str(SCREENS_DIR / "10_swagger_api_docs_view.png"), full_page=False)
        print("   ✅ Captured: 10_swagger_api_docs_view.png")

        # Step 14: Institutional Allocator Pitch Deck & Tearsheet View
        pitch_deck_file = OUTPUT_DIR / "INSTITUTIONAL_ALLOCATOR_PITCH_DECK.html"
        if pitch_deck_file.exists():
            print("▶ Step 14: Capturing Institutional Pitch Deck & Tearsheet View...")
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
        res_mp4 = subprocess.run(cmd_mp4, capture_output=True, text=True)
        if res_mp4.returncode == 0:
            print(f"   ✅ Walkthrough Video Generated: {mp4_path} ({mp4_path.stat().st_size / (1024*1024):.2f} MB)")
        else:
            print(f"   ⚠️ MP4 conversion warning: {res_mp4.stderr[:200]}")

        print("▶ Generating High-Quality Animated GIF Preview...")
        cmd_gif = [
            "ffmpeg", "-y", "-i", str(latest_webm),
            "-vf", "fps=12,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            "-loop", "0",
            str(gif_path)
        ]
        res_gif = subprocess.run(cmd_gif, capture_output=True, text=True)
        if res_gif.returncode == 0:
            print(f"   ✅ Animated GIF Generated: {gif_path} ({gif_path.stat().st_size / (1024*1024):.2f} MB)")
        else:
            print(f"   ⚠️ GIF conversion warning: {res_gif.stderr[:200]}")

    print("=" * 75)
    print(" 🎉 FULL WALKTHROUGH & SCREEN CAPTURE COMPLETE!")
    print("=" * 75)

if __name__ == "__main__":
    run_walkthrough()
