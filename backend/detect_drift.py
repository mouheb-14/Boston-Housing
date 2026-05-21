import pandas as pd
import numpy as np
import os
import sys
import subprocess
import mlflow
from scipy import stats

# Imports d'Evidently
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.metrics import DatasetDriftMetric

def detect_and_handle_drift():
    print("[MLOps] Analyse du drift de données...")
    
    # 1. Déterminer les bons chemins d'accès
    data_dir = 'data' if os.path.exists('data') else '../data'
    ref_path = os.path.join(data_dir, 'reference_data.csv')
    prod_path = os.path.join(data_dir, 'production_data.csv')
    
    if not os.path.exists(ref_path) or not os.path.exists(prod_path):
        print("[MLOps] Erreur : Les fichiers de référence ou de production sont introuvables. Lancez d'abord 'simulate_drift.py'.")
        return
        
    ref_df = pd.read_csv(ref_path)
    prod_df = pd.read_csv(prod_path)
    
    # Séparer les features de la cible
    X_train = ref_df.drop(columns=['medv'])
    X_prod = prod_df.drop(columns=['medv'])
    
    # 2. Configurer l'expérience MLflow
    mlflow.set_tracking_uri("sqlite:///mlflow.db" if os.path.exists("mlflow.db") else "sqlite:///backend/mlflow.db")
    mlflow.set_experiment("monitoring_drift")
    
    with mlflow.start_run(run_name="drift_check_v1"):
        # --- PARTIE 6.3: Génération du rapport Evidently ---
        print("[MLOps] Exécution du rapport de drift avec Evidently AI...")
        report = Report(metrics=[DataDriftPreset(), DataQualityPreset()])
        report.run(reference_data=X_train, current_data=X_prod)
        
        drift_report_html = "drift_report.html"
        report.save_html(drift_report_html)
        mlflow.log_artifact(drift_report_html)
        
        # Extraction des scores numériques
        score_report = Report(metrics=[DatasetDriftMetric()])
        score_report.run(reference_data=X_train, current_data=X_prod)
        result = score_report.as_dict()
        
        drift_share = result['metrics'][0]['result']['drift_share']
        dataset_drift = result['metrics'][0]['result']['dataset_drift']
        n_drifted = result['metrics'][0]['result']['number_of_drifted_columns']
        n_total = result['metrics'][0]['result']['number_of_columns']
        
        # Logger dans MLflow
        mlflow.log_metric('drift_share', drift_share)
        mlflow.log_metric('drifted_columns', n_drifted)
        mlflow.log_metric('total_columns', n_total)
        mlflow.log_metric('dataset_drifted', int(dataset_drift))
        
        print(f"[MLOps] Part de drift : {drift_share:.2%} | Colonnes driftées : {n_drifted}/{n_total}")
        
        # --- PARTIE 6.4: Test statistique KS-test par feature ---
        print("[MLOps] Calcul des tests statistiques Kolmogorov-Smirnov...")
        ks_results = []
        for col in X_train.select_dtypes(include='number').columns:
            stat, pvalue = stats.ks_2samp(X_train[col], X_prod[col])
            drifted = pvalue < 0.05
            ks_results.append({
                'feature': col,
                'ks_stat': round(stat, 4),
                'p_value': round(pvalue, 4),
                'drifted': drifted
            })
            mlflow.log_metric(f'ks_pvalue_{col}', pvalue)
            
        df_drift = pd.DataFrame(ks_results)
        ks_results_csv = 'ks_drift_results.csv'
        df_drift.to_csv(ks_results_csv, index=False)
        mlflow.log_artifact(ks_results_csv)
        
        print(df_drift.to_string(index=False))
        
        # Nettoyage des fichiers HTML/CSV locaux pour garder le repo propre
        if os.path.exists(drift_report_html): os.remove(drift_report_html)
        if os.path.exists(ks_results_csv): os.remove(ks_results_csv)
        
        # --- PARTIE 6.5: Déclenchement automatique du ré-entraînement ---
        SEUIL_DRIFT = 0.30  # 30% de features driftées -> ré-entraînement
        SEUIL_WARN = 0.15   # 15% -> alerte sans ré-entraînement
        
        # Déterminer le script train.py
        train_script = 'backend/train.py' if os.path.exists('backend/train.py') else 'train.py'
        
        if drift_share > SEUIL_DRIFT:
            print(f"[MLOps] CRITIQUE : Drift de {drift_share:.2%} > Seuil de {SEUIL_DRIFT:.0%}")
            print(f"[MLOps] Déclenchement automatique du ré-entraînement de modèle...")
            
            # Utilise le même interpréteur Python que celui qui exécute ce script
            subprocess.run([sys.executable, train_script, '--retrain'], check=True)
            mlflow.log_metric('retrain_triggered', 1)
            print("[MLOps] Ré-entraînement terminé avec succès.")
            
            # Enregistrer le modèle fraîchement entraîné
            register_script = 'backend/register_best_model.py' if os.path.exists('backend/register_best_model.py') else 'register_best_model.py'
            subprocess.run([sys.executable, register_script], check=True)
            print("[MLOps] Meilleur modèle ré-enregistré dans le Model Registry.")
            
        elif drift_share > SEUIL_WARN:
            print(f"[MLOps] AVERTISSEMENT : Drift de {drift_share:.2%} - Surveillance renforcée requise.")
            mlflow.log_metric('retrain_triggered', 0)
        else:
            print(f"[MLOps] OK : Drift de {drift_share:.2%} - Modèle stable.")
            mlflow.log_metric('retrain_triggered', 0)

if __name__ == "__main__":
    detect_and_handle_drift()
