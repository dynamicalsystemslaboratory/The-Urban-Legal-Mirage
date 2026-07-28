# Legal-Economy-Coupling

Builds the balanced legal-economy panel and estimates the annual coupling results.

## Execution order

1. **`Legal_Economy_Data.ipynb`** — Creates the balanced legal-economy panel.
2. **`Legal_Economy_Results.ipynb`** — Uses that panel to estimate and export the annual results.

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
- Annual `Data/Processed Data/Filtered Tables/MSA_<year>_Filtered_Extended_Professions.xlsx` files

### Outputs

- `Data/Processed Data/Legal-Economy-Coupling/Legal_Economy_Data.csv`

### Dependencies

- `pandas`
- `geopandas`
- `openpyxl`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. The code assumes `PROJECT_ROOT = /Users/<username>/Final_Lawyer_Git July10`.

### Notes

- GDP is read as real GDP in thousands of chained 2017 dollars and multiplied by 1,000.
- The final panel reflects the intersection of years available in the population, GDP, and BLS sources.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.

---

## Legal-Economy Coupling Results

**Code file:** `Legal_Economy_Results.ipynb`

### Purpose

Estimates annual scaling relationships for the legal economy and the yearly association between lawyers per capita and legal expenditure as a share of GDP.

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

- `Data/Processed Data/Legal-Economy-Coupling/Legal_Economy_Results.csv`
- Yearly plots displayed in the notebook.
- Optional `Data/Processed Data/Figuresscaling_table.csv` and `Figures/Affordability/legal_share_<year>.pdf` when the save flags are enabled.

### Dependencies

- `pandas`
- `numpy`
- `statsmodels`
- `matplotlib`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. The code assumes `PROJECT_ROOT = /Users/<username>/Final_Lawyer_Git July10`.

### Notes

- The notebook defaults to `save = 0` for optional figures and the scaling table.
- HC1 heteroskedasticity-robust covariance estimates are used.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.
