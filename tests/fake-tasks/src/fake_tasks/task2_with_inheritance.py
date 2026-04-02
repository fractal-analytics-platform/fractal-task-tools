from pydantic import BaseModel


class GenericParameters(BaseModel):
    a: int
    """
    Description of `a` in `GenericParameters`.
    """


class SpecificParameters(GenericParameters):
    """
    Description
    """

    b: int
    """
    Description of `b` in `SpecificParameters`.
    """
    c: int
    """
    Description of `c` in `SpecificParameters`.
    """


def task2_with_inheritance(
    zarr_urls: list[str],
    zarr_dir: str,
    arg_1: SpecificParameters,
):
    """
    Short description

    Args:
        zarr_urls: Default
        zarr_dir: Default
        arg_1: Description of arg_1.
    """
