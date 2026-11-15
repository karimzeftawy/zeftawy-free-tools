# How to clean messy CSV files in Python without Pandas

A CSV export can look clean in a spreadsheet but still have leading spaces, a UTF-8 byte-order mark (BOM), empty records, and repeated data. Here's a repeatable way to handle the **safe, simple** cases with Python's standard library.

## 1. Understand what you're cleaning

Consider this input:

```csv
Name,City,Role
 Alice  , Cairo , Analyst
 , ,
 Bob , Giza ,Developer
 Alice  , Cairo , Analyst
```

We want to trim whitespace in each cell and remove the all-blank row. **We will keep the duplicate Alice row on purpose.** Deduplication is a different decision and could discard meaningful records.

## 2. Use the built-in CSV parser

A common mistake is calling `line.split(",")`. That breaks quoted fields such as `"New York, NY"`. The `csv.reader` parser correctly handles commas and quote escaping.

Read your file with `encoding="utf-8-sig"` so Python removes a UTF-8 BOM when present. Open files with `newline=""` so the CSV module controls newline handling correctly.

```python
import csv

with open("input.csv", encoding="utf-8-sig", newline="") as inp:
    for row in csv.reader(inp):
        trimmed = [cell.strip() for cell in row]
        if not trimmed or all(not value for value in trimmed):
            continue
        print(trimmed)
```

The header stays capitalized; exact duplicate rows remain.

## 3. Don't overwrite the source

For a first pass, always write to a different file. Safer tools should also avoid overwriting an existing output path.

```python
with open("input.csv", encoding="utf-8-sig", newline="") as inp:
    with open("clean.csv", "x", encoding="utf-8", newline="") as out:
        reader = csv.reader(inp)
        writer = csv.writer(out)
        for row in reader:
            cleaned = [value.strip() for value in row]
            if cleaned and any(cleaned):
                writer.writerow(cleaned)
```

`"x"` fails if the output already exists. If the input is malformed or the process fails partway through, review or remove any partially written output before reusing the name.

## 4. Why duplicate removal is not always safe

Two records with identical values may represent separate legitimate events. Removing them automatically can corrupt logs, accounting data, or time-series data.

If you explicitly need exact-row deduplication, you can maintain a set of row tuples and skip repeated tuples; test this on noncritical data first. For large datasets, an in-memory set might consume substantial memory.

## 5. Important limitations

CSV is not a fully typed format. Simple whitespace cleanup does not validate numeric values, date formats, or formulas. It also does not protect against spreadsheet formula injection when untrusted content is later opened in Excel. Treat external CSV content as untrusted input.

## Try the open-source tool

[CleanCSV Lite source and tests](../cleancsv-lite/) implements blank-row removal with a new output file and no external dependencies. The full source is free here.

For an optional CLI upgrade with header normalization and exact duplicate removal, see [CleanCSV Pro — $8](https://zeftawy.gumroad.com/l/jnqegk?utm_source=github&utm_medium=guide&utm_campaign=csv_help).

**No purchase is needed to run the free tool.**
