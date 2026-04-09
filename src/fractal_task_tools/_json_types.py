from typing import TypeAlias

JSONType: TypeAlias = (
    dict[str, "JSONType"] | list["JSONType"] | str | int | float | bool | None
)
"""
Type of a JSON document.
"""

JSONdictType = dict[str, JSONType]
"""
Type of a JSON-object document.
"""
