# Model Monitoring & Automated Retraining

Detects data drift and performance decay on a deployed model using Evidently, generates HTML drift reports, and triggers retraining when thresholds are breached.

## Flow
```
reference data ──┐
                 ├─ monitor.py ─→ drift report (HTML) ─→ threshold breached? ─→ retrain.py ─→ new model + versioned artifact
production data ─┘
```

## Quickstart
```bash
pip install -r requirements.txt
python simulate.py      # creates reference + "drifted" production batches
python monitor.py       # writes reports/drift_report.html, exits 1 if drift
python monitor.py && echo "healthy" || python retrain.py
```
Schedule with cron: `0 6 * * * cd /path && python monitor.py || python retrain.py`

## Results
- Drift share threshold: 30% of features (tunable in `monitor.py`)
- _After running: paste screenshot of the Evidently report and note which features drifted._
