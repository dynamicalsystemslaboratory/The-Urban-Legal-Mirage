# Availability

Uses the completed proxy tables to compare normalized cases per lawyer across specialties.

## Execution order

1. **`Cases per Lawyer Data Collapse.nb`** — Run after all six normalized proxy CSVs have been created and copied beside the Mathematica notebook.

## Code documentation

## Cases per Lawyer Data Collapse

**Code file:** `Cases per Lawyer Data Collapse.nb`

### Purpose

Compares six specialty-specific legal-demand proxies after normalizing each proxy and lawyer-supply series by its own cross-MSA mean.

### What the code does

1. Imports the six normalized proxy tables.
1. Extracts the demand-proxy and specialty-lawyer columns for each legal field.
1. Removes nonpositive observations and divides both coordinates by their respective sample means.
1. Fits separate OLS models in base-10 log space as a sanity check and extracts slopes, confidence intervals, R-squared values, and p-values.
1. Builds a shared log-log plotting range, adds the diagonal reference line, and overlays all six collapsed specialty series with a common legend.

### Required inputs

- `Bankruptcy_Proxy_Normalized.csv`
- `Crime_Proxy_Normalized.csv`
- `Family_Proxy_Normalized.csv`
- `Immigration_Proxy_Normalized.csv`
- `Intellectual_Property_Proxy_Normalized.csv`
- `Real_Estate_Proxy_Normalized.csv`
- All six files must be placed in the Mathematica notebook directory.

### Outputs

- Model results and the combined collapsed plot are displayed in the Mathematica notebook; no separate file is exported.

### Dependencies

- `Wolfram Mathematica 14.1 or a compatible version`

### How to run

Place the six proxy CSVs beside the notebook, open it in Mathematica, and evaluate the notebook from top to bottom.

### Notes

- The collapse divides each x-series and y-series by its own arithmetic mean.
- The notebook uses the same six-color sequence as the Python proxy figure.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.
