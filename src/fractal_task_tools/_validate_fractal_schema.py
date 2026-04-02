import logging

logger = logging.getLogger("validate_schema")

JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


NULL_TYPE = {"type": "null"}
NULLABLE_BOOLEAN_ANYOF_SORTED = [{"type": "boolean"}, {"type": "null"}]


def _is_nullable_boolean_anyof(_anyof: JSON) -> bool:
    return sorted(_anyof, key=lambda obj: obj["type"]) == NULLABLE_BOOLEAN_ANYOF_SORTED


def _is_nullable_enum_anyof(_anyof: JSON) -> bool:
    return NULL_TYPE in _anyof and any(
        "enum" in item.keys() for item in _anyof if isinstance(item, dict)
    )


def validate_schema(*, schema: JSON, path: str):
    """
    Recursive function that checks some patterns on a JSON schema.
    """
    logging.warning(f"START validating {path}")  # FIXME: make info

    # Recursive schema exploration
    for def_key in schema.get("$defs", []):
        validate_schema(
            schema=schema["$defs"][def_key],
            path=f"{path}/$defs/{def_key}",
        )
    for prop_key in schema.get("properties", []):
        validate_schema(
            schema=schema["properties"][prop_key],
            path=f"{path}/properties/{prop_key}",
        )
    if "items" in schema:
        validate_schema(
            schema=schema["items"],
            path=f"{path}/items",
        )
    for ind, item in enumerate(schema.get("anyOf", [])):
        validate_schema(
            schema=item,
            path=f"{path}/anyOf/{ind}",
        )

    # Validation
    if "anyOf" in schema:
        anyOf = schema["anyOf"]
        if _is_nullable_boolean_anyof(anyOf):
            raise ValueError(f"[E01] Nullable boolean at {path}")
        if _is_nullable_enum_anyof(anyOf):
            raise ValueError(f"[E02] Nullable enum at {path}")
    if "enum" in schema:
        if not len(set(type(item) for item in schema["enum"])) == 1:
            raise ValueError(f"[E03] Non-homogeneous enum at {path}")

    if "definitions" in schema:
        raise ValueError(f'[E04] Unsupported keyword "definitions" at {path}')

    logging.warning(f"END validating {path}")  # FIXME: make info
