import sys
import types
import typing

if sys.version_info >= (3, 10):
    _UNION_TYPES = {typing.Union, types.UnionType}
else:
    _UNION_TYPES = {typing.Union}


def is_union(_type) -> bool:
    """
    Determine whether _type is a union.

    Based on
    https://docs.python.org/3/library/typing.html#typing.Union
    https://discuss.python.org/t/how-to-check-if-a-type-annotation-represents-an-union/77692/2.
    """
    result = typing.get_origin(_type) in _UNION_TYPES
    alternative_result = (
        type(_type) is typing._UnionGenericAlias
        or type(_type) is types.UnionType
        or "Union[" in str(_type)
        or "|" in str(_type)
    )
    if result != alternative_result:
        # This is a safety check, which is meant to be unreachable
        raise ValueError(
            f"Could not determine whether {_type} is a union. Please report "
            "this at https://github.com/fractal-analytics-platform/"
            "fractal-task-tools/issues."
        )
    return result
