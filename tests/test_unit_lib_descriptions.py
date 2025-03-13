import pytest
from devtools import debug
from fractal_task_tools._descriptions import _get_class_attrs_descriptions
from fractal_task_tools._descriptions import _get_function_args_descriptions


@pytest.mark.xfail(reason="FIXME: depends on fractal-tasks-core")
def test_get_function_args_descriptions():
    args_descriptions = _get_function_args_descriptions(
        package_name="fractal_tasks_core",
        module_path="dev/lib_signature_constraints.py",
        function_name="_extract_function",
    )
    debug(args_descriptions)
    assert args_descriptions.keys() == set(
        ("package_name", "module_relative_path", "function_name", "verbose")
    )


@pytest.mark.xfail(reason="FIXME: depends on fractal-tasks-core")
def test_get_class_attrs_descriptions():
    attrs_descriptions = _get_class_attrs_descriptions(
        package_name="fractal_tasks_core",
        module_relative_path="channels.py",
        class_name="ChannelInputModel",
    )
    debug(attrs_descriptions)
    assert attrs_descriptions.keys() == set(("wavelength_id", "label"))
