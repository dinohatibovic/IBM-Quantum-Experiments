# data/results/ — raw IBM job exports

This directory holds the raw IBM Quantum job files that make
`parse_ibm_json.py` (and therefore `data/quantum_results_verified.csv`)
reproducible end-to-end:

```text
job-<job_id>-info.json      — job metadata (backend, created, shots, cost)
job-<job_id>-result.json    — SamplerV2 result (DataBin/BitArray, RuntimeEncoder format)
```

One pair per job, for the eight job IDs listed in `docs/JOB_IDS.md` and in
`KNOWN_JOBS` of `parse_ibm_json.py`.

## How to populate this directory

Raw experimental data can only come from the IBM Quantum account that ran
the jobs — it must never be reconstructed or hand-written.

Option 1 — automated (requires the account's API token):

```bash
pip install qiskit-ibm-runtime
python scripts/fetch_raw_results.py              # all 8 jobs
python scripts/fetch_raw_results.py --calibration  # + calibration snapshots
```

Option 2 — manual: IBM Quantum dashboard → Workloads → select the job →
Download the info and result JSON files, rename them to the pattern above,
and place them here.

## Verifying

```bash
python parse_ibm_json.py --results_dir data/results \
    --output data/quantum_results_verified.csv
bash scripts/smoke_test.sh
```

The regenerated CSV must match the committed one (job `d5sd9mveglic739vatm0`
is expected to differ from pre-v1.1.1 history: it is flagged anomalous — see
`docs/REMEDIATION_PLAN.md` §2.1). After adding files here, extend
`data/checksums/release_sha256.txt` so releases cover the raw data too.

Note: IBM's job retention window is limited; if the API can no longer return
these jobs, only the dashboard download (Option 2) or a previously saved
export can supply them.
