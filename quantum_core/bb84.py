"""
BB84 Quantum Key Distribution Protocol
Functions 1 (key generation, no Eve) and 13 (full protocol with optional Eve).
"""

from __future__ import annotations
from typing import Any, Dict
import numpy as np


def _binary_entropy(p: float) -> float:
    """Shannon binary entropy h(p) = -p log2(p) - (1-p) log2(1-p)."""
    if p <= 0 or p >= 1:
        return 0.0
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)


# ============================================================================
# FUNCTION 1 — BB84 Key Generation (no eavesdropper)
# ============================================================================


def bb84_key_generation(n_bits: int = 256) -> Dict[str, Any]:
    """
    Ideal BB84 protocol: Alice → Bob, no eavesdropper.

    Parameters
    ----------
    n_bits : qubits Alice prepares

    Returns
    -------
    dict with sifted_key_length, qber, secure_key_rate, interpretation
    """
    rng = np.random.default_rng(seed=42)

    alice_bits = rng.integers(0, 2, n_bits)
    alice_bases = rng.integers(0, 2, n_bits)  # 0=Z, 1=X
    bob_bases = rng.integers(0, 2, n_bits)

    # Bob measures; perfect channel when bases match
    bob_bits = np.where(
        bob_bases == alice_bases,
        alice_bits,
        rng.integers(0, 2, n_bits),
    )

    # Sifting
    match = alice_bases == bob_bases
    sifted_alice = alice_bits[match]
    sifted_bob = bob_bits[match]
    sifted_length = int(match.sum())

    errors = int((sifted_alice != sifted_bob).sum())
    qber = errors / sifted_length if sifted_length else 0.0

    secure_key_rate = (1.0 - _binary_entropy(qber)) * sifted_length / n_bits

    interpretation = (
        f"BB84 (no Eve): Alice sent {n_bits} qubits. "
        f"After basis sifting: {sifted_length} bits kept (~50%). "
        f"QBER = {qber:.6f} (ideal ≈ 0; eavesdropping threshold > 0.11). "
        f"Secure key rate = {secure_key_rate:.4f}. "
        f"Quantum no-cloning theorem guarantees eavesdropping is detectable."
    )

    return {
        "raw_key_length": n_bits,
        "sifted_key_length": sifted_length,
        "qber": float(qber),
        "secure_key_rate": float(secure_key_rate),
        "interpretation": interpretation,
    }


# ============================================================================
# FUNCTION 13 — BB84 Full Protocol with Optional Eve
# ============================================================================


def bb84_full_protocol(
    n_bits: int = 256,
    eve_present: bool = False,
) -> Dict[str, Any]:
    """
    Full BB84 with optional intercept-resend eavesdropper (Eve).

    Eve introduces ~25% QBER when present; threshold 0.11 detects her.

    Parameters
    ----------
    n_bits       : qubits Alice prepares
    eve_present  : whether Eve eavesdrops

    Returns
    -------
    dict with sifted_length, qber, eve_detected, secure_key_length,
    interpretation
    """
    rng = np.random.default_rng(seed=42)

    alice_bits = rng.integers(0, 2, n_bits)
    alice_bases = rng.integers(0, 2, n_bits)

    # Eve intercepts (intercept-resend attack)
    if eve_present:
        eve_bases = rng.integers(0, 2, n_bits)
        eve_bits = np.where(
            eve_bases == alice_bases,
            alice_bits,
            rng.integers(0, 2, n_bits),
        )
        transmitted = eve_bits  # Eve resends what she measured
    else:
        transmitted = alice_bits  # Ideal channel

    # Bob
    bob_bases = rng.integers(0, 2, n_bits)
    bob_bits = np.where(
        bob_bases == alice_bases,
        transmitted,
        rng.integers(0, 2, n_bits),
    )

    # Sifting (Alice–Bob basis match)
    match = alice_bases == bob_bases
    sifted_alice = alice_bits[match]
    sifted_bob = bob_bits[match]
    sifted_length = int(match.sum())

    errors = int((sifted_alice != sifted_bob).sum())
    qber = errors / sifted_length if sifted_length else 0.0

    eve_detected = qber > 0.11

    h = _binary_entropy(qber)
    secure_key_length = 0 if eve_detected else int(sifted_length * (1.0 - h))

    interpretation = (
        f"BB84 (Eve {'present' if eve_present else 'absent'}): "
        f"{n_bits} qubits → {sifted_length} sifted bits. "
        f"QBER = {qber:.6f}. "
        f"Eve detected = {eve_detected} (threshold 0.11). "
        f"Secure key = {secure_key_length} bits. "
        f"When Eve intercepts with random basis she has 50% chance of "
        f"choosing wrong basis, introducing ~25% errors in sifted key."
    )

    return {
        "n_bits": n_bits,
        "eve_present": eve_present,
        "sifted_length": sifted_length,
        "qber": float(qber),
        "eve_detected": bool(eve_detected),
        "secure_key_length": secure_key_length,
        "interpretation": interpretation,
    }
