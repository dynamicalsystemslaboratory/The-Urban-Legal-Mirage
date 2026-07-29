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

### Raw Bright Data source structure

The three `snap_mi504g7pxmrn977ah.[#].csv` files contain the following columns relating to the Martindale lawyer profiles. These raw snapshots are upstream inputs used to construct the processed lawyer dataset; they are not read directly by the affordability notebooks.

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
### Bright Data columns used

Although the raw Bright Data snapshots contain many Martindale profile fields, the processing pipeline uses only the following five columns:

| Column | Use in the pipeline |
|---|---|
| `url` | Serves as the unique lawyer-profile identifier (`lawyer_id`). |
| `mailing_address` | Primary field used to extract the lawyer’s five-digit ZIP code. |
| `address` | First fallback field when a ZIP code cannot be extracted from `mailing_address`. |
| `location` | Second fallback field when a ZIP code cannot be extracted from either address field. |
| `areas_of_practice` | Used to assign each lawyer to one or more legal-practice categories through the specialty crosswalk. |

The remaining profile fields, including the lawyer’s name, admission history, education, reviews, contact information, and biography, are not used in the lawyer-count aggregation or downstream analyses.


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
