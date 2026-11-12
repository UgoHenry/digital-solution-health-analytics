# Community Hypertension Screening & Triage Analytics (`US-10` – `US-12`)

An end-to-end data engineering, machine learning, and interactive decision-support application designed to prioritize community blood pressure screening under constrained outreach budgets.

## 1. Clinical & Business Problem
Hypertension affects roughly **58%** of the surveyed cohort, yet community outreach teams operate with limited test kits and nursing capacity. Nurses need a **non-invasive, under-two-minute intake triage filter** to rank individuals by hypertension risk *before* administering a physical blood pressure cuff measurement.

## 2. Dataset & Governance (Synthetic Cohort)
- **Scale:** 157,894 synthetic survey records across Nigerian states and geopolitical zones.
- **Target (`HIGH_BP_FLAG`):** `1` if Systolic BP >= 140 mmHg or Diastolic BP >= 90 mmHg, else `0`.
- **Anti-Leakage Controls:** Direct clinical readings (`SYSTOLIC_BP`, `DIASTOLIC_BP`), prior diagnoses (`DIAGNOSED_HYPERTENSION`), and derived categories (`BP_CATEGORY`) are strictly excluded from input features.
- **Disclaimer:** Trained on **synthetic data** for portfolio demonstration; strictly non-diagnostic and not intended for live clinical decision-making.

## 3. Architecture & Methods
- **Machine Learning Pipeline (`scikit-learn`):** Encapsulated preprocessing (`SimpleImputer`, `StandardScaler`, `OneHotEncoder(handle_unknown='ignore')`) paired with `LogisticRegression`, serialized to `models/hypertension_model.joblib`.
- **Interactive Web App (`Streamlit`):** Backed by pre-aggregated Parquet summaries (`agg_by_state.parquet`, `agg_by_zone_year.parquet`, `agg_by_age_group.parquet`) for sub-2-second load times and dynamic zone/year filtering (`app.py`).
- **Big Data & Cloud Portability:** Chunked Snappy Parquet compression (`pyarrow`), cross-warehouse SQL validation in **Google BigQuery**, and distributed aggregation benchmarks in **Apache Spark (PySpark)**.

## 4. Key Results & Clinical Impact
| Model / Benchmark | Accuracy | ROC-AUC | Recall | Operational Takeaway |
| :--- | :---: | :---: | :---: | :--- |
| **Zero-Rule Baseline** | 59.4% | 0.500 | 100.0% | Naive majority-class benchmark |
| **Logistic Regression (Selected)** | **59.3%** | **0.612** | **85.1%** | **Best generalization (±0.0028 5-fold CV) & clinical explainability** |
| **Random Forest (100 trees)** | 58.3% | 0.598 | 70.9% | 28x slower training with lower discriminative power |

- **Resource Lift:** Screening the **top 10,000 individuals** ranked by predicted risk captures **~6,740 hypertensive cases** vs. ~5,800 under random testing (**+940 additional cases detected** with zero extra test kits).

## 5. Key Project Deliverables
- **Streamlit Dashboard:** `app.py`
- **Board Executive Report:** `docs/ML_BOARD_REPORT_US10.docx`
- **Model Card & Ethics:** `docs/MODEL_CARD.md`
- **EDA & Visual Charts:** `outputs/`
- **BigQuery & Parquet Scripts:** `sql/bigquery_migration_notes.sql`, `w12_day67_parquet_benchmark.py`

## 6. How to Run Locally
```bash
git clone [https://github.com/UgoHenry/digital-solution-health-analytics.git](https://github.com/UgoHenry/digital-solution-health-analytics.git)
cd digital-solution-health-analytics
pip install pandas numpy scikit-learn pyarrow streamlit joblib
streamlit run app.py