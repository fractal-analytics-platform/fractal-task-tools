from typing import Union

ValidType = Union[list, dict, str, int, float, bool, None]


def deepdiff(
    a: ValidType,
    b: ValidType,
    path: str,
):
    if type(a) is not type(b):
        raise ValueError(
            f"[{path}] Type difference ({type(a)} differs from {type(b)})"
        )

    if type(a) is dict:
        if list(a.keys()) != list(b.keys()):
            raise ValueError(
                f"[{path}] Dictionaries have different keys "
                f"({set(a.keys())} vs {set(b.keys())})"
            )

        for key, value_a in a.items():
            deepdiff(
                value_a,
                b[key],
                path=f"{path}['{key}']",
            )
    elif type(a) is list:
        if len(a) != len(b):
            raise ValueError(
                f"{path} Lists have different lengths ({len(a)} vs {len(b)})"
            )
        for ind, item_a in enumerate(a):
            deepdiff(
                item_a,
                b[ind],
                path=f"{path}[{ind}]",
            )
    else:
        if a != b:
            raise ValueError(f"{path} Values are different ('{a}' vs '{b}')")
