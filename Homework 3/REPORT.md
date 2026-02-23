# Data Quality Report: Page Blocks

**Date:** Feb 15, 2026  
**Dataset:** `page_blocks_dirty.csv` (5473 data rows)

## Part 1: Mechanical Checks (gawk)

### S1: Ragged Rows
* **Status:** ✅ Clean
* **Findings:** All rows have exactly 13 fields (matching the header). No parsing errors detected.

### S2: Missing Values
* **Status:** ⚠️ Issues Found
* **Affected Columns:** `P_AND`, `MEAN_TR`
* **Affected Rows:** ~23 rows contain the placeholder `?`.
* **Impact:** Missing data appears random; these rows must be handled (imputed or dropped) before statistical analysis.

### S3: Constant Columns
* **Status:** ⚠️ Issues Found
* **Column:** `DATASET_ID`
* **Findings:** This column contains the value `1` for every single row. It provides no information and should be dropped.

### S4: Bad Class Labels
* **Status:** ❌ Critical Data Error
* **Findings:** The `class!` target variable contains invalid values (expected `1`–`5`).
* **Examples:** Row 987 contains `7`; Row 1222 contains `0`.
* **Action:** These labels are likely typos or corruption and will break classification models.

### S5: Duplicate Rows
* **Status:** ⚠️ Issues Found
* **Findings:** Several rows are exact duplicates of earlier rows.
* **Example:** Row 580 is an exact copy of Row 11.
* **Action:** Duplicates artificially inflate sample weight and should be deduplicated.

---
*Summary: The dataset has structural integrity (no ragged rows) but suffers from significant content errors, including corrupt target labels and useless constant features.*

## Part 2: Statistical & Domain Knowledge Checks (Python)

### Feature-Level Issues (Checks A–F)
* **A & B (Identical & Correlated Features):** Evaluated feature redundancy. Highly correlated columns (Pearson |r| > 0.95) and identical columns point to opportunities for dimensionality reduction.
* **C (Outlier Features):** Several features contained values exceeding 3 standard deviations (3σ) from the column mean, indicating heavy right-skew or extreme anomalies in the data collection.
* **D & E (Conflicting & Implausible Features):** Highlighted features that violated fundamental physical logic (e.g., negative physical dimensions like `HEIGHT` at row 140) or referential logic (e.g., mismatch between `AREA` and `HEIGHT * LENGHT`).
* **Total Problem Features (F):** A significant subset of the columns exhibit at least one logical or statistical anomaly, necessitating heavy scaling/cleaning before modeling.

### Case-Level Issues (Checks G–M)
* **G & I (Outlier Cases):** Evaluated rows containing anomalies both globally (>3σ from overall mean) and class-conditionally (>3σ from class mean). A row might look normal overall but be completely anomalous for its specific `class!`.
* **H (Inconsistent Cases):** Uncovered a small set of rows (12 instances) that have the exact same feature inputs but map to different output classes. This inconsistency creates impossible contradictory mapping for ML algorithms. 
* **J & K (Conflicting & Implausible Cases):** Flagged 16 specific rows with mathematically impossible proportions or bounding-box constraints.
* **Total Problem Cases (L & M):** In total, **753 unique rows** contain at least one data quality defect. This implies that roughly **13.7%** of the dataset (753 out of 5473 rows) requires imputation, bounding, or dropping prior to training a machine learning model.