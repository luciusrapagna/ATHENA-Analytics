import numpy as np
import pandas as pd

from scipy.stats import shapiro, levene


class DataDrivenAdvisorV3:

    def __init__(self):
        pass

    def inspect_dataset(self, df, group_column=None):

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        report = {
            "n_rows": int(df.shape[0]),
            "n_columns": int(df.shape[1]),
            "numeric_columns": numeric_cols,
            "n_numeric": len(numeric_cols),
            "group_column": group_column,
            "n_groups": None,
            "normality_ok": None,
            "homogeneity_ok": None,
            "many_zeros": False,
            "multivariate_ready": False
        }

        if group_column and group_column in df.columns:
            report["n_groups"] = int(df[group_column].nunique(dropna=True))

        if len(numeric_cols) >= 2:
            report["multivariate_ready"] = True

        numeric_df = df[numeric_cols].dropna()

        if not numeric_df.empty:
            zero_ratio = (numeric_df == 0).sum().sum() / numeric_df.size
            report["many_zeros"] = bool(zero_ratio > 0.30)

        normality_results = []

        for col in numeric_cols:
            values = df[col].dropna()

            if len(values) >= 3 and len(values) <= 5000:
                try:
                    _, p = shapiro(values)
                    normality_results.append(p > 0.05)
                except Exception:
                    pass

        if normality_results:
            report["normality_ok"] = bool(all(normality_results))

        if group_column and group_column in df.columns and numeric_cols:

            homogeneity_results = []

            for col in numeric_cols:
                temp = df[[group_column, col]].dropna()

                groups = [
                    g[col].values
                    for _, g in temp.groupby(group_column)
                    if len(g[col].values) >= 3
                ]

                if len(groups) >= 2:
                    try:
                        _, p = levene(*groups)
                        homogeneity_results.append(p > 0.05)
                    except Exception:
                        pass

            if homogeneity_results:
                report["homogeneity_ok"] = bool(all(homogeneity_results))

        return report

    def recommend(self, df, domain="generic", group_column=None):

        report = self.inspect_dataset(
            df,
            group_column=group_column
        )

        analyses = []

        reasons = []

        analyses.append("estatistica")
        reasons.append(
            "Estatística descritiva recomendada para caracterizar o conjunto de dados."
        )

        if report["group_column"] and report["n_groups"] and report["n_groups"] >= 2:

            if report["normality_ok"] and report["homogeneity_ok"]:

                analyses += [
                    "anova",
                    "pressupostos_posthoc"
                ]

                reasons.append(
                    "ANOVA recomendada porque há grupos definidos, normalidade e homogeneidade foram compatíveis."
                )

                reasons.append(
                    "Tukey recomendado para identificar quais grupos diferem após teste global significativo."
                )

            else:

                analyses += [
                    "pressupostos_posthoc"
                ]

                reasons.append(
                    "Testes não paramétricos e pós-teste de Dunn recomendados porque normalidade ou homogeneidade podem não estar atendidas."
                )

        if report["multivariate_ready"]:

            analyses.append("pca")

            reasons.append(
                "PCA recomendada porque há múltiplas variáveis numéricas para exploração multivariada."
            )

        if report["n_rows"] >= 10 and report["n_numeric"] >= 2:

            analyses.append("kmeans")

            reasons.append(
                "KMeans recomendado para detectar perfis ou agrupamentos com base nas variáveis numéricas."
            )

        if report["n_rows"] >= 15 and report["n_numeric"] >= 2:

            analyses += [
                "umap",
                "hdbscan"
            ]

            reasons.append(
                "UMAP e HDBSCAN recomendados para identificar padrões não lineares e clusters latentes."
            )

        if domain in [
            "ecologia",
            "oceanografia",
            "citometria_ambiental"
        ] or report["many_zeros"]:

            analyses.append("similaridade")

            reasons.append(
                "Análises de similaridade recomendadas para dados ambientais, ecológicos, citométricos ou com muitos zeros."
            )

        analyses += [
            "graficos",
            "relatorio_word"
        ]

        reasons.append(
            "Gráficos e relatório Word recomendados para comunicação científica dos resultados."
        )

        analyses = list(dict.fromkeys(analyses))

        return {
            "domain": domain,
            "data_report": report,
            "recommended_analyses": analyses,
            "methodological_reasons": reasons
        }

    def print_recommendation(self, recommendation):

        print("\n===================================")
        print("ATHENA v3 - DATA-DRIVEN ADVISOR")
        print("===================================")

        print(f"\nDomínio detectado: {recommendation['domain']}")

        print("\nDiagnóstico dos dados:")
        for key, value in recommendation["data_report"].items():
            print(f"- {key}: {value}")

        print("\nPlano metodológico recomendado:")
        for analysis in recommendation["recommended_analyses"]:
            print(f"✓ {analysis}")

        print("\nJustificativas:")
        for reason in recommendation["methodological_reasons"]:
            print(f"→ {reason}")
