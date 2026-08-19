#!/usr/bin/env bash

echo
echo "===== STATUS ====="
test -f STATUS.md && echo OK

echo
echo "===== NOTEBOOKS ====="
ls notebooks/*.ipynb

echo
echo "===== BENCHMARK RECORDS ====="
find data/benchmark_records -type f

echo
echo "===== RUNTIME JOBS ====="
find data/results/runtime_jobs -type f

echo
echo "===== CHECKSUMS ====="
test -f SHA256SUMS.txt && echo OK
