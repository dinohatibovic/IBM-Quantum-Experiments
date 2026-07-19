"""
Local demo — runs all 14 functions on AerSimulator (no IBM credentials needed).
Usage: python examples/local_demo.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from quantum_core import (
    QuantumBackend,
    bb84_key_generation,
    bb84_full_protocol,
    grover_search,
    bell_inequality_test,
    quantum_phase_estimation,
    quantum_fourier_transform,
    qiskit_circuit_optimization,
    atomic_clock_comparison,
    nist_pqc_key_sizes,
    wkb_tunneling,
    quantum_zeno_effect,
    quantum_harmonic_oscillator,
    hydrogen_atom_spectrum,
    heisenberg_uncertainty,
)

LOCAL = QuantumBackend(mode="local")
SEP = "=" * 70


def run(label, fn, *args, **kwargs):
    print(f"\n{SEP}")
    print(f"  {label}")
    print(SEP)
    r = fn(*args, **kwargs)
    print(r["interpretation"])
    return r


if __name__ == "__main__":
    run("F1  BB84 Key Generation (no Eve)", bb84_key_generation, n_bits=256)

    run("F2  Grover Search (3 qubits, target=5)", grover_search, 3, 5, backend=LOCAL)

    run(
        "F3  Atomic Clock: Sr87 vs Yb171", atomic_clock_comparison, "Sr87", "Yb171", 1.0
    )

    run("F4  NIST PQC: ML-KEM level 3", nist_pqc_key_sizes, "ML-KEM", 3)

    run("F5  WKB Tunneling (V=2 eV, E=0.5 eV, L=0.3 nm)", wkb_tunneling, 2.0, 0.5, 0.3)

    run("F6  Circuit Optimization (5 qubits)", qiskit_circuit_optimization, 5)

    run("F7  Quantum Zeno Effect (10 measurements)", quantum_zeno_effect, 10, 1e-6, 1e6)

    run(
        "F8  Quantum Phase Estimation (φ=0.375, 4 qubits)",
        quantum_phase_estimation,
        0.375,
        4,
        backend=LOCAL,
    )

    run(
        "F9  Bell Inequality Test (CHSH, 1000 trials)",
        bell_inequality_test,
        1000,
        backend=LOCAL,
    )

    run("F10 Quantum Harmonic Oscillator (n=0)", quantum_harmonic_oscillator, 0)

    run("F11 Hydrogen Spectrum (3→2, H-alpha)", hydrogen_atom_spectrum, 3, 2)

    run("F12 Quantum Fourier Transform (3 qubits)", quantum_fourier_transform, 3)

    run("F13 BB84 Full Protocol (Eve present)", bb84_full_protocol, 256, True)

    run(
        "F14 Heisenberg Uncertainty (electron, Δx=0.1 nm)",
        heisenberg_uncertainty,
        "electron",
        0.1,
    )

    print(f"\n{SEP}")
    print("  All 14 functions completed successfully.")
    print(SEP)
