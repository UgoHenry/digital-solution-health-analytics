-- ============================================================================
-- Day 68: Google BigQuery Sandbox Queries & Oracle Syntax Comparison (US-12)
-- ============================================================================
-- Key Differences from Oracle SQL:
-- 1. Row Limiting: BigQuery uses `LIMIT 5` instead of Oracle's `FETCH FIRST 5 ROWS ONLY` (or `ROWNUM <= 5`).
-- 2. Identifiers: BigQuery encloses dataset.table references in backticks (`digital_solution.agg_by_state`) rather than double quotes or unquoted schema prefixes.
-- 3. Safe Division: BigQuery provides built-in `SAFE_DIVIDE(a, b)` instead of verbose `CASE WHEN b = 0 THEN NULL ELSE a / b END` or `NULLIF` wrappers.
-- 4. Conditional Aggregation: BigQuery supports `COUNTIF(condition)` directly instead of `SUM(CASE WHEN condition THEN 1 ELSE 0 END)`.

-- Query 1: Overall Cohort Totals & Weighted Prevalence
SELECT
    SUM(total_surveys) AS overall_screened,
    SUM(hypertensive_count) AS overall_hypertensive,
    ROUND(SAFE_DIVIDE(SUM(hypertensive_count), SUM(total_surveys)) * 100, 2) AS overall_prevalence_pct
FROM `digital_solution.agg_by_state`;

-- Query 2: Top 5 States by Hypertension Prevalence
SELECT
    NIGERIAN_STATE,
    total_surveys,
    ROUND(avg_systolic, 1) AS avg_systolic,
    ROUND(prevalence_rate * 100, 2) AS prevalence_pct
FROM `digital_solution.agg_by_state`
ORDER BY prevalence_rate DESC
LIMIT 5;

-- Query 3: High-Burden State Screening
SELECT
    COUNT(*) AS total_states,
    COUNTIF(prevalence_rate >= 0.60) AS states_above_60pct_prevalence,
    ROUND(AVG(avg_bmi), 2) AS national_avg_bmi
FROM `digital_solution.agg_by_state`;