"""Create a reference batch and a drifted production batch for the demo."""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
Path("data").mkdir(exist_ok=True)

n = 2000
ref = pd.DataFrame({
    "age": rng.normal(40, 10, n).clip(18, 90),
    "income": rng.lognormal(10.5, 0.4, n),
    "sessions_per_week": rng.poisson(4, n),
})
ref["target"] = ((ref.age < 35) & (ref.sessions_per_week > 3)).astype(int)

prod = ref.copy()
prod["age"] = rng.normal(50, 12, n).clip(18, 90)          # population shifted older
prod["income"] = rng.lognormal(10.8, 0.5, n)              # incomes drifted up
prod["target"] = ((prod.age < 35) & (prod.sessions_per_week > 3)).astype(int)

ref.to_csv("data/reference.csv", index=False)
prod.to_csv("data/production.csv", index=False)
print("wrote data/reference.csv and data/production.csv")
