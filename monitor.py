"""Run Evidently drift detection; exit non-zero when drift exceeds threshold."""
import sys
from pathlib import Path

import pandas as pd
from evidently.metric_preset import DataDriftPreset
from evidently.report import Report

DRIFT_SHARE_THRESHOLD = 0.30

ref = pd.read_csv("data/reference.csv")
prod = pd.read_csv("data/production.csv")

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=ref, current_data=prod)

Path("reports").mkdir(exist_ok=True)
report.save_html("reports/drift_report.html")

result = report.as_dict()["metrics"][0]["result"]
share = result["share_of_drifted_columns"]
print(f"Drifted columns: {result['number_of_drifted_columns']} "
      f"({share:.0%}) — threshold {DRIFT_SHARE_THRESHOLD:.0%}")

if share >= DRIFT_SHARE_THRESHOLD:
    print("DRIFT DETECTED — retraining required")
    sys.exit(1)
print("No significant drift")
