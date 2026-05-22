import os
import json
import pandas as pd
import mlflow
import subprocess
from evidently import Report
from evidently.presets import DataDriftPreset
from scipy.stats import ks_2samp

# Configuration MLflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment('monitoring_drift')

# Paths to data
TRAIN_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "boston_train.csv")
PROD_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "test.csv")

# Load datasets
train_df = pd.read_csv(TRAIN_PATH)
prod_df = pd.read_csv(PROD_PATH)

# Ne comparer que les colonnes numeriques presentes dans les deux datasets
numeric_cols = [col for col in train_df.select_dtypes(include='number').columns if col in prod_df.columns]

with mlflow.start_run(run_name='drift_check_v1'):
    # 6.3 - Generation du rapport Evidently
    report = Report(metrics=[DataDriftPreset()])
    snapshot = report.run(reference_data=train_df, current_data=prod_df)
    
    report_path = os.path.join(os.path.dirname(__file__), "..", "reports", "data_drift_report.html")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    snapshot.save_html(report_path)
    mlflow.log_artifact(report_path)
    print(f"[Drift] Evidently report saved and logged as artifact.")

    # 6.4 - Test statistique KS-test par feature
    results = []
    drifted_count = 0
    for col in numeric_cols:
        stat, pvalue = ks_2samp(train_df[col], prod_df[col])
        is_drifted = pvalue < 0.05
        if is_drifted:
            drifted_count += 1
            
        results.append({
            'feature': col,
            'ks_stat': round(stat, 4),
            'p_value': round(pvalue, 4),
            'drifted': is_drifted
        })
        mlflow.log_metric(f'ks_pvalue_{col}', pvalue)
        
    df_drift = pd.DataFrame(results)
    csv_path = os.path.join(os.path.dirname(__file__), "..", "reports", "ks_drift_results.csv")
    df_drift.to_csv(csv_path, index=False)
    mlflow.log_artifact(csv_path)
    
    # Metriques globales de drift
    n_total = len(numeric_cols)
    drift_share = drifted_count / n_total if n_total > 0 else 0
    dataset_drifted = 1 if drift_share > 0.3 else 0
    
    mlflow.log_metric('drift_share', drift_share)
    mlflow.log_metric('drifted_columns', drifted_count)
    mlflow.log_metric('total_columns', n_total)
    mlflow.log_metric('dataset_drifted', dataset_drifted)
    
    print(f"Drift share : {drift_share:.2%} | Colonnes driftees : {drifted_count}/{n_total}")

    # 6.5 - Declenchement automatique du re-entrainement
    SEUIL_DRIFT = 0.30
    SEUIL_WARN = 0.15

    if drift_share > SEUIL_DRIFT:
        print(f"CRITIQUE : drift ({drift_share:.2%}) > seuil ({SEUIL_DRIFT:.0%})")
        mlflow.log_metric('retrain_triggered', 1)
        # Call training script
        train_script = os.path.join(os.path.dirname(__file__), "train.py")
        subprocess.run(['python', train_script, '--retrain'], check=True)
    elif drift_share > SEUIL_WARN:
        print(f"AVERTISSEMENT : drift ({drift_share:.2%}) - surveillance renforcee")
        mlflow.log_metric('retrain_triggered', 0)
    else:
        print(f"OK : drift ({drift_share:.2%}) - modle stable")
        mlflow.log_metric('retrain_triggered', 0)
