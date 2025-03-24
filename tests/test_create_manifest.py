import json
import subprocess
import sys
from pathlib import Path

import pytest
from devtools import debug
from fractal_task_tools._cli import check_manifest
from fractal_task_tools._cli import write_manifest_to_file
from fractal_task_tools._create_manifest import create_manifest
from fractal_task_tools._create_manifest import MANIFEST_FILENAME


def test_create_manifest(tmp_path: Path, caplog):
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "./tests/fake-tasks",
        ]
    )

    import fake_tasks

    manifest = create_manifest(
        raw_package_name="fake-tasks",
        task_list_path="task_list",
    )
    debug(manifest)
    write_manifest_to_file(
        raw_package_name="fake-tasks",
        manifest=manifest,
    )

    check_manifest(
        raw_package_name="fake-tasks",
        manifest=manifest,
        ignore_keys_order=False,
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
        )
    assert "On-disk manifest is not up to date." in caplog.text

    # Clean up
    MANIFEST_PATH.unlink()

    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "uninstall",
            "fake-tasks",
            "--yes",
        ]
    )
