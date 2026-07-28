# Proxies

Constructs six specialty-specific legal-demand proxies and then creates the combined scaling figure.

## Execution order

1. **`Bankruptcy_Proxy_Normalized.ipynb`** — Creates the bankruptcy proxy table.
2. **`Crime_Proxy_Normalized.ipynb`** — Creates the crime proxy table.
3. **`Family_Proxy_Normalized.ipynb`** — Creates the family-law proxy table.
4. **`Immigration_Proxy_Normalized.ipynb`** — Creates the immigration proxy table.
5. **`Intellectual_Property_Proxy_Normalized.ipynb`** — Creates the intellectual-property proxy table. The corrected version removes the final subtotal row and retains San Jose.
6. **`Real_Estate_Proxy_Normalized.ipynb`** — Creates the real-estate proxy table.
7. **`Proxies_Plots.ipynb`** — Run only after all six proxy CSVs exist; creates Supplementary Figure 6.

The first six notebooks are independent of one another once the normalized lawyer master exists, but all six must be completed before `Proxies_Plots.ipynb`.

## Code documentation

## Bankruptcy Demand Proxy

**Code file:** `Bankruptcy_Proxy_Normalized.ipynb`

### Purpose

Builds the MSA-level bankruptcy-law supply and demand table using 2024 bankruptcy filings and 1-over-N normalized bankruptcy lawyer counts.

### What the code does

1. Defines the valid metropolitan MSA set.
1. Loads normalized specialty lawyer counts.
1. Loads county-level 2024 bankruptcy filings for all chapters.
1. Merges counties to MSAs using the QCEW county-to-MSA crosswalk.
1. Aggregates filings to MSA and merges normalized Bankruptcy Law supply.
1. Removes MSAs without a corresponding lawyer-supply value.

### Required inputs

- `Data/BrightData_Lawyers/BrightData_Lawyers_master_normalized_1overN.csv`
- `Data/Proxies/Bankruptcy/bf_f5a_1231.2024_clean.xlsx`
- `Data/Geography/Crosswalks/qcew-county-msa-csa-crosswalk-clean.xlsx`
- `Data/Geography/CBSA_shapefile_2025/tl_2025_us_cbsa.shp`
- `Data/Geography/FIPS/US states FIPS.csv`

### Outputs

- `Data/Proxies/Bankruptcy/Bankruptcy_Proxy_Normalized.csv`

### Dependencies

- `pandas`
- `geopandas`
- `openpyxl`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. The code assumes `PROJECT_ROOT = /Users/<username>/Final_Lawyer_Git July10`.

### Notes

- The output columns used by the plotting notebook are `Bankruptcy filings` and `Bankruptcy`.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.

---

## Crime Demand Proxy

**Code file:** `Crime_Proxy_Normalized.ipynb`

### Purpose

Builds the 2024 MSA criminal-defense demand proxy by combining NIBRS Group A incidents and arrests with Group B arrest records and normalized criminal-defense lawyer supply.

### What the code does

1. Loads agency metadata from each state folder and builds agency-ID and ORI-to-MSA lookup tables.
1. Loads 2024 NIBRS incident and arrestee files for each state and creates state-qualified unique incident and arrest identifiers.
1. Loads the national Group B arrest-report segment from a local CSV or the downloaded ZIP archive.
1. Maps Group B ORIs to MSAs and counts unique Group B arrests.
1. Maps NIBRS MSA names to ACS CBSA codes using exact and looser city/state matching.
1. Aggregates Group A incidents, Group A arrests, and Group B arrests to MSA.
1. Merges normalized Criminal Defense lawyer supply and calculates total arrests as Group A plus Group B.
1. Removes the two asserted zero-incident MSAs and validates the final 380-row sample.

### Required inputs

- Per-state folders matching `~/Desktop/Crime24/<state>-2024/`, each containing `agencies.csv`, `NIBRS_incident.csv`, and `NIBRS_ARRESTEE.csv`
- `~/Downloads/group_b_arrest_report_segment_csv_1991_2024.zip` or `Data/Proxies/Crime/nibrs_group_b_arrest_report_segment_2024.csv`
- `Data/BrightData_Lawyers/BrightData_Lawyers_master_normalized_1overN.csv`
- `Data/Population Data/MSA Population/ACSDT1Y2024.B01003-Data.csv`

