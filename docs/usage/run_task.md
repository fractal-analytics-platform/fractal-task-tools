# Run a task

Within the Fractal framework, tasks are run as executable commands with a given signature, which looks like
```console
python task.py --args-json /path/to/arguments.json --out-json /path/to/output/metadata.json
```

The [`run_fractal_task` wrapper](../reference/fractal_task_tools/task_wrapper.md#fractal_task_tools.task_wrapper.run_fractal_task) converts a Python function into such a command-line interface.
It can be used by writing a task Python module like
```python title="my_task.py"
from pydantic import validate_call

@validate_call
def my_task(
    zarr_url: str,
    argument_1: int,
):
    # This is the task function, which performs some image-processing task
    # ...

if __name__ == "__main__":
    from fractal_task_tools.task_wrapper import run_fractal_task
    run_fractal_task(task_function=my_task)
```
where the `if __name__ == "__main__"` block at the end is the one introducing the proper command-line interface.


## Log configuration

By default, the task wrapper sets a default format (`%(asctime)s; %(name)s; %(levelname)s; %(message)s`) and a default logging level (`INFO`) loggers based on the Python `logging` library. As an example, when running the following updated version of the example above
```python title="my_task_with_logs.py"
import logging
from pydantic import validate_call

logger = logging.getLogger("my_task_with_logs")

@validate_call
def my_task_with_logs(
    zarr_url: str,
    argument_1: int,
):
    # This is the task function, which performs some image-processing task
    # ...

    logger.debug(f"Here is a DEBUG log from the task.")
    logger.info(f"Here is an INFO log from the task.")
    logger.warning("Here is a WARNING log from the task")

if __name__ == "__main__":
    from fractal_task_tools.task_wrapper import run_fractal_task
    run_fractal_task(task_function=my_task_with_logs)
```
the logs look like
```
2026-02-10 09:31:33,338; run_fractal_task; INFO; START my_task task
2026-02-10 09:31:33,338; my_task_with_logs; INFO; Here is an INFO log from the task.
2026-02-10 09:31:33,339; my_task_with_logs; WARNING; Here is a WARNING log from the task
2026-02-10 09:31:33,339; run_fractal_task; INFO; END my_task task
```

The task developer can fully disable any logging configuration in the task wrapper by calling it as in
```python
run_fractal_task(task_function=my_task_with_logs, skip_logging_configuration=True)
```

The task user can customize the default format and logging level by setting any of the following environment variables:

* `FRACTAL_TASK_LOG_LEVEL`, which must be a value in `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.
* `FRACTAL_TASK_LOG_FORMAT`, which must be in the same style as the default value (`%(asctime)s; %(name)s; %(levelname)s; %(message)s`) and can include any attribute from https://docs.python.org/3/library/logging.html#logrecord-attributes.
* `FRACTAL_TASK_SKIP_LOG_CONFIG`: whenever this is set (to any arbitrary value), it has the same effect as `skip_logging_configuration=True`.
