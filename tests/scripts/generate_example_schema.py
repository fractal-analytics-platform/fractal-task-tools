import json
from enum import Enum
from typing import Optional

from devtools import debug
from fractal_task_tools._args_schemas import create_schema_for_single_task
from pydantic import BaseModel
from pydantic import validate_call


class ModelAllOptional(BaseModel):
    """
    Short description of `ModelAllOptional`.
    """

    x: int | None = None
    """
    Description of x.
    """
    y: int = 1
    """
    Description of y.
    """


class ModelSomeRequired(BaseModel):
    """
    Short description of `ModelSomeRequired`.
    """

    x: int | None = None
    y: str


@validate_call
def task_function(
    *,
    # Scalar arguments
    zarr_url: str,
    int_1: int,
    int_2: int = 1,
    str_1: str,
    str_2: str = "default",
    bool_1: bool,
    bool_2: bool = False,
    float_1: float,
    float_2: float,
    # Complex arguments
    pydantic_1: ModelAllOptional,
    pydantic_2: ModelAllOptional = ModelAllOptional(),
    pydantic_3: ModelSomeRequired,
):
    """
    Short description

    Long description of this wonderful task that is called `task_function` and
    actually only represents a mock task for testing.

    Args:
        int_1: Description of int_1.
        int_2: Description of int_2.
        str_1: Description of str_1.
        str_2: Description of str_2.
        bool_1: Description of bool_1.
        bool_2: Description of bool_2.
        float_1: Description of float_1.
        float_2: Description of float_2.
        pydantic_1: Description of pydantic_1.
        pydantic_2: Description of pydantic_2.
        pydantic_3: Description of pydantic_3.
    """
    pass


schema = create_schema_for_single_task(
    task_function=task_function,
    executable=__file__,
    package=None,
    verbose=True,
)
print()
print(json.dumps(schema))
