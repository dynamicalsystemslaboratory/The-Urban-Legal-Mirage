# The Urban Legal Mirage

This repository contains the data-processing and analysis pipeline for **“The Urban Legal Mirage: Abundance and affordability of legal services in U.S. cities.”** The code constructs metropolitan-area lawyer datasets, estimates scaling relationships, builds specialty-specific demand proxies, measures affordability and legal-economy coupling, and generates the figures and result tables covered by this paper.

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
│   ├── BLS Data/
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

The three `.nb` analyses require **Wolfram Mathematica 14.1 or a compatible version**:

- `Scripts/Availability/Cases per Lawyer Data Collapse.nb`
- `Scripts/Affordability/Affordability analysis.nb`
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
The first three files were obtained from Bright Data and contain all the individual lawyer profiles. These datasets are confidential and cannot be shared herein. 


`ZIP_CBSA_122024.xlsx` is the HUD-USPS ZIP Code Crosswalk File published by the U.S. Department of Housing and Urban Development (HUD), which allocates USPS ZIP Codes to CBSAs, and can be obtained here: https://www.huduser.gov/portal/datasets/usps_crosswalk.html. The downloaded crosswalk file is named "ZIP-CBSA_122024" and should be renamed to "ZIP_CBSA_122024". Newer versions of this crosswalk may contain new headers. For reproducibility, please follow the following headers' naming scheme:
* "ZIP" -  5 digit USPS ZIP code
* "CBSA" - 5 digit CBSA code for Micropolitan and Metropolitan Areas as defined by OMB in February of 2013. ZIP codes with a CBSA code of ‘99999’ are not located within a CBSA. 
* "USPS_ZIP_PREF_CITY" - USPS preferred city name
* "USPS_ZIP_PREF_STATE" - USPS preferred state address state
* "RES_RATIO" - The ratio of residential addresses in the ZIP – Tract, County, or CBSA part to the total number of residential addresses in the entire ZIP.
* "BUS_RATIO" - The ratio of business addresses in the ZIP – Tract, County, or CBSA part to the total number of business addresses in the entire ZIP.
* "OTH_RATIO" - The ratio of other addresses in the ZIP – Tract, County, or CBSA part to the total number of other addresses in the entire ZIP.
* "TOT_RATIO" - The ratio of all addresses in the ZIP – Tract, County, or CBSA part to the total number of all types of addresses in the entire ZIP.

The definitions above are taken directly from HUD documentation section: https://www.huduser.gov/portal/datasets/usps_crosswalk.html

To download, one has to register on the HUD website (link provided in the webpage above). After registering, one should select ZIP-CBSA for "Crosswalk Type" and 4th Quarter 2024 under "Select Data Year and Quarter." 

`qcew-county-msa-csa-crosswalk-clean.xlsx` is the BLS' county to CBSA Crosswalk File, which maps counties to corresponding CBSAs. The raw crosswalk can be obtained by clicking "COUNTY-MSA-CSA CROSSWALKS: XLSX" in: https://www.bls.gov/cew/classifications/areas/county-msa-csa-crosswalk.htm. Our cleaned crosswalk, `qcew-county-msa-csa-crosswalk-clean.xlsx`, is obtained by removing the unnecessary sheets from the downloaded file, named qcew-county-msa-csa-crosswalk.xlsx, and keeping only the "Jul. 2023 Crosswalk" sheet.

`brightdata_practice_area_to_12_crosswalk_90pct.csv` is the crosswalk that maps Martindale's listed areas of practice to lawyer specializations. This crosswalk was manually created by us for the purposes of this paper and is not an official or endorsed crosswalk from Martindale. The crosswalk is located in `Scripts/Data Processing/` and should be downloaded before running `Lawyer_Paper_Complete_Pipeline.ipynb`.

The pipeline, `Lawyer_Paper_Complete_Pipeline.ipynb`, produces the three core files used throughout the repository:

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
The first file includes US states Federal Information Processing System (FIPS) codes and is provided in `Data/Geography/FIPS/US states FIPS.csv`.

Each shapefile folder should include all shapefile components, including `.shp` and the corresponding `.dbf`, `.shx`, and `.prj` files. All shapefiles can be downloaded from the TIGER/Line® Shapefiles web interface: https://www.census.gov/cgi-bin/geo/shapefiles/index.php. To obtain the CBSA shapefiles, one should select 2025 and Core Based Statistical Areas under "Select year" and "Select a layer type," respectively, click submit, and then select "Metropolitan/Micropolitan Statistical Area." To obtain the States shapefiles, one should follow the same steps, selecting States (and equivalent) under "Select a layer type." All files need to be unzipped, taken from the folder, and placed into the corresponding Data/Geography folder (CBSA_shapefile_2025 and State_shapefile_2025, see directory structure above).

