import pandas as pd
import numpy as np

from pathlib import Path
from scipy.spatial.distance import pdist, squareform
from sklearn.manifold import MDS
from skbio.stats.distance import DistanceMatrix, permanova, anosim


class SimilarityAnalysisEngine:

    def __init__(self, output_dir="outputs"):
        self.output_dir = Path(output_dir)
        self.similarity_dir = self.output_dir / "similarity"
        self.similarity_dir.mkdir(parents=True, exist_ok=True)

    def prepare_matrix(self, df):

        numeric_df = df.select_dtypes(include=[np.number]).copy()
        numeric_df = numeric_df.dropna()
        numeric_df = numeric_df.loc[:, numeric_df.var() > 0]

        if numeric_df.shape[0] < 3 or numeric_df.shape[1] < 2:
            return None

        return numeric_df

    def run(self, df, group_column=None):

        numeric_df = self.prepare_matrix(df)

        if numeric_df is None:
            print("[ATHENA SIMILARITY] Dados insuficientes.")
            return None

        distance = squareform(
            pdist(numeric_df, metric="braycurtis")
        )

        distance_df = pd.DataFrame(
            distance,
            index=numeric_df.index,
            columns=numeric_df.index
        )

        distance_path = self.similarity_dir / "bray_curtis_distance_matrix.xlsx"
        distance_df.to_excel(distance_path)

        model = MDS(
            n_components=2,
            dissimilarity="precomputed",
            metric=False,
            random_state=42,
            normalized_stress="auto"
        )

        coords = model.fit_transform(distance)

        nmds_df = pd.DataFrame({
            "NMDS1": coords[:, 0],
            "NMDS2": coords[:, 1]
        }, index=numeric_df.index)

        if group_column and group_column in df.columns:
            nmds_df[group_column] = df.loc[numeric_df.index, group_column].values

        nmds_path = self.similarity_dir / "nmds_coordinates.xlsx"
        nmds_df.to_excel(nmds_path)

        results = {
            "bray_curtis": str(distance_path),
            "nmds": str(nmds_path)
        }

        if group_column and group_column in df.columns:

            valid_groups = df.loc[numeric_df.index, group_column].astype(str)
            dm = DistanceMatrix(distance, ids=list(map(str, numeric_df.index)))

            try:
                permanova_result = permanova(
                    dm,
                    valid_groups,
                    permutations=999
                )

                permanova_path = self.similarity_dir / "permanova_results.txt"

                with open(permanova_path, "w", encoding="utf-8") as f:
                    f.write(str(permanova_result))

                results["permanova"] = str(permanova_path)

            except Exception as e:
                results["permanova_error"] = str(e)

            try:
                anosim_result = anosim(
                    dm,
                    valid_groups,
                    permutations=999
                )

                anosim_path = self.similarity_dir / "anosim_results.txt"

                with open(anosim_path, "w", encoding="utf-8") as f:
                    f.write(str(anosim_result))

                results["anosim"] = str(anosim_path)

            except Exception as e:
                results["anosim_error"] = str(e)

        summary_path = self.similarity_dir / "similarity_summary.xlsx"
        pd.DataFrame([results]).to_excel(summary_path, index=False)

        print("[ATHENA SIMILARITY] Similaridade executada.")

        return results
