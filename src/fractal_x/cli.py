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
parser.add_argument(
    "--authors",
    type=str,
    help="Example: 'Name1 Surname1, Name2 Surname2'",
    required=False,
    default=None,
)
parser.add_argument(
    "--docs-link",
    type=str,
    help="Example: https://example.org'",
    required=False,
    default=None,
)


def main():
    args = parser.parse_args()
    create_manifest(
        package=args.package,
        task_list_relative_path=args.task_list_relative_path,
        authors=args.authors,
        docs_link=args.docs_link,
    )
