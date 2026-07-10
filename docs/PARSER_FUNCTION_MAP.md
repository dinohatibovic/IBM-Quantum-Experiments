# Parser Function Map

```text
31:def load_json(path: str) -> dict:
37:def load_job(job_id: str, base_dir: str = "data/results") -> tuple[dict, dict]:
57:def decode_bitarray(b64_string: str) -> np.ndarray:
80:def bitarray_to_shots(arr: np.ndarray, num_bits: int) -> list[str]:
114:def extract_registers(result_json: dict) -> list[dict]:
184:def bell_fidelity(counts: dict, total: int,
195:def concurrence(fidelity: float) -> float:
203:def tangle(C: float) -> float:
208:def qber(bob_counts: dict, total: int, alice_sends: str = "0") -> float:
218:def shannon_entropy(counts: dict, total: int) -> float:
227:def wilson_ci(count: int, n: int, z: float = 1.96) -> tuple[float, float]:
241:def chi2_reproducibility(counts1: dict, counts2: dict,
253:def uniformity_test(counts: dict, num_states: int,
271:def extract_info(info_json: dict) -> dict:
304:def process_job(job_id: str, base_dir: str = "data/results",
413:def test_reproducibility(job_id_1: str, job_id_2: str,
451:def load_calibration(calib_path: str, qubits: list[int] = None) -> dict:
510:def save_csv(rows: list[dict], output_path: str = "quantum_results.csv"):
535:def main():
```

## STEP markers

```text
28:# STEP 1: Load JSON files
54:# STEP 2: Decode BitArray
111:# STEP 3: Extract all registers from result.json
181:# STEP 4: Compute metrics
268:# STEP 5: Extract job-level metadata from info.json
301:# STEP 6: Build full metrics dict for a single job
410:# STEP 7: Reproducibility test
448:# STEP 8: Load calibration JSON (when available)
495:# STEP 9: Save CSV
520:# STEP 10: CLI entry point
```
