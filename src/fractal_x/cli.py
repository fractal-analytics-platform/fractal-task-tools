from fractal_x.create_manifest import create_manifest

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--package",
    type=str,
    help="Example: 'fractal_tasks_core'",
    required=True,
)
parser.add_argument(
    "--task-list-relative-path",
    type=str,
    help="Example: '.dev.task_list'",
    required=True,
)

# FIXME: these two should come from the task_list.py (name TBD file)



def main():
    args = parser.parse_args()
    create_manifest(
        package=args.package,
        task_list_relative_path=args.task_list_relative_path,
    )
