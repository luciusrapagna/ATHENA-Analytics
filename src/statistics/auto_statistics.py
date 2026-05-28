import pandas as pd
import numpy as np

from scipy.stats import ttest_ind
from scipy.stats import f_oneway


def run_auto_statistics(df, group_column=None):

    results = []

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if group_column is None:
        return results

    groups = df[group_column].dropna().unique()

    # -----------------------------------------
    # TESTE T
    # -----------------------------------------

    if len(groups) == 2:

        g1 = df[df[group_column] == groups[0]]
        g2 = df[df[group_column] == groups[1]]

        for col in numeric_cols:

            try:

                stat, p = ttest_ind(
                    g1[col],
                    g2[col],
                    nan_policy="omit"
                )

                results.append({
                    "analysis": "t-test",
                    "variable": col,
                    "p_value": p
                })

            except:
                pass

    # -----------------------------------------
    # ANOVA
    # -----------------------------------------

    elif len(groups) >= 3:

        for col in numeric_cols:

            try:

                samples = []

                for g in groups:

                    values = df[
                        df[group_column] == g
                    ][col].dropna()

                    samples.append(values)

                stat, p = f_oneway(*samples)

                results.append({
                    "analysis": "anova",
                    "variable": col,
                    "p_value": p
                })

            except:
                pass

    return pd.DataFrame(results)
