from fractal_task_tools.task_models import CompoundTask
from fractal_task_tools.task_models import ConverterCompoundTask
from fractal_task_tools.task_models import ConverterNonParallelTask
from fractal_task_tools.task_models import NonParallelTask
from fractal_task_tools.task_models import ParallelTask

NAME = "name"
EXECUTABLE = "executable"
EXECUTABLE_INIT = "executable_init"
META = {"some": "thing"}
META_INIT = {"some": "thing-init"}


def test_compound_task_model():
    t = CompoundTask(
        name=NAME,
        executable_init=EXECUTABLE_INIT,
        meta_init=META_INIT,
        executable=EXECUTABLE,
        meta=META,
    )
    assert t.executable_non_parallel == EXECUTABLE_INIT
    assert t.meta_non_parallel == META_INIT
    assert t.executable_parallel == EXECUTABLE
    assert t.meta_parallel == META

    t = ConverterCompoundTask(
        name=NAME,
        executable_init=EXECUTABLE_INIT,
        meta_init=META_INIT,
        executable=EXECUTABLE,
        meta=META,
    )
    assert t.executable_non_parallel == EXECUTABLE_INIT
    assert t.meta_non_parallel == META_INIT
    assert t.executable_parallel == EXECUTABLE
    assert t.meta_parallel == META


def test_non_parallel_task_model():
    t = NonParallelTask(
        name=NAME,
        executable=EXECUTABLE_INIT,
        meta=META_INIT,
    )
    assert t.executable_non_parallel == EXECUTABLE_INIT
    assert t.meta_non_parallel == META_INIT
    assert t.executable_parallel is None
    assert t.meta_parallel is None

    t = ConverterNonParallelTask(
        name=NAME,
        executable=EXECUTABLE_INIT,
        meta=META_INIT,
    )
    assert t.executable_non_parallel == EXECUTABLE_INIT
    assert t.meta_non_parallel == META_INIT
    assert t.executable_parallel is None
    assert t.meta_parallel is None


def test_parallel_task_model():
    t = ParallelTask(
        name=NAME,
        executable=EXECUTABLE,
        meta=META,
    )
    assert t.executable_non_parallel is None
    assert t.meta_non_parallel is None
    assert t.executable_parallel == EXECUTABLE
    assert t.meta_parallel == META
