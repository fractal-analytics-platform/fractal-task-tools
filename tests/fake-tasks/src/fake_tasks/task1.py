from pydantic import BaseModel, Field


class MyModel(BaseModel):
    """
    Short description of `MyModel`

    Attributes:
        inner_arg: Description from docstring
        another_arg: Description from docstring
    """

    inner_arg: int = Field(description="Description from field")
    another_arg: int


def task1(
    zarr_urls: list[str],
    zarr_dir: str,
    arg2: MyModel,
):
    """
    Short description of `task1`.

    Long description (very very long).

    Arguments:
        zarr_urls: Default
        zarr_dir: Default
        arg2: A `MyModel` object
    """
    pass
