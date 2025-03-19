import re


def normalize_package_name(pkg_name: str) -> str:
    """
    Implement both PyPa and custom package-name normalization

    1. PyPa normalization: The name should be lowercased with all runs of the
        characters `.`, `-`, or `_` replaced with a single `-` character
        (https://packaging.python.org/en/latest/specifications/name-normalization).
    2. Custom normalization: Replace `-` with `_`, to obtain the
        imported-module name.

    Args:
        pkg_name: The non-normalized package name.

    Returns:
        The normalized package name.
    """

    # Apply PyPa normalization
    pypa_normalized_package_name = re.sub(r"[-_.]+", "-", pkg_name).lower()

    # Replace `-` with `_`
    final_package_name = pypa_normalized_package_name.replace("-", "_")

    return final_package_name
