"""
Standard input/output interface for tasks.
"""
import json
import logging
from argparse import ArgumentParser
from json import JSONEncoder
from pathlib import Path
from typing import Optional


class TaskParameterEncoder(JSONEncoder):
    """
    Custom JSONEncoder that transforms Path objects to strings.

    Ref https://docs.python.org/3/library/json.html
    """

    def default(self, obj):
        if isinstance(obj, Path):
            return obj.as_posix()
        return super().default(obj)


def run_fractal_task(
    *,
    task_function: callable,
    logger_name: Optional[str] = None,
):
    """
    Implement standard task interface and call task_function.

    Args:
        task_function: the callable function that runs the task.
        logger_name: TBD
    """

    # Parse `-j` and `--metadata-out` arguments
    parser = ArgumentParser()
    parser.add_argument(
        "--args-json", help="Read parameters from json file", required=True
    )
    parser.add_argument(
        "--out-json",
        help="Output file to redirect serialised returned data",
        required=True,
    )
    parsed_args = parser.parse_args()

    # Set logger
    logger = logging.getLogger(logger_name)

    # Preliminary check
    if Path(parsed_args.out_json).exists():
        logger.error(
            f"Output file {parsed_args.out_json} already exists. Terminating"
        )
        exit(1)

    # Read parameters dictionary
    with open(parsed_args.args_json, "r") as f:
        pars = json.load(f)

    # Run task
    logger.info(f"START {task_function.__name__} task")
    metadata_update = task_function(**pars)
    logger.info(f"END {task_function.__name__} task")

    # Write output metadata to file, with custom JSON encoder
    with open(parsed_args.out_json, "w") as fout:
        json.dump(metadata_update, fout, cls=TaskParameterEncoder, indent=2)
