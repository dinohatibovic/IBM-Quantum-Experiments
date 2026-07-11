# Runtime Safety Notes

Notes on the runtime behavior of `parse_ibm_json.py` for anyone auditing this
repository before citing it or running it locally.

## What the parser does
- Reads local JSON files only, from the directory passed via `--results_dir`
  (default `data/results`). It does not make any network calls.
- Decodes base64/zlib-compressed `BitArray` payloads embedded in IBM Qiskit
  SamplerV2 `result.json` exports using `base64`, `zlib`, and `numpy`'s
  buffer/array reconstruction — no `pickle`, `eval`, or `exec` is used anywhere
  in the script.
- Writes a single CSV output file to the path passed via `--output` (default
  `data/quantum_results_verified.csv`). No other files are written.

## What it does not do
- No shelling out to external processes.
- No dependency on IBM Quantum credentials, tokens, or the `qiskit-ibm-runtime`
  SDK — it operates purely on already-exported JSON files.
- No dynamic code execution based on file contents.

## Known limitations
- `data/results/`, `data/circuits/`, and `data/calibration/` are currently
  empty in this repository (see `docs/DATA_AVAILABILITY.md`), so the default
  invocation (`python parse_ibm_json.py`) cannot process real data end-to-end
  here — it can only run in single-job (`--job`) or reproducibility (`--repro`)
  mode against locally supplied JSON files, or via `--calib` once calibration
  data is supplied by the user.
- Malformed or truncated JSON input raises a standard Python exception rather
  than failing silently.
