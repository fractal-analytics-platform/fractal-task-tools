from typing import Self
from typing import TypeAlias

JSONType: TypeAlias = (
    dict[str, "JSONType"] | list["JSONType"] | str | int | float | bool | None
)

MAX_RECURSION_LEVEL = 20
ERRORS = []


class Errors:
    """
    An item of `self._data` is made of the old JSON object, the new JSON object
    and the error message.
    """

    _data: list[tuple[JSONType, JSONType, str]]

    def __init__(self):
        self._data = []

    def reset_state(self):
        self._data = []

    def append(self: Self, item: tuple[JSONType, JSONType, str]):
        self._data.append(item)

    @property
    def tot_errors(self: Self) -> int:
        return len(self._data)

    @property
    def messages_str(self: Self) -> str:
        return str([item[2] for item in self._data])

    @property
    def data(self: Self) -> list[tuple[JSONType, JSONType, str]]:
        return self._data


ERRORS = Errors()


def deepdiff(
    *,
    old_object: JSONType,
    new_object: JSONType,
    path: str,
    ignore_keys_order: bool,
    recursion_level: int = 1,
    verbose: bool = False,
):
    if type(old_object) is not type(new_object):
        ERRORS.append(
            (
                old_object,
                new_object,
                f"[{path}] Type difference:\n"
                f"\tOld: {type(old_object)}\n\tNew: {type(new_object)}",
            )
        )
        return

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
            ERRORS.append(
                (
                    old_object,
                    new_object,
                    f"[{path}] Dictionaries have different keys:\n"
                    f"\tOld: {old_keys}\n\tNew: {new_keys}",
                )
            )
            return

        for key, value_a in old_object.items():
            deepdiff(
                old_object=value_a,
                new_object=new_object[key],
                path=f"{path}['{key}']",
                ignore_keys_order=ignore_keys_order,
                recursion_level=recursion_level + 1,
                verbose=verbose,
            )
    elif type(old_object) is list:
        if len(old_object) != len(new_object):
            ERRORS.append(
                (
                    old_object,
                    new_object,
                    f"[{path}] Lists have different lengths:\n"
                    f"\tOld:{len(old_object)}\n\tNew: {len(new_object)}",
                )
            )
            return

        for ind, item_a in enumerate(old_object):
            deepdiff(
                old_object=item_a,
                new_object=new_object[ind],
                path=f"{path}[{ind}]",
                ignore_keys_order=ignore_keys_order,
                recursion_level=recursion_level + 1,
                verbose=verbose,
            )
    else:
        if old_object != new_object:
            ERRORS.append(
                (
                    old_object,
                    new_object,
                    f"[{path}] Values are different:\n"
                    f"\tOld: '{old_object}'\n\tNew: '{new_object}'",
                )
            )
            return
