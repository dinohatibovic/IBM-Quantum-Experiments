"""
parse_ibm_json.py
─────────────────
Parses IBM SamplerV2 result.json and info.json files
and extracts all metrics: counts, QBER, fidelity, concurrence,
Shannon entropy, chi-squared reproducibility, and calibration values.

Usage:
    python parse_ibm_json.py --results_dir data/results/ --output data/quantum_results_verified.csv
    python parse_ibm_json.py --job d5sd9mveglic739vatm0 --verbose
    python parse_ibm_json.py --repro d5scvp3v0pgs7392jj30 d5sd2ioubqnc73c4im80
"""

import argparse
import base64
import csv
import io
import json
import math
import os
import sys
import zlib

import numpy as np
from scipy import stats

# ─────────────────────────────────────────────────────────────────
# STEP 1: Load JSON files
# ─────────────────────────────────────────────────────────────────

def load_json(path: str) -> dict:
    """Load a JSON file. Raises FileNotFoundError if missing."""
    with open(path, "r") as f:
        return json.load(f)


def load_job(job_id: str, base_dir: str = "data/results") -> tuple[dict, dict]:
    """
    Load both info.json and result.json for a given job_id.
    Returns (info_dict, result_dict).
    """
    info_path   = os.path.join(base_dir, f"job-{job_id}-info.json")
    result_path = os.path.join(base_dir, f"job-{job_id}-result.json")

    if not os.path.exists(info_path):
        raise FileNotFoundError(f"Missing: {info_path}")
    if not os.path.exists(result_path):
        raise FileNotFoundError(f"Missing: {result_path}")

    return load_json(info_path), load_json(result_path)


# ─────────────────────────────────────────────────────────────────
# STEP 2: Decode BitArray
# ─────────────────────────────────────────────────────────────────

def decode_bitarray(b64_string: str) -> np.ndarray:
    """
    Decode IBM SamplerV2 BitArray from its serialized form.

    Encoding pipeline (IBM's format):
        numpy array  →  .npy binary  →  zlib compress  →  base64 encode

    We reverse this:
        base64 decode  →  zlib decompress  →  numpy .load()

    Returns:
        ndarray of shape (shots, num_bytes_per_shot)
        dtype: uint8
    """
    # base64 decode (add padding to be safe)
    raw_bytes    = base64.b64decode(b64_string + "===")
    # zlib decompress
    decompressed = zlib.decompress(raw_bytes)
    # numpy .npy load
    buffer       = io.BytesIO(decompressed)
    return np.load(buffer, allow_pickle=False)


def bitarray_to_shots(arr: np.ndarray, num_bits: int) -> list[str]:
    """
    Convert a decoded BitArray ndarray to a list of bitstrings.

    Qiskit packs bits MSB-first into uint8 bytes.
    For num_bits=2: each row is 1 byte, we take the last 2 bits.
    For num_bits=4: each row is 1 byte, we take the last 4 bits.
    For num_bits=8: each row is 1 byte, all 8 bits.

    Args:
        arr:      ndarray shape (shots, ceil(num_bits/8))
        num_bits: number of classical bits in this register

    Returns:
        list of bitstrings, e.g. ['11', '00', '11', '01', ...]
    """
    shots = []
    for i in range(arr.shape[0]):
        row = arr[i]
        # Unpack each byte MSB-first
        full_bits = "".join(
            str((byte >> bit_pos) & 1)
            for byte in row
            for bit_pos in range(7, -1, -1)
        )
        # Take only the rightmost num_bits
        shots.append(full_bits[-num_bits:])
    return shots


# ─────────────────────────────────────────────────────────────────
# STEP 3: Extract all registers from result.json
# ─────────────────────────────────────────────────────────────────

