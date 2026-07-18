import pytest


def test_import_parse_ibm_json():
    pytest.importorskip("scipy")
    import parse_ibm_json
    assert parse_ibm_json is not None
