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