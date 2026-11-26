#!/usr/bin/env python3
"""Append stable sample_id values to a prepared QA CSV.

The ID is SHA-256 over [source_dataset, split, context, question], serialized
as compact UTF-8 JSON. This exactly matches the IDs used in public result CSVs.
"""
import argparse
import hashlib
import json
import pandas as pd

def sample_id(row):
    payload = json.dumps(
        [str(row["source_dataset"]), str(row["split"]), str(row["context"]), str(row["question"])],
        ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", help="Prepared dataset CSV with source_dataset, split, context, question")
    parser.add_argument("output_csv", help="Destination CSV")
    args = parser.parse_args()
    df = pd.read_csv(args.input_csv)
    required = {"source_dataset", "split", "context", "question"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {sorted(missing)}")
    df.insert(0, "sample_id", df.apply(sample_id, axis=1))
    if df["sample_id"].duplicated().any():
        raise SystemExit("Duplicate sample_id values found; inspect duplicate input examples.")
    df.to_csv(args.output_csv, index=False)

if __name__ == "__main__":
    main()
