"""
Pure-classical physics functions (no quantum hardware required).
Functions: 3 atomic_clock, 4 pqc, 5 tunneling, 7 zeno,
           10 harmonic_oscillator, 11 hydrogen, 14 uncertainty.
Uses NIST CODATA 2022 constants only.
"""

from __future__ import annotations
from typing import Any, Dict
import math
import numpy as np
from scipy import special

from .constants import (
    H_PLANCK,
    HBAR,
    C_LIGHT,
    E_ELEMENTARY,
    M_ELECTRON,
    M_PROTON,
    M_NEUTRON,
    RYDBERG_ENERGY,
    BOHR_RADIUS,
)

# ============================================================================
# FUNCTION 3 — Atomic Clock Comparison
# ============================================================================

_CLOCK_SPECS = {
    "Cs133": {
        "frequency_hz": 9_192_631_770,  # exact SI definition
        "fractional_uncertainty": 1e-14,
        "name": "Cesium-133",
    },
    "Sr87": {
        "frequency_hz": 429_228_004_229_873.7,
        "fractional_uncertainty": 2e-18,
        "name": "Strontium-87",
    },
    "Yb171": {
        "frequency_hz": 518_295_881_394_505.77,
        "fractional_uncertainty": 1e-18,
        "name": "Ytterbium-171",
    },
    "H_maser": {
        "frequency_hz": 1_420_405_751.768,
        "fractional_uncertainty": 1e-12,
        "name": "Hydrogen Maser",
    },
}


def atomic_clock_comparison(
    clock_type_1: str,
    clock_type_2: str,
    measurement_duration_s: float = 1.0,
) -> Dict[str, Any]:
    """Function 3: Compare two atomic clocks; return timing drift."""
    for k in (clock_type_1, clock_type_2):
        if k not in _CLOCK_SPECS:
            raise ValueError(f"Unknown clock '{k}'. Options: {list(_CLOCK_SPECS)}")

    s1, s2 = _CLOCK_SPECS[clock_type_1], _CLOCK_SPECS[clock_type_2]

    combined_frac = math.sqrt(
        s1["fractional_uncertainty"] ** 2 + s2["fractional_uncertainty"] ** 2
    )

    # Allan deviation drift over measurement_duration_s (simple model)
    drift_per_day_s = (
        combined_frac
        * s1["frequency_hz"]
        * math.sqrt(measurement_duration_s)
        * 86_400
        / s1["frequency_hz"]
    )
    drift_per_day_ns = drift_per_day_s * 1e9
    time_to_1ns = (1e-9 / drift_per_day_s) if drift_per_day_s > 0 else float("inf")

    interpretation = (
        f"Atomic Clock Comparison: {s1['name']} vs {s2['name']}. "
        f"Combined fractional uncertainty: {combined_frac:.3e}. "
        f"Drift per day: {drift_per_day_ns:.3f} ns. "
        f"Time to 1 ns drift: {time_to_1ns:.1f} days."
    )

    return {
        "clock_1": clock_type_1,
        "clock_2": clock_type_2,
        "freq_1_hz": s1["frequency_hz"],
        "freq_2_hz": s2["frequency_hz"],
        "fractional_uncertainty": float(combined_frac),
        "drift_per_day_ns": float(drift_per_day_ns),
        "time_to_1ns_drift_days": float(time_to_1ns),
        "interpretation": interpretation,
    }


# ============================================================================
# FUNCTION 4 — NIST PQC Key Sizes (FIPS 203/204/205)
# ============================================================================

