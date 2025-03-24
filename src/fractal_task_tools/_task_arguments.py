import logging
from typing import Any
from typing import Literal


REQUIRED_ARGUMENTS: dict[tuple[str, str], set[str]] = {
    ("non_parallel", "non_parallel"): {"zarr_urls", "zarr_dir"},
    ("compound", "non_parallel"): {"zarr_urls", "zarr_dir"},
    ("parallel", "parallel"): {"zarr_url"},
    ("compound", "parallel"): {"zarr_url", "init_args"},
    ("converter_non_parallel", "non_parallel"): {"zarr_dir"},
    ("converter_compound", "non_parallel"): {"zarr_dir"},
    ("converter_compound", "parallel"): {"zarr_url", "init_args"},
}
FORBIDDEN_ARGUMENTS: dict[tuple[str, str], set[str]] = {
    ("non_parallel", "non_parallel"): {"zarr_url"},
    ("compound", "non_parallel"): {"zarr_url"},
    ("parallel", "parallel"): {"zarr_urls", "zarr_dir"},
    ("compound", "parallel"): {"zarr_urls", "zarr_dir"},
    ("converter_non_parallel", "non_parallel"): {"zarr_url", "zarr_urls"},
    ("converter_compound", "non_parallel"): {"zarr_url", "zarr_urls"},
    ("converter_compound", "parallel"): {"zarr_urls", "zarr_dir"},
}


def validate_arguments(
    *,
    task_type: Literal["parallel", "non_parallel", "compound"],
    executable_kind: Literal["parallel", "non_parallel"],
    schema: dict[str, Any],
) -> None:
    """
    Validate schema arguments against required/forbidden ones.

    Arguments:
        task_type:
        executable_kind: The `parallel`/`non_parallel` part of the task.
        schema:
    """

    key = (task_type, executable_kind)
    if not (key in REQUIRED_ARGUMENTS and key in FORBIDDEN_ARGUMENTS):
        logging.error(f"Invalid {task_type=}, {executable_kind=}.")
        raise ValueError(f"Invalid {task_type=}, {executable_kind=}.")

    required_args = REQUIRED_ARGUMENTS[key]
    forbidden_args = FORBIDDEN_ARGUMENTS[key]

    schema_properties = set(schema["properties"].keys())

    logging.info(
        f"[validate_arguments] Task has arguments: {schema_properties}"
    )
    logging.info(f"[validate_arguments] Required arguments: {required_args}")
    logging.info(f"[validate_arguments] Forbidden arguments: {forbidden_args}")

    missing_required_arguments = {
        arg for arg in required_args if arg not in schema_properties
    }
    if missing_required_arguments:
        error_msg = (
            "[validate_arguments] Required arguments "
            f"{missing_required_arguments} are missing."
        )
        logging.error(error_msg)
        raise ValueError(error_msg)

    present_forbidden_args = forbidden_args.intersection(schema_properties)
    if present_forbidden_args:
        error_msg = (
            "[validate_arguments] Forbidden arguments "
            f"{present_forbidden_args} are present."
        )
        logging.error(error_msg)
        raise ValueError(error_msg)
