from typing import Annotated
from typing import Literal
from typing import Optional
from typing import Union

import pytest
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


def fun_plain_union_valid_4(arg: Optional[None]):
    pass


def fun_plain_union_valid_5(arg: Optional[None] = None):
    pass


def fun_tagged_union_valid_1(
    arg: Annotated[Model1 | Model2 | Model3, Field(discriminator="label")],
):
    pass


AnyModel = Annotated[Model1 | Model2 | Model3, Field(discriminator="label")]


class NestedModel(BaseModel):
    arg: AnyModel


class NestedModelWithDefault(BaseModel):
    arg: AnyModel = Model1()


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


def fun_non_tagged_union_invalid_1(arg: Annotated[int | str, "comment"]):
    pass


def fun_non_tagged_union_invalid_2(
    arg: Annotated[int | None, "comment"] = 123
):
    pass


def test_validate_function_signature():
    for valid_function in (
        fun_plain_union_valid_1,
        fun_plain_union_valid_2,
        fun_plain_union_valid_3,
        fun_plain_union_valid_4,
        fun_plain_union_valid_5,
        fun_tagged_union_valid_1,
        fun_non_tagged_union_valid_1,
        fun_non_tagged_union_valid_2,
        fun_nested_tagged_union_valid_1,
        fun_nested_tagged_union_valid_2,
    ):
        _validate_function_signature(function=valid_function)

    for valid_function in (
        fun_plain_union_invalid_1,
        fun_plain_union_invalid_2,
        fun_non_tagged_union_invalid_1,
        fun_non_tagged_union_invalid_2,
    ):
        with pytest.raises(ValueError):
            _validate_function_signature(function=valid_function)
