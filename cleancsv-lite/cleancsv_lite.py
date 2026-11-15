#!/usr/bin/env python3
"""CleanCSV Lite — safe, dependency-free CSV whitespace and empty-row cleanup."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Tuple


def clean_csv(source: Path, destination: Path) -> Tuple[int, int]:
    """Write trimmed nonblank rows to a *new* CSV. Return kept, skipped counts."""
    source = Path(source)
    destination = Path(destination)
    if source.resolve() == destination.resolve():
        raise ValueError("Input and output must be different files; in-place edits are disabled")
    if not source.is_file():
        raise FileNotFoundError(f"Input CSV does not exist: {source}")
    if destination.exists():
        raise FileExistsError(f"Output already exists: {destination} (choose another path)")
    if not destination.parent.is_dir():
        raise FileNotFoundError(f"Output folder does not exist: {destination.parent}")

    kept = skipped = 0
    try:
        # 'x' prevents silent overwrite, and utf-8-sig handles BOM from Excel exports.
        with source.open("r", encoding="utf-8-sig", newline="") as infile,                 destination.open("x", encoding="utf-8", newline="") as outfile:
            reader = csv.reader(infile, strict=True)
            writer = csv.writer(outfile)
            for row in reader:
                normalized = [cell.strip() for cell in row]
                if not row or all(not cell for cell in normalized):
                    skipped += 1
                    continue
                writer.writerow(normalized)
                kept += 1
    except (csv.Error, UnicodeError):
        # Only delete the new output file we created; never modify the source.
        if destination.exists():
            destination.unlink()
        raise
    return kept, skipped


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Trim CSV cells and remove empty rows (free edition).")
    parser.add_argument("input", type=Path, help="Source CSV path")
    parser.add_argument("output", type=Path, help="Path to a new CSV (must not exist)")
    args = parser.parse_args(argv)
    try:
        kept, skipped = clean_csv(args.input, args.output)
    except (OSError, ValueError, csv.Error, UnicodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(f"Saved {args.output} | rows kept: {kept} | blank rows removed: {skipped}")
    print("Tip: Need exact duplicate removal or lowercased column headers? Try CleanCSV Pro.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
