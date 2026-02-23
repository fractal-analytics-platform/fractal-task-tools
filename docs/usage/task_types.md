# Task types

This page provides additional details about the task types supported by the [Fractal tasks specification](https://fractal-analytics-platform.github.io/tasks_spec/).

There are five types of tasks:

1. A **parallel task** processes a single OME-Zarr image and it is meant to run in parallel across many OME-Zarr images.
	- Parallel tasks are the typical scenario for compute tasks that don't need special input handling or subset parallelization.
	- Parallel tasks can typically be run on any collection of OME-Zarrs.
2. A **non-parallel task** processes a list of images, and it only runs as a single job.
	- Non-parallel tasks are useful to aggregate information across many OME-Zarrs or to create image-list updates (see [the Fractal image list](./image_list.md)).
	- Non-parallel tasks can often be specific to given collection types like OME-Zarr HCS plates.
3. A **compound task** consists of an (non-parallel) *initialization* task and a (parallel) *compute* task.
	- The initialization task runs in the same way as a non-parallel task and generates a custom parallelization list of zarr_urls & parameters to be used in the compute task.
	- The compute tasks are run in parallel for each entry of the parallelization list and use the `init_args` dictionary as an extra input from the initialization task.
	- Compound tasks can often be specific to given collection types like OME-Zarr HCS plates. A typical example are multiplexing-related tasks that use `acquisition` metadata on the well level to decide which pairs of images need to be processed.
4. A **non-parallel converter task** converts raw microscope data to OME-Zarr image(s), and it only runs as a single job.
5. A **compound converter task** converts raw microscope data to OME-Zarr image(s), and it has the same initialization/compute structure as a compound task.



## Task parameters

Tasks have some required parameters, which depend on the task type - see description below. Each task can also take an arbitrary list of parameters that are specific to the task function and that the user can set.

All parameters mentioned below (`zarr_url`, `zarr_urls`, `zarr_dir`, `init_args`) are reserved keyword arguments: when running tasks through Fractal server, the server takes care to pass the correct value for this arguments, and the user cannot set them directly.

### Parallel tasks

The parameters of a Fractal parallel tasks must include a `zarr_url` string argument. The `zarr_url` contains the full path to the zarr file to be processed. Only filesystem paths are currently supported, not S3 urls.

### Non-parallel tasks

The parameters of a Fractal non-parallel task must include a `zarr_urls` arguments (a list of strings) and `zarr_dir` argument (a single string). `zarr_urls` contains the full paths to the OME-Zarr images to be processed. We currently just support paths on filesystems, not S3 urls. `zarr_dir` is the base directory into which new OME-Zarr files will be written by the task.

### Compound tasks

Compound tasks consist of an initialization part (similar to the non-parallel task) and a compute part (similar to the parallel task).
The initialization part has the same required parameters as the non-parallel task (`zarr_urls` and `zarr_dir`), but it provides the parallelization list for the compute part as an output.
The compute part takes the `zarr_url` argument and an extra `init_args` dictionary argument (which is coming from the `parallelization_list` provided by the init task).

### Non-parallel converter tasks

The parameters of a Fractal non-parallel converter task must include the `zarr_dir` argument, which is the base directory into which OME-Zarr files will be written by tasks.

### Compound converter tasks

Compound converter tasks have the same structure as compound tasks, with the difference that they do not require a `zarr_urls` parameter. The initialization part requires the `zarr_dir` argument, and it provides the parallelization list for the compute part as an output. The compute part requires the `zarr_url` argument and an extra `init_args` dictionary argument (which is coming from the `parallelization_list` provided by the init task).
