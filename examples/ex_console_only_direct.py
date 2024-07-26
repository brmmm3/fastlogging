
from fastlogging import LogInit, Colors

if __name__ == "__main__":
    logger = LogInit(console=True, colors=True)
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.fatal("This is a fatal message.")
    logger.rotate()
    logger.fatal("This is a fatal message.")
    logger.fatal("This is a fatal message.")
    logger.fatal("This is a fatal message.")
    logger.exception("This is a exception message.")
    logger.shutdown()
