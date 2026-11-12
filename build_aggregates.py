import os
import pandas as pd
import numpy as np

# 1. Load data
try:
    df = pd.read_parquet("data/analysis_sample.parquet")
except Exception:
    df = pd.read_csv("powerbi/analysis_sample.csv")

# 2. Re-create target and derived bins if missing
if 'HIGH_BP_FLAG' not in df.columns:
    df['HIGH_BP_FLAG'] = np.where(
        (df['SYSTOLIC_BP'] >= 140) | (df['DIASTOLIC_BP'] >= 90), 1, 0
    )

# Ensure an AGE_GROUP column exists
if 'AGE_GROUP' not in df.columns:
    bins = [0, 29, 44, 59, 120]
    labels = ['18-29', '30-44', '45-59', '60+']
    df['AGE_GROUP'] = pd.cut(df['AGE'], bins=bins, labels=labels, right=True)

# Ensure a SURVEY_YEAR column exists (or extract from survey date if available, else default)
if 'SURVEY_YEAR' not in df.columns:
    if 'SURVEY_DATE' in df.columns:
        df['SURVEY_YEAR'] = pd.to_datetime(df['SURVEY_DATE']).dt.year
    else:
        df['SURVEY_YEAR'] = 2026

os.makedirs("data", exist_ok=True)

# Aggregation 1: By State
agg_state = df.groupby('NIGERIAN_STATE').agg(
    total_surveys=('HIGH_BP_FLAG', 'count'),
    hypertensive_count=('HIGH_BP_FLAG', 'sum'),
    avg_systolic=('SYSTOLIC_BP', 'mean'),
    avg_diastolic=('DIASTOLIC_BP', 'mean'),
    avg_bmi=('BMI', 'mean')
).reset_index()
agg_state['prevalence_rate'] = agg_state['hypertensive_count'] / agg_state['total_surveys']
agg_state.to_parquet("data/agg_by_state.parquet", index=False)

# Aggregation 2: By Geopolitical Zone and Year
agg_zone_year = df.groupby(['GEOPOLITICAL_ZONE', 'SURVEY_YEAR']).agg(
    total_surveys=('HIGH_BP_FLAG', 'count'),
    hypertensive_count=('HIGH_BP_FLAG', 'sum'),
    avg_systolic=('SYSTOLIC_BP', 'mean'),
    avg_diastolic=('DIASTOLIC_BP', 'mean')
).reset_index()
agg_zone_year['prevalence_rate'] = agg_zone_year['hypertensive_count'] / agg_zone_year['total_surveys']
agg_zone_year.to_parquet("data/agg_by_zone_year.parquet", index=False)

# Aggregation 3: By Age Group
agg_age = df.groupby('AGE_GROUP', observed=True).agg(
    total_surveys=('HIGH_BP_FLAG', 'count'),
    hypertensive_count=('HIGH_BP_FLAG', 'sum'),
    avg_systolic=('SYSTOLIC_BP', 'mean'),
    avg_diastolic=('DIASTOLIC_BP', 'mean'),
    avg_bmi=('BMI', 'mean')
).reset_index()
agg_age['prevalence_rate'] = agg_age['hypertensive_count'] / agg_age['total_surveys']
agg_age.to_parquet("data/agg_by_age_group.parquet", index=False)

print("Pre-aggregated Parquet files successfully generated in 'data/':")
print(f"1. agg_by_state.parquet: {len(agg_state)} rows")
print(f"2. agg_by_zone_year.parquet: {len(agg_zone_year)} rows")
print(f"3. agg_by_age_group.parquet: {len(agg_age)} rows")

# Reconciliation totals for comparison
total_pop = len(df)
total_high_bp = df['HIGH_BP_FLAG'].sum()
overall_prev = total_high_bp / total_pop

print("\n--- Raw Reconciliation Benchmarks ---")
print(f"Total Surveys:        {total_pop:,}")
print(f"Total Hypertensive:   {total_high_bp:,}")
print(f"Overall Prevalence:   {overall_prev * 100:.2f}%")