"""
fetch_raw_results.py
────────────────────
Download the raw IBM Quantum job data for the eight verified jobs and save
them into data/results/ in the exact format parse_ibm_json.py expects:

    data/results/job-<job_id>-info.json
    data/results/job-<job_id>-result.json

This script cannot invent data: it retrieves the original job records from
the IBM Quantum account that executed them, using qiskit-ibm-runtime's own
RuntimeEncoder serialization (the same __type__/__value__ DataBin/BitArray
format the parser decodes).

Prerequisites:
    pip install qiskit-ibm-runtime
    Saved credentials (once):
        from qiskit_ibm_runtime import QiskitRuntimeService
        QiskitRuntimeService.save_account(channel="ibm_quantum_platform",
                                          token="<YOUR_IBM_QUANTUM_API_TOKEN>")

Usage:
    python scripts/fetch_raw_results.py                 # all 8 known jobs
    python scripts/fetch_raw_results.py --job <job_id>  # a single job
    python scripts/fetch_raw_results.py --calibration   # also export backend
                                                        # calibration snapshots

Note on retention: IBM retains job results for a limited period. If a job is
no longer retrievable through the API, download its files manually from the
IBM Quantum dashboard (Workloads → job → Download) and place them in
data/results/ under the same names.
"""

import argparse
import json
import os
import sys

try:
    from qiskit_ibm_runtime import QiskitRuntimeService
    from qiskit_ibm_runtime.utils.json import RuntimeEncoder
except ImportError:
    sys.exit(
        "qiskit-ibm-runtime is required: pip install qiskit-ibm-runtime"
    )

# Must stay in sync with KNOWN_JOBS in parse_ibm_json.py.
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

RESULTS_DIR = os.path.join("data", "results")
CALIBRATION_DIR = os.path.join("data", "calibration")


def build_info(job) -> dict:
    """
    Assemble the job-<id>-info.json payload with every field
    parse_ibm_json.py:extract_info() reads.
    """
    metrics = {}
    try:
        metrics = job.metrics() or {}
    except Exception:
        pass

    created = ""
    if getattr(job, "creation_date", None):
        created = job.creation_date.isoformat()

    status = job.status()
    status = getattr(status, "value", str(status))

    # job.inputs holds the primitive parameters (pubs, shots, ...);
    # RuntimeEncoder round-trip makes them plain JSON.
    params = {}
    try:
        params = json.loads(json.dumps(job.inputs, cls=RuntimeEncoder))
    except Exception:
        pass

    usage = metrics.get("usage", {}) if isinstance(metrics, dict) else {}

    return {
        "id": job.job_id(),
        "status": status,
        "backend": job.backend().name if job.backend() else "MISSING",
        "created": created,
        "user_id": metrics.get("user_id", "MISSING"),
        "cost": usage.get("quantum_seconds", metrics.get("cost", "MISSING")),
        "estimated_running_time_seconds": metrics.get(
            "estimated_running_time_seconds",
            usage.get("seconds", "MISSING"),
        ),
        "program": {"id": getattr(job, "primitive_id", "sampler")},
        "params": params,
    }


def fetch_job(service: QiskitRuntimeService, job_id: str) -> bool:
    """Fetch one job's info + result and write both JSON files."""
    try:
        job = service.job(job_id)
    except Exception as exc:
        print(f"  FAIL  {job_id}  (not retrievable: {exc})")
        return False

    info_path = os.path.join(RESULTS_DIR, f"job-{job_id}-info.json")
    result_path = os.path.join(RESULTS_DIR, f"job-{job_id}-result.json")

    with open(info_path, "w") as f:
        json.dump(build_info(job), f, indent=2)

    try:
        result = job.result()
    except Exception as exc:
        print(f"  FAIL  {job_id}  (result not retrievable: {exc})")
        return False

    with open(result_path, "w") as f:
        json.dump(result, f, cls=RuntimeEncoder, indent=2)

    print(f"  OK    {job_id}  → {info_path}, {result_path}")
    return True


def fetch_calibration(service: QiskitRuntimeService) -> None:
    """
    Export calibration snapshots for the backends used by the dataset,
    as close as possible to the experiment date (2026-01-27).
    """
    from datetime import datetime

    os.makedirs(CALIBRATION_DIR, exist_ok=True)
    when = datetime(2026, 1, 27, 15, 0, 0)

    for backend_name in ("ibm_fez", "ibm_torino"):
        try:
            backend = service.backend(backend_name)
            props = backend.properties(datetime=when)
            out = os.path.join(
                CALIBRATION_DIR, f"{backend_name}-2026-01-27.json"
            )
            with open(out, "w") as f:
                json.dump(props.to_dict(), f, default=str, indent=2)
            print(f"  OK    calibration {backend_name} → {out}")
        except Exception as exc:
            print(f"  FAIL  calibration {backend_name}  ({exc})")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch raw IBM Quantum job JSONs for the verified dataset."
    )
    parser.add_argument("--job", default=None, help="Fetch a single job ID")
    parser.add_argument("--calibration", action="store_true",
                        help="Also export backend calibration snapshots")
    args = parser.parse_args()

    os.makedirs(RESULTS_DIR, exist_ok=True)
    service = QiskitRuntimeService()

    jobs = [args.job] if args.job else KNOWN_JOBS
    ok = sum(fetch_job(service, job_id) for job_id in jobs)
    print(f"\nFetched {ok}/{len(jobs)} jobs into {RESULTS_DIR}/")

    if args.calibration:
        fetch_calibration(service)

    if ok == len(jobs):
        print("Next: python parse_ibm_json.py --results_dir data/results "
              "--output data/quantum_results_verified.csv")


if __name__ == "__main__":
    main()
