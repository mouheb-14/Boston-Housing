import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os

def simulate_drift():
    print("[MLOps] Simulation du drift de données...")
    
    # Charger les données d'entraînement
    train_path = 'data/boston_train.csv'
    if not os.path.exists(train_path):
        train_path = '../data/boston_train.csv'
        
    df = pd.read_csv(train_path)
    
    if 'ID' in df.columns:
        df = df.drop(columns=['ID'])
        
    X = df.drop(columns=['medv'])
    y = df['medv']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Simulation du drift : décalage de la moyenne + bruit
    X_prod = X_test.copy()
    num_cols = X_prod.select_dtypes(include=np.number).columns
    
    # Appliquer le drift sur les deux premières colonnes
    for col in num_cols[:2]:
        X_prod[col] = X_prod[col] * 1.6 + np.random.normal(0, 0.5, len(X_prod))
        
    # Afficher la différence de moyenne pour la première feature
    feature_name = num_cols[0]
    print(f"[MLOps] Moyenne {feature_name} - Référence: {X_train[feature_name].mean():.3f} | Production: {X_prod[feature_name].mean():.3f}")
    
    # Déterminer le bon dossier de sauvegarde
    data_dir = 'data' if os.path.exists('data') else '../data'
    
    # Sauvegarder les jeux de données pour Evidently
    ref_data = X_train.copy()
    ref_data['medv'] = y_train
    ref_data.to_csv(os.path.join(data_dir, 'reference_data.csv'), index=False)
    
    prod_data = X_prod.copy()
    prod_data['medv'] = y_test
    prod_data.to_csv(os.path.join(data_dir, 'production_data.csv'), index=False)
    print(f"[MLOps] Données de référence et de production sauvegardées dans {data_dir}/")

if __name__ == "__main__":
    simulate_drift()
