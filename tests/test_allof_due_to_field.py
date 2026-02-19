from enum import Enum

from devtools import debug
from pydantic import validate_call

from fractal_task_tools._args_schemas import _remove_top_level_single_element_allof
from fractal_task_tools._args_schemas import create_schema_for_single_task


class MyEnum(Enum):
    OPTION1 = "option1"


@validate_call
def task_function_with_field(arg_1: MyEnum = MyEnum.OPTION1):
    """
    Short description

    Args:
        arg_1: Description of arg_1.
    """


def test_create_schema_with_field():
    """
    When running with pydantic 2.8.2, this test verifies that
    `_remove_top_level_single_element_allof` is effective.
    """
    schema = create_schema_for_single_task(
        task_function=task_function_with_field,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    target_properties = {
        "arg_1": {
            "$ref": "#/$defs/MyEnum",
            "default": "option1",
            "title": "Arg 1",
            "description": "Description of arg_1.",
        },
    }
    assert target_properties == schema["properties"]


def test_unit_remove_top_level_single_element_allof():
    VALUE = "#/$defs/Something"
    old_schema = dict(properties=dict(arg={"allOf": [{"$ref": VALUE}]}))
    new_schema = _remove_top_level_single_element_allof(old_schema)
    debug(new_schema)
    assert new_schema == {"properties": {"arg": {"$ref": VALUE}}}
