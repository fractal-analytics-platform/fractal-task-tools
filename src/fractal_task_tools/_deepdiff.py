from typing import Union

ValidType = Union[list, dict, str, int, float, bool, None]


def deepdiff(
    *,
    old_object: ValidType,
    new_object: ValidType,
    path: str,
    ignore_keys_order: bool,
):
    if type(old_object) is not type(new_object):
        raise ValueError(
            f"[{path}] Type difference: "
            f"{type(old_object)} (old) vs {type(new_object)} (new)."
        )

    if type(old_object) is dict:
        old_keys = list(old_object.keys())
        new_keys = list(new_object.keys())
        if ignore_keys_order:
            old_keys = sorted(old_keys)
            new_keys = sorted(new_keys)
        if old_keys != new_keys:
            raise ValueError(
                f"[{path}] Dictionaries have different keys "
                f"{old_keys} (old) vs {new_keys} (new)."
            )

        for key, value_a in old_object.items():
            deepdiff(
                value_a,
                new_object[key],
                path=f"{path}['{key}']",
            )
    elif type(old_object) is list:
        if len(old_object) != len(new_object):
            raise ValueError(
                f"{path} Lists have different lengths "
                f"{len(old_object)} (old) vs {len(new_object)} (new)."
            )
        for ind, item_a in enumerate(old_object):
            deepdiff(
                item_a,
                new_object[ind],
                path=f"{path}[{ind}]",
            )
    else:
        if old_object != new_object:
            raise ValueError(
                f"{path} Values are different "
                "'{old_object}' (old) vs '{new_object}' (new)."
            )
