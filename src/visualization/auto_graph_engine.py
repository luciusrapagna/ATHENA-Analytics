import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path


class AutoGraphEngine:

    def __init__(self, output_dir="outputs"):

        self.output_dir = Path(output_dir)
        self.figures_dir = self.output_dir / "figures"

        self.figures_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def generate_histograms(self, df):

        numeric_cols = df.select_dtypes(
            include=[np.number]
        ).columns

        for col in numeric_cols:

            try:

                plt.figure(figsize=(8,5))

                df[col].dropna().hist()

                plt.title(f"Distribuição - {col}")

                plt.xlabel(col)

                plt.ylabel("Frequência")

                output = (
                    self.figures_dir /
                    f"hist_{col}.png"
                )

                plt.savefig(
                    output,
                    dpi=300,
                    bbox_inches="tight"
                )

                plt.close()

            except:
                pass
