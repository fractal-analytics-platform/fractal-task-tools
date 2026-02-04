import logging
import os

from devtools import debug
from fractal_task_tools.logging_config import setup_logging_config


def test_setup_logging_config(caplog):
    print()

    os.environ["FRACTAL_TASK_LOG_LEVEL"] = "WARNING"
    os.environ["FRACTAL_TASK_LOG_FORMAT"] = r"PLACEHOLDER %(message)s"
    setup_logging_config()
    logger = logging.getLogger("logger-name")
    logger.info("test info")
    logger.warning("test warning")
    logger.error("test error")

    debug(caplog.get_records(when="call"))
