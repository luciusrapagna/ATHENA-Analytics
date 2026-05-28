import pandas as pd
import numpy as np


def smart_imputation(df):

    cleaned_df = df.copy()

    # -----------------------------------------
    # Remover colunas de índice importadas
    # -----------------------------------------

    cleaned_df = cleaned_df.loc[
        :,
        ~cleaned_df.columns.astype(str).str.contains(
            "^Unnamed",
            case=False,
            regex=True
        )
    ]

    # -----------------------------------------
    # Remover colunas totalmente vazias
    # -----------------------------------------

    cleaned_df = cleaned_df.dropna(
        axis=1,
        how="all"
    )

    # -----------------------------------------
    # Preencher NaN numérico com média
    # -----------------------------------------

    numeric_cols = cleaned_df.select_dtypes(
        include=np.number
    ).columns

    for col in numeric_cols:

        cleaned_df[col] = cleaned_df[col].fillna(
            cleaned_df[col].mean()
        )

    return cleaned_df
