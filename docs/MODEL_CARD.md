# Model Card: Hypertension Community Triage Model (US-10)

## 1. Model Details
- **Developer:** AI Engineering & Health Analytics Team
- **Model Date:** December 2026
- **Model Version:** v1.0.0
- **Model Type:** Scikit-Learn Pipeline (`StandardScaler`, `OneHotEncoder`, `LogisticRegression`)
- **Serialized Asset:** `models/hypertension_model.joblib`

## 2. Intended Use & Clinical Purpose
- **Primary Purpose:** Fast, non-invasive risk stratification to prioritize individuals for blood pressure screening during community outreach.
- **Workflow Position:** Triage intake filter (under 2 minutes per patient) used prior to screening cuff measurements.
- **Out of Scope / Prohibited Use:** 
  - **Diagnostic Use:** This model is **not a diagnostic tool** and must never replace clinical assessment, diagnostic protocols, or physical blood pressure cuff measurements.
  - **Real Clinical Decisions:** This model is trained on synthetic survey data generated for training and prototyping. **It must not be used for real clinical decision-making or real patient management.**

## 3. Data & Permitted Inputs
- **Training Population:** Nigerian healthcare demographic and lifestyle survey (synthetic cohort).
- **Target Definition:** `HIGH_BP_FLAG` (1 if Systolic BP >= 140 mmHg or Diastolic BP >= 90 mmHg, else 0).
- **Permitted Features:**
  - Demographic: `AGE`, `NIGERIAN_STATE`, `GEOPOLITICAL_ZONE`
  - Anthropometric: `WEIGHT_KG`, `BMI`
  - Socioeconomic & Behavioral: `HOUSEHOLD_INCOME`, `SMOKING_STATUS`, `MALARIA_REPORTED`
- **Leakage Controls:** Direct blood pressure measurements (`SYSTOLIC_BP`, `DIASTOLIC_BP`), clinical diagnoses (`DIAGNOSED_HYPERTENSION`), and derived groupings (`BP_CATEGORY`) were strictly excluded.

## 4. Performance & Evaluation Metrics
Evaluated on an 80/20 stratified test split (31,579 records):
- **ROC-AUC:** ~0.612 (Exceeds zero-rule baseline of 0.500)
- **Baseline Majority Accuracy:** 58.02%
- **Recall:** ~85.1% (Tuned to minimize false negatives and catch potential cases)
- **Precision:** ~61.4%
- **Top 10% Lift:** Delivers substantial precision gain over random selection for fixed outreach budgets (e.g., screening 10,000 individuals).

## 5. Limitations & Ethical Considerations
- **Synthetic Data Limitations:** The dataset reflects simulated distributions. Patterns may not account for real-world unmeasured confounders (e.g., genetic predispositions, dietary sodium, severe stress).
- **False Negative Risk:** Patients with atypical or early-stage hypertension who lack elevated BMI or advanced age may be assigned low triage risk scores. Community teams should maintain routine opportunistic screening regardless of model score.
- **Geographic Bias:** Categorical encoding reflects predefined administrative zones; regional health teams must monitor for disparate false-negative rates across states.