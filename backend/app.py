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

# Chargement du preprocessor et du modèle par défaut
MODEL_PATH = "../models/random_forest_model.joblib"
PREPROCESSOR_PATH = "../models/preprocessor.joblib"

# Configurer l'URI de tracking MLflow vers SQLite
mlflow.set_tracking_uri("sqlite:///mlflow.db")

def load_production_model():
    """Tente de charger le modèle depuis le Model Registry, sinon utilise le modèle local."""
    try:
        model = mlflow.sklearn.load_model("models:/boston_housing_model/Production")
        return model, True
    except Exception as e:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            return model, False
        return None, False

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Projet MLA - Boston Housing"}

@app.get("/models/status")
def get_models_status():
    """Vérifie si les modèles ont été entraînés."""
    model, from_registry = load_production_model()
    return {
        "models_trained": model is not None,
        "source": "Model Registry (Production)" if from_registry else "Local joblib"
    }

@app.post("/predict")
def predict(data: dict):
    """
    Endpoint de prédiction conforme au format MLflow.
    Format attendu : {"instances": [[...]]}
    """
    model, from_registry = load_production_model()
    if not model:
        raise HTTPException(status_code=500, detail="Aucun modèle disponible pour la prédiction.")
    
    try:
        # Chargement du préprocesseur
        if os.path.exists(PREPROCESSOR_PATH):
            preprocessor = joblib.load(PREPROCESSOR_PATH)
        else:
            raise Exception("Préprocesseur introuvable.")
            
        instances = data.get("instances", [])
        if not instances:
            raise Exception("Le paramètre 'instances' est vide ou manquant.")
            
        # Colonnes standards du dataset Boston Housing (sans ID ni medv)
        columns = ["crim", "zn", "indus", "chas", "nox", "rm", "age", "dis", "rad", "tax", "ptratio", "black", "lstat"]
        df = pd.DataFrame(instances, columns=columns)
        
        # Prétraitement
        df_proc = preprocessor.transform(df)
        
        # Prédictions
        preds = model.predict(df_proc)
        
        return {
            "predictions": preds.tolist(),
            "model_source": "Model Registry (Production)" if from_registry else "Local Fallback"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur de prédiction : {str(e)}")

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
