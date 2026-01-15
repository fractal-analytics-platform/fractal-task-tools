from enum import Enum
from typing import Literal
from typing import Optional

from pydantic import validate_call


class MyEnum(Enum):
    name1 = "Value 1"
    name2 = "Value 2"


@validate_call
def task1(
    *,
    # Fractal-specific arguments
    zarr_urls: list[str],
    zarr_dir: str,
    # Task-specific arguments
    int_1: int,
    int_2: int = 1,
    int_3: int | None = None,
    int_4: Optional[int] = None,
    str_1: str,
    str_2: str = "default",
    bool_1: bool,
    bool_2: bool = False,
    float_1: float,
    float_2: float = 1.23,
    enum_1: MyEnum,
    enum_2: MyEnum = MyEnum.name1,
    literal_1: Literal["a", "b", "c"],
    literal_2: Literal["a", "b", "c"] = "a",
):
    """
    Short description

    Long description of this wonderful task that is called `task_function` and
    actually only represents a mock task for testing.

    Args:
        int_1: Integer argument.
        int_2: Integer argument with a default value.
        int_3: Integer or null argument, with default value set to null.
        int_4: Integer or null argument, with default value set to null.
        str_1: String argument.
        str_2: String argument with a default value.
        bool_1: Boolean argument.
        bool_2: Boolean argument with a default value.
        float_1: Float argument.
        float_2: Float argument with a default value
        enum_1: Enum argument.
        enum_2: Enum argument with a default.
        literal_1: Literal argument.
        literal_2: Literal argument with a default value.
    """
    pass
