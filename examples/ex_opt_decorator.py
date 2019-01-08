
from fastlogging import LogInit, INFO, Optimize


logger = LogInit(console=True)


@Optimize(globals(), "logger", remove=INFO)
def bar():
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")


bar()
