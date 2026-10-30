#!/usr/bin/env python3
"""
CME Gold Platform Master DevOps & Developer CLI (manage.py)
===========================================================
Unified automation CLI for testing, daemon monitoring, service management,
and institutional benchmarks without external dependencies.

Usage:
  python3 manage.py test        - Run complete pytest automated test suite
  python3 manage.py status      - Display real-time quantitative cockpit
  python3 manage.py health      - Check REST API health status
  python3 manage.py pnl         - Inspect live paper trading blotter
  python3 manage.py orderbook   - Query Top-5 Level-2 DOM ladder
  python3 manage.py fix-test    - Execute institutional FIX 4.4 round-trip
  python3 manage.py benchmark   - Run transformer parameter scaling benchmark
  python3 manage.py optimize    - Run Bayesian Walk-Forward Hyperparameter Optimizer
  python3 manage.py memo        - Generate daily pre-market intelligence dossier
  python3 manage.py dispatch    - Preview pre-market briefing dispatch package
  python3 manage.py tearsheet   - Generate institutional risk & performance tearsheet
  python3 manage.py clean       - Remove cached pyc, pytest, and temporary files
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
_venv_python = BASE_DIR / ".venv" / "bin" / "python3"
PYTHON = _venv_python if _venv_python.exists() else Path(sys.executable)
_venv_pytest = BASE_DIR / ".venv" / "bin" / "pytest"
PYTEST = _venv_pytest if _venv_pytest.exists() else Path("pytest")


def run_test():
    print("🧪 Running complete institutional test suite...")
    cmd = [str(PYTEST), str(BASE_DIR / "tests"), "-v"]
    res = subprocess.run(cmd)
    sys.exit(res.returncode)


def run_status():
    cmd = ["bash", str(BASE_DIR / "scripts" / "daemon_status.sh")]
    subprocess.run(cmd)


def run_health():
    import urllib.request
    import json
    try:
        req = urllib.request.urlopen("http://localhost:8085/api/v1/health", timeout=3)
        data = json.loads(req.read().decode())
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"[!] Health check failed: {e}")


def run_pnl():
    import urllib.request
    import json
    try:
        req = urllib.request.urlopen("http://localhost:8085/api/v1/pnl", timeout=3)
        data = json.loads(req.read().decode())
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"[!] PnL check failed: {e}")


def run_orderbook():
    import urllib.request
    import json
    try:
        req = urllib.request.urlopen("http://localhost:8085/api/v1/orderbook", timeout=3)
        data = json.loads(req.read().decode())
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"[!] Orderbook check failed: {e}")


def run_fix_test():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "fix_protocol_gateway.py"), "--test-client"]
    subprocess.run(cmd)


def run_benchmark():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "train_scaled_foundation_transformer.py")]
    subprocess.run(cmd)


def run_optimize():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "bayesian_walk_forward_optimizer.py")]
    subprocess.run(cmd)


def run_memo():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "generate_daily_market_memo.py")]
    subprocess.run(cmd)


def run_dispatch():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "dispatch_premarket_briefing.py"), "--preview"]
    subprocess.run(cmd)


def run_tearsheet():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "generate_institutional_risk_tearsheet.py")]
    subprocess.run(cmd)


def run_board():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "jira_sprint_tracker.py"), "board"]
    subprocess.run(cmd)


def run_multiscale():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "multiscale_data_engine.py")]
    subprocess.run(cmd)


def run_clean():
    print("🧹 Cleaning up pycache and test temporary directories...")
    for root, dirs, files in os.walk(BASE_DIR):
        for d in list(dirs):
            if d in ("__pycache__", ".pytest_cache"):
                p = Path(root) / d
                import shutil
                shutil.rmtree(p, ignore_errors=True)
                dirs.remove(d)
    print("✅ Clean complete!")


def run_quality():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "quality" / "data_quality_auditor.py")]
    subprocess.run(cmd)


def run_moe():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "moe" / "audit_moe_parameters.py")]
    subprocess.run(cmd)


def run_ingest_global():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "data_pipelines" / "ingest_global_multi_asset_lake.py")]
    subprocess.run(cmd)


def run_extract_all():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "data_pipelines" / "extract_global_intraday_bars.py")]
    subprocess.run(cmd)


def run_harvest_all():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "data_pipelines" / "harvest_global_multi_asset.py"), "--once"]
    subprocess.run(cmd)


def run_mine_all():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "data_pipelines" / "mine_global_microstructure_metrics.py")]
    subprocess.run(cmd)


def run_macro_aladdin():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "data_pipelines" / "ingest_blackrock_bloomberg_macro_lake.py")]
    subprocess.run(cmd)


def run_duckdb_sync():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "lake" / "duckdb_analytical_engine.py")]
    subprocess.run(cmd)


def run_duckdb_query():
    sql = sys.argv[2] if len(sys.argv) > 2 else "SELECT * FROM v_daily_10y LIMIT 5"
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "lake" / "duckdb_analytical_engine.py"), "--query", sql]
    subprocess.run(cmd)


def run_disk_guard():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "storage" / "disk_space_guardian.py"), "--audit"]
    subprocess.run(cmd)


def run_stream_1year():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "pipeline" / "full_1year_multi_schema_pipeline.py")] + sys.argv[2:]
    subprocess.run(cmd)


def run_stream_1year_status():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "pipeline" / "full_1year_multi_schema_pipeline.py"), "--status"]
    subprocess.run(cmd)


def run_commodities_stream():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "pipeline" / "cme_all_commodities_1year_pipeline.py")] + sys.argv[2:]
    subprocess.run(cmd)


def run_commodities_status():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "pipeline" / "cme_all_commodities_1year_pipeline.py"), "--status"]
    subprocess.run(cmd)


def run_commodities_real_lake():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "pipeline" / "build_real_multicommodity_continuous_lake.py")] + sys.argv[2:]
    subprocess.run(cmd)


def run_commodities_harvest():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "pipeline" / "harvest_multicommodity_continuous.py")] + sys.argv[2:]
    subprocess.run(cmd)


def run_stream_mbp1():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "pipeline" / "download_in_parts_to_gdrive.py")] + sys.argv[2:]
    subprocess.run(cmd)


def run_mbp1_status():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "pipeline" / "download_in_parts_to_gdrive.py"), "--status"]
    subprocess.run(cmd)


def run_gdrive_sync():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "storage" / "disk_space_guardian.py"), "--sync-gdrive"]
    subprocess.run(cmd)


def run_start():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "start_parallel_daemons.py")]
    subprocess.run(cmd)


def run_stop():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "start_parallel_daemons.py"), "stop"]
    subprocess.run(cmd)


def run_push():
    from datetime import datetime, timezone
    msg = sys.argv[2] if len(sys.argv) > 2 else f"chore(sync): automated update [{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}]"
    print(f"[*] Staging and committing changes with message: '{msg}'...")
    subprocess.run(["git", "-C", str(BASE_DIR), "add", "."], check=True)
    res = subprocess.run(["git", "-C", str(BASE_DIR), "commit", "-m", msg], stdout=subprocess.PIPE, text=True)
    if "nothing to commit" in res.stdout:
        print("[✓] Nothing to commit — working tree clean.")
    else:
        print(f"[✓] Committed: {res.stdout.strip()[:100]}")
    print("[*] Pushing to GitHub remote (origin main)...")
    push_res = subprocess.run(["git", "-C", str(BASE_DIR), "push", "origin", "main"])
    if push_res.returncode == 0:
        print("✅ Successfully pushed to GitHub!")
    else:
        print(f"[!] Push completed with code {push_res.returncode}")


def run_train_colab():
    colab_parser = argparse.ArgumentParser(description="Run training on Google Colab T4 GPU")
    colab_parser.add_argument("--model", type=str, default="scaled_transformer", choices=["scaled_transformer", "gat", "tft"], help="Model to train")
    colab_parser.add_argument("--epochs", type=int, default=15, help="Number of epochs")
    colab_parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    colab_parser.add_argument("--session", type=str, default="cme-gold-t4", help="Colab session name")
    colab_parser.add_argument("--teardown", action="store_true", help="Teardown session after run")
    colab_args, _ = colab_parser.parse_known_args(sys.argv[2:])

    cmd = [
        str(PYTHON), str(BASE_DIR / "scripts" / "colab_gpu_orchestrator.py"),
        "--model", colab_args.model,
        "--epochs", str(colab_args.epochs),
        "--batch-size", str(colab_args.batch_size),
        "--session", colab_args.session,
        "--root", str(BASE_DIR)
    ]
    if colab_args.teardown:
        cmd.append("--teardown")
    subprocess.run(cmd)


def run_kaggle_push():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "kaggle_runner.py"), "--push"]
    subprocess.run(cmd)


def run_kaggle_status():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "kaggle_runner.py"), "--status"]
    subprocess.run(cmd)


def run_kaggle_output():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "kaggle_runner.py"), "--output"]
    subprocess.run(cmd)


def run_hf_push():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "hf_sync_models.py")] + sys.argv[2:]
    subprocess.run(cmd)


def run_cli():
    cmd = [str(PYTHON), str(BASE_DIR / "scripts" / "gold_quant_cli.py")] + sys.argv[2:]
    subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(description="CME Gold Master DevOps CLI")
    parser.add_argument("command", choices=[
        "test", "status", "health", "pnl", "orderbook", "fix-test",
        "benchmark", "optimize", "memo", "dispatch", "tearsheet", "board", "multiscale", "clean", "cli",
        "start", "stop", "quality", "moe", "ingest-global", "extract-all", "harvest-all", "mine-all",
        "macro-aladdin", "duckdb-sync", "duckdb-query", "disk-guard", "gdrive-sync", "push", "train-colab",
        "stream-mbp1", "mbp1-status", "stream-1year", "stream-1year-status",
        "commodities-stream", "commodities-status",
        "commodities-real-lake", "commodities-harvest",
        "kaggle-push", "kaggle-status", "kaggle-output", "hf-push"
    ])
    args, _ = parser.parse_known_args()

    commands = {
        "test": run_test,
        "status": run_status,
        "health": run_health,
        "pnl": run_pnl,
        "orderbook": run_orderbook,
        "fix-test": run_fix_test,
        "benchmark": run_benchmark,
        "optimize": run_optimize,
        "memo": run_memo,
        "dispatch": run_dispatch,
        "tearsheet": run_tearsheet,
        "board": run_board,
        "multiscale": run_multiscale,
        "clean": run_clean,
        "cli": run_cli,
        "start": run_start,
        "stop": run_stop,
        "quality": run_quality,
        "moe": run_moe,
        "ingest-global": run_ingest_global,
        "extract-all": run_extract_all,
        "harvest-all": run_harvest_all,
        "mine-all": run_mine_all,
        "macro-aladdin": run_macro_aladdin,
        "duckdb-sync": run_duckdb_sync,
        "duckdb-query": run_duckdb_query,
        "disk-guard": run_disk_guard,
        "gdrive-sync": run_gdrive_sync,
        "push": run_push,
        "train-colab": run_train_colab,
        "stream-mbp1": run_stream_mbp1,
        "mbp1-status": run_mbp1_status,
        "stream-1year": run_stream_1year,
        "stream-1year-status": run_stream_1year_status,
        "commodities-stream": run_commodities_stream,
        "commodities-status": run_commodities_status,
        "commodities-real-lake": run_commodities_real_lake,
        "commodities-harvest": run_commodities_harvest,
        "kaggle-push": run_kaggle_push,
        "kaggle-status": run_kaggle_status,
        "kaggle-output": run_kaggle_output,
        "hf-push": run_hf_push,
    }
    commands[args.command]()


if __name__ == "__main__":
    main()
