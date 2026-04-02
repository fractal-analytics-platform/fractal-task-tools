from typing import Literal

import pytest
from devtools import debug

from fractal_task_tools._args_schemas import create_schema_for_single_task
from fractal_task_tools._specs import validate_schema


def test_E01():
    def task_fun(optional_bool: bool | None):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    with pytest.raises(ValueError, match="E01"):
        validate_schema(schema=schema, path="")


def test_E02():
    def task_fun(optional_enum: Literal["a", "b"] | None):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    with pytest.raises(ValueError, match="E02"):
        validate_schema(schema=schema, path="")


def test_E03():
    def task_fun(optional_enum: Literal["a", "b", None]):
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


def test_E04():
    schema = dict(definitions=123)
    with pytest.raises(ValueError, match="E04"):
        validate_schema(schema=schema, path="")


def test_E05():
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
        with pytest.raises(ValueError, match="E05"):
            validate_schema(schema=schema, path="")


def test_E06():
    # FIXME: Is this a good example?
    oneof_no_discriminator = {
        "items": {"type": "number"},
        "oneOf": [
            {"$ref": "#/$defs/Case1"},
            {"$ref": "#/$defs/Case2"},
        ],
        "type": "array",
    }

    with pytest.raises(ValueError, match="E06"):
        validate_schema(schema=oneof_no_discriminator, path="")


def test_E07():
    oneof_primitive = {
        "oneOf": [
            {"type": "number", "multipleOf": 5},
            {"type": "number", "multipleOf": 3},
        ]
    }
    with pytest.raises(ValueError, match="E07"):
        validate_schema(schema=oneof_primitive, path="")


def test_E00():
    with pytest.raises(ValueError, match="E00"):
        validate_schema(schema={"name": "args"}, path="")
