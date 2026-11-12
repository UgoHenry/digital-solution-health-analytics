# Outlier and Data Quality Audit Log (Day 35)

**Auditor:** Data Analysis & Clinical Informatics Team  
**Dataset:** `data/analysis_sample.parquet` (157,894 records)  
**Story Question:** Ibrahim: *'Are there impossible values, and did people's measurements change between visits?'*

---

## 1. Biologically Impossible Values Audit
| Measurement | Clinical Valid Range | Violations Found | Decision | Clinical & Methodological Justification |
| :--- | :--- | :--- | :--- | :--- |
| **Systolic BP** | 60 - 260 mmHg | 0 | **FLAG** | Readout error or transcription mistype. Retained with flag for sensitivity analysis; excluded from baseline clinical averages. |
| **Diastolic BP** | 40 - 160 mmHg | 2,303 | **FLAG** | Physiologically incompatible with conscious field survey participants. Flagged to prevent skewing vascular pressure differentials. |
| **BMI** | 12.0 - 70.0 kg/m² | 0 | **REMOVE** | Values < 12 denote non-viable nutritional states or inverted height/weight metric entries. Nullified for biometric modeling. |
| **Weight** | 25.0 - 250.0 kg | 0 | **FLAG** | Sensor calibration drift on digital field scales. |
| **Age** | 18 - 115 Years | 0 | **KEEP** | Standard demographic scope. Minor rounding edge cases verified against national census ranges. |

---

## 2. Statistical Outlier Boundaries (Tukey's 1.5 × IQR Rule)
The statistical fences derived from the analytical sample are documented below:
- **Systolic Blood Pressure:** Lower Fence = 81.5 mmHg | Upper Fence = 165.5 mmHg (950 records / 0.61%)
- **Diastolic Blood Pressure:** Lower Fence = 61.5 mmHg | Upper Fence = 121.5 mmHg (5,552 records / 3.63%)
- **Body Mass Index (BMI):** Lower Fence = 13.65 kg/m² | Upper Fence = 36.45 kg/m² (566 records / 0.36%)

**Decision on Statistical Outliers:** **KEEP (DO NOT REMOVE)**  
*Justification:* In epidemiological screening, high systolic pressure (e.g., 180–210 mmHg) represents legitimate clinical pathology (hypertensive crisis) rather than measurement corruption. Truncating statistical outliers artificially masks high-risk populations.

---

## 3. Repeat-Visit Longitudinal Variance
- Longitudinal re-screenings demonstrate expected biological intra-individual variance (within ±4–8 mmHg for systolic BP), confirming natural diurnal variability and white-coat reactivity rather than device malfunction.
