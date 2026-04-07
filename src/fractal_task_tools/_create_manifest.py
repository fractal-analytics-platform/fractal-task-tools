"""
Generate JSON schemas for task arguments and combine them into a manifest.
"""

import logging
from importlib import import_module
from pathlib import Path
from typing import Any

import fractal_task_tools

from ._args_schemas import create_schema_for_single_task
from ._package_name_tools import normalize_package_name
from ._parse_pyproject import get_author_names_from_pyproject
from ._specs import validate_schema
from ._task_arguments import validate_arguments
from ._task_docs import create_docs_info
from ._task_docs import read_docs_info_from_file
from .task_models import _BaseTask

ARGS_SCHEMA_VERSION = "fractal_schema_v1"
MANIFEST_FILENAME = "__FRACTAL_MANIFEST__.json"
MANIFEST_VERSION = "2"


logger = logging.getLogger(__name__)


def create_manifest(
    *,
    raw_package_name: str,
    task_list_path: str,
    verbose: bool = False,
) -> dict[str, Any]:
    """
    Create the package manifest based on a `task_list.py` module

    Arguments:
        raw_package_name:
            The name of the package. Note that this name must be importable
            (after normalization).
        task_list_path:
            Relative path to the `task_list.py` module, with respect to the
            package root (example `dev.task_list`).
        verbose: Whether to print more verbose logs.

    Returns:
        Task-package manifest.
    """

    # Preliminary validation
    if "/" in task_list_path or task_list_path.endswith(".py"):
        raise ValueError(f"Invalid {task_list_path=} (valid example: `dev.task_list`).")

    # Normalize package name
    package_name = normalize_package_name(raw_package_name)

    logger.info(f"fractal-task-tools version: {fractal_task_tools.__VERSION__}")
    logger.info(f"Start generating a new manifest for {package_name}")

    # Prepare an empty manifest
    manifest = dict(
        manifest_version=MANIFEST_VERSION,
        task_list=[],
        has_args_schemas=True,
        args_schema_version=ARGS_SCHEMA_VERSION,
        authors=None,
    )

    # Import the task-list module
    task_list_module = import_module(f"{package_name}.{task_list_path}")

    # Load TASK_LIST
    TASK_LIST: list[_BaseTask] = getattr(task_list_module, "TASK_LIST")

    # Load AUTHORS
    AUTHORS = getattr(task_list_module, "AUTHORS", None)
    if AUTHORS is None:
        logger.warning("No `AUTHORS` found in task_list module.")
        AUTHORS = get_author_names_from_pyproject(Path.cwd() / "pyproject.toml")
    manifest["authors"] = AUTHORS

    # Load DOCS_LINK
    try:
        DOCS_LINK = getattr(task_list_module, "DOCS_LINK")
        # Transform empty string into None
        if DOCS_LINK == "":
            DOCS_LINK = None
            logger.warning("`DOCS_LINK=` transformed into `DOCS_LINK=None`.")
    except AttributeError:
        DOCS_LINK = None
        logger.warning("No `DOCS_LINK` found in task_list module.")

    # Loop over TASK_LIST, and append the proper task dictionaries
    # to manifest["task_list"]
    for task_obj in TASK_LIST:
        # Convert Pydantic object to dictionary
        task_dict = task_obj.model_dump(
            exclude={
                "meta_init",
                "executable_init",
                "meta",
                "executable",
            },
            exclude_unset=True,
        )
        task_dict["type"] = task_obj.type

        # Copy some properties from `task_obj` to `task_dict`
        if task_obj.executable_non_parallel is not None:
            task_dict["executable_non_parallel"] = task_obj.executable_non_parallel
        if task_obj.executable_parallel is not None:
            task_dict["executable_parallel"] = task_obj.executable_parallel
        if task_obj.meta_non_parallel is not None:
            task_dict["meta_non_parallel"] = task_obj.meta_non_parallel
        if task_obj.meta_parallel is not None:
            task_dict["meta_parallel"] = task_obj.meta_parallel

        # Autogenerate JSON Schemas for non-parallel/parallel task arguments
        for kind in ["non_parallel", "parallel"]:
            executable = task_dict.get(f"executable_{kind}")
            if executable is not None:
                logger.info(f"[{executable}] START")
                schema = create_schema_for_single_task(
                    executable,
                    package=package_name,
                    verbose=verbose,
                )

                validate_arguments(
                    task_type=task_obj.type,
                    schema=schema,
                    executable_kind=kind,
                )

                validate_schema(
                    schema=schema,
                    path=schema["title"],
                    verbose=verbose,
                )

                logger.info(f"[{executable}] END (new schema)")
                task_dict[f"args_schema_{kind}"] = schema

        # Compute and set `docs_info`
        docs_info = task_dict.get("docs_info")
        if docs_info is None:
            docs_info = create_docs_info(
                executable_non_parallel=task_obj.executable_non_parallel,
                executable_parallel=task_obj.executable_parallel,
                package=package_name,
            )
        elif docs_info.startswith("file:"):
            docs_info = read_docs_info_from_file(
                docs_info=docs_info,
                task_list_path=task_list_module.__file__,
            )
        if docs_info is not None:
            task_dict["docs_info"] = docs_info

        # Set `docs_link`
        if DOCS_LINK is not None:
            task_dict["docs_link"] = DOCS_LINK

        # Append task
        manifest["task_list"].append(task_dict)
    return manifest
