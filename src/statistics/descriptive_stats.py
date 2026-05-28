import pandas as pd
from pathlib import Path
from datetime import datetime


def detectar_colunas_numericas(df):
    ignorar = ["Unnamed: 0", "ID", "id", "Código", "codigo"]
    colunas = []

    for coluna in df.select_dtypes(include="number").columns:
        if coluna not in ignorar:
            colunas.append(coluna)

    return colunas


def estatistica_descritiva_geral(df):
    colunas_numericas = detectar_colunas_numericas(df)

    tabela = df[colunas_numericas].agg([
        "count",
        "mean",
        "median",
        "std",
        "min",
        "max"
    ]).T.reset_index()

    tabela.columns = [
        "Variável",
        "N válidos",
        "Média",
        "Mediana",
        "Desvio-padrão",
        "Mínimo",
        "Máximo"
    ]

    tabela["Faltosos/Ausentes"] = len(df) - tabela["N válidos"]
    tabela["CV (%)"] = (tabela["Desvio-padrão"] / tabela["Média"]) * 100

    return tabela.round(2)


def estatistica_por_grupo(df, coluna_grupo="Período"):
    colunas_numericas = detectar_colunas_numericas(df)

    if coluna_grupo not in df.columns:
        return None

    resultados = []

    for grupo, dados in df.groupby(coluna_grupo):
        for variavel in colunas_numericas:
            serie = dados[variavel].dropna()

            resultados.append({
                coluna_grupo: grupo,
                "Variável": variavel,
                "N válidos": serie.count(),
                "Faltosos/Ausentes": dados[variavel].isna().sum(),
                "Média": serie.mean(),
                "Mediana": serie.median(),
                "Desvio-padrão": serie.std(),
                "Mínimo": serie.min(),
                "Máximo": serie.max(),
                "CV (%)": (serie.std() / serie.mean() * 100) if serie.mean() != 0 else None
            })

    return pd.DataFrame(resultados).round(2)


def criar_pontuacao_total(df):
    colunas_numericas = detectar_colunas_numericas(df)

    df = df.copy()
    df["TOTAL"] = df[colunas_numericas].sum(axis=1, skipna=True)
    df["PERCENTUAL_TOTAL"] = (df["TOTAL"] / df[colunas_numericas].sum().max()) * 100

    return df


def salvar_estatisticas(tabela_geral, tabela_grupo=None):
    pasta_saida = Path("outputs")
    pasta_saida.mkdir(parents=True, exist_ok=True)

    agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    caminho_saida = pasta_saida / f"estatistica_descritiva_{agora}.xlsx"

    with pd.ExcelWriter(caminho_saida, engine="openpyxl") as writer:
        tabela_geral.to_excel(writer, sheet_name="Descritiva Geral", index=False)

        if tabela_grupo is not None:
            tabela_grupo.to_excel(writer, sheet_name="Descritiva por Grupo", index=False)

    print(f"\nEstatísticas salvas em:")
    print(caminho_saida)

    return caminho_saida


def executar_estatistica_descritiva(df):
    print("\n" + "=" * 70)
    print("ATHENA ANALYTICS - ESTATÍSTICA DESCRITIVA")
    print("=" * 70)

    tabela_geral = estatistica_descritiva_geral(df)
    print("\nDESCRITIVA GERAL:")
    print(tabela_geral)

    tabela_grupo = estatistica_por_grupo(df, coluna_grupo="Período")

    if tabela_grupo is not None:
        print("\nDESCRITIVA POR PERÍODO:")
        print(tabela_grupo)

    salvar_estatisticas(tabela_geral, tabela_grupo)

    return tabela_geral, tabela_grupo
