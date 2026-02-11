"""
Custom Pydantic v2 JSON Schema generation tools.

As of Pydantic V2, the JSON Schema representation of model attributes marked
as `Optional` changed, and the new behavior consists in marking the
corresponding properties as an `anyOf` of either a `null` or the actual type.
This is not always the required behavior, see e.g.
* https://github.com/pydantic/pydantic/issues/7161
* https://github.com/pydantic/pydantic/issues/8394
"""

import logging
from typing import Any

import pydantic_core
from pydantic.json_schema import GenerateJsonSchema
from pydantic.json_schema import JsonSchemaValue
from pydantic.json_schema import NoDefault
from pydantic_core import core_schema

logger = logging.getLogger("CustomGenerateJsonSchema")


class _CustomGenerateJsonSchema(GenerateJsonSchema):
    """
    FIXME
    """

    def get_flattened_anyof(self, schemas: list[JsonSchemaValue]) -> JsonSchemaValue:
        """
        FIXME
        """
        null_schema = {"type": "null"}
        if null_schema in schemas:
            logger.warning("Drop `null_schema` before calling `get_flattened_anyof`")
            schemas.pop(schemas.index(null_schema))
        return super().get_flattened_anyof(schemas)


class CustomGenerateJsonSchemaLegacy(_CustomGenerateJsonSchema):
    """
    FIXME
    """

    def default_schema(self, schema: core_schema.WithDefaultSchema) -> JsonSchemaValue:
        """Generates a JSON schema that matches a schema with a default value.

        Args:
            schema: The core schema.

        Returns:
            The generated JSON schema.
        """
        json_schema = self.generate_inner(schema["schema"])

        if "default" in schema:
            default = schema["default"]
            if default is None:
                logger.warning(f"Pop `None` default value from {schema=}")
                json_schema.pop("default")
        elif "default_factory" in schema:
            default = schema["default_factory"]()
        else:
            return json_schema

        # we reflect the application of custom plain, no-info serializers to defaults for
        # JSON Schemas viewed in serialization mode:
        # TODO: improvements along with https://github.com/pydantic/pydantic/issues/8208
        if (
            self.mode == "serialization"
            and (ser_schema := schema["schema"].get("serialization"))
            and (ser_func := ser_schema.get("function"))
            and ser_schema.get("type") == "function-plain"
            and not ser_schema.get("info_arg")
            and not (
                default is None
                and ser_schema.get("when_used") in ("unless-none", "json-unless-none")
            )
        ):
            try:
                default = ser_func(default)  # type: ignore
            except Exception:
                # It might be that the provided default needs to be validated (read: parsed) first
                # (assuming `validate_default` is enabled). However, we can't perform
                # such validation during JSON Schema generation so we don't support
                # this pattern for now.
                # (One example is when using `foo: ByteSize = '1MB'`, which validates and
                # serializes as an int. In this case, `ser_func` is `int` and `int('1MB')` fails).
                self.emit_warning(
                    "non-serializable-default",
                    f"Unable to serialize value {default!r} with the plain serializer; excluding default from JSON schema",
                )
                return json_schema

        try:
            encoded_default = self.encode_default(default)
        except pydantic_core.PydanticSerializationError:
            self.emit_warning(
                "non-serializable-default",
                f"Default value {default} is not JSON serializable; excluding default from JSON schema",
            )
            # Return the inner schema, as though there was no default
            return json_schema

        json_schema["default"] = encoded_default
        return json_schema


class CustomGenerateJsonSchema(_CustomGenerateJsonSchema):
    """
    FIXME
    """

    def get_default_value(self, schema: core_schema.WithDefaultSchema) -> Any:
        """
        FIXME
        Requires `pydantic>=2.11.0`
        See https://github.com/pydantic/pydantic/issues/11622#issuecomment-2757419692
        """
        if "default" in schema:
            if schema["default"] is None:
                logger.warning(f"Ignore `None` default value from {schema=}")
                return NoDefault
            return schema["default"]
        elif "default_factory" in schema and not schema.get(
            "default_factory_takes_data"
        ):
            return schema["default_factory"]()
        return NoDefault
