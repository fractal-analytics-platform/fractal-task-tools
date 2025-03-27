from fractal_task_tools.task_models import NonParallelTask

AUTHORS = "Fake Fake"
DOCS_LINK = "https://www.example.org"
INPUT_MODELS = [
    ["fake_tasks", "task1.py", "MyModel"],
]


TASK_LIST = [
    NonParallelTask(
        name="Task1",
        executable="task1.py",
        meta={"cpus_per_task": 1, "mem": 4000},
        category="Conversion",
        modality="HCS",
        tags=["Yokogawa", "Cellvoyager", "2D", "3D"],
    ),
]
