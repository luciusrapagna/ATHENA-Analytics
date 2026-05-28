import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from matplotlib.patches import Ellipse


def _safe_name(name):
    return (
        str(name)
        .replace("/", "_")
        .replace("\\", "_")
        .replace("\n", "_")
        .replace(" ", "_")
    )


def _confidence_ellipse(x, y, ax, n_std=2.0, edgecolor="black"):

    if len(x) < 3:
        return

    cov = np.cov(x, y)

    if np.any(np.isnan(cov)):
        return

    vals, vecs = np.linalg.eigh(cov)

    order = vals.argsort()[::-1]
    vals = vals[order]
    vecs = vecs[:, order]

    theta = np.degrees(
        np.arctan2(*vecs[:, 0][::-1])
    )

    width, height = 2 * n_std * np.sqrt(vals)

    ellipse = Ellipse(
        xy=(np.mean(x), np.mean(y)),
        width=width,
        height=height,
        angle=theta,
        fill=False,
        linestyle="--",
        linewidth=1.8,
        edgecolor=edgecolor
    )

    ax.add_patch(ellipse)


def _apply_a1_style():

    plt.rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "font.size": 11,
        "axes.titlesize": 16,
        "axes.labelsize": 13,
        "legend.fontsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "axes.spines.top": True,
        "axes.spines.right": True,
        "axes.grid": False
    })


def run_pca(df, group_column=None, output_path="outputs"):

    _apply_a1_style()

    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    numeric_df = df.select_dtypes(include=[np.number]).copy()
    numeric_df = numeric_df.loc[:, numeric_df.var(skipna=True) > 0]
    numeric_df = numeric_df.dropna()

    if numeric_df.shape[1] < 2:
        raise ValueError("PCA requer pelo menos duas variáveis numéricas.")

    scaler = StandardScaler()
    X = scaler.fit_transform(numeric_df)

    pca = PCA(n_components=2)
    coords = pca.fit_transform(X)

    explained = pca.explained_variance_ratio_ * 100

    scores = pd.DataFrame(
        {
            "Dim1": coords[:, 0],
            "Dim2": coords[:, 1]
        },
        index=numeric_df.index
    )

    if group_column and group_column in df.columns:
        scores[group_column] = df.loc[numeric_df.index, group_column].astype(str).values
    else:
        group_column = "Grupo"
        scores[group_column] = "Amostras"

    loadings = pd.DataFrame(
        pca.components_.T,
        columns=["Dim1", "Dim2"],
        index=numeric_df.columns
    )

    fig, ax = plt.subplots(figsize=(9, 8))

    groups = scores[group_column].dropna().unique()

    markers = ["o", ">", "s", "^", "D", "P", "X", "v", "<"]
    colors = [
        "black",
        "red",
        "blue",
        "green",
        "purple",
        "orange",
        "brown",
        "gray",
        "magenta"
    ]

    # -----------------------------
    # Pontos e elipses
    # -----------------------------
    for i, group in enumerate(groups):

        subset = scores[scores[group_column] == group]

        marker = markers[i % len(markers)]
        color = colors[i % len(colors)]

        ax.scatter(
            subset["Dim1"],
            subset["Dim2"],
            s=45,
            marker=marker,
            color=color,
            label=str(group),
            alpha=0.90
        )

        _confidence_ellipse(
            subset["Dim1"].values,
            subset["Dim2"].values,
            ax,
            n_std=2.0,
            edgecolor=color
        )

        # centroide do grupo
        cx = subset["Dim1"].mean()
        cy = subset["Dim2"].mean()

        ax.arrow(
            0,
            0,
            cx,
            cy,
            color="navy",
            linewidth=2.5,
            head_width=0.06,
            length_includes_head=True
        )

        ax.text(
            cx * 1.08,
            cy * 1.08,
            str(group),
            color="navy",
            fontsize=15,
            fontstyle="italic"
        )

    # -----------------------------
    # Vetores das variáveis
    # -----------------------------
    max_score = np.max(
        np.abs(scores[["Dim1", "Dim2"]].values)
    )

    max_loading = np.max(
        np.abs(loadings[["Dim1", "Dim2"]].values)
    )

    scale = max_score / max_loading * 0.55

    for variable in loadings.index:

        x = loadings.loc[variable, "Dim1"] * scale
        y = loadings.loc[variable, "Dim2"] * scale

        ax.arrow(
            0,
            0,
            x,
            y,
            color="black",
            linewidth=0.9,
            head_width=0.035,
            length_includes_head=True
        )

        ax.text(
            x * 1.08,
            y * 1.08,
            str(variable),
            fontsize=10,
            ha="center",
            va="center"
        )

    # -----------------------------
    # Eixos
    # -----------------------------
    ax.axhline(
        0,
        color="black",
        linestyle=(0, (2, 3)),
        linewidth=0.9
    )

    ax.axvline(
        0,
        color="black",
        linestyle=(0, (2, 3)),
        linewidth=0.9
    )

    ax.set_xlabel(f"Dim 1 ({explained[0]:.1f}%)")
    ax.set_ylabel(f"Dim 2 ({explained[1]:.1f}%)")

    ax.set_title("PCA - Biplot")

    ax.legend(
        title="Legenda:",
        frameon=False,
        loc="upper right"
    )

    ax.text(
        0.02,
        0.02,
        "Elipses: 95% de confiança\nMétodo: PCA",
        transform=ax.transAxes,
        fontsize=9,
        va="bottom"
    )

    plt.tight_layout()

    png_path = output_path / "pca_biplot_a1.png"
    svg_path = output_path / "pca_biplot_a1.svg"
    scores_path = output_path / "pca_scores.xlsx"
    loadings_path = output_path / "pca_loadings.xlsx"

    plt.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.savefig(svg_path, bbox_inches="tight")
    plt.close()

    scores.to_excel(scores_path)
    loadings.to_excel(loadings_path)

    return {
        "scores": scores_path,
        "loadings": loadings_path,
        "figure_png": png_path,
        "figure_svg": svg_path,
        "explained_variance": explained
    }
