# Rapport d'Analyse : Régression Boston Housing
**Cours : Machine Learning & Analyse de Données**

---

## 1. Analyse des résidus
L'analyse de la distribution des erreurs (résidus) de notre modèle Random Forest révèle les points suivants :
*   **Normalité** : La distribution est approximativement gaussienne (normale) et centrée sur zéro. Cela confirme que le modèle ne surestime ni ne sous-estime les prix de manière systématique sur l'ensemble du dataset.
*   **Hétéroscédasticité** : On observe une variance des erreurs plus importante pour les valeurs cibles élevées (> 40k$). Ce pattern indique que le modèle a plus de mal à prédire avec précision le prix des propriétés de luxe, car ces dernières dépendent souvent de facteurs qualitatifs non présents dans le dataset (vue, finitions, cachet historique).

## 2. Métriques de performance
Nous avons comparé les trois métriques classiques :
*   **MAE (Mean Absolute Error)** : Erreur moyenne absolue. Elle est la plus simple à interpréter pour un non-expert.
*   **MSE (Mean Squared Error)** : Erreur quadratique moyenne. Elle est très sensible aux grandes erreurs.
*   **R² (Coefficient de détermination)** : Indique la proportion de variance capturée.
*   **Verdict** : Le **RMSE (Root Mean Squared Error)** est ici la métrique la plus informative. Elle combine la sensibilité aux valeurs aberrantes du MSE tout en restant dans l'unité d'origine (k$), ce qui permet de dire : "Le modèle se trompe en moyenne de X milliers de dollars".

## 3. Impact des variables
Dans notre modèle non-linéaire (Random Forest) :
*   Une augmentation d'une unité de **RM** (nombre de pièces) a un impact positif majeur sur le prix.
*   À l'inverse, une augmentation de **LSTAT** (% de population à bas revenus dans le quartier) entraîne une chute rapide de la valeur immobilière.
*   *Note* : Contrairement à la régression linéaire, cet impact n'est pas constant mais dépend de la valeur des autres variables (interactions).

## 4. Comparaison des features
*   **Variables dominantes** : **LSTAT** (Statut social) et **RM** (Nombre de pièces) possèdent le plus grand pouvoir prédictif.
*   **Cohérence théorique** : Ces résultats sont parfaitement cohérents avec la théorie économique. La localisation sociale et la surface habitable sont les deux déterminants principaux du prix d'un logement dans toutes les études urbaines classiques.

## 5. Étude Biais et Variance (Random Forest)

| n_estimators | max_depth | Train RMSE | Test RMSE | Biais | Variance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 10 | 3 | 3.22 | 3.11 | Élevé | Faible |
| 100 | 5 | 2.14 | 2.94 | Moyen | Modérée |
| 200 | 20 | 1.29 | 2.87 | Faible | Élevée |

*   **Observation** : À `max_depth=20`, on observe un début d'**overfitting** (sur-apprentissage) : l'erreur d'entraînement est très faible (1.29) mais l'erreur de test ne diminue plus proportionnellement, montrant que le modèle commence à apprendre le "bruit" des données.
*   **Limites** : Le modèle est moins performant sur les valeurs extrêmes.
*   **Pourquoi ?** Phénomène de "régression vers la moyenne" propre aux forêts aléatoires qui ont du mal à prédire des valeurs hors de la plage rencontrée lors de l'entraînement.

## 6. Comparaison avec l'Arbre de Décision
L'utilisation d'un algorithme d'ensemble (Random Forest) apporte une amélioration drastique :
*   **Single Decision Tree** : Test RMSE ≈ **4.94**
*   **Random Forest** : Test RMSE ≈ **2.87**
*   **Analyse** : L'Arbre de décision seul est très instable et sujet à une variance élevée. Le Random Forest, en agrégeant 100 à 200 arbres, lisse ces erreurs et offre une prédiction beaucoup plus robuste et généralisable.
