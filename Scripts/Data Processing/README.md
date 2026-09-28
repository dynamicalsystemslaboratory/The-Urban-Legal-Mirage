# Data Processing

Processes the Bright Data lawyer files and harmonizes the annual BLS occupation tables used by downstream analyses.

## Execution order

1. **`Preprocessing_and_Anonymization.ipynb`** — When the original Bright Data snapshots are available, creates the anonymized lawyer files and firm-address counts. This step does not need to be rerun when using the anonymized archive and processed firm-address counts provided with the repository.
2. **`Lawyer_Paper_Complete_Pipeline.ipynb`** — Creates the lawyer master tables required by most downstream notebooks from the anonymized lawyer files.
3. **`Filtering_BLS_Data_Extended_Professions.ipynb`** — Creates the harmonized annual BLS files required by the affordability, consistency, and legal-economy analyses.

The lawyer and BLS notebooks produce different processed inputs. The lawyer pipeline is listed first because its outputs are used most broadly across the repository.

## Code documentation

## Complete Lawyer Data Processing Pipeline

**Code files:** `Preprocessing_and_Anonymization.ipynb` and `Lawyer_Paper_Complete_Pipeline.ipynb`

### Purpose

`Preprocessing_and_Anonymization.ipynb` processes the three original Bright Data lawyer snapshots into three row-level anonymized files and the aggregated MSA-level firm-address statistics. `Lawyer_Paper_Complete_Pipeline.ipynb` then processes the anonymized files into the MSA-level lawyer master and the 1-over-N normalized specialty master used throughout the paper.

### Raw Bright Data source structure

The three `snap_mi504g7pxmrn977ah.[#].csv` files contain the following columns relating to the Martindale lawyer profiles. These original files contain identifying profile information and are not provided in the repository. They are read only by `Preprocessing_and_Anonymization.ipynb`; the public lawyer master pipeline instead reads the anonymized files distributed in `Data/BrightData_Lawyers/BrightData_Lawyer_Snapshots.zip`.

The column names below are reproduced exactly as they appear in the raw files (spelling errors are in original source):

```text
url
address
admission
areas_of_practice
isln
law_school_attended
location
name
practice_count
type
university_attended
year_of_first_admission
filial
people
awards
profile_peer_review_count
profile_peer_review_star
profile_peer_review_awards
fax
languages
mailing_address
office_hours
office_size
phone
photo
profile_peer_review_detail
profile_visibility
video_call
website
biography
birth_information
memberships
hobbies_interests
profile_client_recomendation_count
profile_client_recomendation_rating
profile_client_review_count
profile_client_review_detail
profile_client_review_list
profile_client_review_rating
clients
clients2
year_established
about
payment_information
state_bar_summary
transactions
minority_owned
phone_cell
phone_telecopier
company
```

### Raw Bright Data columns used during preprocessing

Although the raw Bright Data snapshots contain many Martindale profile fields, the processing pipeline uses only the following five columns:

| Column | Use in the pipeline |
|---|---|
| `url` | Serves as the unique lawyer-profile identifier (`lawyer_id`). |
| `mailing_address` | Primary field used to extract the lawyer's five-digit ZIP code. |
| `address` | First fallback field when a ZIP code cannot be extracted from `mailing_address`. |
| `location` | Second fallback field when a ZIP code cannot be extracted from either address field. |
| `areas_of_practice` | Used to assign each lawyer to one or more legal-practice categories through the specialty crosswalk. |

The remaining profile fields, including the lawyer's name, admission history, education, reviews, contact information, and biography, are not used in the lawyer-count aggregation or downstream analyses.

The preprocessing step converts the original row-level data into seven public columns:

| Column | Use |
|---|---|
| `ID` | Anonymous seven-digit lawyer identifier replacing the profile URL. |
| `zip_code` | ZIP used by the downstream pipeline for MSA assignment. It is selected from `mailing_address`, then `address`, then `location`. |
| `mailing_zip` | ZIP extracted from `mailing_address` and retained separately for transparency. |
| `city` | City derived from `zip_code` using the HUD ZIP geography. |
| `state` | State derived from `zip_code` using the HUD ZIP geography. |
| `specializations` | Renamed `areas_of_practice` values used by the specialty crosswalk. |
| `number_of_specializations` | Number of reported practice areas. |

`Lawyer_Paper_Complete_Pipeline.ipynb` uses `ID`, `zip_code`, and `specializations`; the other released columns are retained in the anonymized files but are not required to build the lawyer master.

### What the code does

