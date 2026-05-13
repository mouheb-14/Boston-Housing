from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd

class BostonPreprocessor:
    def __init__(self, n_components=None):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=n_components) if n_components else None

    def fit_transform(self, X):
        """
        Applique le scaling (et la PCA optionnelle) sur les données d'entraînement.
        """
        X_scaled = self.scaler.fit_transform(X)
        if self.pca:
            X_scaled = self.pca.fit_transform(X_scaled)
        return X_scaled

    def transform(self, X):
        """
        Applique les transformations déjà apprises sur de nouvelles données.
        """
        X_scaled = self.scaler.transform(X)
        if self.pca:
            X_scaled = self.pca.transform(X_scaled)
        return X_scaled
