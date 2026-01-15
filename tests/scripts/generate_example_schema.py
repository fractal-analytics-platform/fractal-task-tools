import json
from enum import Enum
from typing import Annotated
from typing import Literal
from typing import Optional

from devtools import debug
from fractal_task_tools._args_schemas import create_schema_for_single_task
from pydantic import BaseModel
from pydantic import Field
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


class InternalModel1(BaseModel):
    label: Literal["label1"] = "label1"
    field: int = 1


class InternalModel2(BaseModel):
    label: Literal["label2"] = "label2"
    field: str


class InternalModel3(BaseModel):
    label: Literal["label3"] = "label3"
    field: bool


TaggedUnion = Annotated[
    InternalModel1 | InternalModel2 | InternalModel3,
    Field(discriminator="label"),
]


class Model2(BaseModel):
    label: Literal["label2"] = "label2"
    field2: int


class Model3(BaseModel):
    label: Literal["label3"] = "label3"
    field3: str


class MyEnum(Enum):
    name1 = "Value 1"
    name2 = "Value 2"


@validate_call
def task_function_scalar_arguments(
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
        int_1: Description of `int_1`.
        int_2: Description of `int_2`.
        str_1: Description of `str_1`.
        str_2: Description of `str_2`.
        bool_1: Description of `bool_1`.
        bool_2: Description of `bool_2`.
        float_1: Description of `float_1`.
        float_2: Description of `float_2`.
        enum_1: Description of `enum_1`.
        enum_2: Description of `enum_2`.
        literal_1: Description of `literal_1`.
        literal_2: Description of `literal_2`.
    """
    pass


@validate_call
def task_function_array_arguments(
    *,
    # Scalar arguments
    zarr_url: str,
    list_arg: list[int],
    tuple_arg: tuple[int, int, int],
    optional_list_arg: list[int] | None = None,
    optional_tuple_arg: tuple[int, int, int] | None = None,
):
    """
    Short description

    Long description of this wonderful task that is called `task_function` and
    actually only represents a mock task for testing.

    Args:
        list_arg: An arbitrary-size array of integers.
        tuple_arg: A fixed-size array of integers.
        optional_list_arg: An optional arbitrary-size array of integers.
        optional_tuple_arg: An optional fixed-size array of integers.
    """
    pass


@validate_call
def task_function_object_arguments(
    *,
    # Scalar arguments
    zarr_url: str,
    object_arg: dict[int, bool],
    optional_object_arg: dict[int, bool] | None = None,
):
    """
    Short description

    Long description of this wonderful task that is called `task_function` and
    actually only represents a mock task for testing.
    """
    pass


@validate_call
def task_function_2(
    *,
    # Complex arguments
    pydantic_1: ModelAllOptional,
    pydantic_2: ModelAllOptional = ModelAllOptional(),
    pydantic_3: ModelAllOptional = Field(default_factory=ModelAllOptional),
    pydantic_4: ModelSomeRequired,
    tagged_union: TaggedUnion = InternalModel1(),
):
    """
    Short description

    Long description of this wonderful task that is called `task_function` and
    actually only represents a mock task for testing.

    Args:
        pydantic_1: Description of `pydantic_1`.
        pydantic_2: Description of `pydantic_2`.
        pydantic_3: Description of `pydantic_3`.
        pydantic_4: Description of `pydantic_4`.
        tagged_union: Description of `tagged_union`.
    """
    pass


schema1 = create_schema_for_single_task(
    task_function=task_function_scalar_arguments,
    executable=__file__,
    package=None,
    verbose=True,
)
schema2 = create_schema_for_single_task(
    task_function=task_function_array_arguments,
    executable=__file__,
    package=None,
    verbose=True,
)
schema3 = create_schema_for_single_task(
    task_function=task_function_object_arguments,
    executable=__file__,
    package=None,
    verbose=True,
)
schema10 = create_schema_for_single_task(
    task_function=task_function_2,
    executable=__file__,
    package=None,
    verbose=True,
)
print()
print(json.dumps(schema1))
print()
print(json.dumps(schema2))
print()
print(json.dumps(schema3))
print()
