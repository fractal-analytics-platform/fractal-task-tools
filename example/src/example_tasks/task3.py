from pydantic import validate_call


@validate_call
def task3(
    *,
    # Fractal-specific arguments
    zarr_urls: list[str],
    zarr_dir: str,
    # Task-specific arguments
    object_arg: dict[int, bool],
    optional_object_arg: dict[int, bool] | None = None,
    nested_object_arg: dict[str, dict[str, str]],
):
    """
    Short description of task3

    Long description of this wonderful task that actually only represents a
    mock task for testing.

    Args:
        object_arg: Object argument.
        optional_object_arg: Optional object argument.
        nested_object_arg: Nested object argument.
    """
    pass
