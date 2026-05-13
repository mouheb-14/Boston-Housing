import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

from data_loader import load_boston_data, get_train_test_split
from preprocessing import BostonPreprocessor

def plot_residuals(y_true, y_pred, model_name):
    plt.figure(figsize=(10, 6))
    residuals = y_true - y_pred
    sns.histplot(residuals, kde=True)
    plt.title(f'Residuals Distribution - {model_name}')
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plot_path = f"residuals_{model_name.lower()}.png"
    plt.savefig(plot_path)
    plt.close()
    return plot_path

def plot_feature_importance(model, feature_names, model_name):
    if not hasattr(model, 'feature_importances_'):
        return None
    
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(12, 8))
    plt.title(f'Feature Importances - {model_name}')
    plt.bar(range(len(importances)), importances[indices], align='center')
    plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45)
    plt.tight_layout()
    plot_path = f"feature_importance_{model_name.lower()}.png"
    plt.savefig(plot_path)
    plt.close()
    return plot_path

def train_and_log_models():
    # 1. Chargement des données
    print("Chargement des données...")
    X, y = load_boston_data('../data/boston_train.csv')
    X_train, X_test, y_train, y_test = get_train_test_split(X, y)

    # Noms des features
    feature_names = X.columns.tolist()

    # 2. Pré-traitement
    use_pca = False 
    preprocessor = BostonPreprocessor(n_components=5 if use_pca else None)
    
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)

    # Dossier pour les modèles
    if not os.path.exists('../models'):
        os.makedirs('../models')

    # Expérience MLflow
    mlflow.set_experiment("Boston_Housing_Task4")

    # --- PARTIE 1: Comparaison avec Decision Tree ---
    with mlflow.start_run(run_name="Decision_Tree_Baseline"):
        dt = DecisionTreeRegressor(random_state=42)
        dt.fit(X_train_proc, y_train)
        
        y_train_pred = dt.predict(X_train_proc)
        y_test_pred = dt.predict(X_test_proc)
        
        train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
        test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
        
        mlflow.log_param("model_type", "DecisionTree")
        mlflow.log_metric("Train_RMSE", train_rmse)
        mlflow.log_metric("Test_RMSE", test_rmse)
        mlflow.log_metric("R2", r2_score(y_test, y_test_pred))
        
        # Plots
        res_path = plot_residuals(y_test, y_test_pred, "DecisionTree")
        fi_path = plot_feature_importance(dt, feature_names, "DecisionTree")
        mlflow.log_artifact(res_path)
        if fi_path: mlflow.log_artifact(fi_path)
        
        print(f"Decision Tree Baseline: Test RMSE = {test_rmse:.4f}")
        # Clean up local plots
        if os.path.exists(res_path): os.remove(res_path)
        if fi_path and os.path.exists(fi_path): os.remove(fi_path)

    # --- PARTIE 2: Hyperparameter Tuning pour Random Forest (Analyse Biais/Variance) ---
    param_grid = [
        {"n_estimators": 10, "max_depth": 3},   # Potential Underfitting (High Bias)
        {"n_estimators": 100, "max_depth": 5},  # Balanced
        {"n_estimators": 200, "max_depth": 20}, # Potential Overfitting (High Variance)
    ]

    for params in param_grid:
        run_name = f"RF_n{params['n_estimators']}_d{params['max_depth']}"
        with mlflow.start_run(run_name=run_name):
            rf = RandomForestRegressor(
                n_estimators=params['n_estimators'], 
                max_depth=params['max_depth'], 
                random_state=42
            )
            rf.fit(X_train_proc, y_train)
            
            y_train_pred = rf.predict(X_train_proc)
            y_test_pred = rf.predict(X_test_proc)
            
            train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
            bias = train_rmse 
            variance = test_rmse - train_rmse 
            
            mlflow.log_params(params)
            mlflow.log_param("model_type", "RandomForest")
            mlflow.log_metric("Train_RMSE", train_rmse)
            mlflow.log_metric("Test_RMSE", test_rmse)
            mlflow.log_metric("Bias", bias)
            mlflow.log_metric("Variance", variance)
            mlflow.log_metric("R2", r2_score(y_test, y_test_pred))
            
            # Artefacts
            res_path = plot_residuals(y_test, y_test_pred, run_name)
            fi_path = plot_feature_importance(rf, feature_names, run_name)
            mlflow.log_artifact(res_path)
            if fi_path: mlflow.log_artifact(fi_path)
            
            # Clean up local plots
            if os.path.exists(res_path): os.remove(res_path)
            if fi_path and os.path.exists(fi_path): os.remove(fi_path)
            
            print(f"RF {run_name}: Train RMSE={train_rmse:.2f}, Test RMSE={test_rmse:.2f}")

            # Save the balanced model for the API
            if params['max_depth'] == 5:
                joblib.dump(rf, "../models/random_forest_model.joblib")

    # Save preprocessor
    joblib.dump(preprocessor, "../models/preprocessor.joblib")
    print("Analyse de la Tâche 4 terminée. Consultez MLflow pour les résultats détaillés.")

if __name__ == "__main__":
    train_and_log_models()
