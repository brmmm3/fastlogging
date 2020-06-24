from fastlogging import LogInit

logger = LogInit(console=True, colors=True)


def bar():
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