The annual MSA population series uses 2010–2019 and 2021–2024. The one-year 2020 ACS file is not used. These population estimates can be obtained from the Census Data website: https://data.census.gov/table/ACSDT1Y2024.B01003?q=B01003&g=010XX00US$3100000. All files need to be unzipped, taken from the folder, and placed into the corresponding Data/Population Data/MSA Population folder, see directory structure above).

The annual county population series is obtained from the Census Data website: https://www.census.gov/newsroom/press-kits/2020/pop-estimates-county-metro.html. The data can be downloaded by clicking "Population, Population Change, and Estimated Components of Population Change: April 1, 2010 to July 1, 2019 (CO-EST2019-alldata) [CSV]" under the Datasets section. The dataset should be placed into the corresponding Data/Population Data/County Population folder, see directory structure above). The dataset is used in the introduction and is not part of the analysis, see `Scripts/Introduction/ABA_Data_Extraction.ipynb`.

### Occupational and economic inputs

```text
Data/BLS data/Uniform tables/Professional Licensed Occupations.xlsx
Data/BLS data/Uniform tables/MSA_<year>_Uniform.xlsx
Data/BLS data/GDP/GDP and Personal Income Formatted.csv
```
Professional Licensed Occupations.xlsx is a crosswalk we created manually detailing changes in SOC codes and occupation titles for licensed professionals over time in the BLS data. The crosswalk was created by manually tracking changes in the licensed, professional occupations, chosen based on the criteria detailed in the paper, across BLS publications in different years. This crosswalk can be found in `Data/BLS Data/Uniform Tables/Professional Licensed Occupations.xlsx`.

We obtain the BLS data for occupations and salary from the BLS website: https://www.bls.gov/oes/tables.htm. MSA_<year>_Uniform.xlsx files are created as follows:
* For each year, download the zip file associated with "Metropolitan and nonmetropolitan area (XLSX)."
* Extract the "MSA_<year>_dl" from the zip. If multiple files are available (for earlier years), join them into one file.
* Harmonize headers of all files across all years to be consistent. The final headers are: AREA_TITLE	AREA_TYPE	PRIM_STATE	NAICS	NAICS_TITLE	I_GROUP	OWN_CODE	OCC_CODE	OCC_TITLE	O_GROUP	TOT_EMP	EMP_PRSE	JOBS_1000	LOC_QUOTIENT	PCT_TOTAL	PCT_RPT	H_MEAN	A_MEAN	MEAN_PRSE	H_PCT10	H_PCT25	H_MEDIAN	H_PCT75	H_PCT90	A_PCT10	A_PCT25	A_MEDIAN	A_PCT75	A_PCT90	ANNUAL	HOURLY
* Rename files to `MSA_<year>_Uniform.xlsx`, with each year corresponding to a single file.


We use the BEA's MSA-level GDP data, which were available at the time of data collection. BEA subsequently discontinued publication of MSA-level GDP statistics and now publishes GDP estimates only at the county level. The original file was reformatted to be easily read in Python. We provide this file in `Data/BLS Data/GDP/GDP and Personal Income Formatted.csv`.


The `Filtering_BLS_Data_Extended_Professions.ipynb` notebook harmonizes the annual occupation tables and writes:

```text
Data/Processed Data/Filtered tables/MSA_<year>_Filtered_Extended_Professions.xlsx
```

### Additional inputs
## Introduction
The introductory ABA analysis requires:

```text
Data/Introduction/aba_county_lawyers.csv
Data/Population Data/County Population/co-est2019-alldata.csv
```
The `aba_county_lawyers.csv` was obtained by manually collecting county-level lawyer counts from the ABA Profile of the Legal Profession 2020, available at https://www.americanbar.org/content/dam/aba/administrative/news/2020/07/potlp2020.pdf. After running `Scripts/Introduction/ABA_Data_Extraction.ipynb`, the resulting CSV, the resulting CSV, `aba_county_lawyers_intro.csv`, contains the county-level lawyer counts and corresponding 2019 county population, used to identify counties below the lawyer-density threshold applied in the paper.

"_The raw numbers portray two disparate realities of Americans living even within the same state: Just as 40% of U.S. counties fall below the proposed threshold, about 1% exceed it by a factor of ten or more._"

The last part of the above sentence, taken from the paper, is based on these counts (1%).

## Proxies for number of cases

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
    ├── Abundance → Figure 2, Supplementary Figures 1–5, and Supplementary Tables 1-2
    └── Consistency → sanity-check data and Supplementary Figure 8

Normalized lawyer master + six specialty demand sources
    └── Six proxy notebooks
        ├── Six normalized proxy CSVs
        ├── Proxies_Plots.ipynb → Supplementary Figure 6
        └── Cases per Lawyer Data Collapse.nb → Figure 3

