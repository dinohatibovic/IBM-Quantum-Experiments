#!/usr/bin/env bash
set -e

mkdir -p data/benchmark_records/generated

cp data/benchmark_records/bell_template.yaml \
data/benchmark_records/generated/bell_record.yaml

echo "QAB export generated."
