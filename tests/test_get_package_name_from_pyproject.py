from pathlib import Path

import pytest
from devtools import debug

from fractal_task_tools._parse_pyproject import _get_package_name_from_pyproject


def test_get_package_name_from_pyproject():
    with pytest.raises(SystemExit, match="No such file or directory") as exc_info:
        _get_package_name_from_pyproject(Path("/path/to/missing.toml"))
    debug(exc_info.value)

    data_dir = Path(__file__).parent / "data/pyproject-examples"
    debug(data_dir)

    with pytest.raises(
        SystemExit,
    ) as exc_info:
        _get_package_name_from_pyproject(data_dir / "empty.toml")
    debug(exc_info.value)

    with pytest.raises(
        SystemExit,
    ) as exc_info:
        _get_package_name_from_pyproject(data_dir / "no-name.toml")
    debug(exc_info.value)

    assert (
        _get_package_name_from_pyproject(data_dir / "valid-name.toml") == "my-package"
    )

    assert (
        _get_package_name_from_pyproject(data_dir / "valid-import-names.toml")
        == "import1"
    )
    assert (
        _get_package_name_from_pyproject(data_dir / "invalid-import-names.toml")
        == "my-package"
    )
