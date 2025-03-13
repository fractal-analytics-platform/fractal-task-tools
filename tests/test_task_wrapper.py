import json

import pytest
from devtools import debug
from fractal_task_tools.task_wrapper import run_fractal_task
from pydantic import ValidationError
from pydantic.validate_call_decorator import validate_call


TASK_OUTPUT = {"some": "thing", "and": "another"}


@validate_call
def fake_task(zarr_url: str, parameter: float):
    return TASK_OUTPUT


def test_run_fractal_task(tmp_path, monkeypatch, caplog):

    args_path = tmp_path / "args.json"

    # Mock argparse.ArgumentParser
    class MockArgumentParser:
        def add_argument(self, *args, **kwargs):
            pass

        def parse_args(self, *args, **kwargs):
            class Args(object):
                def __init__(self):
                    self.args_json = str(args_path)
                    self.out_json = str(tmp_path / "metadiff.json")

            return Args()

    import fractal_task_tools.task_wrapper  # noqa: F401

    monkeypatch.setattr(
        "fractal_task_tools.task_wrapper.ArgumentParser",
        MockArgumentParser,
    )

    # Success
    args = dict(zarr_url="/somewhere", parameter=1.0)
    debug(args)
    with args_path.open("w") as f:
        json.dump(args, f, indent=2)
    function_output = run_fractal_task(task_function=fake_task)
    assert function_output is None
    with (tmp_path / "metadiff.json").open("r") as f:
        task_output = json.load(f)
    assert task_output == TASK_OUTPUT

    # Failure
    caplog.clear()
    with pytest.raises(SystemExit):
        run_fractal_task(task_function=fake_task)
    assert "already exists" in caplog.text

    # Failure
    (tmp_path / "metadiff.json").unlink()
    args = dict(zarr_url="/somewhere", parameter=None)
    debug(args)
    with args_path.open("w") as f:
        json.dump(args, f, indent=2)
    with pytest.raises(
        ValidationError, match="validation error for fake_task"
    ):
        run_fractal_task(task_function=fake_task)
