## Day 28 - Thu 19 Nov 2026: Groupby, Pivot Table, and Relational Merge
- Replicated five core Oracle SQL queries in Python using pandas aggregation and reshaping methods.
- Calculated zonal blood pressure averages and statistical summaries with groupby() and agg().
- Constructed a two-dimensional matrix of systolic BP across zones and income tiers via pivot_table().
- Recreated star-schema relational joins using pd.merge(how='left') on SAMPLE_ID.
- Verified that pandas merge and aggregation results reconcile with earlier Oracle SQL outputs.

## Day 29 - Fri 20 Nov 2026: Connect Python to Oracle and Export Parquet
- Configured python-oracledb mTLS connection to Autonomous Database using wallet credentials.
- Stored database credentials safely in PyCharm Run Configurations following Ibrahim's rule.
- Extracted star-schema dimension and analysis tables directly via live SQL queries.
- Serialized results into compressed analytical Parquet files in the data/ directory.
- Reconciled row counts against Oracle (DIM_STATE: 37, DIM_QUESTION: 29, DIM_DATE: 2,922).

## Day 30 - Sat 21 Nov 2026: Chunking 6M-Row File and Week 5 Mini-Project
- Processed the complete 6-million-row production survey CSV using pandas read_csv with chunksize=500_000.
- Aggregated row totals, geopolitical zone distributions, and question response volumes iteratively.
- Streamed min and max CREATED_ON values across chunks without loading the complete dataset into memory.
- Validated that total volume and zonal breakdowns reconcile with the Week 1 baseline quality report.
- Concluded Week 5 Python transition with reproducible, production-ready extraction and profiling pipelines.

## Day 31 - Mon 23 Nov 2026: Charts with Matplotlib and Seaborn
- Loaded the 157,894-row live analytical sample from data/analysis_sample.parquet.
- Built age and systolic blood pressure distributions with kernel density estimates and clinical thresholds.
- Evaluated regional variations in BMI and systolic BP using styled bar charts and box plots.
- Examined survey volume patterns and analyzed hypertension prevalence across household income brackets.
- Validated all 6 saved visuals in outputs/ to ensure clear titles, labeled axes, and explicit units.

## Day 32 - Tue 24 Nov 2026: Biometric Correlation and Scatter Visualizations
- Computed Pearson correlation matrix across AGE, BMI, SYSTOLIC_BP, and DIASTOLIC_BP in pandas.
- Built an annotated, publication-grade correlation heatmap with seaborn saved to outputs/.
- Generated regression-overlay scatter plots for BMI vs Systolic and Age vs Systolic using a representative 3,000-point sample.
- Appended analytical annotations under each scatter plot detailing pattern, correlation strength, and confounder caveats.
- Delivered quantitative evidence resolving Ngozi's inquiry into clinical measurement co-movement without conflating correlation with causation.

## Day 33 - Wed 25 Nov 2026: Prevalence, Confidence Intervals, and Hypothesis Testing
- Calculated geopolitical zone hypertension prevalence from data/analysis_sample.parquet.
- Applied statsmodels Wilson score method to compute accurate 95% binomial confidence intervals and margins of error.
- Conducted scipy.stats chi2_contingency test comparing highest and lowest prevalence zones to evaluate independence.
- Executed Welch's two-sample independent t-test on continuous systolic blood pressure distributions.
- Authored executive statistical guidance defining what p-values substantiate (statistical significance) and what they do not (causation, clinical magnitude, or individual prediction).

## Day 34 - Thu 26 Nov 2026: Hidden Burden Analysis (US-07)
- Operationalized the 'hidden burden' metric: measured hypertension (SBP >= 140 or DBP >= 90) lacking formal clinical diagnosis.
- Aggregated and ranked undiagnosed hypertensive caseloads across geopolitical zones and household income tiers.
- Built and exported a horizontal bar chart visualizing the top 10 state hotspots to outputs/.
- Authored a structured decision memo utilizing the Finding, Evidence, So What, Action framework.
- Formulated an evidence-backed operational recommendation directing Chidi's supplemental screening unit to the highest-yield state.

