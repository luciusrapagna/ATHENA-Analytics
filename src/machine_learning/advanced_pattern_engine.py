import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

import umap
import hdbscan


class AdvancedPatternEngine:

    def __init__(self, output_dir="outputs"):
        self.output_dir = Path(output_dir)
        self.ml_dir = self.output_dir / "machine_learning"
        self.ml_dir.mkdir(parents=True, exist_ok=True)

    def prepare_numeric_data(self, df):
        numeric_df = df.select_dtypes(include=[np.number]).copy()
        numeric_df = numeric_df.loc[:, numeric_df.var(skipna=True) > 0]

        if numeric_df.shape[1] < 2:
            return None, None

        imputer = SimpleImputer(strategy="median")
        scaler = StandardScaler()

        X = imputer.fit_transform(numeric_df)
        X_scaled = scaler.fit_transform(X)

        return X_scaled, numeric_df.columns.tolist()

    def run_umap(self, df):
        X, columns = self.prepare_numeric_data(df)

        if X is None or X.shape[0] < 5:
            return None

        reducer = umap.UMAP(
            n_components=2,
            random_state=42,
            n_neighbors=min(15, max(2, X.shape[0] - 1)),
            min_dist=0.1
        )

        coords = reducer.fit_transform(X)

        result = pd.DataFrame({
            "UMAP1": coords[:, 0],
            "UMAP2": coords[:, 1]
        })

        output = self.ml_dir / "umap_coordinates.xlsx"
        result.to_excel(output, index=False)

        return output

    def run_hdbscan(self, df):
        X, columns = self.prepare_numeric_data(df)

        if X is None or X.shape[0] < 5:
            return None

        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=max(2, int(X.shape[0] * 0.05)),
            prediction_data=True
        )

        labels = clusterer.fit_predict(X)

        result = pd.DataFrame({
            "cluster_hdbscan": labels
        })

        output = self.ml_dir / "hdbscan_clusters.xlsx"
        result.to_excel(output, index=False)

        return output

    def run(self, df):
        results = {}

        print("\n[ATHENA ADVANCED] Executando UMAP...")
        results["umap"] = self.run_umap(df)

        print("[ATHENA ADVANCED] Executando HDBSCAN...")
        results["hdbscan"] = self.run_hdbscan(df)

        print("[ATHENA ADVANCED] Engine avançada finalizada.")

        return results
