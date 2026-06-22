# 🏥 Project 4: COVID-19 Healthcare Data Analysis

> **Multi-Domain Data Analysis Portfolio — Project 4 of 5**  
> Domain: Healthcare | Analyst: Binal Doshi | MSc AI & Data Science, University of Mumbai

---

## 📋 Project Overview

This project analyses COVID-19 pandemic data across four key dimensions:

| Analysis Area | Key Insight |
|---|---|
| Global Trends | 4 pandemic waves identified; Omicron had highest case volume |
| Country Comparison | Healthcare Index inversely correlated with CFR |
| Treatment Effectiveness | Combination Therapy achieved 91% recovery rate |
| Vaccination Impact | >60% coverage → ~82% reduction in weekly deaths |

**Datasets used:** 4 structured datasets totalling 3,609 records covering global trends (2020–2023), 12 countries, 2,000 patient records, and weekly vaccination data.

---

## 📁 Project Structure

```
project4_covid_analysis/
├── README.md                        ← This file
├── requirements.txt                 ← Python dependencies
├── generate_visualizations.py       ← Runs all 10 charts
├── data/
│   ├── generate_data.py             ← Dataset generator script
│   ├── covid_global_trends.csv      ← 1,440 rows — daily global cases/deaths
│   ├── covid_country_comparison.csv ← 12 rows  — 12-country comparison
│   ├── covid_patient_treatment.csv  ← 2,000 rows — patient-level clinical data
│   └── covid_vaccination_impact.csv ← 157 rows  — weekly vaccination & cases
├── notebooks/
│   └── covid_analysis.ipynb         ← Full analysis notebook
├── reports/                         ← PDF executive report (auto-generated)
├── src/
│   └── covid_analysis_utils.py      ← Reusable helper functions
├── visualizations/                  ← 10 output charts (PNG)
│   ├── viz1_global_dashboard.png
│   ├── viz2_country_comparison.png
│   ├── viz3_wave_analysis.png
│   ├── viz4_patient_severity.png
│   ├── viz5_treatment_effectiveness.png
│   ├── viz6_comorbidity_impact.png
│   ├── viz7_vaccination_impact.png
│   ├── viz8_correlation_heatmap.png
│   ├── viz9_demographic_analysis.png
│   └── viz10_executive_dashboard.png
├── presentation/                    ← Slide deck materials
└── docs/                            ← Word documentation
    └── Project4_COVID_Documentation.docx
```

---

## 🚀 Quick Start

```bash
# 1. Clone or navigate to the project folder
cd project4_covid_analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate datasets
python data/generate_data.py

# 4. Generate all 10 visualizations
python generate_visualizations.py

# 5. Open the Jupyter notebook
jupyter notebook notebooks/covid_analysis.ipynb
```

---

## 📊 Visualizations (10 Charts)

| # | Chart | Type | Key Finding |
|---|-------|------|-------------|
| 1 | Global KPI Dashboard | KPI + Timeline | Peak cases: 900K/day |
| 2 | Country Comparison | Horizontal Bar | South Africa: highest CFR |
| 3 | Wave Analysis | Box Plot + Bar | Omicron: largest volume |
| 4 | Patient Severity & Outcomes | Multi-panel | Critical: 45% mortality |
| 5 | Treatment Effectiveness | Bar + Scatter | Combo Therapy wins |
| 6 | Comorbidity Impact | Bar + Stacked Bar | Heart Disease: highest risk |
| 7 | Vaccination Impact | 4-panel | 82% death reduction |
| 8 | Correlation Heatmap | Heatmap | Age ↑ → outcomes ↓ |
| 9 | Demographic Analysis | Box + Bar | Age 65+: highest mortality |
| 10 | Executive Dashboard | Dark Multi-panel | Full summary view |

---

## 🔬 Statistical Methods

- **Pearson Correlation** — vaccination coverage vs. mortality/cases
- **Independent Samples T-test** — treatment group comparisons
- **7-Day Rolling Averages** — smoothing daily case/death counts
- **Wave Classification** — time-based segmentation into 4 pandemic phases
- **Descriptive Statistics** — mean, median, IQR for patient metrics

---

## 💡 Business Insights

1. **Combination Therapy** reduces hospitalization by 3.2 days vs. Supportive Care (p < 0.05)
2. Countries with Healthcare Index > 75 show CFR below 1.5%
3. Age 65+ patients account for 62% of COVID-19 deaths despite being 18% of cases
4. Reaching 60% vaccination coverage is the critical threshold for epidemic control
5. Booster doses maintained protection against Omicron's immune escape

---

## 📦 Dependencies

See `requirements.txt` — core stack: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `scikit-learn`, `nbformat`

---

## 👤 Author

**Binal Doshi**  
MSc Artificial Intelligence & Data Science (2025–2027)  
University of Mumbai  
📧 binaldoshi04@gmail.com | 🔗 [LinkedIn](https://linkedin.com/in/binal-doshi-2005abc) | 💻 [GitHub](https://github.com/Binal2004)
