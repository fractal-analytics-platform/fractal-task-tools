import logging
from typing import Any
from pydantic.json_schema import GenerateJsonSchema
from pydantic_core import core_schema


from pydantic.json_schema import NoDefault


logger = logging.getLogger("CustomGenerateJsonSchema")


class CustomGenerateJsonSchema(GenerateJsonSchema):
    """
    Custom JSON-Schema generator.

    General customization approach is described at
    https://docs.pydantic.dev/latest/concepts/json_schema/#customizing-the-json-schema-generation-process


    """

    def get_default_value(self, schema: core_schema.WithDefaultSchema) -> Any:
        """
        Customize default setting

        When possible, `default_factory` is used to compute the `default` value - see
        https://github.com/pydantic/pydantic/issues/11622#issuecomment-2757419692.
        """
        if "default" in schema:
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
