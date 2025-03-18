import subprocess
import sys

from fractal_task_tools._create_manifest import create_manifest


def test_create_manifest():
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "./tests/fake-tasks",
        ]
    )

    create_manifest(
        raw_package_name="fake-tasks",
        task_list_path="task_list",
    )

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
