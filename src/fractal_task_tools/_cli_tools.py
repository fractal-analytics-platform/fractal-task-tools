import json
import logging
import os
import sys
from importlib import import_module
from pathlib import Path

from fractal_task_tools._create_manifest import MANIFEST_FILENAME
from fractal_task_tools._deepdiff import deepdiff
from fractal_task_tools._package_name_tools import normalize_package_name


def write_manifest_to_file(
    *,
    raw_package_name: str,
    manifest: str,
) -> None:
    """
    Write manifest to file.

    Arguments:
        raw_package_name:
        manifest: The manifest object
    """
    logging.info("[write_manifest_to_file] START")

    package_name = normalize_package_name(raw_package_name)
    logging.info(f"[write_manifest_to_file] {package_name=}")

    imported_package = import_module(package_name)
    package_root_dir = Path(imported_package.__file__).parent
    manifest_path = (package_root_dir / MANIFEST_FILENAME).as_posix()
    logging.info(f"[write_manifest_to_file] {os.getcwd()=}")
    logging.info(f"[write_manifest_to_file] {package_root_dir=}")
    logging.info(f"[write_manifest_to_file] {manifest_path=}")

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    logging.info("[write_manifest_to_file] END")


def check_manifest(
    *,
    raw_package_name: str,
    manifest: str,
    ignore_keys_order: bool,
) -> None:
    """
    Write manifest to file.

    Arguments:
        raw_package_name:
        manifest: The manifest object
        ignore_keys_order: Whether to ignore keys order.
    """

    package_name = normalize_package_name(raw_package_name)
    logging.info(f"[check_manifest] {package_name=}")

    imported_package = import_module(package_name)
    package_root_dir = Path(imported_package.__file__).parent
    manifest_path = (package_root_dir / MANIFEST_FILENAME).as_posix()
    logging.info(f"[check_manifest] {os.getcwd()=}")
    logging.info(f"[check_manifest] {package_root_dir=}")
    logging.info(f"[check_manifest] {manifest_path=}")

    with open(manifest_path, "r") as f:
        old_manifest = json.load(f)
    if manifest == old_manifest:
        logging.info("[check_manifest] On-disk manifest is up to date.")
    else:
        logging.error("[check_manifest] On-disk manifest is not up to date.")
        try:
            deepdiff(
                old_object=old_manifest,
                new_object=manifest,
                path="manifest",
                ignore_keys_order=ignore_keys_order,
            )
        except ValueError as e:
            logging.error(str(e))
            sys.exit("New/old manifests differ")

    logging.info("[check_manifest] END")
