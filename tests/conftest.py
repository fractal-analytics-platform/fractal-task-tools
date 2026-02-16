import pytest
from fractal_task_tools._deepdiff import ERRORS


@pytest.fixture(scope="function", autouse=True)
def ERRORS_cleanup():
    """
    Reset `ERRORS` after each test, to keep tests stateless.
    """
    yield
    ERRORS.reset_state()
