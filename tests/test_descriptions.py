import pytest

from fractal_task_tools._descriptions import _get_function_docstring


def test_get_function_docstring():
    docstring = _get_function_docstring(
        package_name="fractal_task_tools",
        module_path="_descriptions.py",
        function_name="_get_function_docstring",
    )
    assert "Args" in docstring

    with pytest.raises(ValueError, match="is absolute"):
        docstring = _get_function_docstring(
            package_name="fractal_task_tools",
            module_path="/tmp/_descriptions.py",
            function_name="_get_function_docstring",
        )
