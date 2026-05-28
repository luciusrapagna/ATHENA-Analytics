import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime


def preparar_pasta_figuras():
    pasta = Path("figures")
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def detectar_colunas_numericas(df):
    ignorar = ["Unnamed: 0", "ID", "id", "Código", "codigo"]
    return [c for c in df.select_dtypes(include="number").columns if c not in ignorar]


def aplicar_estilo_a1():
    sns.set_theme(style="whitegrid", context="talk")
    plt.rcParams["figure.dpi"] = 150
    plt.rcParams["savefig.dpi"] = 300
    plt.rcParams["font.family"] = "Arial"


def salvar_figura(nome_base):
    pasta = preparar_pasta_figuras()
    agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    png = pasta / f"{nome_base}_{agora}.png"
    svg = pasta / f"{nome_base}_{agora}.svg"

    plt.tight_layout()
    plt.savefig(png, bbox_inches="tight")
    plt.savefig(svg, bbox_inches="tight")
    plt.close()

    print(f"Figura salva: {png}")
    print(f"Figura salva: {svg}")


def grafico_boxplot_total_por_periodo(df, coluna_grupo="Período"):
    colunas = detectar_colunas_numericas(df)

    if coluna_grupo not in df.columns:
        print("Coluna de grupo não encontrada para boxplot.")
        return

    dados = df.copy()
    dados["TOTAL"] = dados[colunas].sum(axis=1, skipna=False)

    aplicar_estilo_a1()

    plt.figure(figsize=(12, 7))
    ax = sns.boxplot(
        data=dados,
        x=coluna_grupo,
        y="TOTAL"
    )

    sns.stripplot(
        data=dados,
        x=coluna_grupo,
        y="TOTAL",
        color="black",
        alpha=0.45,
        size=4
    )

    ax.set_title("Distribuição da pontuação total por turma/período", fontsize=18, weight="bold")
    ax.set_xlabel("Turma/Período")
    ax.set_ylabel("Pontuação total")
    ax.grid(axis="y", alpha=0.3)

    salvar_figura("boxplot_total_por_periodo")


def grafico_histograma_total(df):
    colunas = detectar_colunas_numericas(df)

    dados = df.copy()
    dados["TOTAL"] = dados[colunas].sum(axis=1, skipna=False)

    aplicar_estilo_a1()

    plt.figure(figsize=(12, 7))
    ax = sns.histplot(
        data=dados,
        x="TOTAL",
        kde=True,
        bins=15
    )

    ax.set_title("Distribuição geral da pontuação total", fontsize=18, weight="bold")
    ax.set_xlabel("Pontuação total")
    ax.set_ylabel("Frequência")
    ax.grid(axis="y", alpha=0.3)

    salvar_figura("histograma_total")


def grafico_media_por_area(df):
    colunas = detectar_colunas_numericas(df)

    medias = df[colunas].mean().sort_values(ascending=False).reset_index()
    medias.columns = ["Área", "Média"]

    aplicar_estilo_a1()

    plt.figure(figsize=(13, 7))
    ax = sns.barplot(
        data=medias,
        x="Área",
        y="Média"
    )

    ax.set_title("Média de desempenho por área", fontsize=18, weight="bold")
    ax.set_xlabel("Área")
    ax.set_ylabel("Média")
    ax.tick_params(axis="x", rotation=35)
    ax.grid(axis="y", alpha=0.3)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", fontsize=10)

    salvar_figura("media_por_area")


def grafico_media_area_por_periodo(df, coluna_grupo="Período"):
    colunas = detectar_colunas_numericas(df)

    if coluna_grupo not in df.columns:
        print("Coluna de grupo não encontrada para gráfico por período.")
        return

    tabela = df.groupby(coluna_grupo)[colunas].mean().reset_index()

    tabela_long = tabela.melt(
        id_vars=coluna_grupo,
        var_name="Área",
        value_name="Média"
    )

    aplicar_estilo_a1()

    plt.figure(figsize=(15, 8))
    ax = sns.barplot(
        data=tabela_long,
        x=coluna_grupo,
        y="Média",
        hue="Área"
    )

    ax.set_title("Média por área segundo turma/período", fontsize=18, weight="bold")
    ax.set_xlabel("Turma/Período")
    ax.set_ylabel("Média")
    ax.grid(axis="y", alpha=0.3)
    ax.legend(title="Área", bbox_to_anchor=(1.02, 1), loc="upper left")

    salvar_figura("media_area_por_periodo")


def executar_visualizacoes(df):
    print("\n" + "=" * 70)
    print("ATHENA ANALYTICS - VISUALIZAÇÃO CIENTÍFICA A1")
    print("=" * 70)

    grafico_boxplot_total_por_periodo(df)
    grafico_histograma_total(df)
    grafico_media_por_area(df)
    grafico_media_area_por_periodo(df)

    print("\nVisualizações concluídas.")
