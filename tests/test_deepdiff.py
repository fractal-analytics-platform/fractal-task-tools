from datetime import datetime

import pytest
from fractal_task_tools._deepdiff import deepdiff


def test_recursion_level():
    obj = [[[1, 2], [1, 2]], [1, 2]]
    with pytest.raises(
        ValueError,
        match="Reached MAX_RECURSION_LEVEL",
    ):
        deepdiff(
            old_object=obj,
            new_object=obj,
            ignore_keys_order=True,
            path="base",
            recursion_level=19,
        )


def test_ignore_keys_order():
    old_obj = dict(key1=1, key2=2)
    new_obj = dict(key2=2, key1=1)
    with pytest.raises(
        ValueError,
        match="Dictionaries have different keys",
    ):
        deepdiff(
            old_object=old_obj,
            new_object=new_obj,
            ignore_keys_order=False,
            path="base",
        )

    deepdiff(
        old_object=old_obj,
        new_object=new_obj,
        ignore_keys_order=True,
        path="base",
    )


def test_list_length():
    with pytest.raises(
        ValueError,
        match="Lists have different lengths",
    ):
        deepdiff(
            old_object=[1],
            new_object=[2, 3],
            ignore_keys_order=False,
            path="base",
        )


def test_path():
    old_obj = {"mykey1": [1, 2.0, "a", None, {"mykey2": 1}]}
    new_obj = {"mykey1": [1, 2.0, "a", None, {"mykey2": 2}]}
    with pytest.raises(ValueError) as exc_info:
        deepdiff(
            old_object=old_obj,
            new_object=new_obj,
            ignore_keys_order=False,
            path="base",
        )
    assert "base['mykey1'][4]['mykey2']" in str(exc_info.value)


@pytest.mark.parametrize(
    "old_obj,new_obj",
    [
        (1, 2.0),
        (None, "a"),
        ([], {}),
    ],
)
def test_type_diff(old_obj, new_obj):
    with pytest.raises(ValueError, match="Type difference"):
        deepdiff(
            old_object=old_obj,
            new_object=new_obj,
            ignore_keys_order=False,
            path="base",
        )


def test_invalid_type():
    with pytest.raises(ValueError, match="Invalid type"):
        deepdiff(
            old_object=datetime.now(),
            new_object=datetime.now(),
            ignore_keys_order=False,
            path="base",
        )


def test_success():
    old_obj = {"mykey1": [1, 2.0, "a", None], "mykey2": []}
    deepdiff(
        old_object=old_obj,
        new_object=old_obj,
        ignore_keys_order=False,
        path="base",
    )
