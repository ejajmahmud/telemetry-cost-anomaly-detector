"""Core rolling z-score cost anomaly detector for autonomous agent workflows."""
import math
from collections import deque
from typing import Any, Deque, Dict


class CostAnomalyDetector:
    """Detects sudden token-spend spikes against a rolling workflow baseline."""

    def __init__(self, window_size: int = 20, z_threshold: float = 3.0, min_samples: int = 4):
        self.window_size = window_size
        self.z_threshold = z_threshold
        self.min_samples = min_samples
        self._window: Deque[float] = deque(maxlen=window_size)

    def observe(self, cost: float) -> Dict[str, Any]:
        n = len(self._window)
        anomaly = False
        z_score = 0.0
        mean = cost

        if n >= self.min_samples:
            mean = sum(self._window) / n
            variance = sum((x - mean) ** 2 for x in self._window) / n
            std = math.sqrt(variance)
            if std > 1e-9:
                z_score = (cost - mean) / std
                anomaly = z_score >= self.z_threshold
            elif cost > mean * 2.0:
                z_score = float("inf")
                anomaly = True

        if not anomaly:
            self._window.append(cost)

        return {
            "cost": cost,
            "baseline_mean": round(mean, 2),
            "z_score": round(z_score, 2) if z_score != float("inf") else 999.0,
            "anomaly": anomaly,
        }