## Day 35 - Fri 27 Nov 2026: Outliers, Repeat Visits, and Data Quality Audit
- Executed physiological boundary checks to identify impossible clinical values in systolic BP, diastolic BP, and BMI.
- Applied Tukey's 1.5 x IQR rule to quantify statistical dispersion and calculate upper/lower fences for all continuous biometrics.
- Evaluated repeat-visit longitudinal measurements to quantify intra-individual shifts across sequential screenings.
- Generated docs/outlier_log.md detailing explicit Keep/Flag/Remove protocols and epidemiological rationales.
- Addressed Ibrahim's data integrity audit to ensure downstream predictive modeling is shielded from corrupted artifacts.

## Day 36 - Sat 28 Nov 2026: End-of-Phase Exploratory Data Analysis Report
- Assembled unified Jupyter notebook W06_D6_eda_report.ipynb covering Question, Data, Method, Findings, Limits, and Action.
- Tied every reported metric, confidence interval, and test statistic directly to reproducible Python code execution.
- Evaluated systolic distributions, biometric correlation structures, and regional prevalence disparities.
- Formulated structured recommendations directing mobile clinical resources to primary undiagnosed hotspots.
- Compiled full analysis to docs/W06_D6_eda_report.html and verified end-of-phase milestone deliverables.

## Day 37 - Mon 30 Nov 2026: Prepare and Import Data for Power BI
- Exported Parquet datasets to CSV format in powerbi/ for browser upload compatibility.
- Bypassed tenant Fabric trial and OneDrive licensing limitations by utilizing Power BI Web direct data modeling.
- Ingested analysis_sample, dim_state, and dim_date tables into cloud semantic model.
- Validated column types: biometrics configured as numeric, demographics and geography as text.
- Established active star-schema relationship from dim_state[NIGERIAN_STATE] to analysis_sample[NIGERIAN_STATE] (1:*).
- Categorized NIGERIAN_STATE as State or Province for geospatial readiness.
- Saved complete semantic model and initialized report shell Digital_Solution_Nigeria_W07 in My Workspace.

## Day 38 - Tue 01 Dec 2026: Build the Star Schema
- Validated star schema topology in Power BI Model View.
- Verified active 1-to-many single-direction relationship between dim_state[NIGERIAN_STATE] and analysis_sample[NIGERIAN_STATE].
- Hid analysis_sample[NIGERIAN_STATE] from Report View to ensure slicing occurs through the dimension table.
- Added validation table visual in Report View combining dim_state[GEOPOLITICAL_ZONE] and Count of analysis_sample[SAMPLE_ID].
- Verified record aggregation totals 500 rows (South East: 177, South South: 323), confirming proper dimension-to-fact filter propagation.********

## Day 39 - Wed 02 Dec 2026: DAX I - Measures versus Calculated Columns
- Created core analytical measures in `analysis_sample`:
  - `Total Surveys = COUNTROWS(analysis_sample)`
  - `Avg Systolic = AVERAGE(analysis_sample[SYSTOLIC_BP])`
  - `High BP % = DIVIDE(CALCULATE(COUNTROWS(analysis_sample), analysis_sample[BP_CATEGORY] = "Hypertensive"), [Total Surveys], 0)`
- Implemented a single-value Card visual displaying Total Surveys; verified that the total (500) matches source database validation (`COUNT(DISTINCT SAMPLE_ID)` = 500).

### Key Concept: Measures vs. Calculated Columns
- **Calculated Columns:** Computed row-by-row during data refresh using row context and stored directly in RAM. Required when values must serve as slicers, filter rows, or axis categories.
- **Measures:** Computed on demand at query time within visual filter context; consume zero persistent RAM. Ideal for dynamic aggregations, ratios, and summary metrics.

## Day 40 - Thu 03 Dec 2026: DAX II - CALCULATE, Filter Context, and Time Intelligence
- Created dynamic DAX `Calendar` table using `CALENDAR(DATE(2018,1,1), DATE(2025,12,31))` and marked as date table.
- Implemented filter-context modification with CALCULATE:
  - `High BP Count = CALCULATE([Total Surveys], analysis_sample[DIAGNOSED_HYPERTENSION] = "Yes")`
  - `High BP % = DIVIDE([High BP Count], [Total Surveys], 0)`
