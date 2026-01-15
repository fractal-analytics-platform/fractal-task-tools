import inspect
import logging
from enum import Enum
from importlib import import_module
from inspect import Parameter
from inspect import signature
from pathlib import Path

from ._union_types import is_annotated_union
from ._union_types import is_tagged
from ._union_types import is_union


# The following variables are copied from `pydantic.v1.decorator`
# (for pydantic v2.11.10)
ALT_V_ARGS = "v__args"
ALT_V_KWARGS = "v__kwargs"
V_DUPLICATE_KWARGS = "v__duplicate_kwargs"
V_POSITIONAL_ONLY_NAME = "v__positional_only"

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


class UnionCases(str, Enum):
    NON_UNION = "non_union"
    PLAIN_UNION = "plain_union"
    TAGGED_ANNOTATED_UNION = "tagged_annotated_union"
    NON_TAGGED_ANNOTATED_UNION = "non_tagged_annotated_union"


def validate_plain_union(
    *,
    _type,
    param: Parameter,
) -> None:
    annotation_str = str(_type)
    # FIXME: could we avoid annotation_str and be more precise?
    if annotation_str.count("|") > 1 or annotation_str.count(",") > 1:
        raise ValueError(
            "Only unions of two elements are supported, but parameter "
            f"'{param.name}' has type hint '{annotation_str}'."
        )
    elif "None" not in annotation_str and "Optional[" not in annotation_str:
        raise ValueError(
            "One union element must be None, but parameter "
            f"'{param.name}' has type hint '{annotation_str}'."
        )
    elif (param.default is not None) and (param.default != inspect._empty):
        raise ValueError(
            "Non-None default not supported, but parameter "
            f"'{param.name}' has type hint '{annotation_str}' "
            f"and default {param.default}."
        )


def _validate_function_signature(function: callable):
    """
    Validate the function signature.

    Implement a set of checks for type hints that do not play well with the
    creation of JSON Schema, see
    https://github.com/fractal-analytics-platform/fractal-tasks-core/issues/399.
    and
    https://github.com/fractal-analytics-platform/fractal-task-tools/issues/65

    Args:
        function: TBD
    """
    sig = signature(function)
    for param in sig.parameters.values():
        # CASE 1: Check that name is not forbidden
        if param.name in FORBIDDEN_PARAM_NAMES:
            raise ValueError(
                f"Function {function} has argument with "
                f"forbidden name '{param.name}'"
            )

        if is_union(param.annotation):
            what_kind_of_union = UnionCases.PLAIN_UNION
        elif is_annotated_union(param.annotation):
            if is_tagged(param.annotation):
                what_kind_of_union = UnionCases.TAGGED_ANNOTATED_UNION
            else:
                what_kind_of_union = UnionCases.NON_TAGGED_ANNOTATED_UNION
        else:
            what_kind_of_union = UnionCases.NON_UNION

        match what_kind_of_union:
            case UnionCases.PLAIN_UNION:
                validate_plain_union(_type=param.annotation, param=param)
            case UnionCases.NON_TAGGED_ANNOTATED_UNION:
                validate_plain_union(
                    _type=param.annotation.__origin__, param=param
                )
            case UnionCases.TAGGED_ANNOTATED_UNION:
                pass
            case UnionCases.NON_UNION:
                pass

    logging.info("[_validate_function_signature] END")
    return sig
