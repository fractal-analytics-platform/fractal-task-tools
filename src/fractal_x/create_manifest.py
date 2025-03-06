"""
Script to generate JSON schemas for task arguments afresh, and write them
to the package manifest.
"""

import json
import logging
from importlib import import_module
from pathlib import Path
from typing import Optional

from .lib_args_schemas import (
    create_schema_for_single_task,
)
from .lib_task_docs import create_docs_info
from .lib_task_docs import read_docs_info_from_file
from .task_models import CompoundTask, NonParallelTask, ParallelTask
from .package_names import normalize_package_name


ARGS_SCHEMA_VERSION = "pydantic_v2"


def create_manifest(
    package: str,
    task_list_file: str,
    authors: Optional[str] = None,
    manifest_version: str = "2",
    has_args_schemas: bool = True,
    docs_link: Optional[str] = None,
    custom_pydantic_models: Optional[list[tuple[str, str, str]]] = None,
):
    """
    This function creates the package manifest based on a `task_list.py`
    Python module located in the `dev` subfolder of the package, see an
    example of such list at ...

    The manifest is then written to `__FRACTAL_MANIFEST__.json`, in the
    main `package` directory.

    Note: a valid example of `custom_pydantic_models` would be
    ```
    [
        ("my_task_package", "some_module.py", "SomeModel"),
    ]
    ```

    Arguments:
        package: The name of the package (must be importable).
        manifest_version: Only `"2"` is supported.
        has_args_schemas:
            Whether to autogenerate JSON Schemas for task arguments.
        custom_pydantic_models:
            Custom models to be included when building JSON Schemas for task
            arguments.
    """

    # Preliminary check
    if manifest_version != "2":
        raise NotImplementedError(f"{manifest_version=} is not supported")


    # Normalize package name
    package = normalize_package_name(package)
    package = package.replace("-", "_")
    from devtools import debug
    debug(package)

    logging.info("Start generating a new manifest")

    # Prepare an empty manifest
    manifest = dict(
        manifest_version=manifest_version,
        task_list=[],
        has_args_schemas=has_args_schemas,
    )
    if has_args_schemas:
        manifest["args_schema_version"] = ARGS_SCHEMA_VERSION
    if authors is not None:
        manifest["authors"] = authors

    # Import the task list from `dev/task_list.py`
    with open(task_list_file, "r") as f:
        TASK_LIST_JSON = json.load(f)

    TASK_LIST = []
    for task_json in TASK_LIST_JSON:
        task_type = task_json.pop("type")
        debug(task_type)
        if task_type == "compound":
            task = CompoundTask(**task_json)
        elif task_type == "parallel":
            task = ParallelTask(**task_json)
        elif task_type == "non-parallel":
            task = NonParallelTask(**task_json)
        else:
            raise
        TASK_LIST.append(task)
    debug(TASK_LIST)

    # Loop over TASK_LIST, and append the proper task dictionary
    # to manifest["task_list"]
    for task_obj in TASK_LIST:
        # Convert Pydantic object to dictionary
        task_dict = task_obj.model_dump(
            exclude={"meta_init", "executable_init", "meta", "executable"},
            exclude_unset=True,
        )

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
        if has_args_schemas:
            for kind in ["non_parallel", "parallel"]:
                executable = task_dict.get(f"executable_{kind}")
                if executable is not None:
                    logging.info(f"[{executable}] START")
                    schema = create_schema_for_single_task(
                        executable,
                        package=package,
                        pydantic_models=custom_pydantic_models,
                    )
                    logging.info(f"[{executable}] END (new schema)")
                    task_dict[f"args_schema_{kind}"] = schema

        # Update docs_info, based on task-function description
        docs_info = task_dict.get("docs_info")
        if docs_info is None:
            docs_info = create_docs_info(
                executable_non_parallel=task_obj.executable_non_parallel,
                executable_parallel=task_obj.executable_parallel,
                package=package,
            )
        elif docs_info.startswith("file:"):
            docs_info = read_docs_info_from_file(
                docs_info=docs_info,
                task_list_path=task_list_file,
            )

        if docs_info is not None:
            task_dict["docs_info"] = docs_info
        if docs_link is not None:
            task_dict["docs_link"] = docs_link

        manifest["task_list"].append(task_dict)
        print()

    # Write manifest
    imported_package = import_module(package)
    manifest_path = Path(imported_package.__file__).parent / "__FRACTAL_MANIFEST__.json"
    with manifest_path.open("w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    logging.info(f"Manifest stored in {manifest_path.as_posix()}")


def main():
    PACKAGE = "fractal_tasks_core"
    AUTHORS = "Fractal Core Team"
    create_manifest(package=PACKAGE, authors=AUTHORS)
