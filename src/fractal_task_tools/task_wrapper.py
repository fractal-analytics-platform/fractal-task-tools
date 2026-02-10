import json
import logging
import os
import sys
from argparse import ArgumentParser
from json import JSONEncoder
from pathlib import Path

from .logging_config import setup_logging_config
from .logging_config import WRAPPER_LOGGER_NAME

task_wrapper_logger = logging.getLogger(WRAPPER_LOGGER_NAME)


class TaskParameterEncoder(JSONEncoder):
    """
    Custom JSONEncoder that transforms Path objects to strings.

    Ref https://docs.python.org/3/library/json.html
    """

    def default(self, obj):
        if isinstance(obj, Path):
            return obj.as_posix()
        return super().default(obj)


def _check_deprecated_argument(logger_name: str | None = None) -> None:
    """
    Emit warning for deprecated argument.
    """
    if logger_name is not None:
        task_wrapper_logger.warning(
            (
                "`logger_name` function argument is deprecated. "
                f"The value provided ({logger_name}) will be ignored."
            )
        )


def run_fractal_task(
    *,
    task_function: callable,
    skip_logging_configuration: bool = False,
    logger_name: str | None = None,
) -> None:
    """
    Implement standard task interface and call task_function.

    Args:
        task_function:
            Callable function that runs the task.
        skip_logging_configuration:
            If `True`, do not call override logging configuration.
        logger_name:
            Deprecated argument (will be removed in a future version)
    """

    # Parse `--args-json` and `--out-json` CLI arguments
    parser = ArgumentParser()
    parser.add_argument(
        "--args-json",
        help="Read parameters from json file",
        required=True,
        type=str,
    )
    parser.add_argument(
        "--out-json",
        help="Output file to redirect serialised returned data",
        required=True,
        type=str,
    )
    parsed_args = parser.parse_args()

    # Configure root logger
    if not (
        skip_logging_configuration
        or os.getenv(
            "FRACTAL_TASK_SKIP_LOG_CONFIG",
            False,
        )
    ):
        setup_logging_config()

    _check_deprecated_argument(logger_name)

    # Preliminary check
    if Path(parsed_args.out_json).exists():
        msg = f"Output file {parsed_args.out_json} already exists. Terminating"
        task_wrapper_logger.error(msg)
        sys.exit(msg)

    # Read parameters dictionary
    with open(parsed_args.args_json, "r") as f:
        pars = json.load(f)

    # Run task
    task_wrapper_logger.info(f"START {task_function.__name__} task")
    metadata_update = task_function(**pars)
    task_wrapper_logger.info(f"END {task_function.__name__} task")

    # Write output metadata to file, with custom JSON encoder
    with open(parsed_args.out_json, "w") as fout:
        json.dump(
            metadata_update,
            fout,
            cls=TaskParameterEncoder,
            indent=2,
        )
