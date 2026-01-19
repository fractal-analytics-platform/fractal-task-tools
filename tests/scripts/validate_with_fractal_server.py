import glob
import json

import requests
from jsonschema import validate


MANIFEST_SCHEMA_URL = (
    "https://raw.githubusercontent.com/fractal-analytics-platform/"
    "fractal-server/main/"
    "fractal_server/json_schemas/manifest_v2.json"
)

EXAMPLE_MANIFEST_PATH = (
    "./fractal-task-tools/example/src/example_tasks/__FRACTAL_MANIFEST__.json"
)


if __name__ == "__main__":
    manifest_files = [
        f
        for f in glob.glob(
            "./**/__FRACTAL_MANIFEST__.json",
            recursive=True,
        )
        if (
            (
                "tests" not in f
                and "cache" not in f
                and "fractal-task-tools" not in f
            )
            or f == EXAMPLE_MANIFEST_PATH
        )
    ]
    if len(manifest_files) != 1:
        raise ValueError(
            "ERROR: There must only be a one and only one manifest file "
            f"(found: {manifest_files=})."
        )
    with open(manifest_files[0]) as fp:
        manifest_data = json.load(fp)
    print(f"Manifest loaded from {manifest_files[0]}")

    response = requests.get(MANIFEST_SCHEMA_URL)
    response_body = response.content.decode("utf-8")
    manifest_schema = json.loads(response_body)
    print(f"Manifest schema loaded from {MANIFEST_SCHEMA_URL}")

    validate(instance=manifest_data, schema=manifest_schema)
    print("All OK.")
