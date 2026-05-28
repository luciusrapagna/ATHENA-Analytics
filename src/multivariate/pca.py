import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import plotly.express as px


def run_pca(
    df,
    group_column=None,
    output_path=None,
    n_components=2
):

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.shape[1] < 2:
        raise ValueError(
            "PCA requer pelo menos 2 variáveis numéricas."
        )

    # ---------------------------------------------------
    # Padronização
    # ---------------------------------------------------

    scaler = StandardScaler()

    scaled_data = scaler.fit_transform(numeric_df)

    # ---------------------------------------------------
    # PCA
    # ---------------------------------------------------

    pca = PCA(n_components=n_components)

    components = pca.fit_transform(scaled_data)

    explained_variance = pca.explained_variance_ratio_

    # ---------------------------------------------------
    # DataFrame PCA
    # ---------------------------------------------------

    pca_df = pd.DataFrame({
        "PC1": components[:, 0],
        "PC2": components[:, 1]
    })

    # ---------------------------------------------------
    # Gráfico
    # ---------------------------------------------------

    fig = px.scatter(
        pca_df,
        x="PC1",
        y="PC2",
        title="PCA - ATHENA Analytics",
        template="plotly_white"
    )

    # ---------------------------------------------------
    # Exportação
    # ---------------------------------------------------

    if output_path:

        fig.write_image(
            f"{output_path}/pca_plot.png",
            width=1600,
            height=1200,
            scale=2
        )

    # ---------------------------------------------------
    # Resultado
    # ---------------------------------------------------

    result = {
        "explained_variance": explained_variance,
        "pca_dataframe": pca_df,
        "figure": fig
    }

    return result