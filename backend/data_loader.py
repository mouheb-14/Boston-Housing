import pandas as pd
from sklearn.model_selection import train_test_split
import os

def load_boston_data(file_path='../data/boston_train.csv'):
    """
    Charge le dataset Boston Housing et sépare les features de la cible.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} est introuvable.")
    
    df = pd.read_csv(file_path)
    
    # Suppression de la colonne ID si elle existe car elle n'aide pas à la prédiction
    if 'ID' in df.columns:
        df = df.drop(columns=['ID'])
        
    # Séparation Features (X) et Target (y -> medv)
    X = df.drop(columns=['medv'])
    y = df['medv']
    
    return X, y

def get_train_test_split(X, y, test_size=0.2, random_state=42):
    """
    Divise les données en jeux d'entraînement et de validation.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)
