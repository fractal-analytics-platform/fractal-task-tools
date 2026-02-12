from devtools import debug
from fractal_task_tools._args_schemas import create_schema_for_single_task
from pydantic import validate_call, Field, BaseModel


class MyModel(BaseModel):
    x: int
    y: int


@validate_call
def task_function_with_field(
    zarr_url: str,
    arg_1: MyModel,
    arg_2: MyModel = Field(default_factory=MyModel),
):
    """
    Short description

    Args:
        arg_1: Description of arg_1.
        arg_2: Description of arg_2.
    """


def test_create_schema_with_field():
    schema = create_schema_for_single_task(
        task_function=task_function_with_field,
        executable=__file__,
        package=None,
        verbose=True,
    )
    debug(schema)
    # target_schema = {
    #     "additionalProperties": False,
    #     "properties": {
    #         "zarr_url": {
    #             "title": "Zarr Url",
    #             "type": "string",
    #             "description": "Missing description",
    #         },
    #         "arg_1": {
    #             "default": 1,
    #             "title": "Arg 1",
    #             "type": "integer",
    #             "description": "Description of arg_1.",
    #         },
    #     },
    #     "required": ["zarr_url"],
    #     "type": "object",
    #     "title": "TaskFunction",
    # }
    # assert target_schema == schema
