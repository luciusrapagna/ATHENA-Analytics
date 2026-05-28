import pandas as pd
import numpy as np

from pathlib import Path

from src.visualization.auto_graph_engine import AutoGraphEngine
from src.intelligence.auto_interpretation_engine import AutoInterpretationEngine
from src.reports.auto_word_report import AutoWordReport


class AutoAnalysisEngineV2:

    def __init__(self, output_dir="outputs"):

        self.output_dir = Path(output_dir)

        self.tables_dir = self.output_dir / "tables"
        self.figures_dir = self.output_dir / "figures"
        self.reports_dir = self.output_dir / "reports"

        self.tables_dir.mkdir(parents=True, exist_ok=True)
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def remove_trash_columns(self, df):

        trash_patterns = [
            "unnamed",
            "sem nome",
            "index",
            "level_0"
        ]

        cols_to_drop = []

        for col in df.columns:

            col_str = str(col).strip().lower()

            if any(p in col_str for p in trash_patterns):
                cols_to_drop.append(col)

            elif df[col].isna().all():
                cols_to_drop.append(col)

        return df.drop(columns=cols_to_drop, errors="ignore")

    def detect_numeric_columns(self, df):

        return df.select_dtypes(include=[np.number]).columns.tolist()

    def detect_categorical_columns(self, df):

        return df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

    def export_descriptive_table(
        self,
        df,
        filename="descriptive_table.xlsx"
    ):

        numeric_cols = self.detect_numeric_columns(df)

        if not numeric_cols:
            return None

        table = df[numeric_cols].describe().T

        table["cv_percent"] = (
            table["std"] / table["mean"]
        ) * 100

        output_path = self.tables_dir / filename

        table.to_excel(output_path)

        return output_path

    def export_missing_table(
        self,
        df,
        filename="missing_data_table.xlsx"
    ):

        table = pd.DataFrame({

            "coluna": df.columns,

            "dados_ausentes":
                df.isna().sum().values,

            "percentual_ausente":
                (
                    df.isna().sum().values / len(df)
                ) * 100
        })

        output_path = self.tables_dir / filename

        table.to_excel(output_path, index=False)

        return output_path

    def run(self, df):

        results = {}

        print("\n[ATHENA] Limpando colunas lixo...")

        df_clean = self.remove_trash_columns(df)

        print("[ATHENA] Gerando tabelas automáticas...")

        results["clean_dataframe"] = df_clean
        results["numeric_columns"] = self.detect_numeric_columns(df_clean)
        results["categorical_columns"] = self.detect_categorical_columns(df_clean)

        results["descriptive_table"] = self.export_descriptive_table(df_clean)
        results["missing_table"] = self.export_missing_table(df_clean)

        print("[ATHENA] Gerando gráficos automáticos...")

        graph_engine = AutoGraphEngine(
            output_dir=self.output_dir
        )

        graph_engine.generate_histograms(df_clean)

        print("[ATHENA] Gerando interpretação IA...")

        interpretation_engine = AutoInterpretationEngine()

        interpretation = (
            interpretation_engine.generate_basic_interpretation(
                results["numeric_columns"]
            )
        )

        print("[ATHENA] Gerando relatório Word...")

        report_engine = AutoWordReport(
            output_dir=self.output_dir
        )

        results["word_report"] = report_engine.generate(
            interpretation
        )

        print("[ATHENA] Engine V2 finalizada.")

        return results
