
from fastlogging import LogInit, INFO, OptimizeObj


logger = LogInit(console=True)


def bar():
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")


optBar = OptimizeObj(globals(), bar, "logger", remove=INFO)
optBar()
