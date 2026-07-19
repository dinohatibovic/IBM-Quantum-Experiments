"""
Verification tests — mirrors the core verification checklist.

Run:
    python -m pytest tests/ -v
"""

from quantum_core import (
    wkb_tunneling,
    hydrogen_atom_spectrum,
    quantum_harmonic_oscillator,
    heisenberg_uncertainty,
    bell_inequality_test,
    bb84_full_protocol,
    grover_search,
    QuantumBackend,
)

LOCAL = QuantumBackend(mode="local")


def test_wkb_tunneling():
    """
    T for V=2.0 eV, E=0.5 eV, L=1.0 nm should be in a deep-tunneling range.
    """
    result = wkb_tunneling(2.0, 0.5, 1.0)
    assert 1e-9 < result["T_probability"] < 1e-4, f"T = {result['T_probability']:.3e}"


def test_hydrogen_halpha():
    """
    Hydrogen H-alpha transition, n=3 -> n=2, should be approximately 656 nm.
    """
    result = hydrogen_atom_spectrum(3, 2)
    assert (
        650 < result["wavelength_nm"] < 660
    ), f"lambda = {result['wavelength_nm']:.2f} nm"


def test_qho_zero_point():
    """
    Quantum harmonic oscillator zero-point energy for n=0 must be positive.
    """
    result = quantum_harmonic_oscillator(0)
    assert result["zero_point_energy_eV"] > 0


def test_heisenberg_electron():
    """
    Electron confined to dx=0.1 nm should have minimum kinetic energy near 1 eV.
    """
    result = heisenberg_uncertainty("electron", 0.1)
    assert (
        result["min_kinetic_energy_eV"] > 0.9
    ), f"E_k = {result['min_kinetic_energy_eV']:.4f} eV"


def test_bell_chsh():
    """
    CHSH S should be close to 2*sqrt(2), with tolerance for simulator sampling.
    """
    result = bell_inequality_test(2000, backend=LOCAL)
    assert 2.5 < result["S_value"] < 2.95, f"S = {result['S_value']:.4f}"
    assert result["bell_violation"], "Bell violation not detected"


def test_bb84_eve_detection():
    """
    With Eve present, BB84 protocol should detect elevated QBER.
    """
    result = bb84_full_protocol(256, eve_present=True)
    assert result["eve_detected"], f"Eve not detected, QBER = {result['qber']:.4f}"


def test_grover_success():
    """
    Grover search with 3 qubits and target=5 should have high success probability.
    """
    result = grover_search(3, 5, backend=LOCAL, shots=2000)
    assert (
        result["success_probability"] > 0.8
    ), f"P = {result['success_probability']:.3f}"
