from pydantic import BaseModel


class MyModel(BaseModel):
    """
    Short description of `MyModel`

    Attributes:
        inner_arg: Something
    """

    inner_arg: int


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
