# Consistency

Builds and plots the independent consistency checks for the lawyer directory.

## Execution order

1. **`Sanity_Checks_Data.ipynb`** — Creates `sanity_check_data.csv`.
2. **`Sanity_Checks_Plots.ipynb`** — Uses that CSV to create Supplementary Figure 8.

## Code documentation

## Sanity Check Data Construction

**Code file:** `Sanity_Checks_Data.ipynb`

### Purpose

Builds the input table used to compare the lawyer directory with independent firm, employment, population, and geographic measures.

### What the code does

1. Loads the valid metropolitan-area geography and 2024 ACS population.
1. Loads 2024 BLS lawyer employment.
1. Loads the Bright Data MSA lawyer master and firm-address counts.
1. Merges population, BLS employment, the number of firm addresses, and the number of lawyers located at shared firm addresses.
1. Runs exploratory log-log OLS regressions for firms versus population and directory lawyers-in-firms versus BLS employment.
1. Exports the four variables required by the final consistency figure.

### Required inputs

- `Data/Geography/FIPS/US states FIPS.csv`
- `Data/Geography/CBSA_shapefile_2025/tl_2025_us_cbsa.shp`
- `Data/Population Data/MSA Population/ACSDT1Y2024.B01003-Data.csv`
- `Data/Processed Data/Filtered Tables/MSA_2024_Filtered_Extended_Professions.xlsx`
- `Data/BrightData_Lawyers/BrightData_Lawyers_master.csv`
- `Data/BrightData_Lawyers/firm_address_counts_by_MSA.csv`

### Outputs

- `Data/Processed Data/sanity_check_data.csv`
- Two exploratory regression plots displayed in the notebook.

### Dependencies

- `pandas`
- `numpy`
- `geopandas`
- `statsmodels`
- `matplotlib`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. The code assumes `PROJECT_ROOT = /Users/<username>/Final_Lawyer_Git July10`.

### Notes

- The final CSV contains `Population`, `Firms`, `TOT_EMP`, and `lawyers_in_firms`.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.

---

## Sanity Check Plots

**Code file:** `Sanity_Checks_Plots.ipynb`

### Purpose

Creates the three-panel supplementary consistency figure comparing firm counts, lawyer employment sources, and MSA population with land area.

### What the code does

1. Loads the prepared sanity-check CSV.
1. Reconstructs the population-versus-land-area dataset from the lawyer master, ACS population, and CBSA geometry.
1. Passes each panel to `plot_panel` in `Helpers.py`.
1. Fits Bayesian Ridge log-log scaling relationships and calculates 100,000-bootstrap confidence intervals.
1. Plots fitted scaling and linear-scaling reference lines using fixed log-axis limits.

### Required inputs

- `Data/Processed Data/sanity_check_data.csv`
- `Data/BrightData_Lawyers/BrightData_Lawyers_master.csv`
- `Data/Geography/CBSA_shapefile_2025/tl_2025_us_cbsa.shp`
- `Data/Population Data/MSA Population/ACSDT1Y2024.B01003-Data.csv`
- `Scripts/Helpers/Helpers.py`

### Outputs

- `Figures/Supplementary Figure 8/Supplementary_Figure_8.pdf`

### Dependencies

- `pandas`
- `numpy`
- `geopandas`
- `scikit-learn`
- `matplotlib`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. The code assumes `PROJECT_ROOT = /Users/<username>/Final_Lawyer_Git July10`.

### Notes

- The three comparisons are firms versus population, directory lawyers in firms versus BLS lawyer employment, and land area versus population.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.
