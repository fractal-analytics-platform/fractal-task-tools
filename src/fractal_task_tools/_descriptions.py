import ast
import logging
import os
from importlib import import_module
from pathlib import Path
from typing import Optional

from docstring_parser import parse as docparse


def _sanitize_description(string: str) -> str:
    """
    Sanitize a description string.

    This is a provisional helper function that replaces newlines with spaces
    and reduces multiple contiguous whitespace characters to a single one.
    Future iterations of the docstrings format/parsing may render this function
    not-needed or obsolete.

    Args:
        string: TBD
    """
    # Replace newline with space
    new_string = string.replace("\n", " ")
    # Replace N-whitespace characters with a single one
    while "  " in new_string:
        new_string = new_string.replace("  ", " ")
    return new_string


def _get_function_docstring(
    *,
    package_name: Optional[str],
    module_path: str,
    function_name: str,
    verbose: bool = False,
) -> str:
    """
    Extract docstring from a function.


    Args:
        package_name: Example `fractal_tasks_core`.
        module_path:
            This must be an absolute path like `/some/module.py` (if
            `package_name` is `None`) or a relative path like `something.py`
            (if `package_name` is not `None`).
        function_name: Example `create_ome_zarr`.
    """

    if not module_path.endswith(".py"):
        raise ValueError(f"Module {module_path} must end with '.py'")

    # Get the function ast.FunctionDef object
    if package_name is not None:
        if os.path.isabs(module_path):
            raise ValueError(
                "Error in _get_function_docstring: `package_name` is not "
                "None but `module_path` is absolute."
            )
        package_path = Path(import_module(package_name).__file__).parent
        module_path = package_path / module_path
    else:
        if not os.path.isabs(module_path):
            raise ValueError(
                "Error in _get_function_docstring: `package_name` is None "
                "but `module_path` is not absolute."
            )
        module_path = Path(module_path)

    if verbose:
        logging.info(f"[_get_function_docstring] {function_name=}")
        logging.info(f"[_get_function_docstring] {module_path=}")

    tree = ast.parse(module_path.read_text())
    _function = next(
        f
        for f in ast.walk(tree)
        if (isinstance(f, ast.FunctionDef) and f.name == function_name)
    )

    # Extract docstring from ast.FunctionDef
    return ast.get_docstring(_function)


def _get_function_args_descriptions(
    *,
    package_name: Optional[str],
    module_path: str,
    function_name: str,
    verbose: bool = False,
) -> dict[str, str]:
    """
    Extract argument descriptions from a function.

    Args:
        package_name: Example `fractal_tasks_core`.
        module_path:
            This must be an absolute path like `/some/module.py` (if
            `package_name` is `None`) or a relative path like `something.py`
            (if `package_name` is not `None`).
        function_name: Example `create_ome_zarr`.
    """

    # Extract docstring from ast.FunctionDef
    docstring = _get_function_docstring(
        package_name=package_name,
        module_path=module_path,
        function_name=function_name,
        verbose=verbose,
    )
    if verbose:
        logging.info(f"[_get_function_args_descriptions] {docstring}")

    # Parse docstring (via docstring_parser) and prepare output
    parsed_docstring = docparse(docstring)
    descriptions = {
        param.arg_name: _sanitize_description(param.description)
        for param in parsed_docstring.params
    }
    logging.info(f"[_get_function_args_descriptions] END ({function_name=})")
    return descriptions


def _insert_function_args_descriptions(
    *, schema: dict, descriptions: dict, verbose: bool = False
):
    """
    Merge the descriptions obtained via `_get_args_descriptions` into the
    properties of an existing JSON Schema.

    Args:
        schema: TBD
        descriptions: TBD
    """
    new_schema = schema.copy()
    new_properties = schema["properties"].copy()
    for key, value in schema["properties"].items():
        if "description" in value:
            # This branch covers e.g. the `Field(description="...")` case
            pass
        else:
            value["description"] = descriptions.get(key, "Missing description")
            new_properties[key] = value
            if verbose:
                logging.info(
                    f"[_insert_function_args_descriptions] Add {key=}, {value=}"
                )
    new_schema["properties"] = new_properties
    logging.info("[_insert_function_args_descriptions] END")
    return new_schema
