import glob
import json

from jsonschema.validators import Draft201909Validator
from jsonschema.validators import Draft202012Validator
from jsonschema.validators import Draft7Validator

VALIDATORS = (
    Draft7Validator,
    Draft201909Validator,
    Draft202012Validator,
)


if __name__ == "__main__":
    manifest_files = [
        f
        for f in glob.glob(
            "./**/__FRACTAL_MANIFEST__.json",
            recursive=True,
        )
        if ("tests" not in f and "cache" not in f and "fractal-task-tools" not in f)
    ]
    if len(manifest_files) != 1:
        raise ValueError(
            "ERROR: There must only be a single manifest file "
            f"(found: {manifest_files=})."
        )
    with open(manifest_files[0]) as fp:
        manifest = json.load(fp)
    for task in manifest["task_list"]:
        print(f"Now looking at '{task['name']}' task")
        for task_type in ("non_parallel", "parallel"):
            key = f"args_schema_{task_type}"
            schema = task.get(key, None)
            if schema is not None:
                for jsonschema_validator in VALIDATORS:
                    my_validator = jsonschema_validator(schema=schema)
                    my_validator.check_schema(my_validator.schema)
                    print(
                        f"Schema for task '{task['name']}'/{task_type} is "
                        f"valid with {jsonschema_validator}."
                    )
