# Task types

This page provides additional details about the task types supported by the [Fractal tasks specification](https://fractal-analytics-platform.github.io/tasks_spec).


There are five types of Fractal tasks:

1. [_parallel_ tasks](#parallel-tasks)
2. [_non-parallel_ tasks](#non-parallel-tasks)
3. [_compound_ tasks](#compound-tasks)
4. [_non-parallel converter_ tasks](#non-parallel-converter-tasks)
5. [_compound converter_ tasks](#compound-converter-tasks)


Task types differ in what required parameters they need, what kind of metadata they can produce, and how they run in Fractal server.

#### Parameters

Each task type has some required parameters. All required parameters mentioned below (`zarr_url`, `zarr_urls`, `zarr_dir`, `init_args`) are reserved keywords: when running tasks through Fractal server, the server takes care to pass the correct value for these arguments, and the user cannot set them directly. On top of the required parameters, each task also accepts an arbitrary list of other parameters that are specific to the task function and that the user can set.

#### Metadata

Tasks can optionally return updates to [the Fractal image list](https://fractal-analytics-platform.github.io/image_list) (this is true for all tasks except the initialization phase of a compound tasks) or a parallelization list (just the initialization phase of a compound task - see below).

The metadata produced by a task is always a Python dictionary, and **it must be JSON-serializable** (since it will be written to disk so that Fractal server can access it). The keys that let a task act on an existing image list are `image_list_updates` and `image_list_removals`, and both of them may have elements that must be identified by a `zarr_url`.
For more details see [the schema for this metadata dictionary](https://fractal-analytics-platform.github.io/fractal-server/reference/runner/v2/task_interface/#fractal_server.runner.v2.task_interface.TaskOutput) and the description of the [task-execution steps in the Fractal server](https://fractal-analytics-platform.github.io/fractal-server/internals/integrations/_task_execution/).

Here are two examples of how metadata produced by a task may look like.

1. For a task that processed `/path/to/plate.zarr/B/03/0` and created `/path/to/plate.zarr/B/03/0_processed`:
```json
{
  "image_list_updates": [
    {
      "zarr_url": "/path/to/plate.zarr/B/03/0_processed",
      "origin": "/path/to/plate.zarr/B/03/0",
      "attributes": {
        "plate": "plate_name",
        "well": "B03"
      },
      "types": {}
    }
  ]
}
```
2. For a task that deleted the `/path/to/plate.zarr/B/03/0` OME-Zarr image from the image list:
```json
{
  "image_list_removals": ["/path/to/plate.zarr/B/03/0"]
}
```

## Parallel tasks

A parallel task processes a single OME-Zarr image and it is meant to run in parallel across many OME-Zarr images. Its typycal usage is for tasks that do not need special input handling or subset parallelization, and it can typically be run on any collection of OME-Zarrs.

The parameters of a parallel tasks must include a `zarr_url` string argument, which contains the full path to the zarr file to be processed. The current version of Fractal server only supports filesystem paths (e.g. `zarr_url="/some/path/to/my.zarr"`), while support for S3 URLs may be added in the future.

The call signature of a parallel-task Python function looks like:
```python
def my_parallel_task(
    # Fractal-reserved required task arguments
    zarr_url: str,
    # Additional task arguments
    another_parameter_1: int,
    another_parameter_2: list[str],
):
    # ... task code goes here ...
```

## Non-parallel tasks

A non-parallel task processes a list of OME-Zarr images, and it only runs as a single computational job. Non-parallel tasks are useful to aggregate information across many OME-Zarrs or to create image-list updates (see [the Fractal image list](https://fractal-analytics-platform.github.io/image_list)). Non-parallel tasks can often be specific to given collection types like OME-Zarr HCS plates.

The parameters of a non-parallel task must include a `zarr_urls` argument (a list of strings) and `zarr_dir` argument (a single string). `zarr_urls` contains the full paths to the OME-Zarr images to be processed (similar to `zarr_url` above), while `zarr_dir` is the base directory into which new OME-Zarr files may be written by the task.

The call signature of a non-parallel-task Python function looks like:
```python
def my_non_parallel_task(
    # Fractal-reserved required task arguments
    zarr_urls: list[str],
    zarr_dir: str,
    # Additional task arguments
    another_parameter_1: int,
    another_parameter_2: list[str],
):
    # ... task code goes here ...
```

## Compound tasks

A compound task consists of two tasks: A non-parallel *initialization* task and a parallel *compute* task.
The initialization task runs in the same way as a non-parallel task and generates a custom parallelization list of zarr_urls and parameters to be used in the compute task, while the compute tasks are run in parallel for each entry of the parallelization list and use the `init_args` dictionary as an extra input from the initialization task.

Compound tasks can often be specific to given collection types like OME-Zarr HCS plates. A typical example are multiplexing-related tasks that use `acquisition` metadata on the well level to decide which pairs of images need to be processed.

The Python call signatures of the initialization and compute parts of a compound task look like
```python
def my_compound_initialization_task(
    # Fractal-reserved required task arguments
    zarr_urls: list[str],
    zarr_dir: str,
    # Additional task arguments
    another_parameter_1: int,
    another_parameter_2: list[str],
) -> dict[str, list[dict[str, Any]]]:
    # ... task code goes here ...

def my_compound_compute_task(
    # Fractal-reserved required task arguments
    zarr_url: str,
    init_args: dict[str, Any],    # This could also have a more specific type hint
    # Additional task arguments
    another_parameter_3: int,
    another_parameter_4: list[str],
):
    # ... task code goes here ...
```

Fractal server takes care of running the initialization/compute parts of a compound task. The initialization task must produce a "parallelization list", with elements having the `zarr_url` property as well as additional arbitrary arguments as an `init_args` dictionary. This parallelization list is then used by Fractal server to plan which compute tasks should run.

An example of a parallelization list produced by the initialization task looks like
```json
{
  "parallelization_list": [
    {
      "zarr_url": "/path/to/plate.zarr/B/03/0",
      "init_args": {
        "acquisition": 0
      }
    },
    {
      "zarr_url": "/path/to/plate.zarr/B/03/1",
      "init_args": {
        "acquisition": 1
      }
    },
    {
      "zarr_url": "/path/to/plate.zarr/B/03/2",
      "init_args": {
        "acquisition": 2
      }
    }
  ]
}
```
With such a parallelization list, Fractal server would run three copies of the compute tasks, one for each acquisition.


## Non-parallel converter tasks

Converter tasks are used to create new OME-zarr images based on raw microscope data. A _non-parallel_ converter task has the same structure as a non-parallel task, but its argument do not include the `zarr_urls` argument (since there does not exist any OME-Zarr image yet).

The call signature of a non-parallel-converter-task Python function looks like:
```python
def my_non_parallel_converter_task(
    # Fractal-reserved required task arguments
    zarr_dir: str,
    # Additional task arguments
    another_parameter_1: int,
    another_parameter_2: list[str],
):
    # ... task code goes here ...
```

## Compound converter tasks

A compound converter task is a converter task with the same initialization/compute structure as a compound task.
The initialization task only requires a `zarr_dir` parameter, while the compute task has the same required arguments as the one of a non-converter compute task (that is, `zarr_url` and `init_args`):
```python
def my_compound_converter_initialization_task(
    # Fractal-reserved required task arguments
    zarr_dir: str,
    # Additional task arguments
    another_parameter_1: int,
    another_parameter_2: list[str],
) -> dict[str, list[dict[str, Any]]]:
    # ... task code goes here ...

def my_compound_converter_compute_task(
    # Fractal-reserved required task arguments
    zarr_url: str,
    init_args: dict[str, Any],    # This could also have a more specific type hint
    # Additional task arguments
    another_parameter_1: int,
    another_parameter_2: list[str],
):
    # ... task code goes here ...
```
