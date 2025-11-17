# Install `fractal-tasks-tools`

Fractal Task Tools is hosted on [the PyPI
index](https://pypi.org/project/fractal-task-tools), and it can be installed with
`pip` via
```
pip install fractal-task-tools
```

# Use `fractal-task-tools`

The `fractal-task-tools` package mainly includes two main features:

1. Tools for building the manifest for a package of Fractal tasks.
2. A `run_fractal_task` wrapper that wraps a Python function into a command-line interface, meant to be used from within the Fractal framework.

## Build manifest for your Fractal-tasks package

`fractal-task-tools` includes a set of [task models](./reference/fractal_task_tools/task_models.md), to be used in the `task_list.py` module.
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

Once the `task_list.py` module is defined, `fractal-task-tools` also includes a [command-line interface for creating (or checking) a manifest file](./reference/fractal-manifest/index.md). This can be used e.g. as in
```console
fractal-manifest --package my-task-package
```
and it will write the manifest to a file called `__FRACTAL_MANIFEST__.json`, in the root folder where the package `my-task-package` is installed.


## Run tasks through Fractal

Within the Fractal framework, tasks are run as executable commands with a given signature, which looks like
```console
python task.py --args-json /path/to/arguments.json --out-json /path/to/output/metadata.json
```
The [`run_fractal_task`](./reference/fractal_task_tools/task_wrapper.md#fractal_task_tools.task_wrapper.run_fractal_task) wrapper converts a Python function into such a command-line interface, as in
```python
from fractal_task_tools.task_wrapper import run_fractal_task

if __name__ == "__main__":
    run_fractal_task(task_function=some_function)
```


# Migrate from `fractal-tasks-core`

1. Add `fractal_task_tools` as a required dependency for your task package.
2. In the `task_list.py` file of your package, import task models from `fractal_task_tools.task_models` (rather than `fractal_tasks_core.dev.task_models`), as in
```python
from fractal_task_tools.task_models import CompoundTask
from fractal_task_tools.task_models import NonParallelTask
from fractal_task_tools.task_models import ConverterCompoundTask
from fractal_task_tools.task_models import ConverterNonParallelTask
from fractal_task_tools.task_models import ParallelTask
```

2. If some of your tasks are converters (that is, they create OME-Zarr images but do not take any OME-Zarr image as an input), you can now use one of the new available task types (`ConverterCompoundTask` and `ConverterNonParallelTask`).

3. In the `task_list.py` file of your package, optionally include variables for `AUTHORS`, `DOCS_LINK` and `INPUT_MODELS` (if applicable), as in this example:
```python
AUTHORS = "Fractal Core Team"
DOCS_LINK = "https://fractal-analytics-platform.github.io/fractal-tasks-core"
INPUT_MODELS = [
    ["fractal_tasks_core", "channels.py", "OmeroChannel"],
    ["fractal_tasks_core", "channels.py", "Window"],
    ["fractal_tasks_core", "channels.py", "ChannelInputModel"],
    ...
  ]
```

4. In order to create the manifest for your package and write it to disk (within the root directory of the installed package), use
```
fractal-manifest create --package my-fractal-tasks-package
```
This command replaces the custom `create_manifest.py` script, that you can now delete.

5. In order to check that the manifest for your package is up to date (e.g. from within the CI), use
```
fractal-manifest check --package my-fractal-tasks-package
```
This command replaces the custom logic often included in GitHub Actions, which re-creates the manifest and then run a `git diff` to see if it changed.

6. For each one of your tasks' modules, replace the `import` from `fractal_tasks_core.tasks._utils` with
```python
from fractal_task_tools.task_wrapper import run_fractal_task
```
