from enum import Enum
from typing import Annotated
from typing import Literal

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
    """
    Description of InternalModel1.
    """

    label: Literal["label1"] = "label1"
    field: int = 1


class InternalModel2(BaseModel):
    """
    Description of InternalModel2.
    """

    label: Literal["label2"] = "label2"
    field: str


class InternalModel3(BaseModel):
    """
    Description of InternalModel3.

    Attributes:
        label: xxx
        field: yyy
    """

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
def task4(
    *,
    # Fractal-specific arguments
    zarr_urls: list[str],
    zarr_dir: str,
    # Task-specific arguments
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
