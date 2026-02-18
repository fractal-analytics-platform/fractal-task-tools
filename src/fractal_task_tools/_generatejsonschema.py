import logging
from typing import Any
from pydantic.json_schema import GenerateJsonSchema
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


from pydantic.json_schema import NoDefault


logger = logging.getLogger("CustomGenerateJsonSchema")


class CustomGenerateJsonSchema(GenerateJsonSchema):
    """
    Custom JSON-Schema generator.

    General customization approach is described at
    https://docs.pydantic.dev/latest/concepts/json_schema/#customizing-the-json-schema-generation-process


    """

    def get_flattened_anyof(self, schemas: list[JsonSchemaValue]) -> JsonSchemaValue:
        """
        Customize handling of optional fields.

        As of Pydantic V2, the JSON Schema representation of model attributes
        marked as `Optional[X]` changed, and the new behavior consists in
        marking the corresponding properties as an `anyOf` of either a `null`
        or the actual `X` type.

        This is not always the required behavior, see e.g.
        * https://github.com/pydantic/pydantic/issues/7161
        * https://github.com/pydantic/pydantic/issues/8394

        This method override restores the previous behavior, by stripping
        `{"type": "null"}` from `anyOf` entries.
        """
        null_schema = {"type": "null"}
        if null_schema in schemas:
            logger.warning("Drop `null_schema` before calling `get_flattened_anyof`")
            schemas.pop(schemas.index(null_schema))
        return super().get_flattened_anyof(schemas)

    def get_default_value(self, schema: core_schema.WithDefaultSchema) -> Any:
        """
        Customize default setting

        This override introduces two changes with respect to the base class.

        `None` defaults are stripped.

        When possible, `default_factory` is used to compute the `default` value - see
        https://github.com/pydantic/pydantic/issues/11622#issuecomment-2757419692.
        """
        if "default" in schema:
            if schema["default"] is None:
                logger.warning(f"Ignore `None` default value from {schema=}")
                return NoDefault
            return schema["default"]
        elif "default_factory" in schema:
            if schema.get("default_factory_takes_data"):
                logger.warning(
                    "Cannot populate defaults based on "
                    f"default_factory={schema['default_factory']}, "
                    f'since {schema["default_factory_takes_data"]=}.'
                )
                return NoDefault
            else:
                return schema["default_factory"]()
        else:
            return NoDefault
