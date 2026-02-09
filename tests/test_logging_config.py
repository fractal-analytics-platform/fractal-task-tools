import json
import logging
import shlex
import subprocess
import sys
from pathlib import Path

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

        # Properties of another (child) logger
        some_logger = logging.getLogger("my_task")
        assert (
            logging.getLevelName(some_logger.getEffectiveLevel())
            == FRACTAL_TASK_LOG_LEVEL
        )
        assert some_logger.hasHandlers()
        assert some_logger.parent == root_logger


def test_xxx(monkeypatch, tmp_path):
    with monkeypatch.context() as mc:
        FRACTAL_TASK_LOG_LEVEL = "DEBUG"
        mc.setenv("FRACTAL_TASK_LOG_LEVEL", FRACTAL_TASK_LOG_LEVEL)

        task1_path = Path(__file__).parent / "fake-task-for-logging/task1.py"
        task2_path = Path(__file__).parent / "fake-task-for-logging/task2.py"
        args1_path = tmp_path / "args1.json"
        args2_path = tmp_path / "args2.json"
        out1_file = tmp_path / "out1.json"
        out2_file = tmp_path / "out2.json"
        args1_option = f"--args-json {args1_path.as_posix()}"
        args2_option = f"--args-json {args2_path.as_posix()}"
        out1_option = f"--out-json {out1_file.as_posix()}"
        out2_option = f"--out-json {out2_file.as_posix()}"

        with args1_path.open("w") as f:
            json.dump(dict(zarr_urls=[], zarr_dir="/fake", arg=1), f)

        cmd1 = f"{sys.executable} {task1_path} {args1_option} {out1_option}"
        cmd2 = f"{sys.executable} {task2_path} {args2_option} {out2_option}"

        res = subprocess.run(
            shlex.split(cmd1),
            capture_output=True,
            encoding="utf-8",
        )
        assert "root; DEBUG; Logging level" in res.stderr
        assert "task1; DEBUG; DEBUG from task" in res.stderr

        res = subprocess.run(
            shlex.split(cmd1),
            capture_output=True,
            encoding="utf-8",
        )
        assert res.returncode == 1
