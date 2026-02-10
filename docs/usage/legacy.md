# Migrate from legacy

1. Add `fractal-task-tools` as a required dependency for your task package.
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
