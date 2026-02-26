import json
from enum import Enum
from typing import Optional

import pytest
from devtools import debug
from pydantic import BaseModel
from pydantic import Field
from pydantic import validate_call

from fractal_task_tools._args_schemas import create_schema_for_single_task


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
    assert schema["$defs"]["ColorA"] == {
        "enum": [
            "this-is-red",
            "this-is-green",
        ],
        "title": "ColorA",
        "type": "string",
        "description": "Missing description for ColorA.",
    }
    assert schema["$defs"]["ColorB"] == {
        "enum": [
            "this-is-red",
            "this-is-green",
        ],
        "title": "ColorB",
        "type": "string",
        "description": "Missing description for ColorB.",
    }
    assert schema["properties"] == {
        "arg_A": {
            "$ref": "#/$defs/ColorA",
            "title": "Arg A",
            "description": "Description of arg_A.",
        },
        "arg_B": {
            "$ref": "#/$defs/ColorB",
            "title": "Arg B",
            "description": "Description of arg_B.",
        },
    }


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
        task_function=task_function_with_optional,
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
    assert schema["properties"] == {
        "arg_A": {
            "default": [1, 1],
            "maxItems": 2,
            "minItems": 2,
            "prefixItems": [
                {
                    "type": "integer",
                },
                {
                    "type": "integer",
                },
            ],
            "title": "Arg A",
            "type": "array",
            "description": "Description of arg_A.",
        },
    }


@validate_call
def task_function_default_factory_top_level(
    arg_1: int = 1,
    arg_2: int = Field(default_factory=lambda: 1),
):
    """
    Short task description

    Args:
        arg_1: Description of arg_1.
        arg_2: Description of arg_2.
    """
    pass


class ModelWithFactory(BaseModel):
    attr_1: int = 1
    attr_2: int = Field(default_factory=lambda: 1)


@validate_call
def task_function_default_factory_nested(
    arg_1: ModelWithFactory = Field(default_factory=ModelWithFactory),
):
    """
    Short task description

    Args:
        arg_1: Description of arg.
    """
    pass


@validate_call
def task_function_default_factory_needs_data(
    # This factory requires data, and therefore it does not
    # produce any default value
    arg_1: int = Field(default_factory=lambda data: 123),
):
    pass


def test_default_factory():
    schema = create_schema_for_single_task(
        task_function=task_function_default_factory_top_level,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    properties = schema["properties"]
    assert properties["arg_1"]["default"] == properties["arg_2"]["default"]

    schema = create_schema_for_single_task(
        task_function=task_function_default_factory_nested,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    properties = schema["properties"]
    assert properties["arg_1"]["default"] == {"attr_1": 1, "attr_2": 1}
    nested_properties = schema["$defs"]["ModelWithFactory"]["properties"]
    assert (
        nested_properties["attr_1"]["default"] == nested_properties["attr_2"]["default"]
    )

    schema = create_schema_for_single_task(
        task_function=task_function_default_factory_needs_data,
        executable=__file__,
        package=None,
        verbose=True,
    )
    property = schema["properties"]["arg_1"]
    assert "default" not in property.keys()


@validate_call
def task_function_with_description(
    *,
    arg1: str = Field(description="Field-based description 1"),
    arg2: str,
):
    """
    Short task description

    Args:
        arg1: Docstring-based description 1
        arg2: Docstring-based description 2
    """
    pass


def test_descriptions():
    schema = create_schema_for_single_task(
        task_function=task_function_with_description,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    assert schema["properties"]["arg1"]["description"] == "Field-based description 1"
    assert (
        schema["properties"]["arg2"]["description"] == "Docstring-based description 2"
    )


class ModelWithDefaultNone(BaseModel):
    x: str | None = None
    y: str | None = Field(default=None)


@validate_call
def task_function_with_default_none(
    *,
    arg1: str | None = None,
    arg2: str | None = Field(default=None),
    arg3: ModelWithDefaultNone,
    arg4: str | None = Field(description="something"),
):
    pass


def test_default_none():
    schema = create_schema_for_single_task(
        task_function=task_function_with_default_none,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    assert "default" not in json.dumps(schema)
