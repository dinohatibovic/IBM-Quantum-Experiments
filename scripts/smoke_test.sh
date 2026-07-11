#!/usr/bin/env bash
# Compile-checks the parser and validates the shape of the committed CSV.
# Does not run parse_ibm_json.py end-to-end: data/results/ is intentionally
# empty in this repository (see docs/DATA_AVAILABILITY.md), so there is no
# raw JSON input to process yet.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "[1/2] Compiling parse_ibm_json.py..."
python3 -m py_compile parse_ibm_json.py

echo "[2/2] Validating data/quantum_results_verified.csv shape..."
python3 - <<'PY'
import csv

with open("data/quantum_results_verified.csv", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

expected_columns = 24
expected_rows = 8

assert len(header) == expected_columns, (
    f"expected {expected_columns} columns, found {len(header)}"
)
assert len(rows) == expected_rows, (
    f"expected {expected_rows} data rows, found {len(rows)}"
)
print(f"OK: {len(header)} columns, {len(rows)} rows")
PY

echo "Smoke test passed."