1. `Preprocessing_and_Anonymization.ipynb` checks the original Bright Data files and the privacy policy for all raw columns.
1. Extracts the rightmost valid five-digit ZIP using mailing address first, address second, and location third.
1. Builds `firm_address_counts_by_MSA.csv` from the original address information before identifying address fields are removed.
1. Replaces the profile URL with an anonymous seven-digit ID and writes the three anonymized Bright Data files containing only the seven public columns listed above.
1. `Lawyer_Paper_Complete_Pipeline.ipynb` checks the anonymized input files and loads the 13-category practice-area crosswalk.
1. Builds the valid metropolitan MSA list from the QCEW county-to-MSA crosswalk and removes Puerto Rico metropolitan areas.
1. Resolves each `zip_code` to one CBSA using valid-MSA status and available ZIP-to-CBSA ratio fields.
1. Creates a lawyer-by-specialty binary matrix and retains lawyers with zero mapped labels.
1. Assigns each lawyer to a valid MSA and aggregates binary and 1-over-N normalized specialty counts.

### Required inputs

Provided with the repository:

- `Data/BrightData_Lawyers/BrightData_Lawyer_Snapshots.zip`
- `Data/BrightData_Lawyers/firm_address_counts_by_MSA.csv`
- `Data/BrightData_Lawyers/brightdata_practice_area_to_12_crosswalk_90pct.csv`
- `Data/Geography/Crosswalks/qcew-county-msa-csa-crosswalk-clean.xlsx`

Before running `Lawyer_Paper_Complete_Pipeline.ipynb`, extract `BrightData_Lawyer_Snapshots.zip` directly inside `Data/BrightData_Lawyers/`. This should create:

- `Data/BrightData_Lawyers/BrightData_Lawyers_Anonymized_1.csv`
- `Data/BrightData_Lawyers/BrightData_Lawyers_Anonymized_2.csv`
- `Data/BrightData_Lawyers/BrightData_Lawyers_Anonymized_3.csv`

The original `snap_mi504g7pxmrn977ah.[#].csv` files are required only to rerun `Preprocessing_and_Anonymization.ipynb` and are not redistributed.

The remaining required file is not redistributed and must be downloaded separately:

- `Data/Geography/Crosswalks/ZIP_CBSA_122024.xlsx`

Download the 4th Quarter 2024 ZIP-CBSA crosswalk from the HUD-USPS ZIP Code Crosswalk Files, rename it to `ZIP_CBSA_122024.xlsx`, and place it in `Data/Geography/Crosswalks/`.

### Outputs

`Preprocessing_and_Anonymization.ipynb` creates:

- `Data/BrightData_Lawyers/BrightData_Lawyers_Anonymized_1.csv`
- `Data/BrightData_Lawyers/BrightData_Lawyers_Anonymized_2.csv`
- `Data/BrightData_Lawyers/BrightData_Lawyers_Anonymized_3.csv`
- `Data/BrightData_Lawyers/firm_address_counts_by_MSA.csv`

`Lawyer_Paper_Complete_Pipeline.ipynb` creates:

- `Data/BrightData_Lawyers/BrightData_Lawyers_master.csv`
- `Data/BrightData_Lawyers/BrightData_Lawyers_master_normalized_1overN.csv`

### Dependencies

- `pandas`
- `numpy`
- `openpyxl`
- `polars` (optional, used for faster CSV loading)

### How to run

For the public repository workflow, extract `BrightData_Lawyer_Snapshots.zip` inside `Data/BrightData_Lawyers/` and run `Lawyer_Paper_Complete_Pipeline.ipynb` from within the repository. The notebook locates the repository root automatically, prints validation counts, and writes only the two lawyer master files.

If reconstructing the public inputs from the original Bright Data snapshots, first run `Preprocessing_and_Anonymization.ipynb`.

### Notes

- The three anonymized Bright Data snapshots are redistributed in `BrightData_Lawyer_Snapshots.zip` with permission from Bright Data; the original identifying snapshots are not redistributed.
- Each labeled lawyer contributes 1/N to each of their N mapped specialties in the normalized master.
- "Unspecified" retains profiles that cannot be assigned to a valid metropolitan MSA.
- `ZIP_CBSA_122024.xlsx` must be obtained separately from HUD and placed in `Data/Geography/Crosswalks/` with the expected filename.

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
1. Replaces updated titles and codes with the project's original harmonized labels.
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

- The occupation list is designed for licensed, highly educated professions that can be self-employed and are not split across ambiguous "All Others" categories.
- Years with no input file are skipped.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.
