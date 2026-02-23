from devtools import debug

from fractal_task_tools._descriptions import _get_function_args_descriptions


def test_get_function_args_descriptions():
    args_descriptions = _get_function_args_descriptions(
        package_name="fractal_task_tools",
        module_path="_signature_constraints.py",
        function_name="_extract_function",
    )
    debug(args_descriptions)
    assert args_descriptions.keys() == set(
        ("package_name", "module_relative_path", "function_name", "verbose")
    )
