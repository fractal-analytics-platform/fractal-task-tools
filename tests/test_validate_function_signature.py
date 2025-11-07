import typing
from typing import Optional
from typing import Union

import pytest
from fractal_task_tools._signature_constraints import (
    _validate_function_signature,
)


def valid_0(x1_str: str, x2_int: int):
    pass


def valid_1(x1_optional_str: typing.Optional[str]):
    pass


def valid_2(x1_optional_str: typing.Optional[str] = None):
    pass


def valid_3(x1_optional_str: Optional[str]):
    pass


def valid_4(x1_optional_str: Optional[str] = None):
    pass


def valid_5(x1_optional_str: str | None):
    pass


def valid_6(x1_optional_str: str | None = None):
    pass


def valid_7(x1_optional_str: None | str):
    pass


def valid_8(x1_optional_str: None | str = None):
    pass


def valid_9(x1_int_or_int: int | int):
    pass


def invalid_forbidden_1(args: list[str]):
    pass


def invalid_forbidden_2(kwargs: list[str]):
    pass


def invalid_union_of_three_1(x1_int_or_none_or_float: int | None | float):
    pass


def invalid_union_of_three_2(x1_int_or_str_or_float: int | str | float):
    pass


def invalid_no_none_1(x1_int_or_str: typing.Union[int, str]):
    pass


def invalid_no_none_2(x1_int_or_str: Union[int, str]):
    pass


def invalid_no_none_3(x1_int_or_str: int | str):
    pass


def invalid_default_1(x1_optional_int_wrong_defailt: Optional[int] = 1):
    pass


def invalid_default_2(x1_optional_int_wrong_defailt: typing.Optional[int] = 1):
    pass


def invalid_default_3(x1_optional_int_wrong_defailt: int | None = 1):
    pass


def invalid_default_4(x1_optional_int_wrong_defailt: None | int = 1):
    pass


def test_validate_function_signature():
    for valid_function in (
        valid_0,
        valid_1,
        valid_2,
        valid_3,
        valid_4,
        valid_5,
        valid_6,
        valid_7,
        valid_8,
        valid_9,
    ):
        _validate_function_signature(function=valid_function)

    for invalid_fun in (
        invalid_forbidden_1,
        invalid_forbidden_2,
    ):
        with pytest.raises(ValueError) as exc_info:
            _validate_function_signature(function=invalid_fun)
        assert "forbidden name" in str(exc_info.value)

    for invalid_fun in (
        invalid_union_of_three_1,
        invalid_union_of_three_2,
    ):
        with pytest.raises(ValueError) as exc_info:
            _validate_function_signature(function=invalid_fun)
        assert "Only unions of two elements are supported" in str(
            exc_info.value
        )

    for invalid_fun in (
        invalid_no_none_1,
        invalid_no_none_2,
        invalid_no_none_3,
    ):
        with pytest.raises(ValueError) as exc_info:
            _validate_function_signature(function=invalid_fun)
        assert "One union element must be None" in str(exc_info.value)
    for invalid_fun in (
        invalid_default_1,
        invalid_default_2,
        invalid_default_3,
        invalid_default_4,
    ):
        with pytest.raises(ValueError) as exc_info:
            _validate_function_signature(function=invalid_fun)
        assert "Non-None default not supported" in str(exc_info.value)
