import mlflow
from mlflow.tracking import MlflowClient

def register_and_promote_model():
    print("[MLOps] Connexion au serveur MLflow...")
    # S'assurer que l'URI de tracking pointe vers notre base locale SQLite
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    
    client = MlflowClient()
    
    # 1. Récupération de l'expérience
    experiment = client.get_experiment_by_name("Boston_Housing_Task4")
    if not experiment:
        print("[MLOps] Erreur : L'expérience 'Boston_Housing_Task4' est introuvable. Lancez d'abord l'entraînement.")
        return
    
    # 2. Recherche du meilleur run (trié par Test_RMSE ascendant)
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.Test_RMSE ASC"],
        max_results=5
    )
    
    if not runs:
        print("[MLOps] Aucun run trouvé dans l'expérience.")
        return
        
    best_run = runs[0]
    best_run_id = best_run.info.run_id
    best_rmse = best_run.data.metrics.get("Test_RMSE", float("inf"))
    best_r2 = best_run.data.metrics.get("R2", 0.0)
    best_params = best_run.data.params
    best_name = best_run.data.tags.get("mlflow.runName", "N/A")
    
    print(f"[MLOps] Meilleur run identifié : {best_run_id} ({best_name})")
    print(f"[MLOps] Métriques de test -> RMSE: {best_rmse:.4f} | R²: {best_r2:.4f}")
    print(f"[MLOps] Hyperparamètres : {best_params}")

    # 3. Enregistrement du modèle dans le Registry
    model_name = "boston_housing_model"
    model_uri = f"runs:/{best_run_id}/model"
    
    print(f"[MLOps] Enregistrement du modèle sous le nom '{model_name}'...")
    registered = mlflow.register_model(
        model_uri=model_uri,
        name=model_name
    )
    version = registered.version
    print(f"[MLOps] Modèle enregistré avec succès. Version : {version}")

    # 4. Ajout de descriptions et de tags
    client.update_registered_model(
        name=model_name,
        description="Modèle de régression Boston Housing (Random Forest / Decision Tree) optimisé"
    )
    client.set_model_version_tag(
        name=model_name,
        version=version,
        key="validated_by",
        value="equipe_data"
    )

    # 5. Transition vers Staging
    print(f"[MLOps] Promotion de la version {version} vers 'Staging'...")
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage="Staging",
        archive_existing_versions=False
    )

    # 6. Validation avant promotion en Production (seuil RMSE < 3.2)
    SEUIL_RMSE = 3.2
    if best_rmse <= SEUIL_RMSE:
        print(f"[MLOps] Validation réussie ! Test RMSE ({best_rmse:.3f}) <= Seuil ({SEUIL_RMSE})")
        print(f"[MLOps] Promotion de la version {version} en 'Production'...")
        client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage="Production",
            archive_existing_versions=True  # Archiver les anciennes versions en Production
        )
        print(f"[MLOps] Le modèle v{version} est maintenant en Production !")
    else:
        print(f"[MLOps] Promotion en Production refusée : RMSE {best_rmse:.3f} > Seuil {SEUIL_RMSE}")

if __name__ == "__main__":
    register_and_promote_model()
