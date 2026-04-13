from enum import Enum
from typing import Annotated
from typing import Any
from typing import ClassVar
from typing import Literal

import pytest
from devtools import debug
from pydantic import BaseModel
from pydantic import Field

from fractal_task_tools._args_schemas import create_schema_for_single_task
from fractal_task_tools._specs import validate_schema


def test_E01():
    schema = {"name": "args"}
    debug(schema)
    with pytest.raises(ValueError, match="E01"):
        validate_schema(schema=schema, path="", verbose=True)


def test_E02():
    schema = {"definitions": "mock-value"}
    debug(schema)
    with pytest.raises(ValueError, match="E02"):
        validate_schema(schema=schema, path="", verbose=True)


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
        validate_schema(schema=schema, path="", verbose=True)


def test_E04():
    def task_fun(arg_any: Any):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    with pytest.raises(ValueError, match="E04"):
        validate_schema(schema=schema, path="", verbose=True)


def test_E05():
    def task_fun_scalar(bool_with_no_default: bool):
        pass

    def task_fun_array_1(arg: list[bool]):
        pass

    def task_fun_array_2(arg: list[bool] = Field(default_factory=list)):
        pass

    def task_fun_array_3(arg: list[bool] = Field(default=[True, False])):
        pass

    for task_fun in (
        task_fun_scalar,
        task_fun_array_1,
        task_fun_array_2,
        task_fun_array_3,
    ):
        schema = create_schema_for_single_task(
            task_function=task_fun,
            executable=__file__,
            package=None,
            verbose=True,
        )
        debug(schema)
        with pytest.raises(ValueError, match="E05"):
            validate_schema(schema=schema, path="", verbose=True)


def test_E06():
    def task_fun_object_1(arg: dict[str, bool]):
        pass

    def task_fun_object_2(arg: dict[str, bool] = Field(default_factory=dict)):
        pass

    def task_fun_object_3(arg: dict[str, bool] = Field(default={"key": True})):
        pass

    for task_fun in (
        task_fun_object_1,
        task_fun_object_2,
        task_fun_object_3,
    ):
        debug(task_fun)
        schema = create_schema_for_single_task(
            task_function=task_fun,
            executable=__file__,
            package=None,
            verbose=True,
        )
        debug(schema)
        with pytest.raises(ValueError, match="E06"):
            validate_schema(schema=schema, path="", verbose=True)


def test_E07():
    def task_fun1(empty_string: str = " "):
        pass

    def task_fun2(empty_string_in_array: list[str] = ["\n"]):
        pass

    def task_fun3(empty_string_key: dict[str, str] = {"  ": "value"}):
        pass

    def task_fun4(empty_string_value: dict[str, str] = {"key": ""}):
        pass

    for task_fun in (task_fun1, task_fun2, task_fun3, task_fun4):
        schema = create_schema_for_single_task(
            task_function=task_fun,
            executable=__file__,
            package=None,
            verbose=True,
        )
        debug(schema)
        with pytest.raises(ValueError, match="E07"):
            validate_schema(schema=schema, path="", verbose=True)


def test_E10():
    def task_fun(optional_bool: bool | None = None):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    with pytest.raises(ValueError, match="E10"):
        validate_schema(schema=schema, path="", verbose=True)


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
        validate_schema(schema=schema, path="", verbose=True)


def test_E12():
    class MyEnum(Enum):
        key1 = "VALUE1"
        key2 = "VALUE2"

    def task_fun(optional_enum: MyEnum | None):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    with pytest.raises(ValueError, match="E12"):
        validate_schema(
            schema=schema,
            path="",
            verbose=True,
            root_schema=schema,
        )


def test_E13():
    def task_fun0(x: int | None):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun0,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    validate_schema(schema=schema, path="", verbose=True)

    def task_fun1(x: int | str | float):
        pass

    def task_fun2(x: int | str | None):
        pass

    def task_fun3(x: int | float):
        pass

    def task_fun4(x: bool | float = True):
        pass

    for task_fun in [task_fun1, task_fun2, task_fun3, task_fun4]:
        schema = create_schema_for_single_task(
            task_function=task_fun,
            executable=__file__,
            package=None,
            verbose=True,
        )
        debug(schema)
        with pytest.raises(ValueError, match="E13"):
            validate_schema(schema=schema, path="", verbose=True)

    # Redundant unions are handled correctly
    def task_fun5(x: int | int | int):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun5,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    validate_schema(schema=schema, path="", verbose=True)


def test_anyof_edge_cases():
    schema_E12 = {
        "$defs": {
            "MyEnum1": {"enum": ["1a", "1b"], "type": "string"},
            "MyEnum2": {"enum": ["2a", "2b"], "type": "string"},
        },
        "properties": {
            "optional_enum": {
                "anyOf": [
                    {"$ref": "#/$defs/MyEnum1"},
                    {"$ref": "#/$defs/MyEnum2"},
                    {"type": "null"},
                ]
            }
        },
        "type": "object",
    }
    debug(schema_E12)
    with pytest.raises(ValueError, match="E12"):
        validate_schema(
            schema=schema_E12,
            path="",
            verbose=True,
            root_schema=schema_E12,
        )

    schema_E14 = {
        "$defs": {
            "MyEnum1": {"enum": ["1a", "1b"], "type": "string"},
            "MyEnum2": {"enum": ["2a", "2b"], "type": "string"},
        },
        "properties": {
            "optional_enum": {
                "anyOf": [
                    {"$ref": "#/$defs/MyEnum1"},
                    {"$ref": "#/$defs/MyEnum2"},
                ]
            }
        },
        "type": "object",
    }
    debug(schema_E14)
    with pytest.raises(ValueError, match="E14"):
        validate_schema(
            schema=schema_E14,
            path="",
            verbose=True,
            root_schema=schema_E14,
        )


