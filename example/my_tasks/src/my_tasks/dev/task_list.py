from fractal_task_tools.task_models import NonParallelTask

TASK_LIST = [
    NonParallelTask(name="task1", executable="task1.py"),
    NonParallelTask(name="task2", executable="task2.py"),
    NonParallelTask(name="task3", executable="task3.py"),
    NonParallelTask(name="task4", executable="task4.py"),
]


PACKAGE = "my-tasks"
AUTHORS = "Your Name"
INPUT_MODELS = [
    ("my_tasks", "task4.py", "ModelAllOptional"),
    ("my_tasks", "task4.py", "ModelSomeRequired"),
    ("my_tasks", "task4.py", "InternalModel1"),
    ("my_tasks", "task4.py", "InternalModel2"),
    ("my_tasks", "task4.py", "InternalModel3"),
]
