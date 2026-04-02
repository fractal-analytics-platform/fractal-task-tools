from fractal_task_tools.task_models import NonParallelTask

DOCS_LINK = "https://www.example.org"
TASK_LIST = [
    NonParallelTask(
        name="Task1",
        executable="task1.py",
        meta={"cpus_per_task": 1, "mem": 4000},
        category="Conversion",
        modality="HCS",
        tags=["Yokogawa", "Cellvoyager", "2D", "3D"],
    ),
    NonParallelTask(
        name="Task2",
        executable="task2_with_inheritance.py",
    ),
    NonParallelTask(
        name="Task3",
        executable="task3_for_descriptions.py",
    ),
]
