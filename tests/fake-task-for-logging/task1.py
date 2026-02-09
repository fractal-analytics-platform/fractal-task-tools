import logging

from pydantic import validate_call

logger_name = "task1"
logger = logging.getLogger(logger_name)


@validate_call
def task1(
    zarr_urls: list[str],
    zarr_dir: str,
    arg: int | None = None,
):
    logger.debug("DEBUG from task")
    logger.info("INFO from task")
    logger.warning("WARNING from task")
    logger.error("ERROR from task")

    return ["something"]


if __name__ == "__main__":
    from fractal_task_tools.task_wrapper import run_fractal_task

    run_fractal_task(
        task_function=task1,
        logger_name=logger_name,
    )
