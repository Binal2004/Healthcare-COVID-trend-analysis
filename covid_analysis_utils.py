"""
src/covid_analysis_utils.py
Reusable helper functions for COVID-19 Data Analysis Project
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats

# ── Colour palette ────────────────────────────────────────────────────────────
PALETTE = {
    "primary":   "#003366",
    "danger":    "#CC2936",
    "warning":   "#F4A261",
    "success":   "#2A9D8F",
    "accent":    "#E76F51",
    "light":     "#E8F4FD",
    "grid":      "#EAEAEA",
    "text":      "#1A1A2E",
    "muted":     "#6C757D",
}
VARIANT_COLORS = {"Alpha": "#4E9AF1", "Delta": "#F4A261", "Omicron": "#CC2936", "XBB/BQ": "#8B5CF6"}


def set_plot_style():
    """Apply consistent visual style across all charts."""
    plt.rcParams.update({
        "figure.facecolor":  "white",
        "axes.facecolor":    "white",
        "axes.edgecolor":    "#CCCCCC",
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "axes.grid":         True,
        "grid.color":        PALETTE["grid"],
        "grid.linewidth":    0.6,
        "font.family":       "DejaVu Sans",
        "font.size":         11,
        "axes.titlesize":    14,
        "axes.titleweight":  "bold",
        "axes.labelsize":    11,
        "legend.frameon":    False,
        "xtick.color":       PALETTE["text"],
        "ytick.color":       PALETTE["text"],
    })


def add_watermark(ax, text="COVID-19 Analysis | Portfolio Project 4"):
    ax.text(0.99, 0.01, text, transform=ax.transAxes,
            fontsize=7, color="lightgray", ha="right", va="bottom", style="italic")


def load_datasets(data_dir: str) -> dict:
    """Load all four COVID datasets and return as a dict."""
    paths = {
        "global":      f"{data_dir}/covid_global_trends.csv",
        "countries":   f"{data_dir}/covid_country_comparison.csv",
        "patients":    f"{data_dir}/covid_patient_treatment.csv",
        "vaccination": f"{data_dir}/covid_vaccination_impact.csv",
    }
    dfs = {}
    for key, path in paths.items():
        dfs[key] = pd.read_csv(path, parse_dates=["date"] if key in ["global"] else
                               ["week"] if key == "vaccination" else None)
        print(f"  ✅ Loaded [{key}]: {dfs[key].shape}")
    return dfs


def compute_rolling_metrics(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    """Add 7-day rolling averages for cases, deaths, and positivity."""
    df = df.copy()
    df["rolling_cases"]  = df["new_cases"].rolling(window).mean()
    df["rolling_deaths"] = df["new_deaths"].rolling(window).mean()
    df["cfr_7d"]         = (df["rolling_deaths"] / df["rolling_cases"].replace(0, np.nan) * 100).round(3)
    return df


def classify_wave(date: pd.Series) -> pd.Series:
    """Assign pandemic wave label to each date."""
    conditions = [
        date < "2020-10-01",
        (date >= "2020-10-01") & (date < "2021-05-01"),
        (date >= "2021-05-01") & (date < "2022-03-01"),
        date >= "2022-03-01",
    ]
    labels = ["Wave 1 (Original)", "Wave 2 (Alpha)", "Wave 3 (Delta)", "Wave 4 (Omicron+)"]
    return np.select(conditions, labels, default="Unknown")


def treatment_summary(patient_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate patient data by treatment type."""
    return (
        patient_df.groupby("treatment")
        .agg(
            patients=("patient_id", "count"),
            avg_days=("hospitalization_days", "mean"),
            recovery_rate=("outcome", lambda x: (x == "Recovered").mean() * 100),
            icu_rate=("icu_required", "mean"),
            avg_effectiveness=("treatment_effectiveness_score", "mean"),
        )
        .round(2)
        .sort_values("recovery_rate", ascending=False)
        .reset_index()
    )


def correlation_report(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """Return Pearson correlation matrix for selected columns."""
    return df[cols].corr().round(3)


def generate_kpi_banner(ax, kpis: list):
    """
    Render a row of KPI boxes inside *ax*.
    kpis: list of (label, value, colour) tuples.
    """
    ax.set_xlim(0, len(kpis))
    ax.set_ylim(0, 1)
    ax.axis("off")
    for i, (label, value, colour) in enumerate(kpis):
        rect = mpatches.FancyBboxPatch((i + 0.05, 0.05), 0.88, 0.90,
                                       boxstyle="round,pad=0.05",
                                       facecolor=colour, edgecolor="white",
                                       linewidth=2, alpha=0.92)
        ax.add_patch(rect)
        ax.text(i + 0.49, 0.62, value, ha="center", va="center",
                fontsize=18, fontweight="bold", color="white")
        ax.text(i + 0.49, 0.25, label, ha="center", va="center",
                fontsize=9, color="white", alpha=0.90)


def significance_test(group_a: pd.Series, group_b: pd.Series, label_a="A", label_b="B") -> dict:
    """Run two-sample t-test and return summary dict."""
    stat, pval = stats.ttest_ind(group_a.dropna(), group_b.dropna())
    return {
        "group_a": label_a, "mean_a": round(group_a.mean(), 3),
        "group_b": label_b, "mean_b": round(group_b.mean(), 3),
        "t_statistic": round(stat, 4), "p_value": round(pval, 6),
        "significant": pval < 0.05,
    }


def save_figure(fig, path: str, dpi: int = 150):
    """Save figure with tight layout."""
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  💾 Saved: {path}")
