# Install `fractal-tasks-tools`

Fractal Task Tools is hosted on [the PyPI
index](https://pypi.org/project/fractal-task-tools), and it can be installed with
`pip` via
```
pip install fractal-task-tools
```

# Use `fractal-tasks-tools`

## Build tasks manifest

-- IN PROGRESS --

See details about:
* [The `fractal-manifest` command-line interface](/reference/fractal-task-tools/fractal-manifest).
* The [task models](/reference/fractal-task-tools/fractal_task_tools/task_models) to be used in `task_list.py`.

## Run tasks

-- IN PROGRESS --


# Migrate from `fractal-tasks-core`

## Build tasks manifest

1. In the `task_list.py` file of your package, replace `import`s from `fractal_tasks_core.dev.task_models` with
```python
from fractal_task_tools.task_models import CompoundTask
from fractal_task_tools.task_models import NonParallelTask
from fractal_task_tools.task_models import ParallelTask
```

2. In the `task_list.py` file of your package, include `AUTHORS`, `DOCS_LINK` and `INPUT_MODELS` (if applicable), as in this example:
```python
AUTHORS = "Fractal Core Team"
DOCS_LINK = "https://fractal-analytics-platform.github.io/fractal-tasks-core"
INPUT_MODELS = [
    ["fractal_tasks_core", "channels.py", "OmeroChannel"],
    ["fractal_tasks_core", "channels.py", "Window"],
    ["fractal_tasks_core", "channels.py", "ChannelInputModel"],
    ["fractal_tasks_core", "tasks/io_models.py", "NapariWorkflowsInput"],
    ["fractal_tasks_core", "tasks/io_models.py", "NapariWorkflowsOutput"],
  ]
```

3. In order to create the manifest for your package and write to disk, use
```
fractal-manifest create --package my-fractal-tasks-package
```

4. In order to check that the manifest for your package is up to date (e.g. from within the CI), use
```
fractal-manifest check --package my-fractal-tasks-package
```


## Run tasks

For each one of your tasks' modules, replace the `import` from `fractal_tasks_core.tasks._utils` with
```python
from fractal_task_tools.task_wrapper import run_fractal_task
```