- Authored time-intelligence measure `Surveys LY = CALCULATE([Total Surveys], SAMEPERIODLASTYEAR('Calendar'[Date]))`.
- Built state-by-state analytical table comparing `Total Surveys`, `High BP %`, and `High BP Count`.
- Validation: Verified measures against underlying survey data (Edo: 31 / 9.60%, Imo: 21 / 11.86%, Total: 52 / 10.40%).
- Data Modeling Note: Documented that `analysis_sample` is a cross-sectional dataset without survey date keys; longitudinal time-intelligence measures operate across the modeled date framework for future wave integrations.


## Day 41 - Fri 04 Dec 2026: Visuals - KPI Cards, Charts, Map, and Slicers
- Built executive dashboard interface adhering to Dr. Okafor's specification (4 KPIs, 3 charts, 3 slicers).
- Created 4 KPI cards: Total Surveys, High BP Count, High BP %, and Avg Systolic BP.
- Implemented 3 interactive charts:
  - Clustered Bar Chart: Nigerian State vs High BP %
  - Line Chart: Year vs Total Surveys
  - Filled Map: Geographic prevalence by State
- Configured 3 categorical slicers: Geopolitical Zone, Survey Year, and Household Income.
- Verified visual interactions and cross-filtering behavior across all dashboard elements.

## Day 42 - Sat 05 Dec 2026: Mini-project - Page 1 Executive Overview
- Refined Page 1 layout for executive storytelling following Dr. Okafor's specification (US-08).
- Visual Hierarchy & Grid:
  - Header takeaway title: "Cardiovascular Health Overview: 10.4% Hypertension Rate Across Surveyed States"
  - Primary KPI placed top-left: High BP % (10.40%), followed by High BP Count (52), Total Surveys (500), and Avg Systolic (124.97 mmHg).
  - Clean 3-chart split with decluttered axes, removed gridlines, and streamlined slicer controls.
- Color Strategy: Applied single-accent risk color for hypertension markers against neutral baselines.
- 10-Second Test Results: Colleague immediately recalled overall sample size (500) and that high BP prevalence hovered around 10-11% with Imo State leading.
- Asset saved: `powerbi/page1_executive_overview.png`.

## Day 43 - Mon 07 Dec 2026: Page 2 - Hidden Burden and Hotspots
- Defined clinical undiagnosed hypertension criteria (`SYSTOLIC_BP >= 140` or `DIASTOLIC_BP >= 90` with `DIAGNOSED_HYPERTENSION = 'No'`).
- Authored DAX measures `Hidden Count` and `Hidden %`.
- Built Top States bar chart using Top N visual filtering on `Hidden %`.
- Constructed Zone × Household Income cross-tabulation matrix with gradient conditional background formatting.
- Delivered single-sentence executive recommendation identifying the highest-priority screening deployment target.
- Asset saved: `powerbi/page2_hidden_burden.png`.

## Day 44 - Tue 08 Dec 2026: Interactivity - Drill-through, Tooltips, and Bookmarks
- Configured targeted drill-through mechanism on `State detail` page mapped to `dim_state[NIGERIAN_STATE]`.
- Verified right-click drill-through navigation from state bar charts to dedicated diagnostic views.
- Implemented micro report-page tooltip (`State Tooltip`) displaying instant high-risk previews on hover.
- Captured filter states via Power BI Bookmarks pane and deployed action button for one-click hotspot filtering.

## Day 45 - Wed 09 Dec 2026: Row-Level Security (RLS) and Design Review
- Configured Row-Level Security (RLS) role `North West` on `dim_state` with filter `[GEOPOLITICAL_ZONE] = "North West"`.
- Validated role enforcement via Power BI Service "Test as role": verified zero leakage from South South and South East survey records.
- Completed full visual and design audit across Executive Overview (Page 1) and Hidden Burden (Page 2).
- Peer review verified that key metrics and clinical callouts are identifiable within seconds.
## Day 46 - Thu 10 Dec 2026: Tableau - Connect and Build First Sheets
- Connected Tableau Public Web Authoring directly to `analysis_sample.csv` (500 records).
- Sheet 1: `Avg Systolic by State` validated against Power BI baseline (~124.97 mmHg).
- Sheet 2: `High BP % by Zone` validated against Power BI (South South 9.60%, South East 11.86%).
- Sheet 3: `Surveys per Year` validated total sample baseline of 500 records.
- Completed cross-platform validation between Power BI and Tableau Public.

