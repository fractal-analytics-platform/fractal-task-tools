# Task types

This page provides additional details about the task types supported by the [Fractal tasks specification](https://fractal-analytics-platform.github.io/tasks_spec).


There are five types of Fractal tasks:
1. _parallel_ tasks,
2. _non-parallel_ tasks,
3. _compound_ tasks,
4. _compound converter_ tasks,
4. _non-parallel converter_ tasks.


Task types differ in how they are run, and also in what parameters are required.

All parameters mentioned below (`zarr_url`, `zarr_urls`, `zarr_dir`, `init_args`) are reserved keyword arguments: when running tasks through Fractal server, the server takes care to pass the correct value for this arguments, and the user cannot set them directly. On top of them, each task can also take an arbitrary list of parameters that are specific to the task function and that the user can set.


## Parallel tasks

A parallel task processes a single OME-Zarr image and it is meant to run in parallel across many OME-Zarr images.
Its typycal usage is for tasks that do not need special input handling or subset parallelization, and it can typically be run on any collection of OME-Zarrs.

The parameters of a parallel tasks must include a `zarr_url` string argument, which contains the full path to the zarr file to be processed. The current version of Fractal server only supports filesystem paths (e.g. `zarr_url = "/some/path/to/my.zarr"`), but support for S3 URLs may be added in the future.

The call-signature of a parallel-task Python function looks like:
```python
def my_parallel_task(
    # Standard task arguments
    zarr_url: str,
    # Non-standard task arguments
    another_parameter_1: int,
    another_parameter_2: list[str],
):
    # ... task code goes here ...
```


## Non-parallel tasks

A non-parallel task processes a list of OME-Zarr images, and it only runs as a single job.
Non-parallel tasks are useful to aggregate information across many OME-Zarrs or to create image-list updates (see [the Fractal image list](https://fractal-analytics-platform.github.io/image_list)). Non-parallel tasks can often be specific to given collection types like OME-Zarr HCS plates.

The parameters of a non-parallel task must include a `zarr_urls` arguments (a list of strings) and `zarr_dir` argument (a single string). `zarr_urls` contains the full paths to the OME-Zarr images to be processed (similar to `zarr_url` above), while `zarr_dir` is the base directory into which new OME-Zarr files will be written by the task.

The call-signature of a non-parallel-task Python function looks like:
```python
def my_non_parallel_task(
    # Standard task arguments
    zarr_urls: list[str],
    zarr_dir: str,
    # Non-standard task arguments
    another_parameter_1: int,
    another_parameter_2: list[str],
):
    # ... task code goes here ...
```


## Compound tasks

A compound task consists of two tasks: A non-parallel *initialization* task and a parallel *compute* task.
The initialization task runs in the same way as a non-parallel task and generates a custom parallelization list of zarr_urls & parameters to be used in the compute task, while the compute tasks are run in parallel for each entry of the parallelization list and use the `init_args` dictionary as an extra input from the initialization task.

Compound tasks can often be specific to given collection types like OME-Zarr HCS plates. A typical example are multiplexing-related tasks that use `acquisition` metadata on the well level to decide which pairs of images need to be processed.

The Python call signatures of the initialization and compute parts of a compound task look like
```python
def my_compound_initialization_task(
    # Standard task arguments
    zarr_urls: list[str],
    zarr_dir: str,
    # Non-standard task arguments
    another_parameter_1: int,
    another_parameter_2: list[str],
) -> dict[str, list[dict[str, Any]]]:
    # ... task code goes here ...

def my_compound_compute_task(
    # Standard task arguments
    zarr_url: str,
    init_args: dict[str, Any],    # This could also have a more specific type hint
    # Non-standard task arguments
    another_parameter_1: int,
    another_parameter_2: list[str],
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
        "another_parameter_1": 0
      }
    },
    {
      "zarr_url": "/path/to/plate.zarr/B/03/1",
      "init_args": {
        "another_parameter_1": 1
      }
    },
    {
      "zarr_url": "/path/to/plate.zarr/B/03/2",
      "init_args": {
        "another_parameter_1": 2
      }
    }
  ]
}
```
With such a parallelization list, Fractal server would run three copies of the compute tasks.


## Non-parallel converter tasks

Converter tasks are used to create new OME-zarr images based on raw microscope data. A _non-parallel_ converter task has the same structure as a .non-parallel task, but its argument do not include the `zarr_urls` argument (since there does not exist any OME-Zarr image yet).

The call-signature of a non-parallel-converter-task Python function looks like:
```python
def my_non_parallel_converter_task(
    # Standard task arguments
    zarr_dir: str,
    # Non-standard task arguments
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
    # Standard task arguments
    zarr_dir: str,
    # Non-standard task arguments
    another_parameter_1: int,
    another_parameter_2: list[str],
) -> dict[str, list[dict[str, Any]]]:
    # ... task code goes here ...

def my_compound_converter_compute_task(
    # Standard task arguments
    zarr_url: str,
    init_args: dict[str, Any],    # This could also have a more specific type hint
    # Non-standard task arguments
    another_parameter_1: int,
    another_parameter_2: list[str],
):
    # ... task code goes here ...
```
