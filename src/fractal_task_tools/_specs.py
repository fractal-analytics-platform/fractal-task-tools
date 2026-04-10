import json
import logging

from ._json_types import JSONdictType
from ._json_types import JSONType

logger = logging.getLogger("validate_schema")


# Keywords (to avoid typos)
_ANYOF = "anyOf"
_ONEOF = "oneOf"
_ITEMS = "items"
_PREFIX_ITEMS = "prefixItems"
_DEFS = "$defs"
_PROPERTIES = "properties"
_DEFINITIONS = "definitions"
_ENUM = "enum"
_NAME = "name"
_DISCRIMINATOR = "discriminator"
_REF = "$ref"
_TYPE = "type"
_BOOLEAN = "boolean"
_DEFAULT = "default"
_ADDITIONAL_PROPERTIES = "additionalProperties"
_OBJECT = "object"

_NULL_TYPE = {"type": "null"}
_BOOLEAN_TYPE = {_TYPE: _BOOLEAN}
_CASES_NULLABLE_BOOLEAN_ANYOF = (
    [_NULL_TYPE, _BOOLEAN_TYPE],
    [_BOOLEAN_TYPE, _NULL_TYPE],
)

_NON_NULL_PRIMITIVE_TYPES = {"boolean", "string", "integer", "number"}
"""
Non-`null` primitive types.
"""

_FORBIDDEN_NAMES = {
    "args",
    "kwargs",
    "v__args",
    "v__kwargs",
    "v__duplicate_kwargs",
    "v__positional_only",
}
"""
Forbidden variable names (including the ones from `pydantic.v1.decorator` for v2.11.10).
"""


def _raise_E07_if_empty_string(arg: JSONType, *, path: str) -> None:
    if isinstance(arg, str) and arg.strip() == "":
        raise ValueError(f"[E07] Empty string default at {path}")


