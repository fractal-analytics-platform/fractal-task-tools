from datetime import datetime

import pytest
from fractal_task_tools._deepdiff import deepdiff, ERRORS, Errors


def test_Errors():
    E = Errors()
    assert E._data == []
    assert E.data == []
    assert E.messages_str == "[]"
    assert E.tot_errors == 0
    E.append((1, 1, "msg1"))
    E.append((2, 2, "msg2"))
    assert E.messages_str == "['msg1', 'msg2']"
    assert E.tot_errors == 2
    E.reset_state()
    assert E._data == []
    assert E.data == []
    assert E.messages_str == "[]"
    assert E.tot_errors == 0


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
            verbose=True,
        )


def test_invalid_type():
    with pytest.raises(ValueError, match="Invalid type"):
        deepdiff(
            old_object=datetime.now(),
            new_object=datetime.now(),
            ignore_keys_order=False,
            path="base",
            verbose=True,
        )


@pytest.mark.parametrize("ignore_keys_order", (True, False))
def test_ignore_keys_order(ignore_keys_order):
    old_obj = dict(key1=1, key2=2)
    new_obj = dict(key2=2, key1=1)
    deepdiff(
        old_object=old_obj,
        new_object=new_obj,
        ignore_keys_order=ignore_keys_order,
        path="base",
        verbose=True,
    )
    if ignore_keys_order:
        assert ERRORS.tot_errors == 0
    else:
        assert ERRORS.tot_errors == 1
        assert "Dictionaries have different keys" in ERRORS.messages_str


def test_list_length():
    deepdiff(
        old_object=[1],
        new_object=[2, 3],
        ignore_keys_order=False,
        path="base",
        verbose=True,
    )
    assert ERRORS.tot_errors == 1
    assert "Lists have different lengths" in ERRORS.messages_str


def test_path():
    old_obj = {"mykey1": [1, 2.0, "a", None, {"mykey2": 1}]}
    new_obj = {"mykey1": [1, 2.0, "a", None, {"mykey2": 2}]}
    deepdiff(
        old_object=old_obj,
        new_object=new_obj,
        ignore_keys_order=False,
        path="base",
        verbose=True,
    )
    assert "base['mykey1'][4]['mykey2']" in ERRORS.messages_str


@pytest.mark.parametrize(
    "old_obj,new_obj",
    [
        (1, 2.0),
        (None, "a"),
        ([], {}),
    ],
)
def test_type_diff(old_obj, new_obj):
    deepdiff(
        old_object=old_obj,
        new_object=new_obj,
        ignore_keys_order=False,
        path="base",
        verbose=True,
    )
    assert ERRORS.tot_errors == 1
    assert "Type difference" in ERRORS.messages_str


def test_success():
    old_obj = {"mykey1": [1, 2.0, "a", None], "mykey2": []}
    deepdiff(
        old_object=old_obj,
        new_object=old_obj,
        ignore_keys_order=False,
        path="base",
        verbose=True,
    )
    assert ERRORS.tot_errors == 0
