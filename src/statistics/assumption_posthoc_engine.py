import pandas as pd
import numpy as np

from pathlib import Path
from scipy.stats import shapiro, levene, f_oneway, kruskal
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import scikit_posthocs as sp


class AssumptionPostHocEngine:

    def __init__(self, output_dir="outputs"):
        self.output_dir = Path(output_dir)
        self.stats_dir = self.output_dir / "statistics"
        self.stats_dir.mkdir(parents=True, exist_ok=True)

    def run(self, df, group_column):

        results = []

        if group_column is None or group_column not in df.columns:
            print("[ATHENA STATS] Coluna de grupo não encontrada.")
            return None

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        for variable in numeric_cols:

            temp = df[[group_column, variable]].dropna()

            if temp[group_column].nunique() < 2:
                continue

            groups = [
                g[variable].values
                for _, g in temp.groupby(group_column)
                if len(g[variable].values) >= 3
            ]

            if len(groups) < 2:
                continue

            normality_pvalues = []

            for group_values in groups:
                try:
                    _, p_norm = shapiro(group_values)
                    normality_pvalues.append(p_norm)
                except Exception:
                    normality_pvalues.append(np.nan)

            try:
                _, p_levene = levene(*groups)
            except Exception:
                p_levene = np.nan

            normal_ok = all(
                p > 0.05 for p in normality_pvalues
                if not np.isnan(p)
            )

            homogeneity_ok = (
                p_levene > 0.05
                if not np.isnan(p_levene)
                else False
            )

            if normal_ok and homogeneity_ok:

                test_name = "ANOVA"
                _, p_global = f_oneway(*groups)

                try:
                    posthoc = pairwise_tukeyhsd(
                        endog=temp[variable],
                        groups=temp[group_column].astype(str),
                        alpha=0.05
                    )

                    posthoc_path = (
                        self.stats_dir /
                        f"posthoc_tukey_{variable}.txt"
                    )

                    with open(posthoc_path, "w", encoding="utf-8") as f:
                        f.write(str(posthoc))

                except Exception:
                    posthoc_path = None

            else:

                test_name = "Kruskal-Wallis"
                _, p_global = kruskal(*groups)

                try:
                    posthoc_df = sp.posthoc_dunn(
                        temp,
                        val_col=variable,
                        group_col=group_column,
                        p_adjust="bonferroni"
                    )

                    posthoc_path = (
                        self.stats_dir /
                        f"posthoc_dunn_{variable}.xlsx"
                    )

                    posthoc_df.to_excel(posthoc_path)

                except Exception:
                    posthoc_path = None

            results.append({
                "variable": variable,
                "test": test_name,
                "normality_ok": normal_ok,
                "homogeneity_ok": homogeneity_ok,
                "levene_p": p_levene,
                "global_p": p_global,
                "posthoc_file": str(posthoc_path) if posthoc_path else None
            })

        results_df = pd.DataFrame(results)

        output = self.stats_dir / "assumptions_posthoc_results.xlsx"
        results_df.to_excel(output, index=False)

        print("[ATHENA STATS] Pressupostos e pós-testes executados.")

        return output
