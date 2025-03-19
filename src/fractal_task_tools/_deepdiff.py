from typing import Union


ValidType = Union[list, dict, str, int, float, bool, None]

MAX_RECURSION_LEVEL = 20


def deepdiff(
    *,
    old_object: ValidType,
    new_object: ValidType,
    path: str,
    ignore_keys_order: bool,
    recursion_level: int = 1,
):
    if type(old_object) is not type(new_object):
        raise ValueError(
            f"[{path}] Type difference:\n"
            f"\tOld: {type(old_object)}\n\tNew: {type(new_object)}"
        )

    if type(old_object) not in [list, dict, str, int, float, bool, type(None)]:
        raise ValueError(f"[{path}] Invalid type {type(old_object)}, exit.")

    if recursion_level > MAX_RECURSION_LEVEL:
        raise ValueError(f"Reached {MAX_RECURSION_LEVEL=}. Exit.")

    if type(old_object) is dict:
        old_keys = list(old_object.keys())
        new_keys = list(new_object.keys())
        if ignore_keys_order:
            old_keys = sorted(old_keys)
            new_keys = sorted(new_keys)
        if old_keys != new_keys:
            raise ValueError(
                f"[{path}] Dictionaries have different keys:\n"
                f"\tOld: {old_keys}\n\tNew: {new_keys}"
            )

        for key, value_a in old_object.items():
            deepdiff(
                old_object=value_a,
                new_object=new_object[key],
                path=f"{path}['{key}']",
                ignore_keys_order=ignore_keys_order,
                recursion_level=recursion_level + 1,
            )
    elif type(old_object) is list:
        if len(old_object) != len(new_object):
            raise ValueError(
                f"{path} Lists have different lengths:\n"
                f"\tOld:{len(old_object)}\n\tNew: {len(new_object)}"
            )
        for ind, item_a in enumerate(old_object):
            deepdiff(
                old_object=item_a,
                new_object=new_object[ind],
                path=f"{path}[{ind}]",
                ignore_keys_order=ignore_keys_order,
                recursion_level=recursion_level + 1,
            )
    else:
        if old_object != new_object:
            raise ValueError(
                f"{path} Values are different:\n"
                f"\tOld: '{old_object}'\n\tNew: '{new_object}'"
            )
