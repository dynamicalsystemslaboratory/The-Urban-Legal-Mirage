# Data Processing

Processes the raw lawyer directory and harmonizes the annual BLS occupation tables used by downstream analyses.

## Execution order

1. **`Lawyer_Paper_Complete_Pipeline.ipynb`** — Creates the lawyer master tables and firm-address counts required by most downstream notebooks.
2. **`Filtering_BLS_Data_Extended_Professions.ipynb`** — Creates the harmonized annual BLS files required by the affordability, consistency, and legal-economy analyses.

The two notebooks produce different processed inputs. The lawyer pipeline is listed first because its outputs are used most broadly across the repository.

## Code documentation

## Complete Lawyer Data Processing Pipeline

**Code file:** `Lawyer_Paper_Complete_Pipeline.ipynb`

### Purpose

Processes the three raw Bright Data lawyer snapshots into the MSA-level lawyer master, the 1-over-N normalized specialty master, and firm-address statistics used throughout the paper.

### What the code does

1. Checks all required raw files and creates the output directory.
1. Loads the 13-category practice-area crosswalk and cleans raw practice-area labels.
1. Builds the valid metropolitan MSA list from the QCEW county-to-MSA crosswalk and removes Puerto Rico metropolitan areas.
1. Resolves each ZIP to one CBSA using valid-MSA status and available ZIP-to-CBSA ratio fields.
1. Uses the profile URL as the lawyer identifier, with a file-and-row fallback when URL is missing.
1. Extracts the rightmost valid five-digit ZIP from mailing address, address, then location.
1. Creates a lawyer-by-specialty binary matrix and retains lawyers with zero mapped labels.
1. Assigns each lawyer to a valid MSA and aggregates binary and 1-over-N normalized specialty counts.
1. Counts shared addresses as firm addresses when at least two unique lawyers use the same cleaned address.

### Required inputs

- In `~/Downloads/`: `snap_mi504g7pxmrn977ah.1.csv`, `.2.csv`, and `.3.csv`
- In `~/Downloads/`: `ZIP_CBSA_122024.xlsx`
- In `~/Downloads/`: `qcew-county-msa-csa-crosswalk-clean.xlsx`
- In `~/Downloads/`: `brightdata_practice_area_to_12_crosswalk_90pct.csv`

### Outputs

- `Data/BrightData_Lawyers/BrightData_Lawyers_master.csv`
- `Data/BrightData_Lawyers/BrightData_Lawyers_master_normalized_1overN.csv`
- `Data/BrightData_Lawyers/firm_address_counts_by_MSA.csv`

### Dependencies

- `pandas`
- `numpy`
- `openpyxl`
- `polars (optional, used for faster CSV loading)`

### How to run

Edit the CONFIG paths if necessary, then run the single pipeline cell. The notebook prints validation counts and writes only the three listed output files.

### Notes

- Raw Bright Data files are private and are not included in the public repository.
- Each labeled lawyer contributes 1/N to each of their N mapped specialties in the normalized master.
- “Unspecified” retains profiles that cannot be assigned to a valid metropolitan MSA.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.

---

## Filtering and Harmonizing BLS Occupation Data

**Code file:** `Filtering_BLS_Data_Extended_Professions.ipynb`

### Purpose

Filters annual MSA BLS occupation tables to the licensed professional occupations used in the affordability and legal-economy analyses while harmonizing changing occupation titles and SOC codes.

### What the code does

1. Loads a manually curated occupation crosswalk containing original and replacement titles and SOC codes.
1. Normalizes occupation titles for text matching.
1. For each year from 2005 through 2024, filters the uniform BLS table once by title and once by SOC code.
1. Applies an additional title validation to address SOC code recycling around 2021.
1. Replaces updated titles and codes with the project’s original harmonized labels.
1. Checks whether title-based and code-based filtering produce identical tables.
1. Saves the title-filtered harmonized table for each available year.

### Required inputs

- `Data/BLS data/Uniform tables/Professional Licensed Occupations.xlsx`
- Annual `Data/BLS data/Uniform tables/MSA_<year>_Uniform.xlsx` files for available years from 2005–2024

### Outputs

- Annual `Data/Processed Data/Filtered tables/MSA_<year>_Filtered_Extended_Professions.xlsx` files

### Dependencies

- `pandas`
- `openpyxl`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. Run it from within the repository; the notebook locates the repository root automatically by searching the current directory and its parents for the `Scripts` folder.

### Notes

- The occupation list is designed for licensed, highly educated professions that can be self-employed and are not split across ambiguous “All Others” categories.
- Years with no input file are skipped.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.