_PQC = {
    "ML-KEM": {
        "standard": "FIPS 203",
        "type": "Key Encapsulation",
        2: {"pk": 800, "sk": 1632, "ct_or_sig": 768, "q_bits": 128},
        3: {"pk": 1184, "sk": 2400, "ct_or_sig": 1088, "q_bits": 192},
        5: {"pk": 1568, "sk": 3168, "ct_or_sig": 1568, "q_bits": 256},
    },
    "ML-DSA": {
        "standard": "FIPS 204",
        "type": "Digital Signature",
        2: {"pk": 1312, "sk": 2544, "ct_or_sig": 2420, "q_bits": 128},
        3: {"pk": 1952, "sk": 4000, "ct_or_sig": 3293, "q_bits": 192},
        5: {"pk": 2592, "sk": 5216, "ct_or_sig": 4595, "q_bits": 256},
    },
    "SLH-DSA": {
        "standard": "FIPS 205",
        "type": "Hash-Based Signature",
        2: {"pk": 32, "sk": 64, "ct_or_sig": 7856, "q_bits": 128},
        3: {"pk": 48, "sk": 96, "ct_or_sig": 17088, "q_bits": 192},
        5: {"pk": 64, "sk": 128, "ct_or_sig": 29792, "q_bits": 256},
    },
}


def nist_pqc_key_sizes(
    algorithm: str = "ML-KEM",
    security_level: int = 3,
) -> Dict[str, Any]:
    """Function 4: FIPS-standard PQC key/signature sizes."""
    if algorithm not in _PQC:
        raise ValueError(f"Algorithms: {list(_PQC)}")
    if security_level not in (2, 3, 5):
        raise ValueError("Security level must be 2, 3, or 5")

    spec = _PQC[algorithm]
    p = spec[security_level]

    interpretation = (
        f"{algorithm} ({spec['standard']}, level {security_level}): "
        f"pk={p['pk']} B, sk={p['sk']} B, ct/sig={p['ct_or_sig']} B. "
        f"Quantum security: {p['q_bits']} bits. "
        f"Resistant to Shor's and Grover's algorithms."
    )

    return {
        "algorithm": algorithm,
        "nist_standard": spec["standard"],
        "security_level": security_level,
        "public_key_bytes": p["pk"],
        "private_key_bytes": p["sk"],
        "ciphertext_or_sig_bytes": p["ct_or_sig"],
        "quantum_security_bits": p["q_bits"],
        "interpretation": interpretation,
    }


# ============================================================================
# FUNCTION 5 — WKB Tunneling Probability
# ============================================================================


def wkb_tunneling(
    barrier_height_eV: float,
    particle_energy_eV: float,
    barrier_width_nm: float,
    particle_mass_kg: float = M_ELECTRON,
) -> Dict[str, Any]:
    """Function 5: WKB T ≈ exp(−2κL), κ = √(2m(V−E))/ℏ."""
    V = barrier_height_eV * E_ELEMENTARY
    E = particle_energy_eV * E_ELEMENTARY
    L = barrier_width_nm * 1e-9

    if E >= V:
        return {
            "T_probability": 1.0,
            "log10_T": 0.0,
            "physical_regime": "above_barrier",
            "interpretation": f"E={particle_energy_eV} eV ≥ V={barrier_height_eV} eV → classical transmission.",
        }

    kappa = math.sqrt(2 * particle_mass_kg * (V - E)) / HBAR
    T = math.exp(-2 * kappa * L)
    log10 = math.log10(T) if T > 0 else float("-inf")

    interpretation = (
        f"WKB Tunneling: V={barrier_height_eV} eV, E={particle_energy_eV} eV, "
        f"L={barrier_width_nm} nm. "
        f"κ = {kappa:.3e} m⁻¹. T = {T:.3e} (log₁₀T = {log10:.1f}). "
        f"Applications: STM, alpha decay, tunnel diodes."
    )

    return {
        "barrier_height_eV": barrier_height_eV,
        "particle_energy_eV": particle_energy_eV,
        "barrier_width_nm": barrier_width_nm,
        "kappa_per_m": float(kappa),
        "T_probability": float(T),
        "log10_T": float(log10),
        "physical_regime": "classically_forbidden",
        "interpretation": interpretation,
    }


