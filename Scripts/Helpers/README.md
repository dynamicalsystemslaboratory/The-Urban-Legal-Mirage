# Helpers

Contains the shared Python functions imported by the abundance, consistency, affordability, and proxy notebooks.

## Execution order

1. **`Helpers.py`** — This is a shared module rather than a standalone analysis. Keep it at `Scripts/Helpers/Helpers.py` before running notebooks that import it.

## Code documentation

## Shared Statistical and Plotting Helpers

**Code file:** `Helpers.py`

### Purpose

Provides the common scaling estimators, bootstrap confidence intervals, color utilities, and figure-building functions used by the abundance, proxy, and consistency notebooks.

### What the code does

1. `scale(x, y)`: Bayesian Ridge power-law exponent, bootstrap 95% interval, and R-squared in base-10 log space.
1. `scale_ols(x, y)`: OLS power-law exponent, analytical confidence interval, and R-squared.
1. `cob(y, x1, x2)`: two-input Bayesian Cobb–Douglas coefficients, their intervals, the coefficient sum and its interval, and R-squared.
1. `darker(color)`: returns a darker edge color for scatter points.
1. `plot_scaling_trip`: total-lawyer population, area, and Cobb–Douglas panels.
1. `plot_population_scaling_grid`, `plot_area_scaling_grid`, and `plot_cobb_douglas_grid`: 4-by-3 specialty grids.
1. `plot_panel`: reusable demand-proxy and sanity-check panel with a Bayesian fit and linear-scaling reference.

### Required inputs

- No standalone data input. Calling notebooks pass arrays or data frames to these functions.

### Outputs

- When called by abundance notebooks, the plotting functions save Supplementary Figures 1–4.
- `plot_panel` draws on an existing Matplotlib axis and leaves final saving to the calling notebook.

### Dependencies

- `pandas`
- `numpy`
- `statsmodels`
- `scikit-learn`
- `scipy`
- `matplotlib`

### How to run

Do not normally execute this file by itself. Keep it at `Scripts/Helpers/Helpers.py`; the analysis notebooks append that folder to `sys.path` and import its functions.

### Notes

- The default bootstrap size is 100,000.
- Bootstrap confidence intervals are stochastic unless the calling session sets a NumPy random seed.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.
