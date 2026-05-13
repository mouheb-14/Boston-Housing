from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os
import mlflow
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Boston Housing MLA API")

# Configuration CORS pour permettre à React de communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du preprocessor et du modèle par défaut (Random Forest)
MODEL_PATH = "../models/random_forest_model.joblib"
PREPROCESSOR_PATH = "../models/preprocessor.joblib"

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Projet MLA - Boston Housing"}

@app.get("/models/status")
def get_models_status():
    """Vérifie si les modèles ont été entraînés."""
    exists = os.path.exists(MODEL_PATH)
    return {"models_trained": exists}

@app.post("/train")
def run_training():
    """Déclenche le script d'entraînement."""
    try:
        # Note: Dans un vrai environnement on utiliserait un worker Celery,
        # ici on appelle directement le script pour la démo.
        import subprocess
        # Utiliser le python du venv pour s'assurer que les dépendances sont présentes
        python_exe = os.path.join(os.getcwd(), "venv_64", "Scripts", "python.exe")
        subprocess.Popen([python_exe, "train.py"])
        return {"status": "Training started in background"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/experiments")
def get_experiments():
    """Récupère les derniers runs depuis MLflow."""
    try:
        client = mlflow.tracking.MlflowClient()
        experiment = client.get_experiment_by_name("Boston_Housing_Task4")
        if not experiment:
            return []
        
        runs = client.search_runs(experiment.experiment_id)
        results = []
        for run in runs:
            results.append({
                "id": run.info.run_id,
                "name": run.data.tags.get("mlflow.runName", "N/A"),
                "metrics": run.data.metrics,
                "params": run.data.params,
                "status": run.info.status,
                "start_time": run.info.start_time
            })
        return results
    except Exception as e:
        return {"error": str(e)}
