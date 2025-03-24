from pathlib import Path

import pytest
from devtools import debug
from fractal_task_tools._descriptions import _get_class_attrs_descriptions
from fractal_task_tools._descriptions import (
    _get_class_attrs_descriptions_from_file,
)
from fractal_task_tools._descriptions import _get_function_args_descriptions
from pydantic import BaseModel


class MyClass(BaseModel):
    """
    Init Args for MIP task.

    Attributes:
        arg1: Description of `arg1`.
    """

    arg1: str


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


def test_get_class_attrs_descriptions_from_file():
    attrs_descriptions = _get_class_attrs_descriptions_from_file(
        module_path=Path(__file__),
        class_name="MyClass",
    )
    debug(attrs_descriptions)
    assert attrs_descriptions == {"arg1": "Description of `arg1`."}


def test_failures():
    with pytest.raises(ValueError, match="must end with '.py'"):
        _get_class_attrs_descriptions(
            package_name="fractal_task_tools",
            module_relative_path="task_models",
            class_name="MyClass",
        )

    with pytest.raises(RuntimeError, match="Cannot find class_name"):
        _get_class_attrs_descriptions(
            package_name="fractal_task_tools",
            module_relative_path="task_models.py",
            class_name="MyClass",
        )
