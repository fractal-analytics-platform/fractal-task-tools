import logging

logger = logging.getLogger("validate_schema")

JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


_ANYOF = "anyOf"
_ONEOF = "oneOf"
_ITEMS = "items"
_DEFS = "$defs"
_PROPERTIES = "properties"
_DEFINITIONS = "definitions"
_ENUM = "enum"
_DISCRIMINATOR = "discriminator"
_REF = "$ref"
NULL_TYPE = {"type": "null"}
NULLABLE_BOOLEAN_ANYOF_SORTED = [{"type": "boolean"}, {"type": "null"}]
NON_NULL_PRIMITIVE_TYPES = {"boolean", "string", "integer", "number"}


def _is_nullable_boolean_anyof(_anyof: JSON) -> bool:
    return sorted(_anyof, key=lambda obj: obj["type"]) == NULLABLE_BOOLEAN_ANYOF_SORTED


def _is_nullable_enum_anyof(_anyof: JSON) -> bool:
    return NULL_TYPE in _anyof and any(
        _ENUM in item.keys() for item in _anyof if isinstance(item, dict)
    )


def _is_invalid_anyof_of_primitive_types(_anyof: JSON) -> bool:
    if len([item for item in _anyof if item["type"] in NON_NULL_PRIMITIVE_TYPES]) > 1:
        return True
    else:
        return False


def validate_schema(*, schema: JSON, path: str):
    """
    Recursive function that checks some patterns on a JSON schema.
    """
    logging.warning(f"START validating {path}")  # FIXME: make info

    # Recursive schema exploration
    for def_key in schema.get(_DEFS, []):
        validate_schema(
            schema=schema[_DEFS][def_key],
            path=f"{path}/{_DEFS}/{def_key}",
        )
    for prop_key in schema.get(_PROPERTIES, []):
        validate_schema(
            schema=schema[_PROPERTIES][prop_key],
            path=f"{path}/{_PROPERTIES}/{prop_key}",
        )
    if _ITEMS in schema:
        validate_schema(
            schema=schema[_ITEMS],
            path=f"{path}/{_ITEMS}",
        )
    for ind, item in enumerate(schema.get(_ANYOF, [])):
        validate_schema(
            schema=item,
            path=f"{path}/{_ANYOF}/{ind}",
        )

    # Validation
    if _ANYOF in schema:
        if _is_nullable_boolean_anyof(schema[_ANYOF]):
            raise ValueError(f"[E01] Nullable boolean at {path}")

        if _is_nullable_enum_anyof(schema[_ANYOF]):
            raise ValueError(f"[E02] Nullable {_ENUM} at {path}")

        if _is_invalid_anyof_of_primitive_types(schema[_ANYOF]):
            raise ValueError(f"[E05] Unsupported {_ANYOF} of primitive types at {path}")

    if _ENUM in schema:
        if not len(set(type(item) for item in schema[_ENUM])) == 1:
            raise ValueError(f"[E03] Non-homogeneous {_ENUM} at {path}")

    if _DEFINITIONS in schema:
        raise ValueError(f'[E04] Unsupported keyword "{_DEFINITIONS}" at {path}')

    if _ONEOF in schema:
        if _ITEMS in schema:
            if _DISCRIMINATOR not in schema[_ITEMS]:
                raise ValueError(f"[E06] {_ONEOF} with no {_DISCRIMINATOR} at {path}")
        else:
            # FIXME: Add equivalent of E06 without _ITEMS
            pass

        if not all(_REF in item for item in schema[_ONEOF]):
            raise ValueError(f"[E07] Unsupported non-{_REF} item in {_ONEOF} at {path}")

    logging.warning(f"END validating {path}")  # FIXME: make info
