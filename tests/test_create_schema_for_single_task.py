import json
from enum import Enum
from typing import Optional

import pytest
from devtools import debug
from fractal_task_tools._args_schemas import create_schema_for_single_task
from pydantic import validate_call


@validate_call
def task_function(
    zarr_url: str,
    arg_1: int = 1,
):
    """
    Short description

    Long description of this beautiful task that is called `task_function` and
    actually only represents a mock task for testing.

    Args:
        arg_1: Description of arg_1.
    """


def test_create_schema_for_single_task():
    """
    This test reproduces the schema-creation scenario starting from an
    existing function, as it's done in tests.
    """
    schema = create_schema_for_single_task(
        task_function=task_function,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    target_schema = {
        "additionalProperties": False,
        "properties": {
            "zarr_url": {
                "title": "Zarr Url",
                "type": "string",
                "description": "Missing description",
            },
            "arg_1": {
                "default": 1,
                "title": "Arg 1",
                "type": "integer",
                "description": "Description of arg_1.",
            },
        },
        "required": ["zarr_url"],
        "type": "object",
        "title": "TaskFunction",
    }
    assert target_schema == schema


def test_create_schema_for_single_task_failures():
    """
    This test reproduces some invalid usage of the schema-creation function
    """
    with pytest.raises(ValueError):
        create_schema_for_single_task(
            task_function=task_function,
            executable=__file__,
            package="something",
            verbose=True,
        )
    with pytest.raises(ValueError):
        create_schema_for_single_task(
            task_function=task_function,
            executable="non_absolute/path/module.py",
            package=None,
            verbose=True,
        )
    with pytest.raises(ValueError):
        create_schema_for_single_task(
            executable="/absolute/path/cellpose_segmentation.py",
            package="fractal_tasks_core",
            verbose=True,
        )
    with pytest.raises(ValueError):
        create_schema_for_single_task(
            executable="cellpose_segmentation.py",
            package=None,
            verbose=True,
        )


class ColorA(Enum):
    RED = "this-is-red"
    GREEN = "this-is-green"


ColorB = Enum(
    "ColorB",
    {"RED": "this-is-red", "GREEN": "this-is-green"},
    type=str,
)


@validate_call
def task_function_with_enum(
    arg_A: ColorA,
    arg_B: ColorB,
):
    """
    Short task description

    Args:
        arg_A: Description of arg_A.
        arg_B: Description of arg_B.
    """
    pass


def test_enum_argument():
    """
    This test only asserts that `create_schema_for_single_task` runs
    successfully. Its goal is also to offer a quick way to experiment
    with new task arguments and play with the generated JSON Schema,
    without re-building the whole fractal-tasks-core manifest.
    """
    schema = create_schema_for_single_task(
        task_function=task_function_with_enum,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    # FIXME: Add assertion


@validate_call
def task_function_with_optional(
    arg1: str,
    arg2: Optional[str] = None,
    arg3: Optional[list[str]] = None,
):
    """
    Short task description

    Args:
        arg1: This is the argument description
        arg2: This is the argument description
        arg3: This is the argument description
    """
    pass


def test_optional_argument():
    """
    As a first implementation of the Pydantic V2 schema generation, we are not
    supporting the `anyOf` pattern for nullable attributes. This test verifies
    that the type of nullable properties is not `anyOf`, and that they are not
    required.

    Note: future versions of fractal-tasks-core may change this behavior.
    """
    schema = create_schema_for_single_task(
        task_function=validate_call(task_function_with_optional),
        executable=__file__,
        package=None,
        verbose=True,
    )
    print(json.dumps(schema, indent=2, sort_keys=True))
    print()
    assert schema["properties"]["arg2"]["type"] == "string"
    assert "arg2" not in schema["required"]
    assert schema["properties"]["arg3"]["type"] == "array"
    assert "arg3" not in schema["required"]


@validate_call
def task_function_with_tuple(arg_A: tuple[int, int] = (1, 1)):
    """
    Short task description

    Args:
        arg_A: Description of arg_A.
    """
    pass


def test_tuple_argument():
    """
    This test only asserts that `create_schema_for_single_task` runs
    successfully. Its goal is also to offer a quick way to experiment
    with new task arguments and play with the generated JSON Schema,
    without re-building the whole fractal-tasks-core manifest.
    """
    schema = create_schema_for_single_task(
        task_function=task_function_with_tuple,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    # FIXME: Add assertion