def validate_schema(
    *,
    schema: JSONdictType,
    path: str,
    anyof_parent_schema: JSONdictType | None = None,
    root_schema: JSONdictType | None = None,
    verbose: bool = False,
):
    """
    Recursive function that checks some patterns on a JSON schema.

    Args:
        schema: The JSON Schema to validate.
        path:
            Current path in the JSON Schema traversal, expanded at each recursive call.
        anyof_parent_schema: Additional context for validation of `anyOf` items.
        verbose: Whether to print additional logs.
    """
    if verbose:
        logger.setLevel(logging.INFO)
        logger.info(f"START validating {path}")

    # Recursive schema exploration
    for def_key in schema.get(_DEFS, []):
        validate_schema(
            schema=schema[_DEFS][def_key],
            path=f"{path}/{_DEFS}/{def_key}",
            verbose=verbose,
            root_schema=root_schema,
        )
    for prop_key in schema.get(_PROPERTIES, []):
        validate_schema(
            schema=schema[_PROPERTIES][prop_key],
            path=f"{path}/{_PROPERTIES}/{prop_key}",
            verbose=verbose,
            root_schema=root_schema,
        )
    if _ITEMS in schema:
        validate_schema(
            schema=schema[_ITEMS],
            path=f"{path}/{_ITEMS}",
            verbose=verbose,
            root_schema=root_schema,
        )
    for ind, item in enumerate(schema.get(_ANYOF, [])):
        validate_schema(
            schema=item,
            path=f"{path}/{_ANYOF}/{ind}",
            verbose=verbose,
            anyof_parent_schema=schema,
            root_schema=root_schema,
        )

    # Validation

    if verbose:
        logger.info(f"Now validate {json.dumps(schema)}")

    # E0x: general errors

    if schema.get(_NAME, None) in _FORBIDDEN_NAMES:
        raise ValueError(f"[E01] Forbidden {_NAME} at {path}")

    if _DEFINITIONS in schema:
        raise ValueError(f'[E02] Unsupported keyword "{_DEFINITIONS}" at {path}')

    if _ENUM in schema:
        if len(set(type(item) for item in schema[_ENUM])) > 1:
            raise ValueError(f"[E03] Non-homogeneous {_ENUM} at {path}")

    if (
        _TYPE not in schema
        and _ANYOF not in schema
        and _ONEOF not in schema
        and _ITEMS not in schema
        and _REF not in schema
    ):
        raise ValueError(f"[E04] Unsupported schema at {path}")

    if schema.get(_TYPE) == _BOOLEAN and not (
        _DEFAULT in schema
        or (
            anyof_parent_schema is not None
            and _ANYOF in anyof_parent_schema
            and _DEFAULT in anyof_parent_schema
        )
    ):
        raise ValueError(f"[E05] Boolean with no {_DEFAULT} at {path}")

    if (
        schema.get(_TYPE) == _OBJECT
        and schema.get(_ADDITIONAL_PROPERTIES) == _BOOLEAN_TYPE
    ):
        raise ValueError(f"[E06] Object of booleans at {path}")

    if _DEFAULT in schema:
        default_value = schema[_DEFAULT]
        if isinstance(default_value, list):
            for item in default_value:
                _raise_E07_if_empty_string(item, path=path)
        elif isinstance(default_value, dict):
            for key, value in default_value.items():
                _raise_E07_if_empty_string(key, path=path)
                _raise_E07_if_empty_string(value, path=path)
        else:
            _raise_E07_if_empty_string(default_value, path=path)

    if _BOOLEAN_TYPE in schema.get(_PREFIX_ITEMS, []):
        raise ValueError(f"[E08] Unsupported boolean in 'tuple' at {path}")

    # E1x: anyOf-related errors
    if _ANYOF in schema:
        if schema[_ANYOF] in _CASES_NULLABLE_BOOLEAN_ANYOF:
            raise ValueError(f"[E10] Nullable boolean at {path}")

        if _NULL_TYPE in schema[_ANYOF]:
            if any(
                _ENUM in item.keys()
                for item in schema[_ANYOF]
                if isinstance(item, dict)
            ):
                raise ValueError(f"[E11] Nullable {_ENUM} at {path}")

            for internal_schema in schema[_ANYOF]:
                if internal_schema == _NULL_TYPE:
                    continue
                if _REF in internal_schema:
                    if root_schema is None:
                        raise RuntimeError(
                            f"[I90] Internal error at {path}: `root_schema` not set."
                        )
                    ref_value = internal_schema.get(_REF)
                    _hash, _defs, ref_key = ref_value.split("/")
                    if _hash != "#" or _defs != _DEFS:
                        raise RuntimeError(
                            f"[I91] Internal error at {path}: "
                            f"Invalid {_REF} string {ref_value}"
                        )
                    try:
                        _internal_def = root_schema[_DEFS][ref_key]
                    except KeyError as e:
                        raise RuntimeError(
                            f"[I92] Internal error at {path}: KeyError {str(e)}"
                        )
                    if _ENUM in _internal_def:
                        raise ValueError(f"[E12] Nullable {_ENUM} at {path}")

        if (
            len(
                [
                    item
                    for item in schema[_ANYOF]
                    if (
                        isinstance(item, dict)
                        and item.get("type", None) in _NON_NULL_PRIMITIVE_TYPES
                    )
                ]
            )
            > 1
        ):
            raise ValueError(f"[E13] Unsupported {_ANYOF} of primitive types at {path}")

        if (
            len(
                [
                    item
                    for item in schema[_ANYOF]
                    if isinstance(item, dict) and _REF in item
                ]
            )
            > 1
        ):
            raise ValueError(
                f"[E14] Unsupported {_ANYOF} with more than one {_REF} at {path}"
            )

        if len(schema[_ANYOF]) > 2:
            raise RuntimeError("DUMMY ERROR")

    # E2x: oneOf-related errors
    if _ONEOF in schema:
        if _ITEMS in schema:
            if _DISCRIMINATOR not in schema[_ITEMS]:
                raise ValueError(f"[E20] {_ONEOF} with no {_DISCRIMINATOR} at {path}")
        else:
            if _DISCRIMINATOR not in schema:
                raise ValueError(f"[E21] {_ONEOF} with no {_DISCRIMINATOR} at {path}")

        if not all(_REF in item for item in schema[_ONEOF]):
            raise ValueError(f"[E22] Unsupported non-{_REF} item in {_ONEOF} at {path}")
