import json
from datetime import datetime
from pathlib import Path

import pytest
from fractal_task_tools.task_wrapper import run_fractal_task
from pydantic import ValidationError
from pydantic.validate_call_decorator import validate_call

TASK_OUTPUT = {
    "some": "thing",
    "path": Path("/something"),
}

SERIALIZED_TASK_OUTPUT = {
    "some": "thing",
    "path": "/something",
}


@validate_call
def fake_task(zarr_url: str, parameter: float):
    return TASK_OUTPUT


@validate_call
def fake_task_invalid_output(zarr_url: str, parameter: float):
    return dict(non_json_serializable=datetime.now())


def test_run_fractal_task(tmp_path, monkeypatch, caplog):

    ARGS_PATH = tmp_path / "args.json"
    METADIFF_PATH = tmp_path / "metadiff.json"

    # Mock argparse.ArgumentParser
    class MockArgumentParser:
        def add_argument(self, *args, **kwargs):
            pass

        def parse_args(self, *args, **kwargs):
            class Args(object):
                def __init__(self):
                    self.args_json = str(ARGS_PATH)
                    self.out_json = str(METADIFF_PATH)

            return Args()

    import fractal_task_tools.task_wrapper  # noqa: F401

    monkeypatch.setattr(
        "fractal_task_tools.task_wrapper.ArgumentParser",
        MockArgumentParser,
    )

    # Success
    args = dict(zarr_url="/somewhere", parameter=1.0)
    with ARGS_PATH.open("w") as f:
        json.dump(args, f, indent=2)
    function_output = run_fractal_task(task_function=fake_task)
    assert function_output is None
    with METADIFF_PATH.open("r") as f:
        task_output = json.load(f)
    assert task_output == SERIALIZED_TASK_OUTPUT

    # Failure (metadiff file already exists)
    caplog.clear()
    with pytest.raises(SystemExit):
        run_fractal_task(task_function=fake_task)
    assert "already exists" in caplog.text

    # Failure (invalid output)
    METADIFF_PATH.unlink()
    with pytest.raises(
        TypeError,
        match="datetime is not JSON serializable",
    ):
        run_fractal_task(task_function=fake_task_invalid_output)

    # Failure (invalid input)
    METADIFF_PATH.unlink()
    args = dict(zarr_url="/somewhere", parameter=None)
    with ARGS_PATH.open("w") as f:
        json.dump(args, f, indent=2)
    with pytest.raises(
        ValidationError, match="validation error for fake_task"
    ):
        run_fractal_task(task_function=fake_task)
