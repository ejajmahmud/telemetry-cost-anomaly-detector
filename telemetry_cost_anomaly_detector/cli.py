"""CLI for Telemetry Cost Anomaly Detector."""
import argparse
import json
from .core import CostAnomalyDetector


def main():
    parser = argparse.ArgumentParser(description="Telemetry Cost Anomaly Detector CLI")
    parser.add_argument("--probe", type=float, default=500.0, help="Candidate token cost to test")
    args = parser.parse_args()

    det = CostAnomalyDetector()
    for v in (100, 102, 99, 104, 97, 101):
        det.observe(v)
    print(json.dumps(det.observe(args.probe), indent=2))


if __name__ == "__main__":
    main()
