# 0.3.0

See https://fractal-analytics-platform.github.io/fractal-task-tools/usage/run_task/#log-configuration
for a description of the new logging-related feature.

* Introduce logging-configuration environment variables (\#70, \#71).
* Mark `logger_name` argument of `run_fractal_task` as deprecated (\#70).
* Dependencies:
    * Bump pydantic requirement to `>=2.6.0,<=2.13.0` (\#74).
* Testing:
    * Add test with `lowest-direct` resolution scheme for Python 3.11 and 3.12 (\#74).
* Development:
    * Adopt `uv` for development (\#74).

# 0.2.1

* Improve support for tagged/non-tagged union arguments (\#68).
* Testing:
    * Add `fractal-ome-zarr-hcs-stitching` to external-packages tests (\#64).
    * Add `operetta-compose` to external-packages tests (\#58).
    * Add `APx_fractal_task_collection` to external-packages tests (\#61).
    * Add `zmb-fractal-tasks` to external-packages tests (\#60).
    * Add `example-tasks` to external-packages tests (\#68).
    * Add `fractal-cellpose-sam-task` to external-packages tests (\#68).

# 0.2.0

[yanked due to a mistake upon release]

# 0.1.1

* Support Python3.14 (\#57).

# 0.1.0

* Deprecate `--fractal-server-2-13` option (\#45).
* Broader support for unions of type and `None` (\#53).
* Support pydantic v2.12 (\#55).

# 0.0.14

* Replace `DOCS_LINK=""` with `DOCS_LINK=None` (\#42).
* Test manifest agains `fractal-server` schema for external packages (\#42).
* Test multiple JSON-Schema drafts, for external packages (\#39).

# 0.0.13

* Support Python 3.13 (\#35).
* Support `pydantic<=2.11.7` (\#37).