### Outputs

- `Data/Proxies/Crime/Crime_Proxy_Normalized.csv`

### Dependencies

- `pandas`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. The code assumes `PROJECT_ROOT = /Users/<username>/Final_Lawyer_Git July10`.

### Notes

- The output keeps `AREA`, `Criminal_Defense`, `Number_of_incidents`, and `Number_of_arrests`.
- Group B fallback IDs use ORI, date, offense, and row index when transaction or sequence identifiers are missing.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.

---

## Family Law Demand Proxy

**Code file:** `Family_Proxy_Normalized.ipynb`

### Purpose

Builds the MSA-level family-law supply and demand table using the number of divorced females and normalized Family Law lawyer counts.

### What the code does

1. Defines the valid metropolitan MSA set.
1. Loads the normalized lawyer master.
1. Loads ACS table B12503 and extracts `B12503_010E` as the number of divorced females.
1. Extracts five-digit CBSA codes and keeps valid MSAs.
1. Merges normalized Family Law lawyer supply and removes missing supply observations.

### Required inputs

- `Data/Proxies/Family/ACSDT1Y2010.B12503-Data.csv`
- `Data/BrightData_Lawyers/BrightData_Lawyers_master_normalized_1overN.csv`
- `Data/Geography/CBSA_shapefile_2025/tl_2025_us_cbsa.shp`
- `Data/Geography/FIPS/US states FIPS.csv`

### Outputs

- `Data/Proxies/Family/Family_Proxy_Normalized.csv`

### Dependencies

- `pandas`
- `geopandas`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. The code assumes `PROJECT_ROOT = /Users/<username>/Final_Lawyer_Git July10`.

### Notes

- The output columns used by the plot are `Female_Divorces` and `Family`.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.

---

## Immigration Law Demand Proxy

**Code file:** `Immigration_Proxy_Normalized.ipynb`

### Purpose

Builds the MSA-level immigration-law supply and demand table using 2024 foreign-born population and normalized Immigration Law lawyer counts.

### What the code does

1. Defines the valid metropolitan MSA set.
1. Loads normalized specialty lawyer counts.
1. Loads the 2024 ACS DP02 table and extracts `DP02_0094E` as foreign-born population.
1. Extracts five-digit CBSA codes and keeps valid metropolitan MSAs.
1. Merges normalized Immigration Law supply and removes missing supply values.

### Required inputs

- `Data/Proxies/Immigration/ACSDP1Y2024.DP02-Data.csv`
- `Data/BrightData_Lawyers/BrightData_Lawyers_master_normalized_1overN.csv`
- `Data/Geography/CBSA_shapefile_2025/tl_2025_us_cbsa.shp`
- `Data/Geography/FIPS/US states FIPS.csv`

### Outputs

- `Data/Proxies/Immigration/Immigration_Proxy_Normalized.csv`

### Dependencies

- `pandas`
- `geopandas`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. The code assumes `PROJECT_ROOT = /Users/<username>/Final_Lawyer_Git July10`.

### Notes

- The output columns used by the plot are `Foreign_Born_Population` and `Immigration`.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.

---

## Intellectual Property Demand Proxy

**Code file:** `Intellectual_Property_Proxy_Normalized.ipynb`

### Purpose

Builds the MSA-level intellectual-property-law supply and demand table using 2015 granted patents and normalized Intellectual Property Law lawyer counts.

### What the code does

1. Defines the valid metropolitan MSA set.
1. Loads normalized specialty lawyer counts.
1. Loads the regional patent table and keeps the MSA identifier, regional title, and 2015 patent count.
1. Removes the subtotal row, standardizes CBSA codes, and keeps valid MSAs.
1. Merges normalized Intellectual Property Law supply and removes missing supply values.

### Required inputs

