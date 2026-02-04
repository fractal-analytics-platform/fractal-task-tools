import logging
import os

ALLOWED_LOGGING_LEVELS = (
    "CRITICAL",
    "ERROR",
    "WARNING",
    "INFO",
    "DEBUG",
)

DEFAULT_LOG_FORMAT = r"%(asctime)s; %(name)s; %(levelname)s; %(message)s"


def setup_logging_config():
    """
    FIXME
    """
    FRACTAL_TASK_LOG_LEVEL = os.getenv("FRACTAL_TASK_LOG_LEVEL", "INFO")
    if FRACTAL_TASK_LOG_LEVEL not in ALLOWED_LOGGING_LEVELS:
        raise ValueError(
            f"Invalid {FRACTAL_TASK_LOG_LEVEL=} environment variables. "
            f"Allowed values: {ALLOWED_LOGGING_LEVELS}."
        )
    FRACTAL_TASK_LOG_FORMAT = os.getenv(
        "FRACTAL_TASK_LOG_FORMAT",
        DEFAULT_LOG_FORMAT,
    )
    logging_skip = os.getenv("FRACTAL_TASK_SKIP_LOG_CONFIG", False)
    if not logging_skip:
        logging.basicConfig(
            level=FRACTAL_TASK_LOG_LEVEL,
            format=FRACTAL_TASK_LOG_FORMAT,
            force=True,
        )
        logging.debug(f"Logging level: {FRACTAL_TASK_LOG_LEVEL=}")
        logging.debug(f"Logging format: {FRACTAL_TASK_LOG_FORMAT=}")
