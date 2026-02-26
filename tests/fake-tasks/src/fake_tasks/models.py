from pydantic import BaseModel
from pydantic import Field


class ModelMixedDocstrings(BaseModel):
    """
    Description of ModelMixedDocstrings

    Attributes:
        a: Old-style for a
        b: Old-style for b
        d: Old-style for d
    """

    a: int = Field(description="Field for a")
    """
    New-style for a
    """

    b: int
    """
    New-style for b
    """

    c: int = Field(description="Field for c")

    d: int