- `Data/Proxies/Intellectual Property/Patents 2000-2015.csv`
- `Data/BrightData_Lawyers/BrightData_Lawyers_master_normalized_1overN.csv`
- `Data/Geography/CBSA_shapefile_2025/tl_2025_us_cbsa.shp`
- `Data/Geography/FIPS/US states FIPS.csv`

### Outputs

- `Data/Proxies/Intellectual Property/Intellectual_Property_Proxy_Normalized.csv`

### Dependencies

- `pandas`
- `geopandas`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. The code assumes `PROJECT_ROOT = /Users/<username>/Final_Lawyer_Git July10`.

### Notes

- The final version must remove the last subtotal row rather than the first valid MSA row.
- The output columns used by the plot are `Patents` and `Intellectual Property`.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.

---

## Real Estate Law Demand Proxy

**Code file:** `Real_Estate_Proxy_Normalized.ipynb`

### Purpose

Builds the MSA-level real-estate-law supply and demand table using total 2024 Zillow transaction value and normalized Real Estate Law lawyer counts.

### What the code does

1. Creates simplified city/state matching fields from the 2025 CBSA shapefile.
1. Loads normalized Real Estate Law supply.
1. Loads Zillow monthly MSA total transaction values and keeps records with all 2024 monthly values.
1. Sums the 2024 monthly values and converts the total to millions of dollars.
1. Matches Zillow regions to CBSA codes by city/state and manually resolves Poughkeepsie, Louisville, and The Villages.
1. Aggregates any repeated CBSA records and inner-merges lawyer supply.

### Required inputs

- `Data/Proxies/Real Estate/Metro_total_transaction_value_now_uc_sfrcondo_month.csv`
- `Data/BrightData_Lawyers/BrightData_Lawyers_master_normalized_1overN.csv`
- `Data/Geography/CBSA_shapefile_2025/tl_2025_us_cbsa.shp`

### Outputs

- `Data/Proxies/Real Estate/Real_Estate_Proxy_Normalized.csv`

### Dependencies

- `pandas`
- `geopandas`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. The code assumes `PROJECT_ROOT = /Users/<username>/Final_Lawyer_Git July10`.

### Notes

- The output includes transaction value in original units and in millions of dollars.
- Only Zillow MSA rows with nonmissing values for every 2024 month are retained.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.

---

## Legal Demand Proxy Scaling Plots

**Code file:** `Proxies_Plots.ipynb`

### Purpose

Creates the six-panel supplementary figure comparing specialty lawyer supply with a corresponding city-level legal-demand proxy.

### What the code does

1. Loads the six specialty proxy tables.
1. Pairs bankruptcy lawyers with bankruptcy filings, criminal-defense lawyers with total arrests, family lawyers with divorced females, immigration lawyers with foreign-born population, IP lawyers with patents, and real-estate lawyers with transaction value.
1. Uses `plot_panel` from `Helpers.py` to remove nonpositive observations and fit Bayesian Ridge models in log-log space.
1. Calculates 100,000-bootstrap confidence intervals for the demand-scaling exponent.
1. Plots the fitted relationship and the exponent-one reference relationship on logarithmic axes.
1. Applies panel-specific axis limits and saves the combined 2-by-3 figure.

### Required inputs

- `Data/Proxies/Bankruptcy/Bankruptcy_Proxy_Normalized.csv`
- `Data/Proxies/Crime/Crime_Proxy_Normalized.csv`
- `Data/Proxies/Family/Family_Proxy_Normalized.csv`
- `Data/Proxies/Immigration/Immigration_Proxy_Normalized.csv`
- `Data/Proxies/Intellectual Property/Intellectual_Property_Proxy_Normalized.csv`
- `Data/Proxies/Real Estate/Real_Estate_Proxy_Normalized.csv`
- `Scripts/Helpers/Helpers.py`

### Outputs

- `Figures/Supplementary Figure 6/Supplementary_Figure_6.pdf`

### Dependencies

- `pandas`
- `numpy`
- `scikit-learn`
- `matplotlib`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. The code assumes `PROJECT_ROOT = /Users/<username>/Final_Lawyer_Git July10`.

### Notes

- The notebook prints the positive-observation sample size for each panel.
- Axis limits are stored as base-10 exponent tuples.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.
