# Legal-Economy-Coupling

Builds the balanced legal-economy panel, estimates the annual coupling results, and produces the values reported in Supplementary Table 4.

## Execution order

1. **`Legal_Economy_Data.ipynb`** — Creates the balanced legal-economy panel.
2. **`Legal_Economy_Results.ipynb`** — Uses that panel to estimate and export the annual results used in Supplementary Table 4.

## Code documentation

## Legal-Economy Coupling Data Construction

**Code file:** `Legal_Economy_Data.ipynb`

### Purpose

Constructs the balanced MSA-year panel used to analyze the relationship between lawyer employment, legal expenditures, population, and metropolitan GDP.

### What the code does

1. Defines the valid metropolitan MSA geography.
1. Loads annual ACS population, BEA real GDP, and harmonized BLS occupational data.
1. Keeps Lawyers and All Occupations from the BLS tables.
1. Computes total legal payroll as mean annual lawyer pay multiplied by lawyer employment and total salary payroll for All Occupations.
1. Adjusts nominal payroll and lawyer wage measures to chained 2017 dollars using the notebook’s inflation factors.
1. Merges population and GDP and retains MSAs observed in every common year.
1. Calculates lawyers per capita and legal expense divided by GDP.

### Required inputs

- `Data/Geography/FIPS/US states FIPS.csv`
- `Data/Geography/CBSA_shapefile_2025/tl_2025_us_cbsa.shp`
- Annual ACS population files in `Data/Population Data/MSA Population/`
- `Data/BLS data/GDP/GDP and Personal Income Formatted.csv`
- Annual `Data/Processed Data/Filtered tables/MSA_<year>_Filtered_Extended_Professions.xlsx` files

### Outputs

- `Data/Processed Data/Legal-Economy-Coupling/Legal_Economy_Data.csv`

### Dependencies

- `pandas`
- `geopandas`
- `openpyxl`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. Run it from within the repository; the notebook locates the repository root automatically by searching the current directory and its parents for the `Scripts` folder.

### Notes

- GDP is read as real GDP in thousands of chained 2017 dollars and multiplied by 1,000.
- The final panel reflects the intersection of years available in the population, GDP, and BLS sources.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.

---

## Legal-Economy Coupling Results

**Code file:** `Legal_Economy_Results.ipynb`

### Purpose

Estimates annual scaling relationships for the legal economy and the yearly association between lawyers per capita and legal expenditure as a share of GDP. The yearly linear-model estimates are the source for Supplementary Table 4.

### What the code does

1. Loads the balanced legal-economy data table.
1. Creates GDP per capita and mean lawyer pay relative to GDP per capita for theoretical comparisons.
1. For each year, fits HC1-robust log-log OLS models of legal expense, GDP, and lawyer employment on population.
1. Optionally creates annual power-law scatter plots when the `plot` flag is enabled.
1. For each year, fits an HC1-robust linear model of lawyers per capita on legal expense divided by GDP.
1. Creates yearly scatter plots and stores slopes, intercepts, confidence intervals, R-squared, and sample sizes.

### Required inputs

- `Data/Processed Data/Legal-Economy-Coupling/Legal_Economy_Data.csv`

### Outputs

- `Data/Processed Data/Legal-Economy-Coupling/scaling_table.csv`
- `Data/Processed Data/Legal-Economy-Coupling/Legal_Economy_Results.csv`
- Yearly diagnostic plots displayed in the notebook; figure files are not saved.

`Legal_Economy_Results.csv` contains the year, slope, intercept, 95% confidence intervals, `R^2`, and sample size used to typeset Supplementary Table 4.

### Dependencies

- `pandas`
- `numpy`
- `statsmodels`
- `matplotlib`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. Run it from within the repository; the notebook locates the repository root automatically by searching the current directory and its parents for the `Scripts` folder.

### Supplementary Table 4 mapping

For each year, Supplementary Table 4 reports:

- slope `theta_t` from the model relating lawyers per capita to legal expense divided by GDP;
- intercept `delta_t`;
- 95% confidence intervals for both coefficients;
- coefficient of determination `R^2`; and
- sample size `n`.

These values come from `Legal_Economy_Results.csv`. Supplementary Table 3 comes from the affordability trend analysis and is documented in `Scripts/Affordability/README.md`.

### Notes

- HC1 heteroskedasticity-robust covariance estimates are used.
- The yearly figures are displayed for inspection but are not saved to disk.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.
