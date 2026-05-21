import requests
import json

def test_prediction():
    url = "http://127.0.0.1:8000/predict"
    
    # Un exemple fictif du dataset Boston Housing (13 features)
    # CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, B, LSTAT
    sample_instance = [0.00632, 18.0, 2.31, 0.0, 0.538, 6.575, 65.2, 4.0900, 1.0, 296.0, 15.3, 396.90, 4.98]
    
    payload = {
        "instances": [sample_instance]
    }
    
    print(f"[Test] Envoi d'une requête POST vers {url}...")
    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"[Test] Code de réponse : {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"[Test] Succès ! Prédictions : {result['predictions']}")
            print(f"[Test] Source du modèle utilisé : {result.get('model_source', 'N/A')}")
        else:
            print(f"[Test] Échec : {response.text}")
    except Exception as e:
        print(f"[Test] Erreur de connexion : {e}. Assurez-vous que le serveur FastAPI tourne sur le port 8000.")

if __name__ == "__main__":
    test_prediction()
