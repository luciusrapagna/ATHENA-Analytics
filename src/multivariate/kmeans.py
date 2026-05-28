import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

import plotly.express as px


def run_kmeans(df, n_clusters=3, group_column=None):

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.shape[1] < 2:
        raise ValueError("KMeans requer pelo menos 2 variáveis numéricas.")

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_df)

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    clusters = model.fit_predict(scaled_data)

    result_df = df.copy()
    result_df["Cluster"] = clusters.astype(str)

    silhouette = silhouette_score(scaled_data, clusters)

    fig = px.scatter(
        result_df,
        x=numeric_df.columns[0],
        y=numeric_df.columns[1],
        color="Cluster",
        symbol=group_column if group_column in df.columns else None,
        title=f"KMeans - {n_clusters} clusters | Silhouette = {silhouette:.3f}",
        template="plotly_white"
    )

    return {
        "clusters": result_df,
        "silhouette": silhouette,
        "figure": fig
    }