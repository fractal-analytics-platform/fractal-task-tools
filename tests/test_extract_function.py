from devtools import debug
from fractal_task_tools._signature_constraints import _extract_function


def test_extract_function():
    fun1 = _extract_function(
        module_relative_path="_create_manifest.py",
        package_name="fractal_task_tools",
        function_name="create_manifest",
        verbose=True,
    )
    debug(fun1)