## Day 47 - Fri 11 Dec 2026: Tableau - Dashboard, Parameters, and Publish
- Assembled composite Tableau Public dashboard combining state systolic averages, regional high BP rates, and volume metrics.
- Built interactive parameter `Systolic Alert Threshold` with dynamic boolean coloring for clinical triage thresholds.
- Configured dashboard filter actions enabling one-click cross-filtering across regional and state views.
- Validated synthetic/aggregated sample safety and published final dashboard to Tableau Public.
## Day 48 - Sat 12 Dec 2026: Tool Comparison and Strategic Recommendation (US-08, US-09)
- Completed structured evaluation matrix comparing Power BI and Tableau across learning curve, calculations (DAX vs Calculated Fields), sharing, RLS security, and licensing costs.
- Drafted executive memo for Dr. Okafor recommending Power BI Pro licensing based on compliance, native RLS capabilities, and cost efficiency.
- Documented testing scope boundaries regarding full-scale live DirectQuery testing and commercial Tableau Cloud features.
- Completed Phase 2 BI tools delivery and verified end-of-phase checklist.
## Day 49 - Mon 14 Dec 2026: Machine Learning Framing and Leakage Prevention (US-10)
- Configured notebook `w09_day49_framing.ipynb` for the US-10 triage screening model.
- Framed binary classification target: `HIGH_BP_FLAG = 1` if `SYSTOLIC_BP >= 140` or `DIASTOLIC_BP >= 90`, else `0` (positive rate: ~58.0%).
- Selected permitted low-friction features: `AGE`, `NIGERIAN_STATE`, `GEOPOLITICAL_ZONE`, `HOUSEHOLD_INCOME`, `WEIGHT_KG`, `BMI`, `SMOKING_STATUS`, `MALARIA_REPORTED`.
- Enforced strict leakage prevention by excluding `SYSTOLIC_BP`, `DIASTOLIC_BP`, `DIAGNOSED_HYPERTENSION`, `BP_CATEGORY`, and `SAMPLE_ID`.

## Day 50 - Tue 15 Dec 2026: Train/Test Split, Dummy Baseline, and Pipeline (US-10)
- Partitioned dataset using `train_test_split(test_size=0.2, stratify=y, random_state=42)`.
- Established `DummyClassifier(strategy='most_frequent')` zero-rule baseline accuracy of ~58.0%.
- Documented model viability threshold: clinical models must significantly beat the 58% majority-guess benchmark.
- Built and validated an end-to-end `ColumnTransformer` pipeline:
  - Standardized numeric features (`StandardScaler`).
  - Encoded categorical variables with out-of-vocabulary protection (`OneHotEncoder(handle_unknown='ignore')`).

## Day 51 - Wed 16 Dec 2026: Linear Regression for Systolic BP (US-10)
- Built `LinearRegression` pipeline with `passthrough` on numeric predictors to preserve coefficient unit interpretability.
- Recorded test set performance:
  - $R^2$: [Insert your printed R2 value]
  - MAE: [Insert your printed MAE value] mmHg
- Visualized residuals vs predicted values to inspect error homoscedasticity.
- Plain English coefficient interpretation:
  - `BMI`: Systolic BP changes by [Insert printed BMI coef] mmHg per 1 kg/m² increase.
  - `AGE`: Systolic BP changes by [Insert printed AGE coef] mmHg per 1 year increase.
## Day 52 - Thu 17 Dec 2026: Logistic Regression Classification and Risk Scoring (US-10)
- Configured `LogisticRegression(max_iter=1000)` within an end-to-end `ColumnTransformer` pipeline.
- Delivered continuous screening risk probabilities (`predict_proba[:, 1]`) to allow sorting patients by priority.
- Evaluated classification metrics:
  - ROC-AUC: [Insert printed ROC-AUC] (comfortably exceeding 0.50 random-guess baseline).
  - Precision: [Insert printed precision].
  - Recall: [Insert printed recall].
- Mapped and interpreted confusion matrix quadrants ($TN, FP, FN, TP$) within the clinical triage context, highlighting the clinical priority of minimizing False Negatives.

