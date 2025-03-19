import argparse as ap
import sys

from fractal_task_tools._cli_tools import check_manifest
from fractal_task_tools._cli_tools import write_manifest_to_file
from fractal_task_tools._create_manifest import create_manifest


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
check_manifest_parser.add_argument(
    "--ignore-keys-order",
    type=bool,
    help=(
        "Ignore the order of dictionary keys when comparing manifests "
        "(default value: False)."
    ),
    default=False,
    required=False,
)


def _parse_arguments(sys_argv: list[str] | None = None) -> ap.Namespace:
    """
    Parse `sys.argv` or custom CLI arguments.

    Arguments:
        sys_argv: If set, overrides `sys.argv` (useful for testing).
    """
    if sys_argv is None:
        sys_argv = sys.argv[:]
    args = main_parser.parse_args(sys_argv[1:])
    return args


def main():
    args = _parse_arguments()
    if args.cmd == "create":
        manifest = create_manifest(
            raw_package_name=args.package,
            task_list_path=args.task_list_path,
        )
        write_manifest_to_file(
            raw_package_name=args.package,
            manifest=manifest,
        )

    elif args.cmd == "check":
        manifest = create_manifest(
            raw_package_name=args.package,
            task_list_path=args.task_list_path,
        )
        check_manifest(
            raw_package_name=args.package,
            manifest=manifest,
            ignore_keys_order=args.ignore_keys_order,
        )
