import logging
import os
import typing


ValidLoggingLevel = typing.Literal[
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
]
ALLOWED_LOGGING_LEVELS: tuple[str, ...] = typing.get_args(ValidLoggingLevel)


DEFAULT_LOG_LEVEL: ValidLoggingLevel = "INFO"
DEFAULT_LOG_FORMAT: str = r"%(asctime)s; %(name)s; %(levelname)s; %(message)s"


def get_logging_format() -> str:
    """
    Get valid logging format from environment variable or default value.
    """
    # Use default value if the env variable is unset or set to an empty string
    log_format = os.getenv("FRACTAL_TASK_LOG_FORMAT") or DEFAULT_LOG_FORMAT
    # Validate `log_format`
    logging.PercentStyle(fmt=log_format).validate()
    return log_format


def get_logging_level() -> ValidLoggingLevel:
    """
    Get valid logging level from environment variable or default value.
    """
    # Use default value if the env variable is unset or set to an empty string
    log_level = os.getenv("FRACTAL_TASK_LOG_LEVEL") or DEFAULT_LOG_LEVEL
    # Validate `log_level`
    if log_level not in ALLOWED_LOGGING_LEVELS:
        raise ValueError(
            f"Invalid FRACTAL_TASK_LOG_LEVEL={log_level} environment "
            f"variable. Allowed values: {ALLOWED_LOGGING_LEVELS}."
        )
    return log_level


def setup_logging_config() -> None:
    """
    Configure root logging handler.

    Note that calling `logging.basicConfig` with `force=True` removes all
    existing handlers of the `root` logger and creates a new handler.
    """
    FRACTAL_TASK_LOG_LEVEL = get_logging_level()
    FRACTAL_TASK_LOG_FORMAT = get_logging_format()
    logging.basicConfig(
        level=FRACTAL_TASK_LOG_LEVEL,
        format=FRACTAL_TASK_LOG_FORMAT,
        force=True,
    )
    logging.debug(f"Logging level: {FRACTAL_TASK_LOG_LEVEL=}")
    logging.debug(f"Logging format: {FRACTAL_TASK_LOG_FORMAT=}")
