from fractal_task_tools._package_name_tools import normalize_package_name


def test_normalize_package_name():
    raw_name = "Aa-_.Aa"
    normalized_name = "aa_aa"
    assert normalize_package_name(raw_name) == normalized_name
