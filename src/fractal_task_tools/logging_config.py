import logging
import os
from typing import Literal

ALLOWED_LOGGING_LEVELS = (
    "CRITICAL",
    "ERROR",
    "WARNING",
    "INFO",
    "DEBUG",
)
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = r"%(asctime)s; %(name)s; %(levelname)s; %(message)s"


def get_logging_format() -> str:
    # Use default values if env variables are unset or set to an empty string
    log_format = os.getenv("FRACTAL_TASK_LOG_FORMAT", None)
    log_format = log_format or DEFAULT_LOG_FORMAT
    logging.PercentStyle(fmt=log_format).validate()
    return log_format


def get_logging_level() -> (
    Literal[
        "CRITICAL",
        "ERROR",
        "WARNING",
        "INFO",
        "DEBUG",
    ]
):
    # Get env variables
    FRACTAL_TASK_LOG_LEVEL = os.getenv(
        "FRACTAL_TASK_LOG_LEVEL",
        None,
    )
    # Use default values if env variables are unset or set to an empty string
    FRACTAL_TASK_LOG_LEVEL = FRACTAL_TASK_LOG_LEVEL or DEFAULT_LOG_LEVEL

    # Validate log-level variable
    if FRACTAL_TASK_LOG_LEVEL not in ALLOWED_LOGGING_LEVELS:
        raise ValueError(
            f"Invalid {FRACTAL_TASK_LOG_LEVEL=} environment variables. "
            f"Allowed values: {ALLOWED_LOGGING_LEVELS}."
        )

    return FRACTAL_TASK_LOG_LEVEL


def setup_logging_config():
    FRACTAL_TASK_LOG_LEVEL = get_logging_level()
    FRACTAL_TASK_LOG_FORMAT = get_logging_format()
    # Apply logging configuration
    logging.basicConfig(
        level=FRACTAL_TASK_LOG_LEVEL,
        format=FRACTAL_TASK_LOG_FORMAT,
        force=True,
    )
    logging.debug(f"Logging level: {FRACTAL_TASK_LOG_LEVEL=}")
    logging.debug(f"Logging format: {FRACTAL_TASK_LOG_FORMAT=}")
