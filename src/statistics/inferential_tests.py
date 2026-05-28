import pandas as pd
from scipy import stats
from pathlib import Path
from datetime import datetime


def detectar_colunas_numericas(df):
    ignorar = ["Unnamed: 0", "ID", "id", "Código", "codigo", "TOTAL", "PERCENTUAL_TOTAL"]
    return [c for c in df.select_dtypes(include="number").columns if c not in ignorar]


def interpretar_p(valor):
    if pd.isna(valor):
        return "Não aplicável"
    if valor < 0.001:
        return "p < 0,001"
    return f"p = {valor:.4f}"


def executar_teste_t(df, coluna_grupo="Período"):
    colunas = detectar_colunas_numericas(df)

    if coluna_grupo not in df.columns:
        return pd.DataFrame()

    grupos = df[coluna_grupo].dropna().unique()

    if len(grupos) != 2:
        return pd.DataFrame()

    resultados = []

    for variavel in colunas:
        g1 = df[df[coluna_grupo] == grupos[0]][variavel].dropna()
        g2 = df[df[coluna_grupo] == grupos[1]][variavel].dropna()

        if len(g1) >= 2 and len(g2) >= 2:
            stat, p = stats.ttest_ind(g1, g2, equal_var=False)

            resultados.append({
                "Teste": "Teste t de Welch",
                "Variável": variavel,
                "Grupo 1": grupos[0],
                "Grupo 2": grupos[1],
                "Média Grupo 1": g1.mean(),
                "Média Grupo 2": g2.mean(),
                "Estatística": stat,
                "p-valor": p,
                "Interpretação": interpretar_p(p)
            })

    return pd.DataFrame(resultados).round(4)


def executar_anova(df, coluna_grupo="Período"):
    colunas = detectar_colunas_numericas(df)

    if coluna_grupo not in df.columns:
        return pd.DataFrame()

    resultados = []

    for variavel in colunas:
        grupos = [
            grupo[variavel].dropna()
            for _, grupo in df.groupby(coluna_grupo)
            if grupo[variavel].dropna().shape[0] >= 2
        ]

        if len(grupos) >= 2:
            stat, p = stats.f_oneway(*grupos)

            resultados.append({
                "Teste": "ANOVA one-way",
                "Variável": variavel,
                "Estatística F": stat,
                "p-valor": p,
                "Interpretação": interpretar_p(p)
            })

    return pd.DataFrame(resultados).round(4)


def salvar_testes_inferenciais(t_teste, anova):
    pasta = Path("outputs")
    pasta.mkdir(parents=True, exist_ok=True)

    agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    caminho = pasta / f"testes_inferenciais_{agora}.xlsx"

    with pd.ExcelWriter(caminho, engine="openpyxl") as writer:
        if not t_teste.empty:
            t_teste.to_excel(writer, sheet_name="Teste t", index=False)

        if not anova.empty:
            anova.to_excel(writer, sheet_name="ANOVA", index=False)

    print(f"\nTestes inferenciais salvos em:")
    print(caminho)

    return caminho


def executar_testes_inferenciais(df):
    print("\n" + "=" * 70)
    print("ATHENA ANALYTICS - TESTES INFERENCIAIS")
    print("=" * 70)

    t_teste = executar_teste_t(df, coluna_grupo="Período")
    anova = executar_anova(df, coluna_grupo="Período")

    if not t_teste.empty:
        print("\nTESTE T:")
        print(t_teste)
    else:
        print("\nTeste t não executado: é necessário exatamente 2 grupos.")

    if not anova.empty:
        print("\nANOVA:")
        print(anova)
    else:
        print("\nANOVA não executada.")

    salvar_testes_inferenciais(t_teste, anova)

    return t_teste, anova
