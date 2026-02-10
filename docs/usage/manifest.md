# Build tasks manifest

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
