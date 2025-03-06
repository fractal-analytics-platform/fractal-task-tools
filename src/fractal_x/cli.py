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
    "--task-list-file",
    type=str,
    help="Example: '/somewhere/task_list.py'",
    required=True,
)
parser.add_argument(
    "--authors",
    type=str,
    help="Example: 'Name1 Surname1, Name2 Surname2'",
    required=False,
    default=None,
)


def main():
    args = parser.parse_args()
    create_manifest(
        task_list_file=args.task_list_file,
        package=args.package,
        authors=args.authors,
    )
