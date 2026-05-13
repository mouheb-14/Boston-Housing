import pandas as pd
import joblib
import os
from preprocessing import BostonPreprocessor

def generate_predictions(model_name='random_forest'):
    print(f"Génération des prédictions avec le modèle : {model_name}...")
    
    # 1. Chargement des données de test
    test_path = '../data/test.csv'
    if not os.path.exists(test_path):
        print(f"Erreur : {test_path} introuvable.")
        return

    df_test = pd.read_csv(test_path)
    ids = df_test['ID']
    X_test = df_test.drop(columns=['ID'])

    # 2. Chargement du preprocessor et du modèle
    try:
        preprocessor = joblib.load('../models/preprocessor.joblib')
        model = joblib.load(f'../models/{model_name}_model.joblib')
    except Exception as e:
        print(f"Erreur lors du chargement des modèles : {e}. Avez-vous lancé train.py ?")
        return

    # 3. Pré-traitement et Prédiction
    X_test_proc = preprocessor.transform(X_test)
    predictions = model.predict(X_test_proc)

    # 4. Création du fichier de soumission
    submission = pd.DataFrame({
        'ID': ids,
        'medv': predictions
    })

    output_path = '../data/submission_results.csv'
    submission.to_csv(output_path, index=False)
    print(f"Succès ! Les prédictions ont été sauvegardées dans : {output_path}")

if __name__ == "__main__":
    generate_predictions()
