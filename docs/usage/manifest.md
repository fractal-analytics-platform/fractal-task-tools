# Tasks manifest

## Build and check manifest

`fractal-task-tools` includes a set of [task models](../reference/fractal_task_tools/task_models.md), to be used in the `task_list.py` module.
See the following example from the `fractal-tasks-core` package:
```python
from fractal_task_tools.task_models import ConverterCompoundTask

TASK_LIST = [
    ConverterCompoundTask(
        name="Convert Cellvoyager to OME-Zarr",
        executable_init="tasks/cellvoyager_to_ome_zarr_init.py",
        executable="tasks/cellvoyager_to_ome_zarr_compute.py",
        meta_init={"cpus_per_task": 1, "mem": 4000},
        meta={"cpus_per_task": 1, "mem": 4000},
        category="Conversion",
        modality="HCS",
        tags=["Yokogawa", "Cellvoyager", "2D", "3D"],
        docs_info="file:task_info/convert_cellvoyager_to_ome_zarr.md",
    ),
]
```

Once the `task_list.py` module is defined, `fractal-task-tools` also includes a command-line interface for creating and checking a manifest file.

The [`create` command](../../reference/fractal-manifest/create/) can be used as in
```console
fractal-manifest create --package my-task-package
```
and it writes the manifest to a file called `__FRACTAL_MANIFEST__.json`, in the root folder where the package `my-task-package` is installed.

The [`check` command](../../reference/fractal-manifest/check/) can be used as in
```console
fractal-manifest check --package my-task-package
```
and it verifies that the on-disk manifest is up-to-date, which is useful e.g. as a continuous-integration step:


## JSON Schemas

Each task listed in the manifest is associated to a JSON Schema that represents its arguments (or two schemas, if the task has both a non-parallel and a parallel unit). These schemas are stored in the `args_schema_non_parallel` and `args_schema_parallel` properties of each task.

This kind of schemas are not used at task runtime (where the validity of task arguments is typically enforced by the [`@pydantic.validate_call` decorator](https://docs.pydantic.dev/latest/concepts/validation_decorator)), but they form the basis for constructing the [`fractal-web`](https://github.com/fractal-analytics-platform/fractal-web) user interface that lets a user edit task arguments.

The `args_schema_version` property, which is set at the manifest level, determines a set of constraints on the task-arguments schemas. What is described below applies to the current one as of `fractal-task-tools=0.4.0a3`, named `args_schema_version = "pydantic_v2"`. The discussion about an upcoming specification is tracked at https://github.com/fractal-analytics-platform/fractal-task-tools/issues/97.

### Restrictions on task functions

Some patterns are forbidden in the Python functions representing Fractal tasks.

#### Argument names

The following keywords are reserved and cannot be used for a task-argument name:

- `"args"`
- `"kwargs"`
- `"v__args"`
- `"v__kwargs"`
- `"v__duplicate_kwargs"`
- `"v__positional_only"`

#### Union types

When top-level task arguments or nested properties have a *union* type annotation, it must be one of the two supported cases described below

##### Supported case 1: Plain binary unions with `None`

The first supported case is the one of an union of a given type and `None`. If the default is set, it must be `None`. Here are some examples of supported and non-supported type annotations for task arguments:
```python
from pydantic import Field

def task_function_ok(
    arg1: int | None,
    arg2: int | None = None,
    arg3: int | None = Field(default=None),
    arg4: int | None = Field(default_factory=lambda: None),
    arg5: Optional[int],
    arg6: Annotated[int | None, "a comment"],
    arg7: Annotated[int | None, "a comment"] = None,
    arg8: Annotated[int | None, "a comment"] = Field(default=None),
    arg9: int | None = Field(default_factory=lambda _: 7),  # Since the factory requires additional data, it is ignored and the default is not populated.
):
    pass

def task_function_bad(
    arg1: int | str,
    arg2: int | str | None,
    arg3: int | None = 1,
    arg4: int | None = Field(default=1),
    arg5: int | None = Field(default_factory=lambda: 1),
):
    pass
```

##### Supported case 2: Tagged unions

The second supported case is the one of a _tagged_ union, see e.g. https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions-with-str-discriminators.

Here is a supported example:
```python
from typing import Literal
from typing import Annotated

class Model1(BaseModel):
    label: Literal["label1"] = "label1"
    field1: int = 1


class Model2(BaseModel):
    label: Literal["label2"] = "label2"
    field1: int
    field2: str

MyTaggedUnion = Annotated[Model1 | Model2, Field(discriminator="label")]

def task_function_ok(
    arg1: MyTaggedUnion,
):
    pass

```

### Customizations of schema generation

The general approach for customizing the Pydantic schema-generation procedure is described at https://docs.pydantic.dev/latest/concepts/json_schema/#customizing-the-json-schema-generation-process.

In `fractal-task-tools`, this includes the following customizations (which are applied at all levels, that is, both for top-level task arguments and for nested properties):

1. When the generated schema includes an `anyOf` array, we remove any `{"type": "null"}` element from it.
2. When the generated schema includes a `default` value which is set to `null`, we remove it.
3. The the type annotation is a `Field` with a `default_factory` which is set and which does not require any argument, we compute the `default` value as `default_factory()`.
