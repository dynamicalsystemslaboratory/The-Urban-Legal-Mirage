# Map

Creates the national metropolitan lawyer-supply and legal-desert maps.

## Execution order

1. **`Total_Lawyers_Map.ipynb`** — Run after the lawyer master and 2024 population data are available.

## Code documentation

## Total Lawyers Map

**Code file:** `Total_Lawyers_Map.ipynb`

### Purpose

Creates the national MSA map of lawyers per capita and a second annotated map identifying metropolitan legal deserts.

### What the code does

1. Loads state and CBSA geometries, valid state codes, 2024 MSA population, and MSA lawyer counts.
1. Calculates lawyers per capita and population density.
1. Reprojects the map to EPSG:2163.
1. Plots MSA centroids as circles whose area reflects population and whose color reflects lawyers per capita.
1. Creates separate exploratory views for Alaska and Hawaii.
1. Identifies legal-desert MSAs at or below 1 lawyer per 1,000 residents and labels them on a second continental-U.S. map.

### Required inputs

- `Data/Geography/FIPS/US states FIPS.csv`
- `Data/Geography/State_shapefile_2025/tl_2025_us_state.shp`
- `Data/Geography/CBSA_shapefile_2025/tl_2025_us_cbsa.shp`
- `Data/Population Data/MSA Population/ACSDT1Y2024.B01003-Data.csv`
- `Data/BrightData_Lawyers/BrightData_Lawyers_master.csv`

### Outputs

- `Figures/Figure 1/Lawyers_USA_Map_Original.pdf`
- `Figures/Figure 1/Lawyers_USA_Map_Legal_Deserts.pdf`
- Exploratory Alaska and Hawaii maps displayed in the notebook.

### Dependencies

- `pandas`
- `numpy`
- `geopandas`
- `matplotlib`
- `seaborn`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. Run it from within the repository; the notebook locates the repository root automatically by searching the current directory and its parents for the `Scripts` folder.

### Notes

- The marker-size scaling and annotation placement are manually tuned for the final figure.
- The legal-desert threshold is `Lawyers_PerCapita <= 1/1000`.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.
