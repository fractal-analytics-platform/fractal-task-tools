from enum import Enum
from typing import Annotated
from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import validate_call


class ModelAllOptional(BaseModel):
    """
    Short description of `ModelAllOptional`.

    Attributes:
        x: FIXME
        y: FIXME
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

    Attributes:
        x: FIXME
        y: FIXME
    """

    x: int | None = None
    """
    Description of x.
    """
    y: str
    """
    Description of y.
    """


class InternalModel1(BaseModel):
    """
    Description of InternalModel1.

    Attributes:
        label: FIXME
        field:
    """

    label: Literal["label1"] = "label1"
    field: int = 1


class InternalModel2(BaseModel):
    """
    Description of InternalModel2.

    Attributes:
        label: FIXME
        field:
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
    nested_tagged_union: list[TaggedUnion] = Field(default_factory=list),
):
    """
    Short description of task4

    Long description of this wonderful task that actually only represents a
    mock task for testing.

    Args:
        pydantic_1: Example of a Pydantic model with no required field.
        pydantic_2:
            Example of a Pydantic model with no required field, with a default
            value.
        pydantic_3:
            Example of a Pydantic model with no required field, with a default
            factory.
        pydantic_4: Example of a Pydantic model with some required field.
        tagged_union:
            Example of a top-level tagged union, with a default value.
        nested_tagged_union:
            Example of a nested tagged union, with a default value.
    """
    pass