# ============================================================================
# FUNCTION 7 — Quantum Zeno Effect
# ============================================================================


def quantum_zeno_effect(
    n_measurements: int,
    total_time_s: float,
    omega_rabi: float = 1e6,
) -> Dict[str, Any]:
    """Function 7: Frequent measurements suppress Rabi oscillation."""
    tau = total_time_s / (n_measurements + 1)

    # Rabi oscillation P(t) = sin²(ω·t/2)
    t_final = total_time_s
    survival_no_meas = 1.0 - math.sin(omega_rabi * t_final / 2) ** 2

    # With measurement: (1 − sin²(ω·τ/2))^N
    survival_per = 1.0 - math.sin(omega_rabi * tau / 2) ** 2
    survival_meas = survival_per**n_measurements

    suppression = survival_meas / survival_no_meas if survival_no_meas > 0 else 1.0

    interpretation = (
        f"Quantum Zeno (ω={omega_rabi:.2e} rad/s, T={total_time_s:.2e} s, "
        f"N={n_measurements} meas). "
        f"Without meas: P_survival={survival_no_meas:.6f}. "
        f"With meas: P_survival={survival_meas:.6f}. "
        f"Suppression factor: {suppression:.3f}. "
        f"Observed in atom traps, cavity QED, superconducting qubits."
    )

    return {
        "n_measurements": n_measurements,
        "total_time_s": total_time_s,
        "omega_rabi": omega_rabi,
        "measurement_interval_s": float(tau),
        "survival_prob_no_measurement": float(survival_no_meas),
        "survival_prob_with_measurement": float(survival_meas),
        "zeno_suppression_factor": float(suppression),
        "interpretation": interpretation,
    }


# ============================================================================
# FUNCTION 10 — Quantum Harmonic Oscillator
# ============================================================================


def quantum_harmonic_oscillator(
    n_level: int,
    x_range_nm: float = 2.0,
    n_points: int = 500,
    omega_hz: float = 1e14,
) -> Dict[str, Any]:
    """Function 10: QHO wavefunction ψ_n, energy E_n = ℏω(n+½)."""
    omega = 2 * math.pi * omega_hz
    x_m = np.linspace(-x_range_nm * 1e-9, x_range_nm * 1e-9, n_points)
    x0 = math.sqrt(HBAR / (M_ELECTRON * omega))  # characteristic length
    xi = x_m / x0

    Hn = special.hermite(n_level)
    norm = (M_ELECTRON * omega / (math.pi * HBAR)) ** 0.25 / math.sqrt(
        2**n_level * math.factorial(n_level)
    )
    psi = norm * Hn(xi) * np.exp(-M_ELECTRON * omega * x_m**2 / (2 * HBAR))
    prob = psi**2

    energy_j = HBAR * omega * (n_level + 0.5)
    energy_eV = energy_j / E_ELEMENTARY
    zpe_eV = (HBAR * omega / 2) / E_ELEMENTARY

    dx = x_m[1] - x_m[0]
    exp_x = float(np.sum(x_m * prob) * dx)
    exp_x2 = float(np.sum(x_m**2 * prob) * dx)
    unc_x_nm = float(math.sqrt(exp_x2 - exp_x**2) * 1e9)

    interpretation = (
        f"QHO (n={n_level}): ω={omega_hz:.3e} Hz. "
        f"E_{n_level} = {energy_eV:.6f} eV. ZPE = {zpe_eV:.6f} eV. "
        f"Δx = {unc_x_nm:.6f} nm."
    )

    return {
        "n_level": n_level,
        "energy_eV": float(energy_eV),
        "zero_point_energy_eV": float(zpe_eV),
        "uncertainty_x_nm": unc_x_nm,
        "x_array_nm": (x_m * 1e9).tolist(),
        "prob_density": prob.tolist(),
        "interpretation": interpretation,
    }


