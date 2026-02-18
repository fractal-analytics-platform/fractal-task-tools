import inspect
import logging
from importlib import import_module
from inspect import Parameter
from inspect import Signature
from inspect import signature
from pathlib import Path
from typing import Any
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined
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
    module_relative_path_no_py = str(Path(module_relative_path).with_suffix(""))
    module_relative_path_dots = module_relative_path_no_py.replace("/", ".")
    if verbose:
        logging.info(
            f"Now calling `import_module` for "
            f"{package_name}.{module_relative_path_dots}"
        )
    imported_module = import_module(f"{package_name}.{module_relative_path_dots}")
    if verbose:
        logging.info(
            f"Now getting attribute {function_name} from "
            f"imported module {imported_module}."
        )
    task_function = getattr(imported_module, function_name)
    return task_function


def _validate_plain_union(
    *,
    param: Parameter,
    _type: Any,
) -> None:
    """
    Fail for known cases of invalid plain-union types.

    A plain union annotation is (by construction) one for which
    `is_union(_type) = True`. The only supported forms of plain unions
    are `X | None` or `X | None = None` (or equivalent forms).

    Note that `Optional[X]` is equivalent to `X | None` and thus it also gets
    validated through this function.

    Args:
        param: The full `inspect.Parameter` object.
        _type:
            The type annotation to review. Note that this may be equal to
            `param.annotation` or to `param.annotation.__origin__` (when the
            original `param.annotation` is an `Annotated` union).
    """
    args = _type.__args__

    if len(args) != 2:
        raise ValueError(
            "Only unions of two elements are supported, but parameter "
            f"'{param.name}' has type hint '{_type}'."
        )
    elif not any(arg is type(None) for arg in args):
        raise ValueError(
            "One union element must be None, but parameter "
            f"'{param.name}' has type hint '{_type}'."
        )
    else:
        # Capture default from both `arg: str = "abc"` and
        # `arg: str = Field(default="abc")`
        if param.default == inspect._empty:
            # Default is not set
            _default = None
        elif not isinstance(param.default, FieldInfo):
            # Default is set directly, and not through `Field(default=123)`
            _default = param.default
        else:
            if param.default.default is PydanticUndefined:
                # `Field` is present, but with no `default`
                _default = None
            else:
                # Field(default=123) case
                _default = param.default.default

        if _default is not None:
            raise ValueError(
                "Non-None default not supported, but parameter "
                f"'{param.name}' has type hint '{_type}' "
                f"and default {_default}."
            )


def _validate_function_signature(function: callable) -> Signature:
    """
    Validate the function signature of a task.

    Implement a set of checks for type hints that do not play well with the
    creation of JSON Schema, see issue 399 in `fractal-tasks-core` and issue
    65 in `fractal-task-tools`.

    Args:
        function: A callable function.
    """
    sig = signature(function)
    for param in sig.parameters.values():
        # Check that name is not forbidden
        if param.name in FORBIDDEN_PARAM_NAMES:
            raise ValueError(
                f"Function {function} has argument with forbidden name '{param.name}'"
            )
        # Validate plain unions or non-tagged annotated unions
        if is_union(param.annotation):
            _validate_plain_union(
                _type=param.annotation,
                param=param,
            )
        elif is_annotated_union(param.annotation):
            if not is_tagged(param.annotation):
                _validate_plain_union(
                    _type=param.annotation.__origin__,
                    param=param,
                )
    logging.info("[_validate_function_signature] END")
    return sig
