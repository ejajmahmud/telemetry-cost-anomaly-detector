"""Tests for Telemetry Cost Anomaly Detector."""
import unittest
from telemetry_cost_anomaly_detector.core import CostAnomalyDetector


class TestCostAnomalyDetector(unittest.TestCase):
    def test_detects_spike_without_polluting_baseline(self):
        det = CostAnomalyDetector(window_size=10, z_threshold=3.0, min_samples=4)
        for v in (100.0, 102.0, 98.0, 101.0, 99.0):
            res = det.observe(v)
            self.assertFalse(res["anomaly"])
        spike = det.observe(450.0)
        self.assertTrue(spike["anomaly"])
        self.assertGreater(spike["z_score"], 3.0)
        normal_after = det.observe(100.5)
        self.assertFalse(normal_after["anomaly"])
