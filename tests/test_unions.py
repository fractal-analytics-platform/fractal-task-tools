from typing import Annotated
from typing import Literal
from typing import Optional
from typing import Union

import pytest
from devtools import debug
from fractal_task_tools._signature_constraints import (
    _validate_function_signature,
)
from pydantic import BaseModel
from pydantic import Field


class Model1(BaseModel):
    label: Literal["label1"] = "label1"
    field1: int = 1


class Model2(BaseModel):
    label: Literal["label2"] = "label2"
    field2: int


class Model3(BaseModel):
    label: Literal["label3"] = "label3"
    field3: str


def fun_plain_union_valid_1(arg: Union[int, None]):
    pass


def fun_plain_union_valid_2(arg: None | int):
    pass


def fun_plain_union_valid_3(arg: None | int = None):
    pass


def fun_plain_union_valid_4(arg: Optional[int]):
    pass


def fun_plain_union_valid_5(arg: Optional[int] = None):
    pass


def fun_plain_union_valid_6(arg: tuple[int, int, int] | None = None):
    pass


def fun_plain_union_valid_7(
    arg: int | None = Field(default_factory=lambda x: 123),
):
    pass


def fun_tagged_union_valid_1(
    arg: Annotated[Model1 | Model2 | Model3, Field(discriminator="label")],
):
    pass


def fun_simple_model_valid_1(
    arg: Model1,
):
    pass


AnyModel = Annotated[Model1 | Model2 | Model3, Field(discriminator="label")]


class NestedModel(BaseModel):
    x: AnyModel


class NestedModelWithDefault(BaseModel):
    x: AnyModel = Model1()


def fun_nested_tagged_union_valid_1(arg: NestedModel):
    pass


def fun_nested_tagged_union_valid_2(arg: NestedModelWithDefault):
    pass


def fun_non_tagged_union_valid_1(arg: Annotated[int | None, "comment"]):
    pass


def fun_non_tagged_union_valid_2(arg: Annotated[int | None, "comment"] = None):
    pass


def fun_plain_union_invalid_1(arg: int | str):
    pass


def fun_plain_union_invalid_2(arg: int | None = 123):
    pass


def fun_plain_union_invalid_3(arg: Optional[int] = 456):
    pass


def fun_plain_union_invalid_4(arg: int | list[Union[int, None]]):
    pass


def fun_plain_union_invalid_5(arg: int | list[Optional[int]]):
    pass


def fun_plain_union_invalid_6(arg: int | None = Field(default=123)):
    pass


def fun_plain_union_invalid_7(arg: int | None = Field(default_factory=lambda: 123)):
    pass


def fun_non_tagged_union_invalid_1(arg: Annotated[int | str, "comment"]):
    pass


def fun_non_tagged_union_invalid_2(arg: Annotated[int | None, "comment"] = 123):
    pass


class _ModelWithInvalidDefaults(BaseModel):
    z: int | None = 7


class ModelWithInvalidDefaults1(BaseModel):
    x: _ModelWithInvalidDefaults


class ModelWithInvalidDefaults2(BaseModel):
    x: int | None = None
    y: ModelWithInvalidDefaults1


def fun_nested_model_invalid_1(arg: ModelWithInvalidDefaults1):
    pass


def fun_nested_model_invalid_2(arg: ModelWithInvalidDefaults2):
    pass


def test_validate_function_signature():
    for valid_function in (
        fun_plain_union_valid_1,
        fun_plain_union_valid_2,
        fun_plain_union_valid_3,
        fun_plain_union_valid_4,
        fun_plain_union_valid_5,
        fun_plain_union_valid_6,
        fun_plain_union_valid_7,
        fun_tagged_union_valid_1,
        fun_non_tagged_union_valid_1,
        fun_non_tagged_union_valid_2,
        fun_nested_tagged_union_valid_1,
        fun_nested_tagged_union_valid_2,
        fun_simple_model_valid_1,
    ):
        debug(valid_function)
        _validate_function_signature(function=valid_function)

    for invalid_function in (
        fun_plain_union_invalid_1,
        fun_plain_union_invalid_2,
        fun_plain_union_invalid_3,
        fun_plain_union_invalid_4,
        fun_plain_union_invalid_5,
        fun_plain_union_invalid_6,
        fun_plain_union_invalid_7,
        fun_non_tagged_union_invalid_1,
        fun_non_tagged_union_invalid_2,
        fun_nested_model_invalid_1,
        fun_nested_model_invalid_2,
    ):
        debug(invalid_function)
        with pytest.raises(ValueError) as exc_info:
            _validate_function_signature(function=invalid_function)
        debug(exc_info.value)
