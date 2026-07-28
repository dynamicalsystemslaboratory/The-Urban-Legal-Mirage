# The Urban Legal Mirage

This repository contains the data-processing and analysis pipeline for **“The Urban Legal Mirage: Abundance and affordability of legal services in U.S. cities.”** The code constructs metropolitan-area lawyer datasets, estimates scaling relationships, builds specialty-specific demand proxies, measures affordability and legal-economy coupling, and generates the figures and result tables covered by this repository.

## Reproducibility options

There are two practical ways to use the repository:

1. **Full reconstruction from raw data.** Start with the three raw Bright Data lawyer snapshots and all geographic, occupational, population, and proxy source files. Run the complete pipeline in the order below.
2. **Downstream analysis from processed data.** Start with the processed lawyer master tables and harmonized BLS tables, then run only the analysis folders needed for a particular figure or result.

The raw Bright Data snapshots and other licensed, restricted, or very large source files are not redistributed in this repository. Full reconstruction therefore requires independent access to those files. When processed core files are available, most downstream analyses can be reproduced without rerunning the raw lawyer pipeline.

## Repository structure

```text
.
├── README.md
├── Scripts/
│   ├── Abundance/
│   ├── Affordability/
│   ├── Availability/
│   ├── Consistency/
│   ├── Data Processing/
│   ├── Helpers/
│   ├── Introduction/
│   ├── Legal-Economy-Coupling/
│   ├── Map/
│   └── Proxies/
├── Data/
│   ├── BLS data/
│   ├── BrightData_Lawyers/
│   ├── Geography/
│   ├── Introduction/
│   ├── Population Data/
│   ├── Processed Data/
│   └── Proxies/
└── Figures/
```

Each subfolder in `Scripts/` contains its own `README.md` with the exact inputs, outputs, dependencies, and execution order for the scripts in that folder.

## Software requirements

The Python notebooks require Jupyter and the following packages:

```bash
pip install jupyter pandas numpy scipy statsmodels scikit-learn matplotlib seaborn geopandas openpyxl tabulate
```

`polars` is optional and can accelerate loading of the large raw lawyer CSV files:

```bash
pip install polars
```

The two `.nb` analyses require **Wolfram Mathematica 14.1 or a compatible version**:

- `Scripts/Availability/Cases per Lawyer Data Collapse.nb`
- `Scripts/Affordability/Linear trend analysis of lawyer affordability.nb`

## Path conventions

The Python notebooks locate the repository root automatically by searching the current directory and its parents for the `Scripts` folder. Run them from the repository root or from a folder inside the repository.

Keep these top-level folder names unchanged:

```text
Scripts
Data
Figures
```

Paths may be case-sensitive. In particular, use:

```text
Data/Processed Data/Filtered tables
```

The raw lawyer pipeline and the crime proxy notebook read some large external files from locations under the user’s home directory. Edit their configuration variables when the files are stored elsewhere:

- `Lawyer_Paper_Complete_Pipeline.ipynb`: raw snapshots and crosswalks are read from `~/Downloads/` by default.
- `Crime_Proxy_Normalized.ipynb`: state NIBRS folders are read from `~/Desktop/Crime24/`, and the Group B archive is read from `~/Downloads/` unless an extracted repository CSV is supplied.

## Core input data

### Lawyer processing inputs

The complete lawyer pipeline expects the following files in `~/Downloads/` unless its configuration is changed:

```text
snap_mi504g7pxmrn977ah.1.csv
snap_mi504g7pxmrn977ah.2.csv
snap_mi504g7pxmrn977ah.3.csv
ZIP_CBSA_122024.xlsx
qcew-county-msa-csa-crosswalk-clean.xlsx
brightdata_practice_area_to_12_crosswalk_90pct.csv
```

It produces the three core files used throughout the repository:

```text
Data/BrightData_Lawyers/BrightData_Lawyers_master.csv
Data/BrightData_Lawyers/BrightData_Lawyers_master_normalized_1overN.csv
Data/BrightData_Lawyers/firm_address_counts_by_MSA.csv
```

### Geography and population inputs

The analyses use the following common files and folders:

```text
Data/Geography/FIPS/US states FIPS.csv
Data/Geography/CBSA_shapefile_2025/tl_2025_us_cbsa.shp
Data/Geography/State_shapefile_2025/tl_2025_us_state.shp
Data/Population Data/MSA Population/ACSDT1Y<year>.B01003-Data.csv
Data/Population Data/County Population/co-est2019-alldata.csv
```

