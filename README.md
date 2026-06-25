# 🏥 COVID-19 Healthcare Data Analysis

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557C?style=for-the-badge)
![SciPy](https://img.shields.io/badge/SciPy-1.10%2B-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)

**Multi-Domain Data Analysis Portfolio — Project 4 of 5**

*Pandemic Trends · Treatment Effectiveness · Vaccination Impact · Risk Factors*

---

| 👤 Analyst | 🎓 Programme |
|---|---|
| Binal Doshi | MSc AI & Data Science |

</div>

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Key Findings](#-key-findings)
- [Project Structure](#-project-structure)
- [Datasets](#-datasets)
- [Quick Start](#-quick-start)
- [Visualizations](#-visualizations)
- [Statistical Methods](#-statistical-methods)
- [Business Insights & Recommendations](#-business-insights--recommendations)
- [Dependencies](#-dependencies)
- [Deliverables](#-deliverables)
- [Author](#-author)

---

## 🔍 Project Overview

This project delivers a comprehensive analysis of COVID-19 pandemic data across **four interconnected dimensions**:

| Dimension | Scope | Key Question |
|-----------|-------|--------------|
| **Global Trends** | 1,440 days of daily data (2020–2023) | How did the pandemic evolve across 4 waves? |
| **Country Comparison** | 12 countries across 5 continents | Which healthcare systems managed COVID best? |
| **Patient Clinical Analysis** | 2,000 patient records, 5 treatment protocols | Which treatment yields the highest recovery rate? |
| **Vaccination Impact** | Weekly data over 3 years | How much did vaccination reduce deaths? |

> **Dataset:** 3,609 total records across 4 structured CSV files — generated with realistic patterns based on real-world COVID-19 data (Our World in Data / Kaggle patterns, seed=42 for reproducibility).

---

## 🏆 Key Findings

```
╔══════════════════════════════════════════════════════════════════╗
║  EXECUTIVE SUMMARY — COVID-19 HEALTHCARE ANALYSIS               ║
╠══════════════════════════════════════════════════════════════════╣
║  Peak Daily Cases       →  ~900,000 (Wave 4 / Omicron)          ║
║  Global CFR Decline     →  2.8% (Wave 1)  →  0.8% (Wave 4)     ║
║  Best Treatment         →  Combination Therapy  (91% recovery)  ║
║  Highest Risk Group     →  Age 65+  (3.2× more deaths)          ║
║  Vaccination Impact     →  ~82% fewer weekly deaths at 60%+ cov ║
║  Deadliest Comorbidity  →  Heart Disease  (~14% mortality)       ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 📁 Project Structure

```
project4_covid_analysis/
│
├── 📄 README.md                              ← You are here
├── 📄 requirements.txt                       ← Python dependencies
│
├── 📂 data/
│   ├── generate_data.py                      ← Generates all 4 datasets
│   ├── covid_global_trends.csv               ← 1,440 rows | Daily global cases/deaths/vaccinations
│   ├── covid_country_comparison.csv          ← 12 rows   | 12-country metrics
│   ├── covid_patient_treatment.csv           ← 2,000 rows| Patient demographics & outcomes
│   └── covid_vaccination_impact.csv          ← 157 rows  | Weekly vaccination vs mortality
│
├── 📂 notebooks/
│   └── covid_analysis_v2.ipynb               ← ✅ MAIN NOTEBOOK (self-contained, no path issues)
│
├── 📂 src/
│   └── covid_analysis_utils.py               ← Reusable helper functions & plotting utilities
│
├── 📂 visualizations/
│   ├── viz1_global_dashboard.png             ← KPI banner + case/death timeline
│   ├── viz2_country_comparison.png           ← Cases per million & CFR by country
│   ├── viz3_wave_analysis.png                ← Box plot + bar chart across 4 waves
│   ├── viz4_patient_severity.png             ← Severity distribution + outcomes + ICU
│   ├── viz5_treatment_effectiveness.png      ← Recovery rates + hospitalization days
│   ├── viz6_comorbidity_impact.png           ← Mortality by comorbidity + severity split
│   ├── viz7_vaccination_impact.png           ← Coverage vs deaths, cases, variants
│   ├── viz8_correlation_heatmap.png          ← Pearson correlation matrices
│   ├── viz9_demographic_analysis.png         ← Age & gender risk analysis
│   └── viz10_executive_dashboard.png         ← Dark-theme multi-panel summary
│
├── 📂 reports/
│   └── COVID19_Executive_Report.pdf          ← 11-page professional PDF report
│
├── 📂 presentation/
│   └── COVID19_Analysis_Presentation.pptx   ← 12-slide PowerPoint deck
│
└── 📂 docs/
    └── Project4_COVID_Documentation.docx     ← Full Word documentation (6 sections)
```

---

## 📊 Datasets

| File | Rows | Columns | Description |
|------|------|---------|-------------|
| `covid_global_trends.csv` | 1,440 | 11 | Daily new cases, deaths, recoveries, active cases, tests, positivity rate, vaccinations (Jan 2020 – Dec 2023) |
| `covid_country_comparison.csv` | 12 | 12 | Total cases/deaths, CFR, vaccination rate, cases per million, healthcare index for 12 countries |
| `covid_patient_treatment.csv` | 2,000 | 13 | Patient age, gender, severity, comorbidity, treatment protocol, ICU/oxygen need, outcome, effectiveness score |
| `covid_vaccination_impact.csv` | 157 | 8 | Weekly vaccination coverage %, weekly cases/deaths/hospitalizations, dominant variant |

> **Note:** Datasets are generated internally inside the notebook (`covid_analysis_v2.ipynb`) — no external files needed to run the analysis.

---

## 🚀 Quick Start

### Option A — Run Notebook (Recommended, No Setup Needed)

```bash
# 1. Open the notebook in Jupyter or Google Colab
jupyter notebook notebooks/covid_analysis_v2.ipynb

# 2. Run All Cells (Kernel → Restart & Run All)
# Datasets are auto-generated inside the notebook ✅
# All 10 visualizations are saved automatically ✅
```

### Option B — Full Local Setup

```bash
# 1. Navigate to project folder
cd project4_covid_analysis

# 2. Install all dependencies
pip install -r requirements.txt

# 3. Generate the 4 CSV datasets
python data/generate_data.py

# 4. Generate all 10 visualizations
python generate_visualizations.py

# 5. Open the notebook
jupyter notebook notebooks/covid_analysis_v2.ipynb
```

### Option C — Google Colab

1. Upload `covid_analysis_v2.ipynb` to [colab.research.google.com](https://colab.research.google.com)
2. Click **Runtime → Run All**
3. No datasets or imports needed — everything is self-contained ✅

---

## 📈 Visualizations

| # | Chart Title | Chart Type | Key Insight |
|---|-------------|------------|-------------|
| 1 | Global KPI Dashboard & Timeline | KPI Banner + Dual-Axis Line | Peak: 900K cases/day; CFR fell 72% from Wave 1 to Wave 4 |
| 2 | Country-Wise Comparison | Horizontal Bar (×2) | South Africa highest CFR (2.5%); Australia lowest (0.7%) |
| 3 | Pandemic Wave Analysis | Box Plot + Grouped Bar | Omicron volume 4.5× Wave 1 but 72% lower fatality |
| 4 | Patient Severity & Outcomes | 4-Panel Multi-chart | Critical severity → 45% mortality, 68% ICU rate |
| 5 | Treatment Effectiveness | Bar + Scatter Matrix | Combination Therapy: 91% recovery, 3.2 days shorter stay |
| 6 | Comorbidity Impact | Bar + Stacked Bar | Heart Disease: ~14% mortality — highest risk group |
| 7 | Vaccination Impact | 4-Panel (Timeline + Scatter + Dual-Axis + Area) | 60%+ coverage → 82% fewer weekly deaths |
| 8 | Correlation Heatmap | Heatmap (×2) | HCI vs CFR: r=−0.68; Age vs Hosp. Days: r=+0.41 |
| 9 | Demographic Risk Analysis | Bar + Stacked Bar + Box Plot | Age 65+ mortality 3.2× higher than 19–35 group |
| 10 | Executive Dashboard | Dark Multi-Panel | Full summary view for stakeholder presentations |

---

## 🔬 Statistical Methods

| Method | Applied To | Result |
|--------|-----------|--------|
| **7-Day Rolling Average** | Daily cases & deaths | Smoothed wave trends removing weekend reporting noise |
| **Pearson Correlation (r)** | Vaccination vs deaths; HCI vs CFR | r=−0.72 (vax vs deaths, p<0.001); r=−0.68 (HCI vs CFR) |
| **Independent T-Test** | Combination Therapy vs Supportive Care | t=4.21, p<0.001 — statistically significant difference |
| **Wave Segmentation** | Date-based classification | 4 waves identified using epidemiological thresholds |
| **Descriptive Statistics** | All numeric variables | Mean, median, IQR, min/max, percentiles |
| **Group Aggregation** | Treatment, comorbidity, age group | Recovery rates, avg hospital days, ICU rates per group |

---

## 💡 Business Insights & Recommendations

| # | Recommendation | Evidence |
|---|----------------|----------|
| 1 | **Prioritise Combination Therapy** for Severe/Critical patients | 91% recovery rate, p<0.001 vs Supportive Care |
| 2 | **Fast-track vaccination** for Age 65+ and comorbid patients | 62% of all deaths in this demographic |
| 3 | **Strengthen ICU infrastructure** in high-CFR nations | ICU availability is strongest predictor of Critical survival |
| 4 | **Early escalation** for Heart Disease & Diabetes patients | ~14% and ~12% mortality respectively — auto-flag needed |
| 5 | **Maintain booster programmes** against new variants | 30% fewer ICU admissions during Omicron with >40% booster uptake |
| 6 | **Cross-country capacity sharing** for low HCI nations | HCI 60→75 could prevent ~35% of excess deaths |

---

## 📦 Dependencies

```txt
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.10.0
scikit-learn>=1.3.0
nbformat>=5.7.0
nbconvert>=7.4.0
openpyxl>=3.1.0
jupyterlab>=4.0.0
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 📋 Deliverables

| File | Description | Location |
|------|-------------|----------|
| `covid_analysis_v2.ipynb` | Main Jupyter notebook — fully self-contained | `notebooks/` |
| `COVID19_Executive_Report.pdf` | 11-page professional PDF with all charts & findings | `reports/` |
| `COVID19_Analysis_Presentation.pptx` | 12-slide PowerPoint deck for presentations | `presentation/` |
| `Project4_COVID_Documentation.docx` | 6-section Word documentation | `docs/` |
| `viz1–viz10 (*.png)` | 10 professional visualizations at 150 DPI | `visualizations/` |
| `covid_*.csv (×4)` | 4 structured datasets totalling 3,609 records | `data/` |
| `covid_analysis_utils.py` | Reusable helper functions module | `src/` |

---

## 👤 Author

<div align="center">

**Binal Doshi**

MSc Artificial Intelligence & Data Science (2025–2027)
University of Mumbai

[![Email](https://img.shields.io/badge/Email-binaldoshi04%40gmail.com-D14836?style=flat&logo=gmail&logoColor=white)](mailto:binaldoshi04@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-binal--doshi--2005abc-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/binal-doshi-2005abc)
[![GitHub](https://img.shields.io/badge/GitHub-Binal2004-181717?style=flat&logo=github&logoColor=white)](https://github.com/Binal2004)

---

*Part of a 5-project Multi-Domain Data Analysis Portfolio*
*Other projects: Retail Sales · Finance/Real Estate · Education · Weather/Climate*

</div>
