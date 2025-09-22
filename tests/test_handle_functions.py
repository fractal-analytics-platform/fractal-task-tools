import typing

import pytest
from fractal_task_tools._signature_constraints import _extract_function
from fractal_task_tools._signature_constraints import (
    _validate_function_signature,
)


def test_validate_function_signature():
    def fun1(args: list[str]):
        pass

    with pytest.raises(
        ValueError,
        match="argument with name args",
    ):
        _validate_function_signature(function=fun1)

    def fun2(x: typing.Union[int, str]):
        pass

    with pytest.raises(
        ValueError,
        match="typing.Union is not supported",
    ):
        _validate_function_signature(function=fun2)

    def fun3(x: int | str):
        pass

    with pytest.raises(
        ValueError,
        match='Use of "|',
    ):
        _validate_function_signature(function=fun3)

    def fun4(x: typing.Optional[int] = 1):
        pass

    with pytest.raises(
        ValueError,
        match="Optional parameter has non-None default value",
    ):
        _validate_function_signature(function=fun4)


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
