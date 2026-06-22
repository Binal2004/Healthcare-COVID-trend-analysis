"""
COVID-19 Dataset Generator
Simulates realistic COVID-19 trends based on real-world patterns (2020-2023)
Dataset inspired by: Our World in Data / Kaggle COVID-19 datasets
"""
import pandas as pd
import numpy as np

np.random.seed(42)

# ─── 1. Global COVID Trends Dataset ──────────────────────────────────────────
dates = pd.date_range("2020-01-22", "2023-12-31", freq="D")
n = len(dates)

def wave(t, peak, center, width):
    return peak * np.exp(-((t - center) ** 2) / (2 * width ** 2))

t = np.arange(n)
# Four waves: Alpha, Delta, Omicron, XBB
cases_base = (
    wave(t, 80000,  120, 40) +
    wave(t, 200000, 350, 60) +
    wave(t, 600000, 600, 80) +
    wave(t, 900000, 730, 70) +
    wave(t, 500000, 900, 90) +
    np.random.normal(0, 5000, n)
).clip(0)

deaths_base = (cases_base * 0.018 * np.exp(-t / 600)).clip(0)  # Declining CFR over time
recoveries = (cases_base * 0.95).clip(0)

global_df = pd.DataFrame({
    "date": dates,
    "new_cases": cases_base.astype(int),
    "new_deaths": deaths_base.astype(int),
    "new_recoveries": recoveries.astype(int),
    "total_cases": np.cumsum(cases_base).astype(int),
    "total_deaths": np.cumsum(deaths_base).astype(int),
    "total_recoveries": np.cumsum(recoveries).astype(int),
    "active_cases": (np.cumsum(cases_base) - np.cumsum(recoveries) - np.cumsum(deaths_base)).clip(0).astype(int),
    "tests_conducted": (cases_base * np.random.uniform(5, 15, n)).astype(int),
    "positivity_rate": (cases_base / (cases_base * np.random.uniform(5, 15, n)) * 100).round(2),
    "vaccinations_daily": np.where(t < 365, 0, wave(t, 3000000, 500, 150) + np.random.normal(0, 50000, n)).clip(0).astype(int),
})
global_df.to_csv("/home/claude/project4_covid_analysis/data/covid_global_trends.csv", index=False)

# ─── 2. Country-wise Dataset ─────────────────────────────────────────────────
countries = {
    "India":         {"pop": 1380, "cfr_base": 0.014, "peak_mul": 1.2},
    "USA":           {"pop": 331,  "cfr_base": 0.018, "peak_mul": 1.5},
    "Brazil":        {"pop": 213,  "cfr_base": 0.022, "peak_mul": 1.1},
    "Germany":       {"pop": 83,   "cfr_base": 0.012, "peak_mul": 0.6},
    "UK":            {"pop": 67,   "cfr_base": 0.016, "peak_mul": 0.7},
    "Italy":         {"pop": 60,   "cfr_base": 0.020, "peak_mul": 0.65},
    "France":        {"pop": 65,   "cfr_base": 0.015, "peak_mul": 0.7},
    "Russia":        {"pop": 146,  "cfr_base": 0.021, "peak_mul": 0.9},
    "Japan":         {"pop": 126,  "cfr_base": 0.008, "peak_mul": 0.4},
    "South Korea":   {"pop": 52,   "cfr_base": 0.009, "peak_mul": 0.35},
    "Australia":     {"pop": 26,   "cfr_base": 0.007, "peak_mul": 0.3},
    "South Africa":  {"pop": 60,   "cfr_base": 0.025, "peak_mul": 0.8},
}

country_rows = []
for country, params in countries.items():
    total_cases = int(params["pop"] * 1e6 * np.random.uniform(0.08, 0.35) * params["peak_mul"])
    total_deaths = int(total_cases * params["cfr_base"] * np.random.uniform(0.8, 1.2))
    total_vaccinated = int(params["pop"] * 1e6 * np.random.uniform(0.55, 0.85))
    country_rows.append({
        "country": country,
        "population_millions": params["pop"],
        "total_cases": total_cases,
        "total_deaths": total_deaths,
        "total_recoveries": int(total_cases * 0.975),
        "total_vaccinated": total_vaccinated,
        "vaccination_rate_pct": round(total_vaccinated / (params["pop"] * 1e6) * 100, 1),
        "cases_per_million": round(total_cases / params["pop"], 1),
        "deaths_per_million": round(total_deaths / params["pop"], 1),
        "case_fatality_rate_pct": round(total_deaths / total_cases * 100, 2),
        "peak_daily_cases": int(total_cases * np.random.uniform(0.003, 0.008)),
        "healthcare_index": round(np.random.uniform(55, 92), 1),
    })

country_df = pd.DataFrame(country_rows)
country_df.to_csv("/home/claude/project4_covid_analysis/data/covid_country_comparison.csv", index=False)

