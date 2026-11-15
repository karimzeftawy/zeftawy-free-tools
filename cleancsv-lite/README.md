# CleanCSV Lite — Free Offline Python CSV Cleaner

CleanCSV Lite is a free command-line utility that trims whitespace from CSV cells and removes fully empty rows. All source code is provided here under the MIT license.

## Requirements
Python 3.9+; no third-party packages or online account.

## Quick start
From this folder:

    python3 cleancsv_lite.py samples/messy.csv clean.csv

A new output file is created; input and existing outputs are never intentionally overwritten. Handles UTF-8 BOM. Test on sample data first.

## Features
- Trim leading and trailing whitespace from each cell
- Remove fully blank rows
- Preserve duplicate rows and original header capitalization
- Write a new CSV, not modify the original
- Test with: python3 -m unittest discover -s tests -v

Limitations: does not repair malformed CSV, detect types, sanitize spreadsheet formulas, preserve formatting, or deduplicate.

Optional paid [CleanCSV Pro — $8](https://zeftawy.gumroad.com/l/jnqegk?utm_source=github&utm_medium=repo_readme&utm_campaign=free_tools) adds deduplication and header normalization. **The free edition is complete and remains free.**
