"""
Generate JSON schemas for task arguments and combine them into a manifest.
"""
import json
import logging
from importlib import import_module
from pathlib import Path
from typing import Any

from ._args_schemas import create_schema_for_single_task
from ._package_name_tools import normalize_package_name
from ._task_docs import create_docs_info
from ._task_docs import read_docs_info_from_file


ARGS_SCHEMA_VERSION = "pydantic_v2"
MANIFEST_FILENAME = "__FRACTAL_MANIFEST__.json"
MANIFEST_VERSION = "2"


def create_manifest(
    *,
    raw_package_name: str,
    task_list_path: str,
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

    Returns:
        Task-package manifest.
    """

    # Preliminary validation
    if "/" in task_list_path or task_list_path.endswith(".py"):
        raise ValueError(
            f"Invalid {task_list_path=} (valid example: `dev.task_list`)."
        )

    # Normalize package name
    package_name = normalize_package_name(raw_package_name)

    logging.info(f"Start generating a new manifest for {package_name}")

    # Prepare an empty manifest
    manifest = dict(
        manifest_version=MANIFEST_VERSION,
        has_args_schemas=True,
        args_schema_version=ARGS_SCHEMA_VERSION,
        task_list=[],
    )

    # Import the task-list module
    task_list_module = import_module(f"{package_name}.{task_list_path}")

    # Load TASK_LIST
    TASK_LIST = getattr(task_list_module, "TASK_LIST")

    # Load INPUT_MODELS
    try:
        INPUT_MODELS = getattr(task_list_module, "INPUT_MODELS")
    except AttributeError:
        INPUT_MODELS = []
        logging.warning(
            "No `INPUT_MODELS` found in task_list module. Setting it to `[]`."
        )

    # Load AUTHORS
    try:
        manifest["authors"] = getattr(task_list_module, "AUTHORS")
    except AttributeError:
        logging.warning("No `AUTHORS` found in task_list module.")

    # Load DOCS_LINK
    try:
        DOCS_LINK = getattr(task_list_module, "DOCS_LINK")
    except AttributeError:
        DOCS_LINK = None
        logging.warning("No `DOCS_LINK` found in task_list module.")

    # Loop over TASK_LIST, and append the proper task dictionaries
    # to manifest["task_list"]
    for task_obj in TASK_LIST:
        # Convert Pydantic object to dictionary
        task_dict = task_obj.model_dump(
            exclude={"meta_init", "executable_init", "meta", "executable"},
            exclude_unset=True,
        )

        # Copy some properties from `task_obj` to `task_dict`
        if task_obj.executable_non_parallel is not None:
            task_dict[
                "executable_non_parallel"
            ] = task_obj.executable_non_parallel
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
                logging.info(f"[{executable}] START")
                schema = create_schema_for_single_task(
                    executable,
                    package=package_name,
                    pydantic_models=INPUT_MODELS,
                )
                logging.info(f"[{executable}] END (new schema)")
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
        print()
    return manifest


def write_manifest_to_file(
    *,
    raw_package_name: str,
    manifest: str,
) -> None:
    """
    Write manifest to file.

    Arguments:
        raw_package_name:
        manifest: The manifest object
    """
    package_name = normalize_package_name(raw_package_name)
    imported_package = import_module(package_name)
    package_root_dir = Path(imported_package.__file__).parent
    manifest_path = package_root_dir / MANIFEST_FILENAME
    with manifest_path.open("w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    logging.info(f"Manifest stored in {manifest_path.as_posix()}")


def check_manifest_unchanged(
    *,
    raw_package_name: str,
    manifest: str,
) -> None:
    """
    Write manifest to file.

    Arguments:
        raw_package_name:
        manifest: The manifest object
    """
    package_name = normalize_package_name(raw_package_name)
    imported_package = import_module(package_name)
    package_root_dir = Path(imported_package.__file__).parent
    manifest_path = package_root_dir / MANIFEST_FILENAME
    with manifest_path.open("f") as f:
        old_manifest = json.load(f)
    logging.info(f"Manifest read from {manifest_path.as_posix()}")
    if manifest != old_manifest:
        raise ValueError("New/old manifests differ")