# ─── 3. Patient Treatment Dataset ────────────────────────────────────────────
n_patients = 2000
age = np.random.normal(48, 18, n_patients).clip(5, 95).astype(int)
gender = np.random.choice(["Male", "Female"], n_patients, p=[0.53, 0.47])
severity = np.where(age > 65, 
                    np.random.choice(["Mild","Moderate","Severe","Critical"], n_patients, p=[0.25,0.35,0.25,0.15]),
                    np.random.choice(["Mild","Moderate","Severe","Critical"], n_patients, p=[0.45,0.35,0.15,0.05]))
comorbidities = np.random.choice(["None","Diabetes","Hypertension","Heart Disease","Obesity","Respiratory"], 
                                  n_patients, p=[0.38,0.18,0.20,0.10,0.08,0.06])
treatment = np.random.choice(["Remdesivir","Dexamethasone","Combination Therapy","Supportive Care","Monoclonal Antibodies"],
                              n_patients, p=[0.22,0.20,0.28,0.18,0.12])
hosp_days = np.where(severity=="Mild", np.random.randint(1,5,n_patients),
             np.where(severity=="Moderate", np.random.randint(5,12,n_patients),
             np.where(severity=="Severe", np.random.randint(10,25,n_patients),
                      np.random.randint(20,45,n_patients))))

recovery_prob = np.where(severity=="Mild",0.99,np.where(severity=="Moderate",0.94,np.where(severity=="Severe",0.80,0.55)))
outcome = np.array(["Recovered" if np.random.random() < p else "Deceased" for p in recovery_prob])
icu_required = np.where(np.isin(severity,["Severe","Critical"]), 
                         np.random.choice([True,False], n_patients, p=[0.7,0.3]), False)
oxygen_required = np.where(np.isin(severity,["Moderate","Severe","Critical"]),
                            np.random.choice([True,False], n_patients, p=[0.75,0.25]), False)

treatment_effectiveness = {
    "Combination Therapy": 0.91, "Remdesivir": 0.87, "Monoclonal Antibodies": 0.89,
    "Dexamethasone": 0.84, "Supportive Care": 0.78
}
effectiveness_score = np.array([treatment_effectiveness[t] * np.random.uniform(0.85,1.1) for t in treatment]).clip(0,1).round(3)

patient_df = pd.DataFrame({
    "patient_id": [f"PT{str(i).zfill(5)}" for i in range(1, n_patients+1)],
    "age": age, "gender": gender, "severity": severity,
    "comorbidity": comorbidities, "treatment": treatment,
    "hospitalization_days": hosp_days.clip(1,60),
    "icu_required": icu_required, "oxygen_required": oxygen_required,
    "outcome": outcome,
    "treatment_effectiveness_score": effectiveness_score,
    "admission_date": pd.date_range("2020-03-01", periods=n_patients, freq="12h")[:n_patients].strftime("%Y-%m-%d"),
    "age_group": pd.cut(age, bins=[0,18,35,50,65,100], labels=["0-18","19-35","36-50","51-65","65+"])
})
patient_df.to_csv("/home/claude/project4_covid_analysis/data/covid_patient_treatment.csv", index=False)

# ─── 4. Vaccination Impact Dataset ───────────────────────────────────────────
vax_dates = pd.date_range("2021-01-01", "2023-12-31", freq="W")
nw = len(vax_dates)
tv = np.arange(nw)
vax_coverage = (100 * (1 - np.exp(-tv / 60)) + np.random.normal(0, 1, nw)).clip(0, 92)
cases_vax = (500000 * np.exp(-tv / 40) + wave(tv, 900000, 80, 20) + np.random.normal(0,10000,nw)).clip(0)
deaths_vax = (cases_vax * (0.025 * np.exp(-tv / 50))).clip(0)
hospitalizations = (cases_vax * (0.12 * np.exp(-tv / 55))).clip(0)

vax_df = pd.DataFrame({
    "week": vax_dates, "vaccination_coverage_pct": vax_coverage.round(2),
    "weekly_cases": cases_vax.astype(int),
    "weekly_deaths": deaths_vax.astype(int),
    "weekly_hospitalizations": hospitalizations.astype(int),
    "vaccine_doses_given": (vax_coverage * 1e6 / 100 * np.random.uniform(0.01,0.03,nw)).astype(int),
    "booster_doses": np.where(tv > 52, (vax_coverage * 5e4 * np.random.uniform(0.8,1.2,nw)).astype(int), 0),
    "variant_dominant": np.where(tv < 30,"Alpha",np.where(tv < 60,"Delta",np.where(tv < 100,"Omicron","XBB/BQ")))
})
vax_df.to_csv("/home/claude/project4_covid_analysis/data/covid_vaccination_impact.csv", index=False)

print("✅ All 4 datasets generated successfully!")
print(f"  • covid_global_trends.csv     : {len(global_df):,} rows")
print(f"  • covid_country_comparison.csv: {len(country_df):,} rows")
print(f"  • covid_patient_treatment.csv : {len(patient_df):,} rows")
print(f"  • covid_vaccination_impact.csv: {len(vax_df):,} rows")
