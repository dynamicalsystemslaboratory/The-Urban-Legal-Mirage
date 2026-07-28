# Introduction

Creates the county-level ABA lawyer measures used for the introductory comparison in the paper.

## Execution order

1. **`ABA_Data_Extraction.ipynb`** — Run from top to bottom after downloading the required ABA and Census county files.

## Code documentation

## ABA County Lawyer Data Extraction

**Code file:** `ABA_Data_Extraction.ipynb`

### Purpose

Merges ABA county-level lawyer counts with 2019 Census county population estimates and calculates the county-level lawyer availability thresholds reported in the introduction.

### What the code does

1. Loads ABA county lawyer counts and Census 2019 county population estimates.
1. Normalizes county names by removing accents, punctuation, and county-type suffixes.
1. Handles independent cities and known county-name mismatches, including a combined Fairfax City and County entry.
1. Merges lawyer counts to population and reports any missing population matches.
1. Calculates lawyers per 1,000 residents.
1. Counts counties below 1 lawyer per 1,000 and counties at or above 10 lawyers per 1,000.

### Required inputs

- `Data/Introduction/aba_county_lawyers.csv`
- `Data/Population Data/County Population/co-est2019-alldata.csv`

### Outputs

- `Data/Introduction/aba_county_lawyers_intro.csv`
- Printed county counts and percentages for the two lawyer-availability thresholds.

### Dependencies

- `pandas`

### How to run

Run the notebook from top to bottom in Jupyter after placing the required files in the paths listed below. The code assumes `PROJECT_ROOT = /Users/<username>/Final_Lawyer_Git July10`.

### Notes

- The Census file is read using `cp1252` encoding.
- County matching uses a combination of explicit corrections and normalized state-plus-county keys.
- Raw or restricted source data are not redistributed with the repository. Download or obtain them separately and preserve the expected filenames and folder structure.
