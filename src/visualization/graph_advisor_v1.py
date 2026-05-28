import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path


class GraphAdvisorV1:

    def __init__(self, output_dir="outputs"):

        self.output_dir = Path(output_dir)
        self.graph_dir = self.output_dir / "graph_advisor"

        self.graph_dir.mkdir(parents=True, exist_ok=True)

        self.available_graphs = {
            "1": "barras",
            "2": "boxplot",
            "3": "pizza",
            "4": "xy",
            "5": "histograma",
            "6": "correlacao",
            "7": "heatmap"
        }

        self.apply_a1_style()

    def apply_a1_style(self):

        plt.rcParams.update({
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "font.size": 12,
            "axes.titlesize": 18,
            "axes.labelsize": 14,
            "legend.fontsize": 11,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "grid.linestyle": "-"
        })

    def choose_graphs(self):

        print("\n===================================")
        print("ATHENA GRAPH ADVISOR v1 - A1 STYLE")
        print("===================================")
        print("[1] Barras A1")
        print("[2] Boxplot A1")
        print("[3] Pizza A1")
        print("[4] Dispersão XY A1")
        print("[5] Histograma A1")
        print("[6] Correlação A1")
        print("[7] Heatmap A1")
        print("[ENTER] Pular gráficos manuais")

        selected = input("\nEscolha os gráficos separados por vírgula: ").strip()

        if not selected:
            return []

        selected_keys = [
            item.strip()
            for item in selected.split(",")
            if item.strip() in self.available_graphs
        ]

        graphs = [
            self.available_graphs[key]
            for key in selected_keys
        ]

        print("\nGráficos selecionados:")
        print(graphs)

        return graphs

    def detect_numeric_columns(self, df):
        return df.select_dtypes(include=[np.number]).columns.tolist()

    def detect_categorical_columns(self, df):
        return df.select_dtypes(include=["object", "category"]).columns.tolist()

    def safe_name(self, name):
        return (
            str(name)
            .replace("/", "_")
            .replace("\\", "_")
            .replace("\n", "_")
            .replace(" ", "_")
        )

    def save_fig(self, filename):

        png = self.graph_dir / f"{filename}.png"
        svg = self.graph_dir / f"{filename}.svg"

        plt.savefig(png, dpi=300, bbox_inches="tight")
        plt.savefig(svg, bbox_inches="tight")
        plt.close()

    def plot_bar(self, df):

        numeric_cols = self.detect_numeric_columns(df)
        categorical_cols = self.detect_categorical_columns(df)

        if not numeric_cols:
            print("[GRAPH] Sem colunas numéricas para barras.")
            return

        fig, ax = plt.subplots(figsize=(10, 6))

        if categorical_cols:
            cat = categorical_cols[0]
            num = numeric_cols[0]

            plot_df = (
                df.groupby(cat)[num]
                .mean()
                .reset_index()
                .dropna()
                .sort_values(num, ascending=True)
            )

            ax.barh(plot_df[cat].astype(str), plot_df[num])
            ax.set_title(f"Média de {num} por {cat}")
            ax.set_xlabel(num)
            ax.set_ylabel(cat)

            filename = f"bar_a1_{self.safe_name(num)}_by_{self.safe_name(cat)}"

        else:
            means = df[numeric_cols].mean().sort_values(ascending=True)

            ax.barh(means.index.astype(str), means.values)
            ax.set_title("Médias das variáveis numéricas")
            ax.set_xlabel("Média")
            filename = "bar_a1_numeric_means"

        plt.tight_layout()
        self.save_fig(filename)

    def plot_boxplot(self, df):

        numeric_cols = self.detect_numeric_columns(df)

        if not numeric_cols:
            print("[GRAPH] Sem colunas numéricas para boxplot.")
            return

        fig, ax = plt.subplots(figsize=(11, 6))

        df[numeric_cols].boxplot(ax=ax)

        ax.set_title("Distribuição das variáveis numéricas")
        ax.set_ylabel("Valores")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        self.save_fig("boxplot_a1_numeric_variables")

    def plot_pie(self, df):

        categorical_cols = self.detect_categorical_columns(df)

        if not categorical_cols:
            print("[GRAPH] Sem coluna categórica para pizza.")
            return

        cat = categorical_cols[0]
        counts = df[cat].value_counts().head(6)

        fig, ax = plt.subplots(figsize=(8, 8))

        ax.pie(
            counts.values,
            labels=counts.index.astype(str),
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"linewidth": 1, "edgecolor": "white"}
        )

        ax.set_title(f"Distribuição de {cat}")
        plt.tight_layout()

        self.save_fig(f"pie_a1_{self.safe_name(cat)}")

    def plot_xy(self, df):

        numeric_cols = self.detect_numeric_columns(df)

        if len(numeric_cols) < 2:
            print("[GRAPH] São necessárias duas colunas numéricas para XY.")
            return

        x = numeric_cols[0]
        y = numeric_cols[1]

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.scatter(
            df[x],
            df[y],
            alpha=0.75,
            s=65,
            edgecolor="black",
            linewidth=0.4
        )

        ax.set_title(f"Relação entre {x} e {y}")
        ax.set_xlabel(x)
        ax.set_ylabel(y)

        plt.tight_layout()

        self.save_fig(f"xy_a1_{self.safe_name(x)}_vs_{self.safe_name(y)}")

    def plot_histogram(self, df):

        numeric_cols = self.detect_numeric_columns(df)

        if not numeric_cols:
            print("[GRAPH] Sem colunas numéricas para histograma.")
            return

        for col in numeric_cols:

            fig, ax = plt.subplots(figsize=(8, 6))

            ax.hist(
                df[col].dropna(),
                bins=20,
                alpha=0.85,
                edgecolor="black",
                linewidth=0.4
            )

            ax.set_title(f"Distribuição de {col}")
            ax.set_xlabel(col)
            ax.set_ylabel("Frequência")

            plt.tight_layout()

            self.save_fig(f"hist_a1_{self.safe_name(col)}")

    def plot_correlation(self, df):

        numeric_cols = self.detect_numeric_columns(df)

        if len(numeric_cols) < 2:
            print("[GRAPH] Sem variáveis suficientes para correlação.")
            return

        corr = df[numeric_cols].corr()

        output_xlsx = self.graph_dir / "correlation_matrix.xlsx"
        corr.to_excel(output_xlsx)

        fig, ax = plt.subplots(figsize=(9, 7))

        im = ax.imshow(corr, aspect="auto", vmin=-1, vmax=1)

        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        ax.set_xticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=45, ha="right")

        ax.set_yticks(range(len(corr.index)))
        ax.set_yticklabels(corr.index)

        ax.set_title("Matriz de correlação")

        for i in range(len(corr.index)):
            for j in range(len(corr.columns)):
                ax.text(
                    j,
                    i,
                    f"{corr.iloc[i, j]:.2f}",
                    ha="center",
                    va="center",
                    fontsize=8
                )

        plt.tight_layout()

        self.save_fig("correlation_a1_heatmap")

    def plot_heatmap(self, df):

        numeric_cols = self.detect_numeric_columns(df)

        if len(numeric_cols) < 2:
            print("[GRAPH] Sem variáveis suficientes para heatmap.")
            return

        data = df[numeric_cols].copy()
        data = data.fillna(data.median())
        data = (data - data.mean()) / data.std(ddof=0)

        fig, ax = plt.subplots(figsize=(11, 7))

        im = ax.imshow(data, aspect="auto")

        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        ax.set_xticks(range(len(numeric_cols)))
        ax.set_xticklabels(numeric_cols, rotation=45, ha="right")

        ax.set_ylabel("Observações")
        ax.set_title("Heatmap das variáveis padronizadas")

        plt.tight_layout()

        self.save_fig("heatmap_a1_standardized_variables")

    def run(self, df):

        graphs = self.choose_graphs()

        if not graphs:
            print("\n[GRAPH ADVISOR] Nenhum gráfico manual selecionado.")
            return []

        generated = []

        if "barras" in graphs:
            self.plot_bar(df)
            generated.append("barras")

        if "boxplot" in graphs:
            self.plot_boxplot(df)
            generated.append("boxplot")

        if "pizza" in graphs:
            self.plot_pie(df)
            generated.append("pizza")

        if "xy" in graphs:
            self.plot_xy(df)
            generated.append("xy")

        if "histograma" in graphs:
            self.plot_histogram(df)
            generated.append("histograma")

        if "correlacao" in graphs:
            self.plot_correlation(df)
            generated.append("correlacao")

        if "heatmap" in graphs:
            self.plot_heatmap(df)
            generated.append("heatmap")

        print("\n[GRAPH ADVISOR] Gráficos A1 gerados em:")
        print(self.graph_dir)

        return generated
