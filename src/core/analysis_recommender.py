import pandas as pd


def recommend_analyses(df, domain="general"):

    recommendations = []

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    n_numeric = len(numeric_cols)
    n_categorical = len(categorical_cols)

    # ---------------------------------------------------
    # Estatística básica
    # ---------------------------------------------------

    if n_numeric >= 1:
        recommendations.append("estatística descritiva")

    # ---------------------------------------------------
    # Inferencial
    # ---------------------------------------------------

    if n_numeric >= 1 and n_categorical == 1:
        recommendations.append("teste t")

    if n_numeric >= 1 and n_categorical >= 2:
        recommendations.append("anova")

    # ---------------------------------------------------
    # Correlação
    # ---------------------------------------------------

    if n_numeric >= 2:
        recommendations.append("correlação")

    # ---------------------------------------------------
    # PCA
    # ---------------------------------------------------

    if n_numeric >= 5:
        recommendations.append("PCA")

    # ---------------------------------------------------
    # Clustering
    # ---------------------------------------------------

    if n_numeric >= 5:
        recommendations.append("KMeans")

    # ---------------------------------------------------
    # Ecologia
    # ---------------------------------------------------

    if domain == "ecology":

        recommendations.extend([
            "NMDS",
            "PERMANOVA",
            "ANOSIM"
        ])

    # ---------------------------------------------------
    # Epidemiologia
    # ---------------------------------------------------

    if domain == "epidemiology":

        recommendations.extend([
            "regressão",
            "mapas epidemiológicos",
            "séries temporais"
        ])

    # ---------------------------------------------------
    # ENAMED
    # ---------------------------------------------------

    if domain == "enamed":

        recommendations.extend([
            "ranking de turmas",
            "análise de risco",
            "desempenho por áreas",
            "boxplots institucionais"
        ])

    recommendations = list(set(recommendations))

    return recommendations