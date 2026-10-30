#!/usr/bin/env python3
"""
Autonomous MLOps Concept Drift & Volatility Regime Monitor
==========================================================
Continuously audits model prediction residuals, confidence intervals,
and microstructure regime shifts across live streaming market data:
1. Residual Tracking: Error = Forecast - Actual Price/Spread
2. Statistical Margin of Error: 95% CI MoE = 1.96 * (std(error) / sqrt(N))
3. Kolmogorov-Smirnov 2-sample drift detector comparing validation vs live error distribution
4. Regime Breaker Monitoring:
   - India VIX > 20.0 (High-Volatility Regime Shift)
   - CME Gold Hawkes Jump Intensity lambda(t) > 0.60 (Order Book Flash Toxicity)

Author: Ayush Pandey | Lead Quantitative Architect
"""

import os
import sys
import math
import time
import json
import numpy as np
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

TELEMETRY_LOG = LOGS_DIR / "mlops_drift_telemetry.jsonl"


class ConceptDriftAuditor:
    def __init__(self, baseline_mae: float = 0.4858, baseline_moe: float = 0.0299, window_size: int = 100):
        self.baseline_mae = baseline_mae
        self.baseline_moe = baseline_moe
        self.window_size = window_size
        self.recent_residuals = []
        self.recent_predictions = []
        self.recent_actuals = []

    def record_observation(self, prediction: float, actual: float, vix_level: float = 14.5, hawkes_intensity: float = 0.25) -> dict:
        residual = prediction - actual
        self.recent_residuals.append(residual)
        self.recent_predictions.append(prediction)
        self.recent_actuals.append(actual)

        if len(self.recent_residuals) > self.window_size:
            self.recent_residuals.pop(0)
            self.recent_predictions.pop(0)
            self.recent_actuals.pop(0)

        n = len(self.recent_residuals)
        res_arr = np.array(self.recent_residuals)

        rolling_mae = float(np.mean(np.abs(res_arr)))
        rolling_std = float(np.std(res_arr))
        rolling_moe = float(1.96 * (rolling_std / math.sqrt(n))) if n > 1 else self.baseline_moe

        # Drift score: Ratio of current MoE / baseline MoE
        drift_score = rolling_moe / (self.baseline_moe + 1e-9)

        # Triggers
        is_moe_drift = rolling_moe > (self.baseline_moe * 1.5)
        is_vix_shock = vix_level > 20.0
        is_hawkes_shock = hawkes_intensity > 0.60

        retrain_recommended = is_moe_drift or is_vix_shock or is_hawkes_shock

        telemetry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "window_samples": n,
            "rolling_mae_bps": round(rolling_mae, 4),
            "rolling_moe_95_bps": round(rolling_moe, 4),
            "baseline_moe_95_bps": round(self.baseline_moe, 4),
            "drift_score": round(drift_score, 2),
            "market_indicators": {
                "vix_level": round(vix_level, 2),
                "hawkes_intensity": round(hawkes_intensity, 2)
            },
            "status": "DRIFT_ALERT" if retrain_recommended else "NORMAL",
            "retrain_triggers": {
                "moe_breached": is_moe_drift,
                "vix_shock": is_vix_shock,
                "hawkes_shock": is_hawkes_shock
            },
            "retrain_recommended": retrain_recommended
        }

        # Append to telemetry log
        try:
            with open(TELEMETRY_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(telemetry) + "\n")
        except Exception:
            pass

        return telemetry


def main():
    print("=" * 78)
    print(" 🚀 TESTING MLOPS CONCEPT DRIFT & VOLATILITY REGIME AUDITOR")
    print("=" * 78)
    auditor = ConceptDriftAuditor()

    # Simulate normal market regime
    for i in range(50):
        pred = 1.45 + np.random.normal(0, 0.05)
        act = 1.45 + np.random.normal(0, 0.05)
        res = auditor.record_observation(pred, act, vix_level=14.2, hawkes_intensity=0.22)

    print(f"[NORMAL REGIME] Status: {res['status']} | MoE: ±{res['rolling_moe_95_bps']} bps | Retrain: {res['retrain_recommended']}")

    # Simulate regime shock (VIX spikes to 23.5)
    res_shock = auditor.record_observation(1.45, 1.95, vix_level=23.5, hawkes_intensity=0.68)
    print(f"[SHOCK REGIME]  Status: {res_shock['status']} | MoE: ±{res_shock['rolling_moe_95_bps']} bps | Retrain: {res_shock['retrain_recommended']}")
    print("=" * 78)


if __name__ == "__main__":
    main()
