# Abundance

Estimates and visualizes the scaling of total and specialty lawyer supply with metropolitan population and land area.

## Execution order

1. **`Abundance_Scaling.ipynb`** — Runs the main scaling analysis and creates Figure 2 and Supplementary Figure 5.
2. **`Abundance_Plots.ipynb`** — Creates Supplementary Figures 1–4. It uses the same processed lawyer, population, geography, and helper inputs.

## Code documentation

## Abundance Scaling Analysis

**Code file:** `Abundance_Scaling.ipynb`

### Purpose

Estimates how total lawyer supply and the supply of 12 legal specialties scale with metropolitan population and land area, and summarizes the corresponding Cobb–Douglas models.

### What the code does

1. Loads MSA-level lawyer counts from the Bright Data master table.
1. Merges 2024 ACS population and 2025 CBSA land area.
1. Fits Bayesian Ridge power-law models for population and area, OLS population models for comparison, and two-variable Cobb–Douglas models.
1. Uses 100,000 bootstrap resamples for Bayesian confidence intervals through `Helpers.py`.
1. Orders specialties by the estimated population-scaling exponent.
1. Creates the main coefficient comparison and the Bayesian-versus-OLS robustness figure.

### Required inputs

- `Data/BrightData_Lawyers/BrightData_Lawyers_master.csv`
- `Data/Geography/CBSA_shapefile_2025/tl_2025_us_cbsa.shp` and associated shapefile components
- `Data/Population Data/MSA Population/ACSDT1Y2024.B01003-Data.csv`
- `Scripts/Helpers/Helpers.py`

### Outputs

- `Figures/Figure 2/Figure_2.pdf`
- `Figures/Supplementary Figure 5/Supplementary_Figure_5.pdf`
- Notebook displays of the Cobb–Douglas coefficient table and model R-squared table.

### Dependencies

- `pandas`
- `numpy`
- `geopandas`
- `statsmodels`
- `scikit-learn`
- `scipy`
- `matplotlib`
- `tabulate`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. Run it from within the repository; the notebook locates the repository root automatically by searching the current directory and its parents for the `Scripts` folder.

### Notes

- The script renames `n_lawyers` to `total_unique_lawyers` for the analysis.
- Bootstrap results are stochastic unless a random seed is set before running.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.

---

## Abundance Scaling Plots

**Code file:** `Abundance_Plots.ipynb`

### Purpose

Generates the detailed abundance scaling panels for total lawyers and individual legal specialties.

### What the code does

1. Loads and merges the MSA lawyer master, ACS population, and CBSA land area.
1. Estimates a preliminary population exponent for each specialty to determine a consistent panel order.
1. Calls the plotting functions in `Helpers.py` to create total-lawyer population/area/Cobb–Douglas plots and specialty grids.
1. Runs a separate intellectual-property area-scaling calculation as a numerical check.

### Required inputs

- `Data/BrightData_Lawyers/BrightData_Lawyers_master.csv`
- `Data/Geography/CBSA_shapefile_2025/tl_2025_us_cbsa.shp`
- `Data/Population Data/MSA Population/ACSDT1Y2024.B01003-Data.csv`
- `Scripts/Helpers/Helpers.py`

### Outputs

- `Figures/Supplementary Figure 1/Supplementary_Figure_1.pdf`
- `Figures/Supplementary Figure 2/Supplementary_Figure_2.pdf`
- `Figures/Supplementary Figure 3/Supplementary_Figure_3.pdf`
- `Figures/Supplementary Figure 4/Supplementary_Figure_4.pdf`

### Dependencies

- `pandas`
- `numpy`
- `geopandas`
- `statsmodels`
- `scikit-learn`
- `scipy`
- `matplotlib`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. Run it from within the repository; the notebook locates the repository root automatically by searching the current directory and its parents for the `Scripts` folder.

### Notes

- The preliminary ordering calculation uses 1,000 bootstrap samples; the final helper plots use 100,000.
- The helper grid functions reverse the supplied list internally, so the notebook reverses the sorted list before plotting.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.
