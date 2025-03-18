from pydantic import BaseModel


class MyModel(BaseModel):
    """
    Short description of `MyModel`

    Attributes:
        inner_arg: Something
    """

    inner_arg: int


def task1(
    arg1: int,
    arg2: MyModel,
):
    """
    Short description of `task1`.

    Long description (very very long).

    Arguments:
        arg1: An integer
        arg2: A `MyModel` object

    """
    pass
