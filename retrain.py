"""Retrain on the latest production batch and version the artifact."""
import time
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/production.csv")
X, y = df.drop(columns=["target"]), df["target"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = GradientBoostingClassifier().fit(X_tr, y_tr)
auc = roc_auc_score(y_te, model.predict_proba(X_te)[:, 1])

Path("models").mkdir(exist_ok=True)
version = time.strftime("%Y%m%d-%H%M%S")
path = f"models/model-{version}.joblib"
joblib.dump(model, path)
print(f"Retrained. ROC-AUC={auc:.4f} → {path}")
