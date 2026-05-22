# Boston Housing – MLOps Pipeline

## 📚 Overview
This repository contains a **complete local MLOps pipeline** for the Boston Housing regression dataset. It demonstrates:
- Experiment tracking with **MLflow** (parameters, metrics, artifacts).
- Model versioning via the **MLflow Model Registry** (Staging → Production).
- A **FastAPI** serving endpoint that automatically loads the production model.
- **Data drift detection** with **Evidently** (HTML report, KS‑test) and automatic retraining when drift exceeds a 30 % threshold.
- End‑to‑end orchestration with a **Makefile** (`make pipeline`).

## 🛠️ Setup
```bash
# 1️⃣ Clone the repo (already done)
# 2️⃣ Create the virtual environment
python -m venv backend/venv_64
.ackend\venv_64\Scripts\activate

# 3️⃣ Install dependencies
pip install -r backend/requirements.txt
pip install evidently scipy

# 4️⃣ Initialise MLflow (SQLite DB created automatically)
mlflow ui   # then open http://127.0.0.1:5000
```

## 🚀 Run the full pipeline
```bash
make pipeline   # runs: train → register → test → drift → (auto‑retrain if needed)
```
The pipeline will:
1. Train three models (Decision Tree baseline + three Random Forest configs) and log everything to **MLflow**.
2. Register the best model (lowest `Test_RMSE`) and promote it to **Production**.
3. Run the FastAPI server (`make serve` or `uvicorn backend.app:app --reload`).
4. Execute `detect_drift.py` which:
   - Generates `reports/data_drift_report.html` (saved as an MLflow artifact).
   - Computes a KS‑test per feature, logs the p‑values, and writes `reports/ks_drift_results.csv`.
   - If the drift share > 30 % it automatically triggers a re‑training (`python backend/train.py --retrain`).

## 📊 Results (screenshots)
* **MLflow UI** – view experiments, runs, metrics and registered model versions.
* **Evidently drift report** – visual HTML report showing feature‑wise drift.
* **FastAPI** – `/predict` endpoint returns predictions from the production model.

> The screenshots required by the assignment are stored in the `screenshots/` folder and referenced in the report.

## 🔧 Useful commands
```bash
# Start FastAPI
make serve
# Run only the drift detection
make drift
# Run unit tests (if any)
make test
```

## 📦 Project structure
```
projet-mla/
├─ backend/                # source code & venv
│   ├─ train.py
│   ├─ register_best_model.py
│   ├─ detect_drift.py
│   ├─ auto_retrain.py
│   ├─ app.py (FastAPI)
│   ├─ requirements.txt
│   └─ mlflow.db
├─ data/                   # boston_train.csv, test.csv
├─ models/                 # .joblib files (ignored in Git)
├─ reports/                # drift HTML & CSV (ignored in Git)
├─ Makefile
├─ README.md               # <-- this file
└─ .gitignore
```

## ✅ Task 5 checklist
- [x] Training & MLflow logging ✅
- [x] Model Registry (Staging → Production) ✅
- [x] FastAPI serving ✅
- [x] Data drift detection with Evidently + KS‑test ✅
- [x] Automatic retraining when drift > 30 % ✅
- [x] Makefile orchestrating the whole pipeline ✅
- [x] Screenshots of MLflow UI, drift report, API test ✅
- [x] Git repository with proper .gitignore ✅
- [ ] README & Tag for submission (we are adding it now) ✅
