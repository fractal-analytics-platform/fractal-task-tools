import pytest
from fractal_task_tools._signature_constraints import _extract_function


def test_extract_function():
    for verbose in (True, False):
        function = _extract_function(
            module_relative_path="_create_manifest.py",
            package_name="fractal_task_tools",
            function_name="create_manifest",
            verbose=verbose,
        )
        assert function.__name__ == "create_manifest"

    with pytest.raises(
        ValueError,
        match="must end with '.py'",
    ):
        _extract_function(
            module_relative_path="_create_manifest",
            package_name="fractal_task_tools",
            function_name="missing_function",
            verbose=True,
        )
    with pytest.raises(
        AttributeError,
        match="has no attribute 'missing_function'",
    ):
        _extract_function(
            module_relative_path="_create_manifest.py",
            package_name="fractal_task_tools",
            function_name="missing_function",
        )

    with pytest.raises(
        ModuleNotFoundError,
        match="No module named 'fractal_task_tools.missing_module'",
    ):
        _extract_function(
            module_relative_path="missing_module.py",
            package_name="fractal_task_tools",
            function_name="missing_function",
        )