Place all shapefile components beside the `.shp` file, including the corresponding `.dbf`, `.shx`, and `.prj` files.

The annual MSA population series uses 2010–2019 and 2021–2024. The one-year 2020 ACS file is not used.

### Occupational and economic inputs

```text
Data/BLS data/Uniform tables/Professional Licensed Occupations.xlsx
Data/BLS data/Uniform tables/MSA_<year>_Uniform.xlsx
Data/BLS data/GDP/GDP and Personal Income Formatted.csv
```

The BLS filtering notebook harmonizes the annual occupation tables and writes:

```text
Data/Processed Data/Filtered tables/MSA_<year>_Filtered_Extended_Professions.xlsx
```

### Additional inputs

The introductory ABA analysis requires:

```text
Data/Introduction/aba_county_lawyers.csv
Data/Population Data/County Population/co-est2019-alldata.csv
```

The six legal-demand proxies require bankruptcy, NIBRS crime, ACS family and immigration, patent, and Zillow real-estate files. Their exact filenames and locations are documented in [`Scripts/Proxies/README.md`](Scripts/Proxies/README.md).

## Pipeline overview

```text
Raw Bright Data snapshots + ZIP/CBSA and specialty crosswalks
    └── Lawyer_Paper_Complete_Pipeline.ipynb
        ├── BrightData_Lawyers_master.csv
        ├── BrightData_Lawyers_master_normalized_1overN.csv
        └── firm_address_counts_by_MSA.csv

Raw annual BLS tables + licensed-profession crosswalk
    └── Filtering_BLS_Data_Extended_Professions.ipynb
        └── annual harmonized BLS tables

Lawyer master + population + geography
    ├── Map → Figure 1
    ├── Abundance → Figure 2 and Supplementary Figures 1–5
    └── Consistency → sanity-check data and Supplementary Figure 8

Normalized lawyer master + six specialty demand sources
    └── Six proxy notebooks
        ├── Six normalized proxy CSVs
        ├── Proxies_Plots.ipynb → Supplementary Figure 6
        └── Cases per Lawyer Data Collapse.nb → collapsed availability analysis

Harmonized BLS tables + ACS population
    └── Extended_Professions_Affordability.ipynb
        ├── Figure 4
        ├── annual affordability tables
        ├── Linear trend analysis of lawyer affordability.nb
        └── Lawyers_2024_Spearman_Plot.ipynb → Supplementary Figure 7

Harmonized BLS tables + ACS population + metropolitan GDP
    └── Legal_Economy_Data.ipynb
        └── Legal_Economy_Results.ipynb → result CSVs and displayed yearly figures

ABA county lawyer counts + county population
    └── ABA_Data_Extraction.ipynb → introductory county statistics
```

## Complete execution order

### 1. Prepare the shared helper module

Keep the helper file at:

```text
Scripts/Helpers/Helpers.py
```

It is imported by the abundance, consistency, and proxy plotting notebooks. It is not normally run as a standalone script.

### 2. Build the processed core data

Run:

1. `Scripts/Data Processing/Lawyer_Paper_Complete_Pipeline.ipynb`
2. `Scripts/Data Processing/Filtering_BLS_Data_Extended_Professions.ipynb`

The two notebooks are independent, but both sets of outputs are needed for the complete repository.

### 3. Run the introductory county analysis

Run:

```text
Scripts/Introduction/ABA_Data_Extraction.ipynb
```

This produces `Data/Introduction/aba_county_lawyers_intro.csv` and prints the county counts below 1 lawyer per 1,000 residents and at or above 10 lawyers per 1,000 residents.

### 4. Run the abundance analyses

Run in this order:

1. `Scripts/Abundance/Abundance_Scaling.ipynb`
2. `Scripts/Abundance/Abundance_Plots.ipynb`

These notebooks use the lawyer master, 2024 ACS population, CBSA land area, and `Helpers.py`.

### 5. Create the national maps

Run:

```text
Scripts/Map/Total_Lawyers_Map.ipynb
```

This creates the metropolitan lawyer-supply map and the legal-desert map.

### 6. Run the consistency checks

Run in this order:

1. `Scripts/Consistency/Sanity_Checks_Data.ipynb`
2. `Scripts/Consistency/Sanity_Checks_Plots.ipynb`

