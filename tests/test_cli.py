import pytest
from fractal_task_tools._cli import _parse_arguments


def test_get_args():
    with pytest.raises(SystemExit):
        _parse_arguments(sys_argv=["xxx", "invalid-cmd"])

    with pytest.raises(SystemExit):
        _parse_arguments(sys_argv=["xxx", "create"])

    with pytest.raises(SystemExit):
        _parse_arguments(sys_argv=["xxx", "check"])

    PACKAGE = "some-package"
    args = _parse_arguments(sys_argv=["xxx", "create", "--package", PACKAGE])
    assert args.cmd == "create"
    assert args.package == PACKAGE
    assert args.task_list_path == "dev.task_list"
