import inspect
import logging
from importlib import import_module
from inspect import Signature
from inspect import signature
from pathlib import Path
from typing import Any
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined
from ._union_types import is_annotated_union
from ._union_types import is_tagged
from ._union_types import is_union
from pydantic import BaseModel

logger = logging.getLogger(__name__)

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

MAX_RECURSION_LEVEL = 7


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
        logger.info(
            f"Now calling `import_module` for "
            f"{package_name}.{module_relative_path_dots}"
        )
    imported_module = import_module(f"{package_name}.{module_relative_path_dots}")
    if verbose:
        logger.info(
            f"Now getting attribute {function_name} from "
            f"imported module {imported_module}."
        )
    task_function = getattr(imported_module, function_name)
    return task_function


def _validate_plain_union(
    *,
    name: str,
    annotation: Any,  # FIXME type hint
    default_value: Any,
) -> None:
    """
    Fail for known cases of invalid plain-union types.

    A plain union annotation is (by construction) one for which
    `is_union(_type) = True`. The only supported forms of plain unions
    are `X | None` or `X | None = None` (or equivalent forms).

    Note that `Optional[X]` is equivalent to `X | None` and thus it also gets
    validated through this function.

    Args:
        name: Name of the annotation to validate.
        annotation:
            Plain-union annotation to validate. Note that this may be equal to
            `param.annotation` (in a non-`Annotated` case) or to
            `param.annotation.__origin__` (when the original annotation is an
            `Annotated` union).
        default_value: Default value.param: The full `inspect.Parameter` object.
    """

    logger.debug(
        f"[_validate_plain_union] START for {name=}, {annotation=}, {default_value=}."
    )

    args = annotation.__args__
    if len(args) != 2:
        raise ValueError(
            "Only unions of two elements are supported, but parameter "
            f"'{name}' has type hint '{annotation}'."
        )
    elif not any(arg is type(None) for arg in args):
        raise ValueError(
            "One union element must be None, but parameter "
            f"'{name}' has type hint '{annotation}'."
        )
    else:
        if default_value not in (None, inspect._empty):
            raise ValueError(
                "Non-None default not supported, but parameter "
                f"'{name}' has type hint '{annotation}' "
                f"and default {default_value}."
            )

    logger.debug(
        f"[_validate_plain_union] END for {name=}, {annotation=}, {default_value=}."
    )


def _extract_default_from_field_info(field_info: FieldInfo) -> Any:
    if field_info.default is not PydanticUndefined:
        # Example: `arg: int | None = Field(default=7)`
        return field_info.default
    elif field_info.default_factory in (PydanticUndefined, None):
        # Example: `arg: int | None = Field(description="abc")`
        return inspect._empty
    elif field_info.default_factory_takes_validated_data:
        # Example: `arg: int | None = Field(default_factory=lambda _: 7)`
        return inspect._empty
    else:
        # Example: `arg: int | None = Field(default_factory=lambda : 7)`
        return field_info.default_factory()


def _recursive_union_validation(
    *,
    name: str,
    annotation: Any,  # FIXME type hint
    default_value: Any,
    recursion_level: int,
) -> None:
    """
    Recursive function for union validation.

    This function browses a tree of annotations, and validate the annotation of
    each node (if it is a union). Each Pydantic-model node then branches into
    additional nodes, while non-Pydantic-model nodes are the final node of their
    branch.

    Args:
        annotation: The annotation of the current node.
        name: The name of the current node.
        default_value: The default value for the current node.
        recursion_level:
    """

    logger.info(
        f"[_recursive_union_validation] {name=}, {annotation=}, {default_value=}"
    )

    if recursion_level >= MAX_RECURSION_LEVEL:
        raise ValueError(f"{recursion_level=} reached {MAX_RECURSION_LEVEL}.")

    if isinstance(default_value, FieldInfo):
        default_value = _extract_default_from_field_info(default_value)

    # Validate plain unions or non-tagged annotated unions
    if is_union(annotation):
        logger.debug(f"[_recursive_union_validation] {name=} is a union.")
        _validate_plain_union(
            annotation=annotation,
            name=name,
            default_value=default_value,
        )
    elif is_annotated_union(annotation):
        if not is_tagged(annotation):
            logger.debug(
                f"[_recursive_union_validation] {name=} is a non-tagged annotated union."
            )
            _validate_plain_union(
                annotation=annotation.__origin__,
                name=name,
                default_value=default_value,
            )

    if type(annotation) is type(BaseModel):
        for attribute_name, field_info in annotation.model_fields.items():
            _recursive_union_validation(
                name=f"{name}['{attribute_name}']",
                annotation=__annotations__.get(attribute_name, field_info.annotation),
                default_value=_extract_default_from_field_info(field_info),
                recursion_level=(recursion_level + 1),
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
    logger.info(f"[_validate_function_signature] START {function.__name__}")
    sig = signature(function)
    for param in sig.parameters.values():
        # Check that name is not forbidden
        if param.name in FORBIDDEN_PARAM_NAMES:
            raise ValueError(
                f"Function {function} has argument with forbidden name '{param.name}'"
            )

        _recursive_union_validation(
            annotation=param.annotation,
            name=param.name,
            default_value=param.default,
            recursion_level=0,
        )

    logger.info("[_validate_function_signature] END")
    return sig