Harmonized BLS tables + ACS population
    └── Extended_Professions_Affordability.ipynb
        ├── Annual_Average_Affordability_All.csv
        ├── Annual_Affordability_Spearman_All.csv
        ├── 2024 lawyer and pharmacist rank datasets
        ├── Affordability analysis.nb → Figure 4
        ├── Linear trend analysis of lawyer affordability.nb → Supplementary Table 3
        └── Lawyers_2024_Spearman_Plot.ipynb → Supplementary Figure 7

Harmonized BLS tables + ACS population + metropolitan GDP
    └── Legal_Economy_Data.ipynb
        └── Legal_Economy_Results.ipynb
            ├── Legal_Economy_Results.csv → Supplementary Table 4
            └── displayed yearly diagnostic figures

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

### 4. Create the national maps

Before running the code, create the output directory for the figure, titled: "Figures/Figure 1".

Run:

```text
Scripts/Map/Total_Lawyers_Map.ipynb
```

This creates the metropolitan lawyer-supply map and the legal-desert map.

### 5. Run the abundance analyses

Run in this order:

1. `Scripts/Abundance/Abundance_Scaling.ipynb`
2. `Scripts/Abundance/Abundance_Plots.ipynb`

These notebooks use the lawyer master, 2024 ACS population, CBSA land area, and `Helpers.py`.


### 6. Run the consistency checks

Run in this order:

1. `Scripts/Consistency/Sanity_Checks_Data.ipynb`
2. `Scripts/Consistency/Sanity_Checks_Plots.ipynb`

The first notebook creates `Data/Processed Data/sanity_check_data.csv`; the second uses it to create Supplementary Figure 8.

### 7. Build the six demand proxies

After the normalized lawyer master csv is generated, run these six notebooks in any order:

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


### 8. Run the availability collapse

Copy the six normalized proxy CSVs into the same folder with:

```text
Scripts/Availability/Cases per Lawyer Data Collapse.nb
```

Open the Mathematica notebook and evaluate it from top to bottom. The model results and collapsed plot are displayed in the notebook.

### 9. Run the affordability analyses

First run:

```text
Scripts/Affordability/Extended_Professions_Affordability.ipynb
```
It generates the following files:
* `Supplementary_Figure_7_Lawyers_data.csv`, data used to generate Panel a. of Supplementary Figure 7
* `Supplementary_Figure_7_Pharmacists_data.csv`, data used to generate Panel b. of Supplementary Figure 7
* `Annual_Average_Affordability_All.csv`, data used to generate Panel a. of Figure 4, and Supplementary Table 3
* `Annual_Affordability_Spearman_All.csv`, data used to generate Panel b. of Figure 4
  
To generate Figure 4, copy Annual_Average_Affordability_All.csv and Annual_Affordability_Spearman_All.csv into Scripts/Affordability/, where they can be accessed by:

Scripts/Affordability/Affordability analysis.nb

To create Supplementary Table 3, evaluate Scripts/Affordability/Linear trend analysis of lawyer affordability.nb. This analysis uses Annual_Average_Affordability_All.csv, not Legal_Economy_Results.csv.

To create Supplementary Figure 7, run:

Scripts/Affordability/Lawyers_2024_Spearman_Plot.ipynb

This notebook reads Supplementary_Figure_7_Lawyers_data.csv and Supplementary_Figure_7_Pharmacists_data.csv directly from Data/Processed Data/Affordability/. It saves the completed figure as:

Figures/Supplementary Figure 7/Supplementary_Figure_7.pdf

After the four affordability CSVs have been created, the analyses for Figure 4, Supplementary Table 3, and Supplementary Figure 7 are independent and may be run in any order.

### 10. Run the legal-economy analysis

Run in this order:

1. `Scripts/Legal-Economy-Coupling/Legal_Economy_Data.ipynb`
2. `Scripts/Legal-Economy-Coupling/Legal_Economy_Results.ipynb`

The second notebook saves `Data/Processed Data/Legal-Economy-Coupling/Legal_Economy_Results.csv`, which contains the annual slope, intercept, confidence intervals, coefficient of determination, and sample size used in Supplementary Table 4. It also displays the yearly diagnostic figures without requiring figure-file export.

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
- Geographic analysis is restricted to valid metropolitan statistical areas; Micropolitan Statistical Areas, Connecticut MSAs, and Puerto Rico metropolitan areas are excluded where specified by the processing pipeline.
- Preserve exact filenames and directory names. Several notebooks rely on fixed source filenames even though the repository root itself is detected automatically.
- Large, private, or licensed raw files are intentionally excluded.
