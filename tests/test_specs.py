from typing import Literal

import pytest
from devtools import debug

from fractal_task_tools._args_schemas import create_schema_for_single_task
from fractal_task_tools._specs import validate_schema


def test_E01():
    schema = {"name": "args"}
    debug(schema)
    with pytest.raises(ValueError, match="E01"):
        validate_schema(schema=schema, path="")


def test_E02():
    schema = {"definitions": "mock-value"}
    debug(schema)
    with pytest.raises(ValueError, match="E02"):
        validate_schema(schema=schema, path="")


def test_E03():
    def task_fun(non_homogeneous_enum: Literal["a", 1]):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    with pytest.raises(ValueError, match="E03"):
        validate_schema(schema=schema, path="")


def test_E10():
    def task_fun(optional_bool: bool | None):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    with pytest.raises(ValueError, match="E10"):
        validate_schema(schema=schema, path="")


def test_E11():
    def task_fun(optional_enum: Literal["a", "b"] | None):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    with pytest.raises(ValueError, match="E11"):
        validate_schema(schema=schema, path="")


def test_E12():
    def task_fun0(x: int | None):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun0,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    validate_schema(schema=schema, path="")

    def task_fun1(x: int | str | float):
        pass

    def task_fun2(x: int | str | None):
        pass

    def task_fun3(x: int | float):
        pass

    def task_fun4(x: bool | float):
        pass

    for task_fun in [task_fun1, task_fun2, task_fun3, task_fun4]:
        schema = create_schema_for_single_task(
            task_function=task_fun,
            executable=__file__,
            package=None,
            verbose=True,
        )
        debug(schema)
        with pytest.raises(ValueError, match="E12"):
            validate_schema(schema=schema, path="")


def test_E20():
    """
    Note: it is unclear whether this can be actually reproduced.
    """
    schema = {
        "items": {"type": "number"},
        "oneOf": [
            {"$ref": "#/$defs/Case1"},
            {"$ref": "#/$defs/Case2"},
        ],
        "type": "array",
    }

    debug(schema)
    with pytest.raises(ValueError, match="E20"):
        validate_schema(schema=schema, path="")


def test_E21():
    oneof_no_discriminator = {
        "oneOf": [
            {"$ref": "#/$defs/Case1"},
            {"$ref": "#/$defs/Case2"},
        ],
        "type": "array",
    }

    with pytest.raises(ValueError, match="E21"):
        validate_schema(schema=oneof_no_discriminator, path="")


def test_E22():
    schema = {
        "discriminator": "mock-value",
        "oneOf": [
            {"type": "number", "multipleOf": 5},
            {"type": "number", "multipleOf": 3},
        ],
    }
    debug(schema)
    with pytest.raises(ValueError, match="E22"):
        validate_schema(schema=schema, path="")


def test_E30():
    def task_fun(list_no_type: list):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    with pytest.raises(ValueError, match="E30"):
        validate_schema(schema=schema, path="")
