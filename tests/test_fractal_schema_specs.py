from typing import Literal

import pytest
from devtools import debug

from fractal_task_tools._args_schemas import create_schema_for_single_task
from fractal_task_tools._validate_fractal_schema import validate_schema


def task_function_E01(optional_bool: bool | None):
    pass


def task_function_E02(optional_enum: Literal["a", "b"] | None):
    pass


def task_function_E03(optional_enum: Literal["a", "b", None]):
    pass


def test_E01():
    schema = create_schema_for_single_task(
        task_function=task_function_E01,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    with pytest.raises(ValueError, match="E01"):
        validate_schema(schema=schema, path="")


def test_E02():
    schema = create_schema_for_single_task(
        task_function=task_function_E02,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    with pytest.raises(ValueError, match="E02"):
        validate_schema(schema=schema, path="")


def test_E03():
    schema = create_schema_for_single_task(
        task_function=task_function_E03,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    with pytest.raises(ValueError, match="E03"):
        validate_schema(schema=schema, path="")


def test_E04():
    schema = dict(definitions=123)
    with pytest.raises(ValueError, match="E04"):
        validate_schema(schema=schema, path="")