The first notebook creates `Data/Processed Data/sanity_check_data.csv`; the second uses it to create Supplementary Figure 8.

### 7. Build the six demand proxies

After the normalized lawyer master exists, run these six notebooks in any order:

1. `Scripts/Proxies/Bankruptcy_Proxy_Normalized.ipynb`
2. `Scripts/Proxies/Crime_Proxy_Normalized.ipynb`
3. `Scripts/Proxies/Family_Proxy_Normalized.ipynb`
4. `Scripts/Proxies/Immigration_Proxy_Normalized.ipynb`
5. `Scripts/Proxies/Intellectual_Property_Proxy_Normalized.ipynb`
6. `Scripts/Proxies/Real_Estate_Proxy_Normalized.ipynb`

Then run:

```text
Scripts/Proxies/Proxies_Plots.ipynb
```

The intellectual-property notebook must remove the final subtotal row while retaining the first valid MSA row.

### 8. Run the availability collapse

Copy the six normalized proxy CSVs beside:

```text
Scripts/Availability/Cases per Lawyer Data Collapse.nb
```

Open the Mathematica notebook and evaluate it from top to bottom. The model results and collapsed plot are displayed in the notebook.

### 9. Run the affordability analyses

First run:

```text
Scripts/Affordability/Extended_Professions_Affordability.ipynb
```

It creates the annual affordability tables, Figure 4, and the two 2024 occupation files. After it finishes, the following analyses are independent:

- Place `Annual_Average_Affordability_All.csv` beside `Linear trend analysis of lawyer affordability.nb`, then evaluate the Mathematica notebook.
- Run `Scripts/Affordability/Lawyers_2024_Spearman_Plot.ipynb` to create Supplementary Figure 7.

### 10. Run the legal-economy analysis

Run in this order:

1. `Scripts/Legal-Economy-Coupling/Legal_Economy_Data.ipynb`
2. `Scripts/Legal-Economy-Coupling/Legal_Economy_Results.ipynb`

The second notebook saves the result CSVs and displays the yearly figures without requiring figure-file export.

## Main outputs

| Analysis | Main output |
|---|---|
| Introduction | `Data/Introduction/aba_county_lawyers_intro.csv` and printed county statistics |
| Map | `Figures/Figure 1/Lawyers_USA_Map_Original.pdf` and `Lawyers_USA_Map_Legal_Deserts.pdf` |
| Abundance | `Figures/Figure 2/Figure_2.pdf` |
| Abundance supplements | Supplementary Figures 1–5 |
| Affordability | `Figures/Figure 4/Figure_4_V1.pdf` and annual affordability CSVs |
| Demand proxies | Six normalized proxy CSVs and Supplementary Figure 6 |
| Rank comparison | Supplementary Figure 7 |
| Consistency checks | `Data/Processed Data/sanity_check_data.csv` and Supplementary Figure 8 |
| Legal-economy coupling | `Legal_Economy_Data.csv`, `scaling_table.csv`, and `Legal_Economy_Results.csv` |

## Detailed documentation

- [Data Processing](Scripts/Data%20Processing/README.md)
- [Helpers](Scripts/Helpers/README.md)
- [Introduction](Scripts/Introduction/README.md)
- [Abundance](Scripts/Abundance/README.md)
- [Map](Scripts/Map/README.md)
- [Consistency](Scripts/Consistency/README.md)
- [Proxies](Scripts/Proxies/README.md)
- [Availability](Scripts/Availability/README.md)
- [Affordability](Scripts/Affordability/README.md)
- [Legal-Economy-Coupling](Scripts/Legal-Economy-Coupling/README.md)

## Reproducibility notes

- The shared scaling helpers use 100,000 bootstrap resamples for final confidence intervals. Results can vary slightly unless a NumPy random seed is set.
- The 1-over-N normalized lawyer master assigns a lawyer with `N` mapped specialties a weight of `1/N` in each specialty.
- Geographic analysis is restricted to valid metropolitan statistical areas; Micropolitan Statistical Areas and Puerto Rico metropolitan areas are excluded where specified by the processing pipeline.
- Preserve exact filenames and directory names. Several notebooks rely on fixed source filenames even though the repository root itself is detected automatically.
- Large, private, or licensed raw files are intentionally excluded. Do not commit them unless their redistribution is permitted.