def extract_registers(result_json: dict) -> list[dict]:
    """
    Traverse result.json and find all DataBin objects.
    Each DataBin is one PUB (circuit execution) containing
    one or more BitArray registers.

    Returns:
        List of dicts, one per PUB:
        {
            'register_name': {
                'num_bits': int,
                'shots':    int,
                'bitstrings': list[str],
                'counts':   dict[str, int],
            },
            ...
        }
    """
    pubs = []

    def _traverse(obj, depth=0):
        if depth > 10:
            return
        if isinstance(obj, dict):
            if obj.get("__type__") == "DataBin":
                val         = obj.get("__value__", {})
                field_names = val.get("field_names", [])
                fields      = val.get("fields", {})

                pub = {}
                for fname in field_names:
                    field = fields.get(fname, {})
                    if field.get("__type__") != "BitArray":
                        continue

                    ba       = field["__value__"]
                    num_bits = ba["num_bits"]
                    b64      = ba["array"]["__value__"]

                    arr      = decode_bitarray(b64)
                    bitstrings = bitarray_to_shots(arr, num_bits)
                    counts   = {}
                    for s in bitstrings:
                        counts[s] = counts.get(s, 0) + 1

                    pub[fname] = {
                        "num_bits":   num_bits,
                        "shots":      len(bitstrings),
                        "bitstrings": bitstrings,
                        "counts":     counts,
                    }

                if pub:
                    pubs.append(pub)

            for v in obj.values():
                _traverse(v, depth + 1)

        elif isinstance(obj, list):
            for item in obj:
                _traverse(item, depth + 1)

    _traverse(result_json)
    return pubs


# ─────────────────────────────────────────────────────────────────
# STEP 4: Compute metrics
# ─────────────────────────────────────────────────────────────────

def bell_fidelity(counts: dict, total: int,
                  target: tuple = ("00", "11")) -> float:
    """
    Bell state fidelity = fraction of shots in target states.
    Default target: ('00', '11') for |Φ+⟩.
    For |11⟩-optimised circuits, use target=('11',).
    """
    signal = sum(counts.get(s, 0) for s in target)
    return signal / total if total > 0 else 0.0


def concurrence(fidelity: float) -> float:
    """
    Concurrence approximation for pure states: C ≈ max(0, 2F − 1).
    Range: 0 (separable) to 1 (maximally entangled).
    """
    return max(0.0, 2.0 * fidelity - 1.0)


def tangle(C: float) -> float:
    """Tangle = C²."""
    return C ** 2


def qber(bob_counts: dict, total: int, alice_sends: str = "0") -> float:
    """
    Quantum Bit Error Rate at Bob's receiver.
    QBER = P(Bob received ≠ alice_sends).
    """
    error_bit = "1" if alice_sends == "0" else "0"
    errors    = bob_counts.get(error_bit, 0)
    return errors / total if total > 0 else 0.0


def shannon_entropy(counts: dict, total: int) -> float:
    """Shannon entropy in bits."""
    return -sum(
        (v / total) * math.log2(v / total)
        for v in counts.values()
        if v > 0
    )


