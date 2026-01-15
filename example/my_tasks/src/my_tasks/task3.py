from pydantic import validate_call


@validate_call
def task3(
    *,
    # Fractal-specific arguments
    zarr_urls: list[str],
    zarr_dir: str,
    # Task-specific arguments
    object_arg: dict[int, bool],
    nested_object_arg: dict[str, dict[str, str]],
    optional_object_arg: dict[int, bool] | None = None,
):
    """
    Short description

    Long description of this wonderful task that is called `task_function` and
    actually only represents a mock task for testing.

    Args:
        object_arg: FIXME
        nested_object_arg: FIXME
        optional_object_arg: FIXME
    """
    pass
