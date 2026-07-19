"""
IBM Quantum demo — runs quantum circuit functions on REAL hardware.
Your verified backends: ibm_fez (Eagle r3, 127q), ibm_torino (Heron r1, 133q)

Prerequisites
-------------
export IBM_QUANTUM_TOKEN="your_token_here"
pip install qiskit-ibm-runtime

Usage
-----
python examples/ibm_demo.py --backend ibm_fez
python examples/ibm_demo.py --backend ibm_torino
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from quantum_core import (
    QuantumBackend,
    grover_search,
    bell_inequality_test,
    quantum_phase_estimation,
)

SEP = "=" * 70


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--backend",
        default="ibm_fez",
        choices=["ibm_fez", "ibm_torino"],
        help="IBM Quantum backend to use",
    )
    parser.add_argument("--shots", type=int, default=1000, help="Shots per circuit")
    args = parser.parse_args()

    token = os.getenv("IBM_QUANTUM_TOKEN")
    if not token:
        print("ERROR: Set IBM_QUANTUM_TOKEN environment variable first.")
        print("  export IBM_QUANTUM_TOKEN='your_token_here'")
        sys.exit(1)

    print(f"\nConnecting to IBM Quantum backend: {args.backend} ...")
    backend = QuantumBackend(mode="ibm", ibm_backend=args.backend, token=token)
    print(f"Connected. Backend: {backend.name}")

    # ── Bell Test (2 qubits — perfect for real hardware) ──────────────
    print(f"\n{SEP}")
    print("  Bell Inequality Test (CHSH) on real quantum hardware")
    print(SEP)
    r = bell_inequality_test(n_trials=args.shots, backend=backend)
    print(r["interpretation"])
    print(f"  S = {r['S_value']:.4f}  |  Bell violation: {r['bell_violation']}")

    # ── Grover Search (3 qubits) ───────────────────────────────────────
    print(f"\n{SEP}")
    print("  Grover Search (3 qubits, target=5) on real quantum hardware")
    print(SEP)
    r = grover_search(3, 5, backend=backend, shots=args.shots)
    print(r["interpretation"])
    print(f"  Success probability: {r['success_probability']:.3f}")

    # ── Quantum Phase Estimation (4 counting qubits) ───────────────────
    print(f"\n{SEP}")
    print("  QPE (φ=0.375, 4 counting qubits) on real quantum hardware")
    print(SEP)
    r = quantum_phase_estimation(0.375, 4, backend=backend, shots=args.shots)
    print(r["interpretation"])
    print(
        f"  Estimated φ: {r['estimated_phase']:.4f}  |  Error: {r['estimation_error']:.4f}"
    )

    print(f"\n{SEP}")
    print(f"  IBM Quantum job complete on {args.backend}.")
    print(SEP)


if __name__ == "__main__":
    main()
