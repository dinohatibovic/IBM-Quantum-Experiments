import math

import pytest

import parse_ibm_json


def test_import_parse_ibm_json():
    assert parse_ibm_json is not None
    assert hasattr(parse_ibm_json, "chisquare_safe")


def test_chisquare_safe_basic_values():
    chi2, p_value = parse_ibm_json.chisquare_safe([10, 10], [10, 10])
    assert chi2 == 0.0
    assert p_value == 1.0

    chi2, p_value = parse_ibm_json.chisquare_safe([12, 8], [10, 10])
    assert math.isclose(chi2, 0.8, rel_tol=1e-12)
    assert 0.0 <= p_value <= 1.0


def test_chisquare_safe_shape_mismatch():
    with pytest.raises(ValueError):
        parse_ibm_json.chisquare_safe([1, 2, 3], [1, 2])


def test_chisquare_safe_zero_expected_with_nonzero_observed():
    chi2, p_value = parse_ibm_json.chisquare_safe([1, 0], [0, 1])
    assert math.isinf(chi2)
    assert p_value == 0.0


def test_uniformity_test_uses_safe_chisquare():
    chi2, p_value = parse_ibm_json.uniformity_test(
        counts={"00": 5, "01": 5, "10": 5, "11": 5},
        num_states=4,
        total=20,
    )
    assert chi2 == 0.0
    assert p_value == 1.0


def test_bell_fidelity_counts_expected_bell_targets():
    import math
    from parse_ibm_json import bell_fidelity

    counts = {"00": 470, "01": 20, "10": 30, "11": 480}

    assert math.isclose(bell_fidelity(counts, 1000), 0.95, rel_tol=1e-12)


def test_bell_fidelity_supports_explicit_single_target():
    import math
    from parse_ibm_json import bell_fidelity

    counts = {"00": 10, "01": 10, "10": 17, "11": 963}

    assert math.isclose(
        bell_fidelity(counts, 1000, target=("11",)),
        0.963,
        rel_tol=1e-12,
    )
