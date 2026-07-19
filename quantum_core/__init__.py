"""
quantum_core — Quantum computing, NISQ, and physics utility functions.

Core exports include 14 quantum computing and quantum physics functions,
plus QuantumBackend for local simulation and IBM Quantum execution.
"""

from .backend import QuantumBackend

from .bb84 import bb84_key_generation, bb84_full_protocol
from .grover import grover_search
from .bell_test import bell_inequality_test
from .phase_estimation import quantum_phase_estimation
from .qft import quantum_fourier_transform
from .optimizer import qiskit_circuit_optimization

from .physics import (
    atomic_clock_comparison,
    nist_pqc_key_sizes,
    wkb_tunneling,
    quantum_zeno_effect,
    quantum_harmonic_oscillator,
    hydrogen_atom_spectrum,
    heisenberg_uncertainty,
)

__all__ = [
    "QuantumBackend",
    # BB84
    "bb84_key_generation",
    "bb84_full_protocol",
    # Grover
    "grover_search",
    # Bell
    "bell_inequality_test",
    # QPE
    "quantum_phase_estimation",
    # QFT
    "quantum_fourier_transform",
    # Circuit optimizer
    "qiskit_circuit_optimization",
    # Pure physics
    "atomic_clock_comparison",
    "nist_pqc_key_sizes",
    "wkb_tunneling",
    "quantum_zeno_effect",
    "quantum_harmonic_oscillator",
    "hydrogen_atom_spectrum",
    "heisenberg_uncertainty",
    # Financial utilities
    "encode_returns_to_circuit",
    "build_correlation_circuit",
    "build_portfolio_ansatz",
    "market_encoding_summary",
    "solve_portfolio_classical",
    "solve_portfolio_qaoa",
    "backtest_portfolio",
    "portfolio_qubo",
]

# Financial module
from .market_encoder import (
    encode_returns_to_circuit,
    build_correlation_circuit,
    build_portfolio_ansatz,
    market_encoding_summary,
)
from .portfolio_optimizer import (
    solve_portfolio_classical,
    solve_portfolio_qaoa,
    backtest_portfolio,
    portfolio_qubo,
)
