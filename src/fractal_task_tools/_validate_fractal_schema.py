import logging

logger = logging.getLogger("validate_schema")

JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


_ANYOF = "anyOf"
_ITEMS = "items"
_DEFS = "$defs"
_PROPERTIES = "properties"
_DEFINITIONS = "definitions"
_ENUM = "enum"

NULL_TYPE = {"type": "null"}
NULLABLE_BOOLEAN_ANYOF_SORTED = [{"type": "boolean"}, {"type": "null"}]


def _is_nullable_boolean_anyof(_anyof: JSON) -> bool:
    return sorted(_anyof, key=lambda obj: obj["type"]) == NULLABLE_BOOLEAN_ANYOF_SORTED


def _is_nullable_enum_anyof(_anyof: JSON) -> bool:
    return NULL_TYPE in _anyof and any(
        _ENUM in item.keys() for item in _anyof if isinstance(item, dict)
    )


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
            raise ValueError(f"[E02] Nullable enum at {path}")

    if _ENUM in schema:
        if not len(set(type(item) for item in schema[_ENUM])) == 1:
            raise ValueError(f"[E03] Non-homogeneous enum at {path}")

    if _DEFINITIONS in schema:
        raise ValueError(f'[E04] Unsupported keyword "{_DEFINITIONS}" at {path}')

    logging.warning(f"END validating {path}")  # FIXME: make info