def test_E15():
    schema = {
        "properties": {
            "optional_enum": {
                "anyOf": [{"type": "fake1"}, {"type": "fake2"}, {"type": "fake3"}]
            }
        },
        "type": "object",
    }
    debug(schema)
    with pytest.raises(ValueError, match="E15"):
        validate_schema(
            schema=schema,
            path="",
            verbose=True,
            root_schema=schema,
        )


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
        validate_schema(schema=schema, path="", verbose=True)


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
        validate_schema(schema=schema, path="", verbose=True)


def test_non_homogeneous_tuple():
    def task_fun(x: tuple[int, str]):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    validate_schema(schema=schema, path="", verbose=True)


def test_E08():
    def task_fun1(x: tuple[int, bool]):
        pass

    def task_fun2(x: tuple[bool]):
        pass

    for task_fun in (task_fun1, task_fun2):
        schema = create_schema_for_single_task(
            task_function=task_fun,
            executable=__file__,
            package=None,
            verbose=True,
        )
        debug(schema)
        with pytest.raises(ValueError, match="E08"):
            validate_schema(schema=schema, path="", verbose=True)


def test_E14():
    class MyModel1(BaseModel):
        x: int

    class MyModel2(BaseModel):
        y: int

    def task_fun(x: MyModel1 | MyModel2):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    with pytest.raises(ValueError, match="E14"):
        validate_schema(schema=schema, path="", verbose=True)


def test_E12_internal_errors():
    schema_nullable_enum = {
        "$defs": {"MyEnum": {"enum": ["VALUE1", "VALUE2"], "type": "string"}},
        "properties": {
            "optional_enum": {"anyOf": [{"$ref": "#/$defs/MyEnum"}, {"type": "null"}]}
        },
        "type": "object",
    }

    with pytest.raises(ValueError, match="E12"):
        validate_schema(
            schema=schema_nullable_enum,
            path="",
            verbose=True,
            root_schema=schema_nullable_enum,
        )

    # Root_schema not set
    with pytest.raises(RuntimeError, match="[I90]") as ei:
        validate_schema(
            schema=schema_nullable_enum,
            path="",
            verbose=True,
        )
    debug(ei.value)

    # Cannot parse "$ref": "INVALID/$defs/MyEnum"
    schema_invalid_ref = {
        "$defs": {"MyEnum": {"enum": ["VALUE1", "VALUE2"], "type": "string"}},
        "properties": {
            "optional_enum": {
                "anyOf": [{"$ref": "INVALID/$defs/MyEnum"}, {"type": "null"}]
            }
        },
        "type": "object",
    }
    with pytest.raises(RuntimeError, match="[I91]") as ei:
        validate_schema(
            schema=schema_invalid_ref,
            path="",
            verbose=True,
            root_schema=schema_invalid_ref,
        )
    debug(ei.value)

    # Missing "$defs"
    schema_invalid_ref = {
        "properties": {
            "optional_enum": {"anyOf": [{"$ref": "#/$defs/MyEnum"}, {"type": "null"}]}
        },
        "type": "object",
    }
    with pytest.raises(RuntimeError, match="[I92]") as ei:
        validate_schema(
            schema=schema_invalid_ref,
            path="",
            verbose=True,
            root_schema=schema_invalid_ref,
        )
    debug(ei.value)

    # Cannot find "$ref in "$defs"
    schema_invalid_ref = {
        "$defs": {"MyEnum": {"enum": ["VALUE1", "VALUE2"], "type": "string"}},
        "properties": {
            "optional_enum": {
                "anyOf": [{"$ref": "#/$defs/WRONG-NAME"}, {"type": "null"}]
            }
        },
        "type": "object",
    }
    with pytest.raises(RuntimeError, match="[I92]") as ei:
        validate_schema(
            schema=schema_invalid_ref,
            path="",
            verbose=True,
            root_schema=schema_invalid_ref,
        )
    debug(ei.value)


def test_tagged_union():
    class MyModel1(BaseModel):
        label: Literal["label1"] = "label1"
        x1: int

    class MyModel2(BaseModel):
        label: Literal["label2"] = "label2"
        x2: int

    class MyModel3(BaseModel):
        label: Literal["label3"] = "label3"
        x3: int

    TaggedUnion = Annotated[
        MyModel1 | MyModel2 | MyModel3,
        Field(discriminator="label"),
    ]

    def task_fun(x: TaggedUnion):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    validate_schema(schema=schema, path="", verbose=True)


def test_classvar():
    class MyModel(BaseModel):
        label: Literal["label-value"] = "label-value"
        property1: ClassVar[bool] = True
        property2: ClassVar[int]

    def task_fun(arg: MyModel):
        pass

    schema = create_schema_for_single_task(
        task_function=task_fun,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    validate_schema(schema=schema, path="", verbose=True)
    mymodel_properties = schema["$defs"]["MyModel"]["properties"]
    assert "label" in mymodel_properties
    assert "property1" not in mymodel_properties
    assert "property2" not in mymodel_properties
