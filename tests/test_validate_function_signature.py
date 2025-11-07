import typing
from typing import Optional
from typing import Union

import pytest
from fractal_task_tools._signature_constraints import (
    _validate_function_signature,
)


def get_valid_functions() -> list[callable]:
    def valid0(x1_str: str, x2_int: int):
        pass

    def valid1(x1_optional_str: typing.Optional[str]):
        pass

    def valid2(x1_optional_str: typing.Optional[str] = None):
        pass

    def valid3(x1_optional_str: Optional[str]):
        pass

    def valid4(x1_optional_str: Optional[str] = None):
        pass

    def valid5(x1_optional_str: str | None):
        pass

    def valid6(x1_optional_str: str | None = None):
        pass

    def valid7(x1_optional_str: None | str):
        pass

    def valid8(x1_optional_str: None | str = None):
        pass

    def valid9(x1_int_or_int: int | int):
        pass

    return (
        valid0,
        valid1,
        valid2,
        valid3,
        valid4,
        valid5,
        valid6,
        valid7,
        valid8,
        valid9,
    )


def get_invalid_functions() -> list[callable]:
    def invalid1(args: list[str]):
        pass

    def invalid2(kwargs: list[str]):
        pass

    def invalid3(x1_int_or_str: typing.Union[int, str]):
        pass

    def invalid4(x1_int_or_str: Union[int, str]):
        pass

    def invalid5(x1_int_or_str: int | str):
        pass

    def invalid6(x1_optional_int_wrong_defailt: Optional[int] = 1):
        pass

    def invalid7(x1_optional_int_wrong_defailt: typing.Optional[int] = 1):
        pass

    def invalid8(x1_optional_int_wrong_defailt: int | None = 1):
        pass

    def invalid9(x1_optional_int_wrong_defailt: None | int = 1):
        pass

    def invalid10(x1_int_or_none_or_float: int | None | str):
        pass

    return (
        invalid1,
        invalid2,
        invalid3,
        invalid4,
        invalid5,
        invalid6,
        invalid7,
        invalid8,
        invalid9,
        invalid10,
    )


def test_validate_function_signature():
    for valid_fun in get_valid_functions():
        _validate_function_signature(function=valid_fun)

    # for invalid_fun in get_invalid_functions():
    #     with pytest.raises(ValueError):
    #         _validate_function_signature(function=invalid_fun)


#         match="argument with name args",
#     ):
#         _validate_function_signature(function=fun1)

#     with pytest.raises(
#         ValueError,
#         match="typing.Union is not supported",
#     ):
#         _validate_function_signature(function=fun2)

#     with pytest.raises(
#         ValueError,
#         match='Use of "|',
#     ):
#         _validate_function_signature(function=fun3)

#     with pytest.raises(
#         ValueError,
#         match='Use of "|',
#     ):
#         _validate_function_signature(function=fun4)

#     with pytest.raises(
#         ValueError,
#         match="Optional parameter has non-None default value",
#     ):
#         _validate_function_signature(function=fun5)

#     _validate_function_signature(function=fun6)
