import json
import logging

logger = logging.getLogger("validate_schema")

JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

# Keywords (to avoid typos)
_NAME = "name"
_ANYOF = "anyOf"
_ONEOF = "oneOf"
_ITEMS = "items"
_DEFS = "$defs"
_PROPERTIES = "properties"
_DEFINITIONS = "definitions"
_ENUM = "enum"
_DISCRIMINATOR = "discriminator"
_REF = "$ref"
_ARRAY = "array"
_TYPE = "type"


NULL_TYPE = {"type": "null"}
NON_NULL_PRIMITIVE_TYPES = {"boolean", "string", "integer", "number"}
CASES_NULLABLE_BOOLEAN_ANYOF = (
    [{"type": "boolean"}, {"type": "null"}],
    [{"type": "null"}, {"type": "boolean"}],
)

# Forbidden variable names based on `pydantic.v1.decorator` for v2.11.10:
FORBIDDEN_NAMES = {
    "args",
    "kwargs",
    "v__args",
    "v__kwargs",
    "v__duplicate_kwargs",
    "v__positional_only",
}


def validate_schema(
    *,
    schema: JSON,
    path: str,
    verbose: bool = False,
):
    """
    Recursive function that checks some patterns on a JSON schema.
    """
    if verbose:
        logger.setLevel(logging.INFO)
        logger.info(f"START validating {path}")  # FIXME: make info

    # Recursive schema exploration
    for def_key in schema.get(_DEFS, []):
        validate_schema(
            schema=schema[_DEFS][def_key],
            path=f"{path}/{_DEFS}/{def_key}",
            verbose=verbose,
        )
    for prop_key in schema.get(_PROPERTIES, []):
        validate_schema(
            schema=schema[_PROPERTIES][prop_key],
            path=f"{path}/{_PROPERTIES}/{prop_key}",
            verbose=verbose,
        )
    if _ITEMS in schema:
        validate_schema(
            schema=schema[_ITEMS],
            path=f"{path}/{_ITEMS}",
            verbose=verbose,
        )
    for ind, item in enumerate(schema.get(_ANYOF, [])):
        validate_schema(
            schema=item,
            path=f"{path}/{_ANYOF}/{ind}",
            verbose=verbose,
        )

    # Validation

    if verbose:
        logger.info(f"Now validate {json.dumps(schema)}")

    # E0x: general errors

    if schema.get(_NAME, None) in FORBIDDEN_NAMES:
        raise ValueError(f"[E01] Forbidden {_NAME} at {path}")

    if _DEFINITIONS in schema:
        raise ValueError(f'[E02] Unsupported keyword "{_DEFINITIONS}" at {path}')

    if _ENUM in schema:
        if len(set(type(item) for item in schema[_ENUM])) > 1:
            raise ValueError(f"[E03] Non-homogeneous {_ENUM} at {path}")

    # E1x: anyOf-related errors
    if _ANYOF in schema:
        if schema[_ANYOF] in CASES_NULLABLE_BOOLEAN_ANYOF:
            raise ValueError(f"[E10] Nullable boolean at {path}")

        if NULL_TYPE in schema[_ANYOF] and any(
            _ENUM in item.keys() for item in schema[_ANYOF] if isinstance(item, dict)
        ):
            raise ValueError(f"[E11] Nullable {_ENUM} at {path}")

        if (
            len(
                [
                    item
                    for item in schema[_ANYOF]
                    if (
                        isinstance(item, dict)
                        and item.get("type", None) in NON_NULL_PRIMITIVE_TYPES
                    )
                ]
            )
            > 1
        ):
            raise ValueError(f"[E12] Unsupported {_ANYOF} of primitive types at {path}")

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

    # E3x: array-related errors
    if schema.get(_TYPE) == _ARRAY and schema.get(_ITEMS) == {}:
        raise ValueError(f"[E30] Unsupported array with {_ITEMS}={{}} at {path}")

    if verbose:
        logger.info(f"END validating {path}")  # FIXME: make info
