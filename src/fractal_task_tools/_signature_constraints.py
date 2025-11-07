import inspect
import logging
from importlib import import_module
from inspect import signature
from pathlib import Path

from pydantic.v1.decorator import ALT_V_ARGS
from pydantic.v1.decorator import ALT_V_KWARGS
from pydantic.v1.decorator import V_DUPLICATE_KWARGS
from pydantic.v1.decorator import V_POSITIONAL_ONLY_NAME

from ._union_types import is_union

FORBIDDEN_PARAM_NAMES = (
    "args",
    "kwargs",
    V_POSITIONAL_ONLY_NAME,
    V_DUPLICATE_KWARGS,
    ALT_V_ARGS,
    ALT_V_KWARGS,
)


def _extract_function(
    module_relative_path: str,
    function_name: str,
    package_name: str,
    verbose: bool = False,
) -> callable:
    """
    Extract function from a module with the same name.

    Args:
        package_name: Example `fractal_tasks_core`.
        module_relative_path: Example `tasks/create_ome_zarr.py`.
        function_name: Example `create_ome_zarr`.
        verbose:
    """
    if not module_relative_path.endswith(".py"):
        raise ValueError(f"{module_relative_path=} must end with '.py'")
    module_relative_path_no_py = str(
        Path(module_relative_path).with_suffix("")
    )
    module_relative_path_dots = module_relative_path_no_py.replace("/", ".")
    if verbose:
        logging.info(
            f"Now calling `import_module` for "
            f"{package_name}.{module_relative_path_dots}"
        )
    imported_module = import_module(
        f"{package_name}.{module_relative_path_dots}"
    )
    if verbose:
        logging.info(
            f"Now getting attribute {function_name} from "
            f"imported module {imported_module}."
        )
    task_function = getattr(imported_module, function_name)
    return task_function


def _validate_function_signature(function: callable):
    """
    Validate the function signature.

    Implement a set of checks for type hints that do not play well with the
    creation of JSON Schema, see
    https://github.com/fractal-analytics-platform/fractal-tasks-core/issues/399.

    Args:
        function: TBD
    """
    sig = signature(function)
    for param in sig.parameters.values():
        # CASE 1: Check that name is not forbidden
        if param.name in FORBIDDEN_PARAM_NAMES:
            raise ValueError(
                f"Function {function} has argument with forbidden "
                f"name '{param.name}'"
            )

        annotation_is_union = is_union(param.annotation)
        annotation_str = str(param.annotation)
        annotation_has_default = (param.default is not None) and (
            param.default != inspect._empty
        )

        if annotation_is_union:
            if annotation_str.count("|") > 1 or annotation_str.count(",") > 1:
                raise ValueError(
                    "Only unions of two elements are supported, but parameter "
                    f"'{param.name}' has type hint '{annotation_str}'."
                )
            elif (
                "None" not in annotation_str
                and "Optional[" not in annotation_str
            ):
                raise ValueError(
                    "One union element must be None, but parameter "
                    f"'{param.name}' has type hint '{annotation_str}'."
                )
            elif annotation_has_default:
                raise ValueError(
                    "Non-None default not supported, but parameter "
                    f"'{param.name}' has type hint '{annotation_str}' "
                    f"and default {param.default}."
                )

    logging.info("[_validate_function_signature] END")
    return sig