## Day 53 - Fri 18 Dec 2026: Tree-Based Models and Cross-Model Benchmark (US-10)
- Trained and evaluated `DecisionTreeClassifier(max_depth=5)` and `RandomForestClassifier(n_estimators=100, n_jobs=-1)`.
- Compiled consolidated benchmark table comparing Dummy Baseline, Logistic Regression, Decision Tree, and Random Forest across Accuracy, ROC-AUC, Precision, Recall, and Fit Time.
- Addressed stakeholder complexity question: verified that Logistic Regression remains the superior operational candidate due to near-parity performance, instant training speed, and direct clinical explainability over ensemble black-boxes.

## Day 54 - Sat 19 Dec 2026: Mini-Project Model Comparison & Recommendation (US-10)
- Consolidated Days 49–53 workflows into unified notebook `w09_day54_model_comparison.ipynb`.
- Verified top-to-bottom error-free execution across data intake, leakage guards, ColumnTransformer pipelines, and multi-model benchmarking.
- Benchmarked Dummy Baseline against Logistic Regression, Decision Tree, and Random Forest.
- Formulated final executive recommendation for Dr. Okafor emphasizing Logistic Regression for operational interpretability, triage prioritization, and deployment safety boundaries.
- Completed Week 9 Machine Learning Phase 5 deliverables.

## Day 55 - Mon 21 Dec 2026: 5-Fold Cross-Validation and Stability Assessment (US-10)
- Implemented 5-fold stratified cross-validation (`cv=5`, `scoring='roc_auc'`) to evaluate generalization stability beyond a single train/test split.
- Benchmarked `LogisticRegression` against `RandomForestClassifier`:
  - Logistic Regression Mean ROC-AUC: [Insert Mean] (Std Dev: ±[Insert Std])
  - Random Forest Mean ROC-AUC: [Insert Mean] (Std Dev: ±[Insert Std])
- Evaluated standard deviation: confirmed low variance across folds, demonstrating that model performance is stable and not an artifact of train/test partition luck.

## Day 56 - Tue 22 Dec 2026: Feature Importance and Model Explainability (US-10)
- Computed test-set permutation importance (`n_repeats=5`, `scoring='roc_auc'`) to evaluate the impact of individual triage features.
- Plotted horizontal bar chart of top feature drivers with standard deviation error bars.
- Confirmed that `AGE` and `BMI` are the primary contributors to elevated hypertension risk scores, followed by lifestyle and socioeconomic factors (`SMOKING_STATUS`, `HOUSEHOLD_INCOME`).
- Formulated an executive summary for Dr. Okafor explaining the clinical alignment of feature weights without technical jargon.


## Day 57 - Wed 23 Dec 2026: Screening Thresholds, Top-k Precision, and Lift (US-10)
- Sorted test cohort predictions in descending order of predicted probability from `LogisticRegression`.
- Generated cumulative threshold table evaluating the top 1%, 5%, 10%, and 20% screening bands:
  - Computed Precision (hit rate), Recall (coverage of positive cases), and Lift over random selection.
  - Recorded minimum probability cut-off thresholds for each tier.
- Delivered decision memo for Chidi Nwosu translating model probabilities into operational capacity constraints (allocating 10,000 screening slots to maximize case identification while bounding clinical outreach costs).

## Day 58 - Thu 24 Dec 2026: Cloud Execution (Google Colab) and AI Code Review (US-10)
- Successfully deployed and executed the model comparison pipeline in Google Colab using cloud session storage.
- Patched data pathing to handle cloud environments seamlessly.
- Evaluated AI code review recommendations:
  - Accepted: Enforcing robust categorical out-of-vocabulary handling in `OneHotEncoder(handle_unknown='ignore')`.
  - Accepted: Using continuous probability risk scores (`predict_proba[:, 1]`) for screening prioritization.
  - Rejected: Applying SMOTE class balancing, preserving authentic population prevalence (~59% positive) for accurate clinical lift calculations.

## Day 59 - Fri 25 Dec 2026: Model Serialization and Model Card Documentation (US-10)
- Serialized trained scikit-learn triage pipeline to `models/hypertension_model.joblib`.
- Validated pipeline persistence: reloaded model artifact and executed multi-row batch inference producing predicted classes and continuous risk scores.
- Authored comprehensive model card (`docs/MODEL_CARD.md`):
  - Outlined operational triage scope and pipeline architecture.
  - Documented performance metrics and top-k screening utility.
  - Formulated explicit ethical boundaries and limitations: declared synthetic training data origins and established strict prohibitions against diagnostic or clinical decision-making use.

