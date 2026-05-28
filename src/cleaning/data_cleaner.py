import pandas as pd
import re
from datetime import datetime
from pathlib import Path


def padronizar_nome_coluna(coluna):
    coluna = str(coluna).strip()
    coluna = coluna.replace("\n", " ")
    coluna = re.sub(r"\s+", " ", coluna)
    return coluna


def limpar_texto(valor):
    if isinstance(valor, str):
        valor = valor.strip()
        valor = re.sub(r"\s+", " ", valor)
        if valor in ["", "-", "NA", "N/A", "nan", "None"]:
            return pd.NA
    return valor


def tentar_converter_numeros(df):
    for coluna in df.columns:
        if df[coluna].dtype == "object":
            serie = df[coluna].astype(str).str.replace(",", ".", regex=False)
            convertida = pd.to_numeric(serie, errors="coerce")

            proporcao_numerica = convertida.notna().mean()

            if proporcao_numerica >= 0.70:
                df[coluna] = convertida

    return df


def limpar_dados(df):
    df = df.copy()

    df.columns = [padronizar_nome_coluna(c) for c in df.columns]

    for coluna in df.columns:
        df[coluna] = df[coluna].map(limpar_texto)

    df = tentar_converter_numeros(df)

    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    return df


def diagnostico_limpeza(df_original, df_limpo):
    print("\n" + "=" * 70)
    print("ATHENA ANALYTICS - SMART CLEANER")
    print("=" * 70)

    print(f"\nLinhas antes: {df_original.shape[0]}")
    print(f"Linhas depois: {df_limpo.shape[0]}")

    print(f"\nColunas antes: {df_original.shape[1]}")
    print(f"Colunas depois: {df_limpo.shape[1]}")

    print("\nVALORES AUSENTES APÓS LIMPEZA:")
    print(df_limpo.isnull().sum())

    print("\nTIPOS APÓS LIMPEZA:")
    print(df_limpo.dtypes)


def salvar_dados_limpos(df):
    pasta_saida = Path("data/processed")
    pasta_saida.mkdir(parents=True, exist_ok=True)

    agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    caminho_saida = pasta_saida / f"dados_limpos_{agora}.xlsx"

    df.to_excel(caminho_saida, index=False)

    print(f"\nPlanilha limpa salva em:")
    print(caminho_saida)

    return caminho_saida
