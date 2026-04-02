import logging
import sys
import tomllib
from pathlib import Path

logger = logging.getLogger(__name__)


def _get_package_name_from_pyproject(pyproject_path: Path) -> str:
    """
    Get the package name from a local `pyproject.toml`.

    Example 1: if the `project` table has `name="xyz"` and
    `import-name=[]`, return `"xyz".

    Example 2: if the `project` table has `name="pillow"` and
    `import-name=["PIL"]`, return `"PIL"`.

    Example 3: if the `project` table has `name="xyz"` and
    `import-name=["xyz1", "xyz2]`, return `"xyz"`.

    Reference:
    https://packaging.python.org/en/latest/specifications/pyproject-toml
    """
    try:
        with Path(pyproject_path).open("rb") as f:
            pyproject = tomllib.load(f)
        project_table = pyproject["project"]
        if "import-names" in project_table and len(project_table["import-names"]) == 1:
            output = project_table["import-names"][0]
            logger.info(f"Identified package name '{output}' from pyproject.toml")
            return output
        else:
            output = project_table["name"]
            logger.info(f"Identified package name '{output}' from pyproject.toml")
            return output
    except Exception as e:
        sys.exit(
            "`--package` was not provided, and discovery based on "
            f"`pyproject.toml` failed with the following error: {str(e)}"
        )


def get_author_names_from_pyproject(pyproject_path: Path) -> str | None:
    """
    Get the package authors from a local `pyproject.toml`.

    Examples:

    ```
    authors = [{"name": "a b", "email": "a@b.c"}]
    authors = [{"name": "a b"}]
    authors = [{"email": "a@b.c"}]
    ```

    Reference:
    https://packaging.python.org/en/latest/specifications/pyproject-toml
    """
    try:
        with Path(pyproject_path).open("rb") as f:
            pyproject = tomllib.load(f)
        authors = pyproject["project"]["authors"]
        author_names = [author["name"] for author in authors]
        author_names_string = ", ".join(author_names)
        return author_names_string
    except Exception as e:
        logger.warning(
            f"Cannot get author names from {pyproject_path.as_posix()}. "
            f"Original error: {str(e)}"
        )
        return None
