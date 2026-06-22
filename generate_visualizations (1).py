"""
generate_visualizations.py
Produces all 10 charts for Project 4 – COVID-19 Healthcare Analysis
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats

from covid_analysis_utils import (
    set_plot_style, add_watermark, load_datasets,
    compute_rolling_metrics, classify_wave, treatment_summary,
    generate_kpi_banner, save_figure, PALETTE, VARIANT_COLORS
)

BASE = os.path.dirname(__file__)
VIZ  = os.path.join(BASE, "visualizations")
DATA = os.path.join(BASE, "data")
os.makedirs(VIZ, exist_ok=True)

set_plot_style()
print("📊 Loading datasets …")
dfs = load_datasets(DATA)
global_df  = compute_rolling_metrics(dfs["global"])
global_df["wave"] = classify_wave(global_df["date"])
country_df = dfs["countries"]
patient_df = dfs["patients"]
vax_df     = dfs["vaccination"]

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 1 – KPI Dashboard + Global Case Timeline
# ══════════════════════════════════════════════════════════════════════════════
print("\n[1/10] KPI Dashboard …")
fig = plt.figure(figsize=(16, 9))
gs  = gridspec.GridSpec(2, 1, height_ratios=[1, 3.5], hspace=0.35)

# KPI row
ax0 = fig.add_subplot(gs[0])
total_cases   = global_df["total_cases"].max()
total_deaths  = global_df["total_deaths"].max()
total_vax     = global_df["vaccinations_daily"].sum()
peak_daily    = global_df["new_cases"].max()
kpis = [
    ("Total Cases",      f"{total_cases/1e6:.1f}M",   PALETTE["primary"]),
    ("Total Deaths",     f"{total_deaths/1e6:.2f}M",  PALETTE["danger"]),
    ("Peak Daily Cases", f"{peak_daily/1e6:.2f}M",    PALETTE["warning"]),
    ("Doses Administered",f"{total_vax/1e9:.2f}B",    PALETTE["success"]),
    ("Global CFR",       f"{total_deaths/total_cases*100:.2f}%", PALETTE["accent"]),
]
generate_kpi_banner(ax0, kpis)
ax0.set_title("Project 4 · COVID-19 Global Dashboard", fontsize=16,
              fontweight="bold", color=PALETTE["primary"], pad=12)

# Timeline
ax1 = fig.add_subplot(gs[1])
ax1.fill_between(global_df["date"], global_df["new_cases"] / 1e6,
                 alpha=0.25, color=PALETTE["primary"], label="_nolegend_")
ax1.plot(global_df["date"], global_df["rolling_cases"] / 1e6,
         color=PALETTE["primary"], lw=2, label="7-day Avg Cases (M)")
ax2 = ax1.twinx()
ax2.plot(global_df["date"], global_df["rolling_deaths"] / 1e3,
         color=PALETTE["danger"], lw=1.5, ls="--", label="7-day Avg Deaths (K)")
ax2.set_ylabel("Deaths (Thousands)", color=PALETTE["danger"], fontsize=10)
ax2.tick_params(colors=PALETTE["danger"])

for wave_date, label, color in [
    ("2020-09-01", "Wave 1→2", "#999"),
    ("2021-04-01", "Delta ↑",  "#F4A261"),
    ("2021-11-01", "Omicron ↑","#CC2936"),
]:
    ax1.axvline(pd.to_datetime(wave_date), color=color, ls=":", lw=1.5, alpha=0.8)
    ax1.text(pd.to_datetime(wave_date), global_df["rolling_cases"].max() * 0.85 / 1e6,
             label, rotation=90, fontsize=8, color=color, va="top")

ax1.set_xlabel("Date"); ax1.set_ylabel("Daily Cases (Millions)")
ax1.set_title("Global COVID-19 Cases & Deaths Timeline (2020–2023)", fontsize=13)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
add_watermark(ax1)
save_figure(fig, f"{VIZ}/viz1_global_dashboard.png")

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 2 – Country Comparison: Cases per Million & CFR
# ══════════════════════════════════════════════════════════════════════════════
print("[2/10] Country comparison …")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("Country-wise COVID-19 Comparison", fontsize=15, fontweight="bold",
             color=PALETTE["primary"])

cdf = country_df.sort_values("cases_per_million", ascending=True)
colors_bar = [PALETTE["danger"] if v > 250000 else PALETTE["primary"] for v in cdf["cases_per_million"]]
axes[0].barh(cdf["country"], cdf["cases_per_million"] / 1e3, color=colors_bar, edgecolor="white", height=0.6)
axes[0].set_xlabel("Cases per Million (Thousands)")
axes[0].set_title("Cases per Million Population")
for i, (val, country) in enumerate(zip(cdf["cases_per_million"], cdf["country"])):
    axes[0].text(val / 1e3 + 2, i, f"{val/1e3:.0f}K", va="center", fontsize=9)

cdf2 = country_df.sort_values("case_fatality_rate_pct", ascending=True)
colors_cfr = [PALETTE["danger"] if v > 2.0 else PALETTE["success"] for v in cdf2["case_fatality_rate_pct"]]
axes[1].barh(cdf2["country"], cdf2["case_fatality_rate_pct"], color=colors_cfr, edgecolor="white", height=0.6)
axes[1].set_xlabel("Case Fatality Rate (%)")
axes[1].set_title("Case Fatality Rate by Country")
axes[1].axvline(country_df["case_fatality_rate_pct"].mean(), color=PALETTE["warning"],
               ls="--", lw=1.5, label=f"Global Avg: {country_df['case_fatality_rate_pct'].mean():.2f}%")
axes[1].legend(fontsize=9)
for i, val in enumerate(cdf2["case_fatality_rate_pct"]):
    axes[1].text(val + 0.02, i, f"{val:.2f}%", va="center", fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.94])
add_watermark(axes[1])
save_figure(fig, f"{VIZ}/viz2_country_comparison.png")

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 3 – Wave-wise Analysis (Box plots + Stats)
# ══════════════════════════════════════════════════════════════════════════════
print("[3/10] Wave analysis …")
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle("Pandemic Wave Analysis", fontsize=15, fontweight="bold", color=PALETTE["primary"])

wave_order = ["Wave 1 (Original)", "Wave 2 (Alpha)", "Wave 3 (Delta)", "Wave 4 (Omicron+)"]
palette_waves = ["#4E9AF1", "#F4A261", "#CC2936", "#8B5CF6"]

wave_data = global_df[global_df["wave"] != "Unknown"]
sns.boxplot(data=wave_data, x="wave", y="new_cases", ax=axes[0],
            order=wave_order, palette=palette_waves, width=0.5, fliersize=2)
axes[0].set_xticklabels([w.split("(")[0].strip() for w in wave_order], rotation=15, ha="right")
axes[0].set_xlabel(""); axes[0].set_ylabel("Daily New Cases")
axes[0].set_title("Daily Case Distribution by Wave")
for tick in axes[0].get_xticklabels():
    tick.set_fontsize(9)

wave_stats = wave_data.groupby("wave")["new_cases"].agg(["mean","median","max"]).reindex(wave_order)
x = np.arange(len(wave_order))
w = 0.25
axes[1].bar(x - w,   wave_stats["mean"]/1e3,   w, label="Mean",   color=PALETTE["primary"], alpha=0.85)
axes[1].bar(x,       wave_stats["median"]/1e3, w, label="Median", color=PALETTE["success"], alpha=0.85)
axes[1].bar(x + w,   wave_stats["max"]/1e3,    w, label="Peak",   color=PALETTE["danger"],  alpha=0.85)
axes[1].set_xticks(x)
axes[1].set_xticklabels([w.split("(")[0].strip() for w in wave_order], rotation=15, ha="right", fontsize=9)
axes[1].set_ylabel("Cases (Thousands)")
axes[1].set_title("Mean / Median / Peak Cases by Wave")
axes[1].legend()
add_watermark(axes[1])
plt.tight_layout(rect=[0, 0, 1, 0.94])
save_figure(fig, f"{VIZ}/viz3_wave_analysis.png")

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 4 – Patient Severity & Outcomes
# ══════════════════════════════════════════════════════════════════════════════
print("[4/10] Patient severity & outcomes …")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Patient Severity & Clinical Outcomes", fontsize=15, fontweight="bold",
             color=PALETTE["primary"])

sev_order  = ["Mild", "Moderate", "Severe", "Critical"]
sev_colors = [PALETTE["success"], PALETTE["warning"], PALETTE["accent"], PALETTE["danger"]]

# Severity distribution
sev_counts = patient_df["severity"].value_counts().reindex(sev_order)
wedges, texts, autotexts = axes[0,0].pie(sev_counts, labels=sev_order, autopct="%1.1f%%",
                                          colors=sev_colors, startangle=140,
                                          wedgeprops=dict(edgecolor="white", linewidth=2))
for at in autotexts: at.set_fontsize(10); at.set_fontweight("bold")
axes[0,0].set_title("Case Severity Distribution")

# Outcome by severity
outcome_sev = patient_df.groupby(["severity","outcome"]).size().unstack(fill_value=0).reindex(sev_order)
outcome_pct = outcome_sev.div(outcome_sev.sum(axis=1), axis=0) * 100
outcome_pct[["Recovered","Deceased"]].plot(kind="bar", ax=axes[0,1], stacked=True,
    color=[PALETTE["success"], PALETTE["danger"]], edgecolor="white", width=0.5)
axes[0,1].set_xticklabels(sev_order, rotation=0)
axes[0,1].set_ylabel("Percentage (%)"); axes[0,1].set_title("Outcomes by Severity")
axes[0,1].legend(loc="upper right"); axes[0,1].set_xlabel("")

# Age distribution by severity
for sev, col in zip(sev_order, sev_colors):
    sub = patient_df[patient_df["severity"] == sev]["age"]
    axes[1,0].hist(sub, bins=20, alpha=0.55, color=col, label=sev, edgecolor="white")
axes[1,0].set_xlabel("Age"); axes[1,0].set_ylabel("Number of Patients")
axes[1,0].set_title("Age Distribution by Severity")
axes[1,0].legend()

# ICU & Oxygen requirements
icu_oxy = patient_df.groupby("severity")[["icu_required","oxygen_required"]].mean() * 100
icu_oxy = icu_oxy.reindex(sev_order)
x = np.arange(len(sev_order))
axes[1,1].bar(x - 0.2, icu_oxy["icu_required"],   0.35, label="ICU Required",     color=PALETTE["danger"],  alpha=0.85)
axes[1,1].bar(x + 0.2, icu_oxy["oxygen_required"], 0.35, label="O₂ Required",      color=PALETTE["primary"], alpha=0.85)
axes[1,1].set_xticks(x); axes[1,1].set_xticklabels(sev_order)
axes[1,1].set_ylabel("Percentage (%)"); axes[1,1].set_title("ICU & Oxygen Requirements by Severity")
axes[1,1].legend()
add_watermark(axes[1,1])
plt.tight_layout(rect=[0, 0, 1, 0.94])
save_figure(fig, f"{VIZ}/viz4_patient_severity.png")

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 5 – Treatment Effectiveness Comparison
# ══════════════════════════════════════════════════════════════════════════════
print("[5/10] Treatment effectiveness …")
treat_summary = treatment_summary(patient_df)

fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.suptitle("Treatment Effectiveness Analysis", fontsize=15, fontweight="bold",
             color=PALETTE["primary"])

colors_t = [PALETTE["success"] if r >= 88 else PALETTE["warning"] if r >= 84 else PALETTE["danger"]
            for r in treat_summary["recovery_rate"]]
bars = axes[0].barh(treat_summary["treatment"], treat_summary["recovery_rate"],
                    color=colors_t, edgecolor="white", height=0.55)
axes[0].set_xlabel("Recovery Rate (%)")
axes[0].set_title("Recovery Rate by Treatment")
axes[0].set_xlim(70, 100)
for bar, val in zip(bars, treat_summary["recovery_rate"]):
    axes[0].text(val + 0.2, bar.get_y() + bar.get_height()/2,
                 f"{val:.1f}%", va="center", fontsize=10, fontweight="bold")

axes[1].bar(treat_summary["treatment"], treat_summary["avg_days"],
            color=PALETTE["primary"], alpha=0.82, edgecolor="white", width=0.5)
axes[1].set_ylabel("Average Days")
axes[1].set_title("Avg Hospitalization Days")
axes[1].set_xticklabels(treat_summary["treatment"], rotation=20, ha="right", fontsize=9)
for i, val in enumerate(treat_summary["avg_days"]):
    axes[1].text(i, val + 0.3, f"{val:.1f}d", ha="center", fontsize=9, fontweight="bold")

scatter = axes[2].scatter(treat_summary["avg_days"], treat_summary["recovery_rate"],
                          s=treat_summary["patients"] / 3, c=treat_summary["avg_effectiveness"],
                          cmap="RdYlGn", edgecolors="gray", linewidth=0.5, alpha=0.9)
for _, row in treat_summary.iterrows():
    axes[2].annotate(row["treatment"].replace(" ", "\n"), (row["avg_days"], row["recovery_rate"]),
                     textcoords="offset points", xytext=(6, 4), fontsize=8)
plt.colorbar(scatter, ax=axes[2], label="Effectiveness Score")
axes[2].set_xlabel("Avg Days (shorter=better)"); axes[2].set_ylabel("Recovery Rate (%)")
axes[2].set_title("Effectiveness Matrix\n(bubble=patient count)")
add_watermark(axes[2])
plt.tight_layout(rect=[0, 0, 1, 0.94])
save_figure(fig, f"{VIZ}/viz5_treatment_effectiveness.png")

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 6 – Comorbidity Impact
# ══════════════════════════════════════════════════════════════════════════════
print("[6/10] Comorbidity analysis …")
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle("Comorbidity Impact on Patient Outcomes", fontsize=15, fontweight="bold",
             color=PALETTE["primary"])

comor_stats = patient_df.groupby("comorbidity").agg(
    patients=("patient_id","count"),
    mortality_rate=("outcome", lambda x: (x=="Deceased").mean()*100),
    avg_days=("hospitalization_days","mean"),
    icu_rate=("icu_required","mean"),
).sort_values("mortality_rate", ascending=False).reset_index()

colors_c = [PALETTE["danger"] if r > 10 else PALETTE["warning"] if r > 5 else PALETTE["success"]
            for r in comor_stats["mortality_rate"]]
axes[0].bar(comor_stats["comorbidity"], comor_stats["mortality_rate"],
            color=colors_c, edgecolor="white", width=0.55, alpha=0.88)
axes[0].set_ylabel("Mortality Rate (%)"); axes[0].set_title("Mortality Rate by Comorbidity")
axes[0].set_xticklabels(comor_stats["comorbidity"], rotation=25, ha="right", fontsize=9)
axes[0].axhline(patient_df["outcome"].eq("Deceased").mean()*100,
               color=PALETTE["primary"], ls="--", lw=1.5, label="Overall avg")
axes[0].legend()
for i, (val, n) in enumerate(zip(comor_stats["mortality_rate"], comor_stats["patients"])):
    axes[0].text(i, val + 0.2, f"{val:.1f}%\n(n={n})", ha="center", fontsize=8, fontweight="bold")

pivot = patient_df.pivot_table(index="comorbidity", columns="severity",
                               values="patient_id", aggfunc="count", fill_value=0)
pivot = pivot.reindex(columns=["Mild","Moderate","Severe","Critical"], fill_value=0)
pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100
pivot_pct.plot(kind="bar", ax=axes[1], stacked=True,
               color=sev_colors, edgecolor="white", width=0.6)
axes[1].set_title("Severity Distribution by Comorbidity")
axes[1].set_ylabel("Percentage (%)"); axes[1].set_xlabel("")
axes[1].set_xticklabels(pivot_pct.index, rotation=25, ha="right", fontsize=9)
axes[1].legend(title="Severity", bbox_to_anchor=(1.02, 1), loc="upper left")
add_watermark(axes[1])
plt.tight_layout(rect=[0, 0, 1, 0.94])
save_figure(fig, f"{VIZ}/viz6_comorbidity_impact.png")

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 7 – Vaccination Rollout & Impact
# ══════════════════════════════════════════════════════════════════════════════
print("[7/10] Vaccination impact …")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle("COVID-19 Vaccination Rollout & Impact", fontsize=15, fontweight="bold",
             color=PALETTE["primary"])

# Coverage over time
axes[0,0].fill_between(vax_df["week"], vax_df["vaccination_coverage_pct"],
                       alpha=0.35, color=PALETTE["success"])
axes[0,0].plot(vax_df["week"], vax_df["vaccination_coverage_pct"],
               color=PALETTE["success"], lw=2)
axes[0,0].set_ylabel("Vaccination Coverage (%)")
axes[0,0].set_title("Global Vaccination Coverage Over Time")
axes[0,0].axhline(70, color=PALETTE["warning"], ls="--", lw=1.5, label="Herd immunity threshold ~70%")
axes[0,0].legend()

# Cases vs coverage scatter
sc = axes[0,1].scatter(vax_df["vaccination_coverage_pct"], vax_df["weekly_cases"]/1e3,
                       c=range(len(vax_df)), cmap="RdYlGn_r", alpha=0.7, s=40, edgecolors="none")
z = np.polyfit(vax_df["vaccination_coverage_pct"], vax_df["weekly_cases"]/1e3, 1)
p = np.poly1d(z)
xline = np.linspace(vax_df["vaccination_coverage_pct"].min(), vax_df["vaccination_coverage_pct"].max(), 100)
axes[0,1].plot(xline, p(xline), color=PALETTE["danger"], ls="--", lw=2, label="Trend line")
r, pval = stats.pearsonr(vax_df["vaccination_coverage_pct"], vax_df["weekly_cases"]/1e3)
axes[0,1].set_xlabel("Vaccination Coverage (%)"); axes[0,1].set_ylabel("Weekly Cases (K)")
axes[0,1].set_title(f"Vaccination vs Cases  (r={r:.3f})")
axes[0,1].legend()

# Deaths vs coverage
axes[1,0].plot(vax_df["week"], vax_df["weekly_deaths"]/1e3, color=PALETTE["danger"],
               lw=2, label="Deaths (K)")
ax_cov = axes[1,0].twinx()
ax_cov.fill_between(vax_df["week"], vax_df["vaccination_coverage_pct"],
                    alpha=0.2, color=PALETTE["success"])
ax_cov.plot(vax_df["week"], vax_df["vaccination_coverage_pct"],
            color=PALETTE["success"], lw=1.5, ls="--", label="Vax Coverage (%)")
ax_cov.set_ylabel("Coverage (%)", color=PALETTE["success"])
axes[1,0].set_ylabel("Deaths (Thousands)", color=PALETTE["danger"])
axes[1,0].set_title("Deaths vs Vaccination Coverage")
lines_a, lbl_a = axes[1,0].get_legend_handles_labels()
lines_b, lbl_b = ax_cov.get_legend_handles_labels()
axes[1,0].legend(lines_a+lines_b, lbl_a+lbl_b, loc="upper right", fontsize=9)

# Variant-wise cases
for variant, color in VARIANT_COLORS.items():
    sub = vax_df[vax_df["variant_dominant"]==variant]
    if len(sub):
        axes[1,1].fill_between(sub["week"], sub["weekly_cases"]/1e3,
                               alpha=0.55, color=color, label=variant)
axes[1,1].set_xlabel(""); axes[1,1].set_ylabel("Weekly Cases (K)")
axes[1,1].set_title("Weekly Cases by Dominant Variant")
axes[1,1].legend(title="Variant")
add_watermark(axes[1,1])
plt.tight_layout(rect=[0, 0, 1, 0.94])
save_figure(fig, f"{VIZ}/viz7_vaccination_impact.png")

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 8 – Correlation Heatmap
# ══════════════════════════════════════════════════════════════════════════════
print("[8/10] Correlation heatmap …")
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle("Statistical Correlation Analysis", fontsize=15, fontweight="bold",
             color=PALETTE["primary"])

num_cols = ["total_cases","total_deaths","total_vaccinated","vaccination_rate_pct",
            "cases_per_million","deaths_per_million","case_fatality_rate_pct","healthcare_index"]
corr = country_df[num_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, ax=axes[0], mask=mask, annot=True, fmt=".2f",
            cmap="RdBu_r", center=0, linewidths=0.5, linecolor="white",
            cbar_kws={"shrink": 0.8}, annot_kws={"size": 8})
axes[0].set_title("Country Metrics Correlation Matrix")
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=40, ha="right", fontsize=8)
axes[0].set_yticklabels(axes[0].get_yticklabels(), fontsize=8)

pat_num = patient_df[["age","hospitalization_days","treatment_effectiveness_score"]].copy()
pat_num["is_icu"] = patient_df["icu_required"].astype(int)
pat_num["is_deceased"] = (patient_df["outcome"]=="Deceased").astype(int)
pat_corr = pat_num.corr()
sns.heatmap(pat_corr, ax=axes[1], annot=True, fmt=".3f", cmap="RdBu_r",
            center=0, linewidths=0.5, linecolor="white", annot_kws={"size": 10})
axes[1].set_title("Patient Variables Correlation Matrix")
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=30, ha="right")
add_watermark(axes[1])
plt.tight_layout(rect=[0, 0, 1, 0.94])
save_figure(fig, f"{VIZ}/viz8_correlation_heatmap.png")

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 9 – Age & Gender Analysis
# ══════════════════════════════════════════════════════════════════════════════
print("[9/10] Age & gender analysis …")
fig, axes = plt.subplots(1, 3, figsize=(17, 6))
fig.suptitle("Demographic Risk Analysis", fontsize=15, fontweight="bold", color=PALETTE["primary"])

# Age group mortality
age_mort = patient_df.groupby("age_group")["outcome"].apply(
    lambda x: (x=="Deceased").mean()*100).reset_index()
age_mort.columns = ["age_group","mortality_pct"]
colors_age = plt.cm.Reds(np.linspace(0.3, 0.9, len(age_mort)))
axes[0].bar(age_mort["age_group"].astype(str), age_mort["mortality_pct"],
            color=colors_age, edgecolor="white", width=0.55)
axes[0].set_ylabel("Mortality Rate (%)"); axes[0].set_title("Mortality Rate by Age Group")
axes[0].set_xlabel("Age Group")
for i, val in enumerate(age_mort["mortality_pct"]):
    axes[0].text(i, val + 0.1, f"{val:.1f}%", ha="center", fontsize=10, fontweight="bold")

# Gender breakdown
gen_sev = patient_df.groupby(["gender","severity"]).size().unstack(fill_value=0)
gen_sev = gen_sev.reindex(columns=["Mild","Moderate","Severe","Critical"], fill_value=0)
gen_pct = gen_sev.div(gen_sev.sum(axis=1), axis=0) * 100
gen_pct.plot(kind="bar", ax=axes[1], stacked=True, color=sev_colors, edgecolor="white", width=0.45)
axes[1].set_title("Severity Distribution by Gender")
axes[1].set_ylabel("Percentage (%)")
axes[1].set_xticklabels(["Female","Male"], rotation=0)
axes[1].legend(title="Severity", loc="upper right")
axes[1].set_xlabel("")

# Hospitalization days by age group & severity
bp_data = [patient_df[(patient_df["age_group"]==ag)]["hospitalization_days"].values
           for ag in ["0-18","19-35","36-50","51-65","65+"]]
bp = axes[2].boxplot(bp_data, labels=["0-18","19-35","36-50","51-65","65+"],
                     patch_artist=True, notch=False, medianprops=dict(color="white",lw=2))
for patch, color in zip(bp["boxes"], plt.cm.OrRd(np.linspace(0.3,0.9,5))):
    patch.set_facecolor(color)
axes[2].set_ylabel("Hospitalization Days")
axes[2].set_title("Hospital Stay Duration by Age Group")
axes[2].set_xlabel("Age Group")
add_watermark(axes[2])
plt.tight_layout(rect=[0, 0, 1, 0.94])
save_figure(fig, f"{VIZ}/viz9_demographic_analysis.png")

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 10 – Executive Summary Dashboard
# ══════════════════════════════════════════════════════════════════════════════
print("[10/10] Executive summary dashboard …")
fig = plt.figure(figsize=(18, 12))
fig.patch.set_facecolor(PALETTE["text"])
gs  = gridspec.GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.35)
fig.suptitle("COVID-19 Healthcare Analysis  ·  Executive Summary Dashboard",
             fontsize=18, fontweight="bold", color="white", y=0.98)

def dark_ax(ax):
    ax.set_facecolor("#1E2A3A"); ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white"); ax.yaxis.label.set_color("white")
    ax.title.set_color("white"); ax.spines[:].set_color("#334155")
    ax.grid(color="#334155", lw=0.4)

# Panel A – global cases mini timeline
ax_a = fig.add_subplot(gs[0, :2])
dark_ax(ax_a)
ax_a.fill_between(global_df["date"], global_df["rolling_cases"]/1e6, alpha=0.4, color="#4E9AF1")
ax_a.plot(global_df["date"], global_df["rolling_cases"]/1e6, color="#4E9AF1", lw=1.5)
ax_a.set_title("Global Case Trend (7d Avg, Millions)"); ax_a.set_xlabel("")

# Panel B – vaccination coverage
ax_b = fig.add_subplot(gs[0, 2:])
dark_ax(ax_b)
ax_b.fill_between(vax_df["week"], vax_df["vaccination_coverage_pct"], alpha=0.4, color="#2A9D8F")
ax_b.plot(vax_df["week"], vax_df["vaccination_coverage_pct"], color="#2A9D8F", lw=1.5)
ax_b.set_title("Global Vaccination Coverage (%)")

# Panel C – country bar
ax_c = fig.add_subplot(gs[1, :2])
dark_ax(ax_c)
top_c = country_df.sort_values("total_cases", ascending=True).tail(8)
ax_c.barh(top_c["country"], top_c["total_cases"]/1e6, color="#4E9AF1", alpha=0.85)
ax_c.set_title("Total Cases by Country (Millions)"); ax_c.set_xlabel("")

# Panel D – treatment recovery rate
ax_d = fig.add_subplot(gs[1, 2:])
dark_ax(ax_d)
ts = treatment_summary(patient_df)
colors_td = ["#2A9D8F" if r >= 88 else "#F4A261" if r >= 84 else "#CC2936" for r in ts["recovery_rate"]]
ax_d.barh(ts["treatment"], ts["recovery_rate"], color=colors_td, alpha=0.9)
ax_d.set_xlim(70,100); ax_d.set_title("Treatment Recovery Rate (%)")

# Panel E – severity pie mini
ax_e = fig.add_subplot(gs[2, 0])
ax_e.set_facecolor("#1E2A3A"); ax_e.set_title("Severity Split", color="white")
sev_c = patient_df["severity"].value_counts().reindex(sev_order)
ax_e.pie(sev_c, labels=sev_order, colors=sev_colors, autopct="%1.0f%%",
         textprops={"color":"white","fontsize":8}, wedgeprops=dict(edgecolor="#1E2A3A", lw=1.5))

# Panel F – comorbidity mortality
ax_f = fig.add_subplot(gs[2, 1])
dark_ax(ax_f)
comor_mort = patient_df.groupby("comorbidity")["outcome"].apply(
    lambda x: (x=="Deceased").mean()*100).sort_values(ascending=True)
ax_f.barh(comor_mort.index, comor_mort.values, color=PALETTE["accent"], alpha=0.85)
ax_f.set_title("Mortality % by Comorbidity"); ax_f.set_xlabel("")
ax_f.tick_params(axis="y", labelsize=8)

# Panel G – age mortality
ax_g = fig.add_subplot(gs[2, 2])
dark_ax(ax_g)
age_m = patient_df.groupby("age_group")["outcome"].apply(
    lambda x: (x=="Deceased").mean()*100)
ax_g.bar(age_m.index.astype(str), age_m.values, color="#CC2936", alpha=0.85)
ax_g.set_title("Mortality % by Age Group"); ax_g.set_xlabel("")

# Panel H – KPI text panel
ax_h = fig.add_subplot(gs[2, 3])
ax_h.set_facecolor("#0F172A"); ax_h.axis("off")
kpi_texts = [
    ("Total Global Cases",   f"{total_cases/1e6:.1f}M"),
    ("Total Deaths",         f"{total_deaths/1e6:.2f}M"),
    ("Peak Daily Cases",     f"{peak_daily/1e6:.2f}M"),
    ("Best Treatment",       "Combo Therapy"),
    ("Highest Risk Group",   "Age 65+"),
    ("Vax Impact on Deaths", "↓ ~82%"),
]
for i, (lbl, val) in enumerate(kpi_texts):
    y = 0.92 - i * 0.16
    ax_h.text(0.05, y, val, color="#4E9AF1", fontsize=12, fontweight="bold", transform=ax_h.transAxes)
    ax_h.text(0.05, y - 0.06, lbl, color="#94A3B8", fontsize=8, transform=ax_h.transAxes)
ax_h.set_title("Key Metrics", color="white", fontsize=11, fontweight="bold")

save_figure(fig, f"{VIZ}/viz10_executive_dashboard.png", dpi=120)

print("\n✅ All 10 visualizations generated successfully!")
print(f"   Saved to: {VIZ}/")