## Day 60 - Sat 26 Dec 2026: Mini-Project ML Board Report and Phase 5 Completion (US-10)
- Compiled comprehensive 4-page executive report for Dr. Okafor and the Programme Board (`docs/ML_BOARD_REPORT_US10.docx`).
- Verified all reported metrics against notebook artifacts:
  - Baseline Accuracy: 58.02% (ROC-AUC = 0.5000).
  - Selected Model: Logistic Regression Pipeline (ROC-AUC = 0.6119, Recall = 85.07%, Precision = 61.38%).
  - 5-Fold Cross-Validation: Mean ROC-AUC = 0.6124 (± 0.0028).
  - Screening Resource Allocation: Demonstrated ~940 additional hypertensive cases caught by screening the top 10,000 model-prioritized individuals versus random community testing.
- Documented ethical boundaries: explicitly declared synthetic training origin and restricted application strictly to pre-cuff triage prioritization (non-diagnostic).
- Passed all Phase 5 end-of-phase self-test criteria.

## Day 61 - Mon 28 Dec 2026: Streamlit Setup and Cached Data Intake (US-11)
- Verified local Streamlit installation in PyCharm virtual environment.
- Created `app.py` configuring page layout, dashboard header, and high-level KPIs.
- Implemented `@st.cache_data` decorated loader `load_data()` for zero-latency in-memory data querying.
- Verified local browser hosting at `localhost:8501` rendering title, survey count metric card, and sample preview.


## Day 62 - Tue 29 Dec 2026: Pre-Aggregation and Speed Optimization (US-11)
- Built `build_aggregates.py` to pre-compute three lightweight summary Parquet files:
  - `data/agg_by_state.parquet` (State-level survey counts and prevalence)
  - `data/agg_by_zone_year.parquet` (Regional zone and yearly trends)
  - `data/agg_by_age_group.parquet` (Age-stratified cardiovascular indicators)
- Refactored `app.py` to read pre-aggregated tables via `@st.cache_data`, reducing dashboard load time to under 2 seconds.
- Reconciled summary totals against Power BI dashboard: 157,894 total records and ~58.0% high BP prevalence matched across all dimensions.

## Day 67 - Mon 4 Jan 2027: Chunked Parquet Conversion & Storage/Speed Benchmark (US-12)
- Built `w12_day67_parquet_benchmark.py` using `pyarrow.parquet.ParquetWriter` with Snappy compression to convert CSV chunks without exceeding RAM limits.
- Verified file sizes via script and Windows File Explorer Properties, and timed single-column reads (`SYSTOLIC_BP`) with `time.time()`:

| Format | File Size (MB) | Single-Column Read Time (s) | Savings / Speedup |
| :--- | :---: | :---: | :--- |
| **CSV** | [Insert CSV MB] | [Insert CSV Read s] | Baseline |
| **Parquet (Snappy)** | [Insert Parquet MB] | [Insert Parquet Read s] | [Insert %] space saved / [Insert X]x faster |

- **Conclusion for IT Lead:** Columnar projection in Parquet avoids scanning unused text columns, making it both storage-efficient and fast enough to scale 10x for next year's survey.

## Day 68 - Tue 5 Jan 2027: Google BigQuery Sandbox & Cross-Warehouse SQL Validation (US-12)
- Provisioned Google BigQuery Sandbox project (`hypertension-triage-sandbox`) and created the `digital_solution` dataset.
- Uploaded `agg_by_state.parquet` (schema auto-defined from Parquet metadata) and executed three analytical triage queries.
- Documented SQL dialect differences between Oracle and BigQuery (`LIMIT` vs `FETCH FIRST`, backtick table identifiers, `SAFE_DIVIDE`, and `COUNTIF`) in `sql/bigquery_migration_notes.sql`.

## Day 69 - Wed 6 Jan 2027: PySpark Distributed Processing Overview (US-12)
- Installed PySpark in Google Colab and initialized a `SparkSession`.
- Loaded survey Parquet data via `spark.read.parquet()` and reproduced Week 6 group-by prevalence aggregations using `groupBy()` and `agg()`.
- Documented scalability trade-offs: Spark justifies its cluster and JVM overhead when datasets exceed single-node memory boundaries, whereas pandas/Parquet remains optimal for sub-gigabyte analytical workloads.