# ============================================================================
# FUNCTION 11 — Hydrogen Atom Spectrum
# ============================================================================

_SERIES = {
    1: "Lyman",
    2: "Balmer",
    3: "Paschen",
    4: "Brackett",
    5: "Pfund",
    6: "Humphreys",
}


def hydrogen_atom_spectrum(n_initial: int, n_final: int) -> Dict[str, Any]:
    """Function 11: Rydberg formula λ = hc/|ΔE|."""
    if n_initial <= 0 or n_final <= 0:
        raise ValueError("Quantum numbers must be positive integers")
    if n_initial == n_final:
        raise ValueError("n_initial ≠ n_final")

    E_i = -RYDBERG_ENERGY / n_initial**2  # eV
    E_f = -RYDBERG_ENERGY / n_final**2
    dE = E_f - E_i  # eV (negative for emission)
    dE_J = abs(dE) * E_ELEMENTARY

    lam_m = H_PLANCK * C_LIGHT / dE_J
    lam_nm = lam_m * 1e9
    freq_hz = C_LIGHT / lam_m

    n_lower = min(n_initial, n_final)
    series = _SERIES.get(n_lower, f"n={n_lower}")

    if lam_nm < 10:
        region = "X-ray"
    elif lam_nm < 400:
        region = "UV"
    elif lam_nm <= 700:
        region = "Visible"
    elif lam_nm < 1e6:
        region = "IR"
    else:
        region = "Radio"

    interpretation = (
        f"H spectrum {n_initial}→{n_final}: ΔE={dE:.4f} eV, "
        f"λ={lam_nm:.2f} nm ({region}), series={series}."
    )

    return {
        "n_initial": n_initial,
        "n_final": n_final,
        "E_initial_eV": float(E_i),
        "E_final_eV": float(E_f),
        "delta_E_eV": float(dE),
        "wavelength_nm": float(lam_nm),
        "frequency_hz": float(freq_hz),
        "spectral_series": series,
        "em_region": region,
        "interpretation": interpretation,
    }


# ============================================================================
# FUNCTION 14 — Heisenberg Uncertainty Principle
# ============================================================================

_MASSES = {"electron": M_ELECTRON, "proton": M_PROTON, "neutron": M_NEUTRON}


def heisenberg_uncertainty(
    particle: str = "electron",
    position_uncertainty_nm: float = 0.1,
) -> Dict[str, Any]:
    """Function 14: Δx·Δp ≥ ℏ/2 → minimum E_k."""
    if particle not in _MASSES:
        raise ValueError(f"Particles: {list(_MASSES)}")

    mass = _MASSES[particle]
    dx_m = position_uncertainty_nm * 1e-9
    dp = HBAR / (2 * dx_m)
    dp_eVc = dp * C_LIGHT / E_ELEMENTARY
    Ek_J = dp**2 / (2 * mass)
    Ek_eV = Ek_J / E_ELEMENTARY
    ldb_nm = (H_PLANCK / dp) * 1e9
    bohr_nm = BOHR_RADIUS * 1e9

    interpretation = (
        f"Heisenberg: {particle} confined to Δx={position_uncertainty_nm} nm. "
        f"Δp={dp:.3e} kg·m/s. E_k_min={Ek_eV:.4f} eV. "
        f"λ_dB={ldb_nm:.4f} nm. "
        f"Ratio to Bohr radius: {position_uncertainty_nm/bohr_nm:.3f}. "
        f"Explains why electrons don't spiral into nucleus."
    )

    return {
        "particle": particle,
        "delta_x_nm": float(position_uncertainty_nm),
        "delta_p_kg_ms": float(dp),
        "delta_p_eV_c": float(dp_eVc),
        "min_kinetic_energy_eV": float(Ek_eV),
        "de_broglie_wavelength_nm": float(ldb_nm),
        "bohr_radius_nm": float(bohr_nm),
        "interpretation": interpretation,
    }
