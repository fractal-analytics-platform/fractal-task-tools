import pytest
from fractal_task_tools._task_arguments import validate_arguments


def _fake_schema(*args: list[str]):
    return dict(properties={key: None for key in args})


def test_validate_arguments():
    with pytest.raises(ValueError, match="Invalid task_type="):
        validate_arguments(
            task_type="invalid",
            executable_kind="non_parallel",
            schema={},
        )

    with pytest.raises(ValueError, match="Invalid task_type="):
        validate_arguments(
            task_type="compound",
            executable_kind="invalid",
            schema={},
        )

    with pytest.raises(ValueError, match="Required arguments"):
        validate_arguments(
            task_type="non_parallel",
            executable_kind="non_parallel",
            schema=_fake_schema("zarr_dir", "arg1"),
        )

    with pytest.raises(ValueError, match="Forbidden arguments"):
        validate_arguments(
            task_type="non_parallel",
            executable_kind="non_parallel",
            schema=_fake_schema("zarr_urls", "zarr_dir", "zarr_url", "arg1"),
        )

    validate_arguments(
        task_type="non_parallel",
        executable_kind="non_parallel",
        schema=_fake_schema("zarr_urls", "zarr_dir", "arg1"),
    )

    validate_arguments(
        task_type="compound",
        executable_kind="non_parallel",
        schema=_fake_schema("zarr_urls", "zarr_dir", "arg1"),
    )

    validate_arguments(
        task_type="compound",
        executable_kind="parallel",
        schema=_fake_schema("zarr_url", "init_args", "arg1"),
    )

    validate_arguments(
        task_type="parallel",
        executable_kind="parallel",
        schema=_fake_schema("zarr_url", "arg1"),
    )

    with pytest.raises(ValueError, match="Forbidden arguments"):
        validate_arguments(
            task_type="converter_non_parallel",
            executable_kind="non_parallel",
            schema=_fake_schema("zarr_urls", "zarr_dir", "arg1"),
        )

    validate_arguments(
        task_type="converter_non_parallel",
        executable_kind="non_parallel",
        schema=_fake_schema("zarr_dir", "arg1"),
    )

    validate_arguments(
        task_type="converter_compound",
        executable_kind="non_parallel",
        schema=_fake_schema("zarr_dir", "arg1"),
    )

    validate_arguments(
        task_type="converter_compound",
        executable_kind="parallel",
        schema=_fake_schema("zarr_url", "init_args", "arg1"),
    )
