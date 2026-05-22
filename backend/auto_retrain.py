import os
import pandas as pd
from scipy.stats import ks_2samp
from evidently.dashboard import Dashboard
from evidently.tabs import DataDriftTab

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TRAIN_PATH = os.path.join(BASE_DIR, "data", "boston_train.csv")
PROD_PATH = os.path.join(BASE_DIR, "data", "test.csv")

# Load data
train_df = pd.read_csv(TRAIN_PATH)
prod_df = pd.read_csv(PROD_PATH)

# Compute drift ratio using KS test
threshold = 0.3
drifted = 0
for col in train_df.columns:
    if col == "target":
        continue
    _, p = ks_2samp(train_df[col], prod_df[col])
    if p < 0.05:
        drifted += 1

drifts_ratio = drifted / (len(train_df.columns) - 1)
print(f"[AutoRetrain] Drift ratio: {drifts_ratio:.2%} (threshold: {threshold:.2%})")

if drifts_ratio > threshold:
    print("[AutoRetrain] Drift exceeds threshold – triggering retraining...")
    # Run training script using the project's virtual environment python
    python_exe = os.path.join(BASE_DIR, "backend", "venv_64", "Scripts", "python.exe")
    train_script = os.path.join(BASE_DIR, "backend", "train.py")
    os.system(f"\"{python_exe}\" \"{train_script}\"")
else:
    print("[AutoRetrain] Drift within acceptable limits – no retraining needed.")
