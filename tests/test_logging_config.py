import logging

import pytest
from fractal_task_tools.logging_config import DEFAULT_LOG_FORMAT
from fractal_task_tools.logging_config import DEFAULT_LOG_LEVEL
from fractal_task_tools.logging_config import get_logging_format
from fractal_task_tools.logging_config import get_logging_level
from fractal_task_tools.logging_config import setup_logging_config


def test_get_logging_level(monkeypatch):
    assert get_logging_level() == DEFAULT_LOG_LEVEL

    with monkeypatch.context() as mc:
        mc.setenv("FRACTAL_TASK_LOG_LEVEL", "invalid-level")
        with pytest.raises(ValueError):
            get_logging_level()

    for levelname in ["DEBUG", "INFO", "WARNING", "CRITICAL"]:
        with monkeypatch.context() as mc:
            mc.setenv("FRACTAL_TASK_LOG_LEVEL", levelname)
            assert get_logging_level() == levelname


def test_get_logging_format(monkeypatch):
    assert get_logging_format() == DEFAULT_LOG_FORMAT

    log_format = r"custom - %(message)s"
    with monkeypatch.context() as mc:
        mc.setenv("FRACTAL_TASK_LOG_FORMAT", log_format)
        assert get_logging_format() == log_format

    log_format = r"custom - %(level)s"
    with monkeypatch.context() as mc:
        mc.setenv("FRACTAL_TASK_LOG_FORMAT", log_format)
        assert get_logging_format() == log_format

    invalid_log_format = r"custom - %(level)"
    with monkeypatch.context() as mc:
        mc.setenv("FRACTAL_TASK_LOG_FORMAT", invalid_log_format)
        with pytest.raises(ValueError, match="Invalid format"):
            get_logging_format()


def test_setup_logging_config(monkeypatch):
    print()

    with monkeypatch.context() as mc:
        FRACTAL_TASK_LOG_LEVEL = "CRITICAL"
        FRACTAL_TASK_LOG_FORMAT = r"xxx %(levelname)s %(message)s"
        mc.setenv("FRACTAL_TASK_LOG_LEVEL", FRACTAL_TASK_LOG_LEVEL)
        mc.setenv("FRACTAL_TASK_LOG_FORMAT", FRACTAL_TASK_LOG_FORMAT)
        setup_logging_config()

        # Properties of root logger
        root_logger = logging.getLogger("root")
        assert len(root_logger.handlers) == 1
        handler = root_logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler)
        assert handler.formatter._fmt == FRACTAL_TASK_LOG_FORMAT

        # Properties of another logger
        some_logger = logging.getLogger("my_task")
        assert (
            logging.getLevelName(some_logger.getEffectiveLevel())
            == FRACTAL_TASK_LOG_LEVEL
        )
        assert some_logger.hasHandlers()
        assert some_logger.parent == root_logger
