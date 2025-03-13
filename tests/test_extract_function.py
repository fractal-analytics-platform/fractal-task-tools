import pytest
from devtools import debug
from fractal_task_tools._signature_constraints import _extract_function


@pytest.mark.xfail(reason="FIXME: depends on fractal-tasks-core")
def test_extract_function():
    """
    This test showcases the use of `_extract_function`.
    """

    fun1 = _extract_function(
        module_relative_path="zarr_utils.py",
        package_name="fractal_tasks_core.ngff",
        function_name="load_NgffImageMeta",
        verbose=True,
    )
    debug(fun1)

    fun2 = _extract_function(
        module_relative_path="ngff.zarr_utils.py",
        package_name="fractal_tasks_core",
        function_name="load_NgffImageMeta",
        verbose=True,
    )
    debug(fun2)
