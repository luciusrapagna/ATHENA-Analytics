import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from scipy.spatial.distance import pdist, squareform
from sklearn.manifold import MDS

from skbio.stats.distance import DistanceMatrix
from skbio.stats.distance import permanova, anosim


class EcologicalAnalysisEngine:

    def __init__(self, output_dir="outputs"):
        self.output_dir = Path(output_dir)
        self.ecology_dir = self.output_dir / "ecology"
        self.figures_dir = self.output_dir / "figures"

        self.ecology_dir.mkdir(parents=True, exist_ok=True)
        self.figures_dir.mkdir(parents=True, exist_ok=True)

    def prepare_numeric_matrix(self, df):
        numeric_df = df.select_dtypes(include=[np.number])
        numeric_df = numeric_df.dropna()
        numeric_df = numeric_df.loc[:, numeric_df.var() > 0]
        return numeric_df

    def bray_curtis_distance(self, numeric_df):
        return squareform(pdist(numeric_df, metric="braycurtis"))

    def run_nmds(self, df, group_column=None):
        numeric_df = self.prepare_numeric_matrix(df)

        if numeric_df.shape[0] < 3 or numeric_df.shape[1] < 2:
            return None

        dist_matrix = self.bray_curtis_distance(numeric_df)

        model = MDS(
            n_components=2,
            dissimilarity="precomputed",
            random_state=42,
            metric=False,
            normalized_stress="auto"
        )

        coords = model.fit_transform(dist_matrix)

        nmds_df = pd.DataFrame({
            "NMDS1": coords[:, 0],
            "NMDS2": coords[:, 1]
        }, index=numeric_df.index)

        if group_column and group_column in df.columns:
            nmds_df[group_column] = df.loc[numeric_df.index, group_column].values

        output_xlsx = self.ecology_dir / "nmds_coordinates.xlsx"
        nmds_df.to_excel(output_xlsx, index=False)

        output_png = self.figures_dir / "nmds_plot.png"

        plt.figure(figsize=(8, 6))

        if group_column and group_column in nmds_df.columns:
            for group in nmds_df[group_column].dropna().unique():
                subset = nmds_df[nmds_df[group_column] == group]
                plt.scatter(subset["NMDS1"], subset["NMDS2"], label=str(group), alpha=0.8)
            plt.legend(title=group_column, bbox_to_anchor=(1.05, 1), loc="upper left")
        else:
            plt.scatter(nmds_df["NMDS1"], nmds_df["NMDS2"], alpha=0.8)

        plt.title("NMDS - Bray-Curtis")
        plt.xlabel("NMDS1")
        plt.ylabel("NMDS2")
        plt.tight_layout()
        plt.savefig(output_png, dpi=300, bbox_inches="tight")
        plt.close()

        return {
            "coordinates": output_xlsx,
            "figure": output_png
        }

    def run_permanova(self, df, group_column):
        numeric_df = self.prepare_numeric_matrix(df)
        valid_df = df.loc[numeric_df.index]

        if group_column not in valid_df.columns:
            return None

        dist_matrix = self.bray_curtis_distance(numeric_df)
        dm = DistanceMatrix(dist_matrix, ids=list(map(str, numeric_df.index)))

        result = permanova(dm, valid_df[group_column].astype(str), permutations=999)

        result_df = result.to_frame(name="valor").reset_index()
        result_df.columns = ["métrica", "valor"]

        output = self.ecology_dir / "permanova_results.xlsx"
        result_df.to_excel(output, index=False)

        return output

    def run_anosim(self, df, group_column):
        numeric_df = self.prepare_numeric_matrix(df)
        valid_df = df.loc[numeric_df.index]

        if group_column not in valid_df.columns:
            return None

        dist_matrix = self.bray_curtis_distance(numeric_df)
        dm = DistanceMatrix(dist_matrix, ids=list(map(str, numeric_df.index)))

        result = anosim(dm, valid_df[group_column].astype(str), permutations=999)

        result_df = result.to_frame(name="valor").reset_index()
        result_df.columns = ["métrica", "valor"]

        output = self.ecology_dir / "anosim_results.xlsx"
        result_df.to_excel(output, index=False)

        return output

    def run(self, df, group_column=None):
        results = {}

        print("\n[ATHENA ECOLOGY] Executando NMDS + gráfico...")
        results["nmds"] = self.run_nmds(df, group_column=group_column)

        if group_column:
            print("[ATHENA ECOLOGY] Executando PERMANOVA...")
            results["permanova"] = self.run_permanova(df, group_column)

            print("[ATHENA ECOLOGY] Executando ANOSIM...")
            results["anosim"] = self.run_anosim(df, group_column)

        print("[ATHENA ECOLOGY] Finalizado.")
        return results
