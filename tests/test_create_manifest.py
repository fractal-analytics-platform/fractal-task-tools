import json
import subprocess
from pathlib import Path

import pytest
from devtools import debug

from fractal_task_tools._cli import check_manifest
from fractal_task_tools._cli import write_manifest_to_file
from fractal_task_tools._create_manifest import MANIFEST_FILENAME
from fractal_task_tools._create_manifest import create_manifest


def test_create_manifest(tmp_path: Path, caplog):
    subprocess.check_call(
        [
            "uv",
            "pip",
            "install",
            "./tests/fake-tasks",
        ]
    )

    import fake_tasks

    # SUCCESS: create manifest with `DOCS_LINK=""` transformed into `None`
    manifest = create_manifest(
        raw_package_name="fake-tasks",
        task_list_path="task_list_with_empty_docs_link",
    )
    for task in manifest["task_list"]:
        assert "docs_link" not in task.keys()

    # SUCCESS: create manifest with authors read from pyproject.toml
    # NOTE: The relevant pyproject.toml is the one in the current directory,
    # that is, the one for `fractal-task-tools`.
    manifest = create_manifest(
        raw_package_name="fake-tasks",
        task_list_path="task_list_no_authors",
    )
    assert manifest["authors"] == "Tommaso Comparin"

    # SUCCESS: create manifest
    manifest = create_manifest(
        raw_package_name="fake-tasks",
        task_list_path="task_list",
    )
    for task in manifest["task_list"]:
        assert "type" in task.keys()
    debug(manifest)

    # TASK 1, see
    # * https://github.com/fractal-analytics-platform/fractal-task-tools/issues/87
    # * https://github.com/fractal-analytics-platform/fractal-task-tools/issues/90
    properties_ModelMixedDocstrings = manifest["task_list"][0][
        "args_schema_non_parallel"
    ]["$defs"]["ModelMixedDocstrings"]["properties"]

    debug(properties_ModelMixedDocstrings)

    assert properties_ModelMixedDocstrings["a"]["description"] == "Field for a"
    assert properties_ModelMixedDocstrings["b"]["description"] == "New-style for b"
    assert properties_ModelMixedDocstrings["c"]["description"] == "Field for c"
    assert "description" not in properties_ModelMixedDocstrings["d"]

    # TASK 2, see
    # * https://github.com/fractal-analytics-platform/fractal-task-tools/issues/119
    task2_defs = manifest["task_list"][1]["args_schema_non_parallel"]["$defs"]
    properties_SpecificParameters = task2_defs["SpecificParameters"]["properties"]
    debug(properties_SpecificParameters)
    description_a = properties_SpecificParameters["a"]["description"]
    description_b = properties_SpecificParameters["b"]["description"]
    assert description_a == "Description of `a` in `GenericParameters`."
    assert description_b == "Description of `b` in `SpecificParameters`."

    # TASK 3, see
    # * https://github.com/fractal-analytics-platform/fractal-task-tools/issues/118
    task3_defs = manifest["task_list"][2]["args_schema_non_parallel"]["$defs"]
    description_B = task3_defs["ParametersB"]["properties"]["b"]["description"]
    description_C = task3_defs["ParametersC"]["properties"]["c"]["description"]
    assert "\n" in description_B
    assert "    " in description_B
    assert description_C == (
        "This is a description where we have full control. "
        "Here is a new line:\nNew line.\n"
        "Here is a tab:\tand then more text."
    )

    write_manifest_to_file(
        raw_package_name="fake-tasks",
        manifest=manifest,
    )

    check_manifest(
        raw_package_name="fake-tasks",
        manifest=manifest,
        ignore_keys_order=False,
        verbose=True,
    )

    MANIFEST_PATH = Path(fake_tasks.__file__).parent / MANIFEST_FILENAME
    with MANIFEST_PATH.open("w") as f:
        json.dump(dict(fake="manifest"), f)

    caplog.clear()
    with pytest.raises(SystemExit):
        check_manifest(
            raw_package_name="fake-tasks",
            manifest=manifest,
            ignore_keys_order=False,
            verbose=True,
        )
    assert "On-disk manifest is not up to date." in caplog.text

    # Clean up
    MANIFEST_PATH.unlink()

    subprocess.check_call(
        [
            "uv",
            "pip",
            "uninstall",
            "fake-tasks",
        ]
    )