def wilson_ci(count: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """
    Wilson score confidence interval for a proportion.
    Returns (lower, upper) as fractions (not percentages).
    """
    if n == 0:
        return 0.0, 1.0
    p      = count / n
    denom  = 1 + z ** 2 / n
    center = (p + z ** 2 / (2 * n)) / denom
    margin = z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / denom
    return max(0.0, center - margin), min(1.0, center + margin)


def chi2_reproducibility(counts1: dict, counts2: dict,
                          states: list) -> tuple[float, float]:
    """
    Chi-squared test for reproducibility between two independent runs.
    H₀: both runs drawn from the same distribution.
    Returns (chi2_stat, p_value).
    """
    obs1 = [counts1.get(s, 0) for s in states]
    obs2 = [counts2.get(s, 0) for s in states]
    return stats.chisquare(obs1, f_exp=obs2)


def uniformity_test(counts: dict, num_states: int,
                    total: int) -> tuple[float, float]:
    """
    Chi-squared uniformity test.
    H₀: distribution is uniform across all num_states states.
    Returns (chi2_stat, p_value).
    """
    all_states = [format(i, f"0{int(math.log2(num_states))}b")
                  for i in range(num_states)]
    observed   = [counts.get(s, 0) for s in all_states]
    expected   = [total / num_states] * num_states
    return stats.chisquare(observed, f_exp=expected)


# ─────────────────────────────────────────────────────────────────
# STEP 5: Extract job-level metadata from info.json
# ─────────────────────────────────────────────────────────────────

def extract_info(info_json: dict) -> dict:
    """
    Extract key metadata fields from *-info.json.
    Returns a flat dict with job-level fields.
    """
    params = info_json.get("params", {})
    pubs   = params.get("pubs", [])

    shots_per_pub = []
    for pub in pubs:
        if isinstance(pub, list) and len(pub) >= 3:
            s = pub[2]
            if isinstance(s, (int, float)):
                shots_per_pub.append(int(s))

    return {
        "job_id":          info_json.get("id",      "MISSING"),
        "status":          info_json.get("status",  "MISSING"),
        "backend":         info_json.get("backend", "MISSING"),
        "created":         info_json.get("created", "MISSING"),
        "user_id":         info_json.get("user_id", "MISSING"),
        "QPU_cost_ms":     info_json.get("cost",    "MISSING"),
        "runtime_s":       info_json.get("estimated_running_time_seconds", "MISSING"),
        "num_pubs":        len(pubs),
        "shots_per_pub":   shots_per_pub,
        "program_id":      info_json.get("program", {}).get("id", "MISSING"),
    }


# ─────────────────────────────────────────────────────────────────
# STEP 6: Build full metrics dict for a single job
# ─────────────────────────────────────────────────────────────────

def process_job(job_id: str, base_dir: str = "data/results",
                verbose: bool = False) -> dict:
    """
    Full pipeline for a single job:
        load → decode → extract counts → compute metrics → return dict

    Returns a flat dict suitable for CSV output.
    """
    info_json, result_json = load_job(job_id, base_dir)

    meta  = extract_info(info_json)
    pubs  = extract_registers(result_json)

    row = {
        "job_id":           job_id,
        "date":             meta["created"][:10] if meta["created"] != "MISSING" else "MISSING",
        "time_utc":         meta["created"][11:16] if meta["created"] != "MISSING" else "MISSING",
        "backend":          meta["backend"],
        "status":           meta["status"],
        "user_id":          meta["user_id"],
        "num_circuits":     meta["num_pubs"],
        "QPU_cost_ms":      meta["QPU_cost_ms"],
        "runtime_s":        meta["runtime_s"],
        "total_shots":      0,
        "registers":        "",
        # Computed metrics
        "fidelity":         "N/A",
        "fidelity_ci_lo":   "N/A",
        "fidelity_ci_hi":   "N/A",
        "concurrence_C":    "N/A",
        "tangle_T":         "N/A",
        "QBER":             "N/A",
        "QBER_ci_lo":       "N/A",
        "QBER_ci_hi":       "N/A",
        "shannon_entropy":  "N/A",
        # Hardware calibration (requires calibration JSON)
        "T1_avg_us":        "MISSING — export backend.properties()",
        "T2_avg_us":        "MISSING — export backend.properties()",
        "CZ_error_pct":     "MISSING — export backend.properties()",
        "readout_error_pct":"MISSING — export backend.properties()",
    }

    alice_counts = None
    bob_counts   = None
    all_shots    = 0

    for pub in pubs:
        for fname, data in pub.items():
            row["registers"] += fname + ";"
            all_shots += data["shots"]
            c  = data["counts"]
            nb = data["num_bits"]
            n  = data["shots"]

            # Bell state (2-bit meas register)
            if fname == "meas" and nb == 2:
                f = bell_fidelity(c, n, target=("00", "11"))
                # If fidelity < 50%, it's probably a |11⟩-optimised circuit
                if c.get("11", 0) / n > 0.80:
                    f = c.get("11", 0) / n  # target is just |11⟩
                C = concurrence(f)
                T = tangle(C)
                lo, hi = wilson_ci(int(f * n), n)

                row["fidelity"]       = round(f, 6)
                row["fidelity_ci_lo"] = round(lo, 6)
                row["fidelity_ci_hi"] = round(hi, 6)
                row["concurrence_C"]  = round(C, 6)
                row["tangle_T"]       = round(T, 6)
                row["shannon_entropy"]= round(shannon_entropy(c, n), 6)

            # BB84 Alice reference
            if fname in ("c0", "safe") and nb == 1:
                alice_counts = c

            # BB84 Bob
            if fname == "bob" and nb == 1:
                bob_counts = c

            # VQC / QRNG multi-bit
            if nb >= 4 and fname == "meas":
                row["shannon_entropy"] = round(shannon_entropy(c, n), 6)

        if verbose:
            print(f"  PUB registers: {list(pub.keys())}")

    row["total_shots"] = all_shots
    row["registers"]   = row["registers"].rstrip(";")

    # Compute QBER if both Alice and Bob registers found
    if alice_counts is not None and bob_counts is not None:
        n_bob  = sum(bob_counts.values())
        q      = qber(bob_counts, n_bob, alice_sends="0")
        lo, hi = wilson_ci(bob_counts.get("1", 0), n_bob)
        row["QBER"]       = round(q, 6)
        row["QBER_ci_lo"] = round(lo, 6)
        row["QBER_ci_hi"] = round(hi, 6)

    if verbose:
        for k, v in row.items():
            print(f"  {k:<22}: {v}")

    return row


# ─────────────────────────────────────────────────────────────────
# STEP 7: Reproducibility test
# ─────────────────────────────────────────────────────────────────

def test_reproducibility(job_id_1: str, job_id_2: str,
                          base_dir: str = "data/results") -> dict:
    """
    Chi-squared reproducibility test between two jobs with identical circuits.
    Both must have a 2-bit 'meas' register.
    """
    _, r1 = load_job(job_id_1, base_dir)
    _, r2 = load_job(job_id_2, base_dir)

    pubs1 = extract_registers(r1)
    pubs2 = extract_registers(r2)

    c1 = next((p["meas"]["counts"] for p in pubs1 if "meas" in p), None)
    c2 = next((p["meas"]["counts"] for p in pubs2 if "meas" in p), None)

    if c1 is None or c2 is None:
        return {"error": "No 'meas' register found in one or both jobs"}

    states     = ["00", "01", "10", "11"]
    chi2_stat, p_val = chi2_reproducibility(c1, c2, states)

    return {
        "job_1":        job_id_1,
        "job_2":        job_id_2,
        "chi2":         round(chi2_stat, 4),
        "p_value":      round(p_val, 4),
        "df":           3,
        "conclusion":   "SAME distribution" if p_val > 0.05 else "DIFFERENT distributions",
        "counts_1":     {s: c1.get(s, 0) for s in states},
        "counts_2":     {s: c2.get(s, 0) for s in states},
        "delta":        {s: abs(c1.get(s,0) - c2.get(s,0)) for s in states},
    }


# ─────────────────────────────────────────────────────────────────
# STEP 8: Load calibration JSON (when available)
# ─────────────────────────────────────────────────────────────────

def load_calibration(calib_path: str, qubits: list[int] = None) -> dict:
    """
    Load IBM calibration JSON (output of backend.properties().to_dict()).
    Extracts T1, T2, readout error, and gate errors for specified qubits.

    Args:
        calib_path: path to *_calib_YYYY-MM-DD.json
        qubits:     list of qubit indices to extract (None = all)

    Returns:
        dict with per-qubit T1, T2, readout error and 2q gate errors
    """
    if not os.path.exists(calib_path):
        return {"error": f"Calibration file not found: {calib_path}"}

    calib = load_json(calib_path)
    result = {}

    # T1 and T2
    for q_data in calib.get("qubits", []):
        for param in q_data:
            name = param.get("name", "")
            idx  = param.get("qubits", [None])[0]
            if qubits and idx not in qubits:
                continue
            if name == "T1":
                result.setdefault(idx, {})["T1_us"] = param.get("value", "MISSING")
            elif name == "T2":
                result.setdefault(idx, {})["T2_us"] = param.get("value", "MISSING")
            elif name == "readout_error":
                result.setdefault(idx, {})["readout_error"] = param.get("value", "MISSING")

    # 2-qubit gate errors
    for gate in calib.get("gates", []):
        if gate.get("gate") in ("cz", "ecr", "cx"):
            q_pair = tuple(gate.get("qubits", []))
            for param in gate.get("parameters", []):
                if param.get("name") == "gate_error":
                    result.setdefault(f"2q_{q_pair}", {})["gate_error"] = param.get("value")

    return result


# ─────────────────────────────────────────────────────────────────
# STEP 9: Save CSV
# ─────────────────────────────────────────────────────────────────

FIELDNAMES = [
    "job_id", "date", "time_utc", "backend", "status", "user_id",
    "num_circuits", "total_shots", "QPU_cost_ms", "runtime_s",
    "registers",
    "fidelity", "fidelity_ci_lo", "fidelity_ci_hi",
    "concurrence_C", "tangle_T",
    "QBER", "QBER_ci_lo", "QBER_ci_hi",
    "shannon_entropy",
    "T1_avg_us", "T2_avg_us", "CZ_error_pct", "readout_error_pct",
]


def save_csv(rows: list[dict], output_path: str = "data/quantum_results_verified.csv"):
    """Write list of metric dicts to CSV."""
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved: {output_path}  ({len(rows)} rows)")


# ─────────────────────────────────────────────────────────────────
# STEP 10: CLI entry point
# ─────────────────────────────────────────────────────────────────

KNOWN_JOBS = [
    "d5scsqneglic739vag9g",
    "d5scvp3v0pgs7392jj30",
    "d5sd2ioubqnc73c4im80",
    "d5sd53k9u8fs73bd8du0",
    "d5sd7vbv0pgs7392jr4g",
    "d5sd8vgubqnc73c4isu0",
    "d5sd9mveglic739vatm0",
    "d5se1sk9u8fs73bd9arg",
]


def main():
    parser = argparse.ArgumentParser(
        description="Parse IBM SamplerV2 result.json and compute quantum metrics."
    )
    parser.add_argument("--results_dir", default="data/results",
                        help="Directory containing job JSON files")
    parser.add_argument("--output", default="data/quantum_results_verified.csv",
                        help="Output CSV file path")
    parser.add_argument("--job", default=None,
                        help="Process a single job ID (verbose output)")
    parser.add_argument("--repro", nargs=2, metavar="JOB_ID",
                        help="Test reproducibility between two job IDs")
    parser.add_argument("--calib", default=None,
                        help="Path to calibration JSON (optional)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    # ── Single job mode ───────────────────────────────────────────
    if args.job:
        print(f"\nProcessing job: {args.job}")
        row = process_job(args.job, args.results_dir, verbose=True)
        return

    # ── Reproducibility test ──────────────────────────────────────
    if args.repro:
        print(f"\nReproducibility test: {args.repro[0]} vs {args.repro[1]}")
        result = test_reproducibility(args.repro[0], args.repro[1], args.results_dir)
        for k, v in result.items():
            print(f"  {k:<20}: {v}")
        return

    # ── Full batch mode ───────────────────────────────────────────
    rows = []
    for job_id in KNOWN_JOBS:
        try:
            row = process_job(job_id, args.results_dir, verbose=args.verbose)
            rows.append(row)
            print(f"  OK  {job_id[:20]}  {row['backend']:12}  "
                  f"shots={row['total_shots']:6}  "
                  f"fidelity={row['fidelity']}  QBER={row['QBER']}")
        except FileNotFoundError as e:
            print(f"  SKIP  {job_id[:20]}  ({e})")

    # Reproducibility between Run 1 and Run 2
    if len(rows) >= 2:
        r = test_reproducibility(
            "d5scvp3v0pgs7392jj30",
            "d5sd2ioubqnc73c4im80",
            args.results_dir
        )
        print(f"\nReproducibility (Run1 vs Run2): χ²={r['chi2']}, "
              f"p={r['p_value']} → {r['conclusion']}")

    save_csv(rows, args.output)


if __name__ == "__main__":
    main()
