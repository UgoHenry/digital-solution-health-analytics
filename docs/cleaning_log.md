# Data Cleaning & Audit Log (Day 27)

**Auditor:** Analytics Candidate  
**Dataset:** DIGITAL_SOLUTION_NIGERIA_SURVEY (sample_500k.csv)  
**Date:** Wed 18 Nov 2026  

---

## 1. Missing Values
- **NUMERIC_VALUE**: 382,481 rows missing (76.50%). Represents non-numeric/categorical survey questions.
- **SECOND_ANSWER_ID / SECOND_ANSWER_TEXT**: 495,680 rows missing (99.14%). Secondary answers only recorded for multi-part survey items.
- **ANSWER**: 903 rows missing (0.18%).
- **Key Identifiers**: `RESPONSE_ID`, `SAMPLE_ID`, `QUESTION_ID`, and `CREATED_ON` have 0 missing values (100% complete).

---

## 2. Type Conversions
- **Field:** `CREATED_ON`
  - **Source Type:** `str` (object)
  - **Target Type:** `datetime64[us]`
  - **Date Range:** 2018-01-01 00:00:00 to 2025-12-30 00:00:00
  - **Converted Rows:** 500,000 cleanly parsed.

---

## 3. Duplicate Validation
- **Field Tested:** `RESPONSE_ID`
- **Duplicate Count:** 0
- **Identical Full-Row Duplicates:** 0
- **Integrity Status:** Passed. Transactional uniqueness verified.