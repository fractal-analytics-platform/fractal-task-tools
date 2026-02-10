# Run a task

Within the Fractal framework, tasks are run as executable commands with a given signature, which looks like
```console
python task.py --args-json /path/to/arguments.json --out-json /path/to/output/metadata.json
```
The [`run_fractal_task`](../reference/fractal_task_tools/task_wrapper.md#fractal_task_tools.task_wrapper.run_fractal_task) wrapper converts a Python function into such a command-line interface, as in
```python
from fractal_task_tools.task_wrapper import run_fractal_task

if __name__ == "__main__":
    run_fractal_task(task_function=some_function)
```
