from pydantic import validate_call


@validate_call
def task2(
    # Fractal-specific arguments
    zarr_urls: list[str],
    zarr_dir: str,
    # Task-specific arguments
    *,
    list_arg: list[int],
    tuple_arg: tuple[int, int, int],
    optional_list_arg: list[int] | None = None,
    optional_tuple_arg: tuple[int, int, int] | None = None,
):
    """
    Short description of task2

    Long description of this wonderful task that actually only represents a
    mock task for testing.

    Args:
        list_arg: An arbitrary-size array of integers.
        tuple_arg: A fixed-size array of integers.
        optional_list_arg: An optional arbitrary-size array of integers.
        optional_tuple_arg: An optional fixed-size array of integers.
    """
    pass
