from pydantic import BaseModel
from pydantic import Field


class ParametersA(BaseModel):
    """
    `ParametersA` model description

    Attributes:
        a: This is a long description with no new lines. This is a long
            description with no new lines.
            Even if I go to a new line, it has no new lines.
                Even I add more indentation, there is no tab.
    """

    a: int


class ParametersB(BaseModel):
    """
    `ParametersB` model description
    """

    b: int
    """
    This is a long description which may include new lines. Here is a new line:
    This is a new line, separated from the previous one. Here is another new line:
        This is a new line, indented by four spaces.
    """


class ParametersC(BaseModel):
    """
    `ParametersC` model description
    """

    c: int = Field(
        description=(
            "This is a description where we have full control. "
            "Here is a new line:\nNew line.\n"
            "Here is a tab:\tand then more text."
        )
    )


def task3_for_descriptions(
    zarr_urls: list[str],
    zarr_dir: str,
    arg_A: ParametersA,
    arg_B: ParametersB,
    arg_C: ParametersC,
):
    """
    Short description

    Args:
        arg_A: This is a very very very very very very very very very very
            very long description, but it has no new lines.

            Even if skip a line, it has no new lines.
                Indentation is ignored.
        arg_B: -
        arg_C: -
    """
