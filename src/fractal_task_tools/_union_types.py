import types
import typing

from pydantic.fields import FieldInfo

_UNION_TYPES = {typing.Union, types.UnionType}


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
    )
    if result != alternative_result:
        # This is a safety check, which is meant to be unreachable
        raise ValueError(
            f"Could not determine whether {_type} is a union. Please report "
            "this at https://github.com/fractal-analytics-platform/"
            "fractal-task-tools/issues."
        )
    return result


def is_annotated_union(_type) -> bool:
    # FIXME https://docs.python.org/3/library/typing.html#typing.Annotated
    return typing.get_origin(_type) is typing.Annotated and is_union(
        _type.__origin__
    )


def is_tagged(_type) -> bool:
    # FIXME https://docs.python.org/3/library/typing.html#typing.Annotated
    return any(
        isinstance(_item, FieldInfo) and _item.discriminator is not None
        for _item in _type.__metadata__
    )
