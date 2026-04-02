from fractal_task_tools.task_models import NonParallelTask

DOCS_LINK = "https://www.example.org"
INPUT_MODELS = [
    ("fake_tasks", "models.py", "ModelMixedDocstrings"),
    ("fake_tasks", "task2_with_inheritance.py", "GenericParameters"),
    ("fake_tasks", "task2_with_inheritance.py", "SpecificParameters"),
    ("fake_tasks", "task3_for_descriptions.py", "ParametersA"),
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
    NonParallelTask(
        name="Task2",
        executable="task2_with_inheritance.py",
    ),
    NonParallelTask(
        name="Task3",
        executable="task3_for_descriptions.py",
    ),
]
