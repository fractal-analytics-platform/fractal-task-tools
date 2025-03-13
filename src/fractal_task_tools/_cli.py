from fractal_task_tools._create_manifest import create_manifest
import sys

import argparse as ap


main_parser = ap.ArgumentParser(
    description="`fractal-manifest` command-line interface",
    allow_abbrev=False,
)

subparsers = main_parser.add_subparsers(
    title="Available commands",
    dest="cmd",
)


create_manifest_parser = subparsers.add_parser(
    "create",
    description="Create new manifest file",
    allow_abbrev=False,
)

check_manifest_parser = subparsers.add_parser(
    "check",
    description="Check existing manifest file",
    allow_abbrev=False,
)


for subparser in (create_manifest_parser, check_manifest_parser):
    subparser.add_argument(
        "--package",
        type=str,
        help="Example: 'fractal_tasks_core'",
        required=True,
    )
    subparser.add_argument(
        "--task-list-path",
        type=str,
        help=(
            "Dot-separated path to the `task_list.py` module, "
            "relative to the package root (default value: 'dev.task_list')."
        ),
        default="dev.task_list",
        required=False,
    )


def main():
    args = main_parser.parse_args(sys.argv[1:])
    if args.cmd == "create":
        create_manifest(
            package=args.package,
            task_list_path=args.task_list_path,
        )
    elif args.cmd == "check":
        raise NotImplementedError()
