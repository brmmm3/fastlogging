
from fastlogging import DEBUG, LogInit

if __name__ == "__main__":
    logger = LogInit("main", DEBUG, "/tmp/example1.log", 1000, 3, True, True, useThreads = True)
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.fatal("This is a fatal message.")
    logger.rotate()
    logger.fatal("This is a fatal message.")
    logger.fatal("This is a fatal message.")
    logger.fatal("This is a fatal message.")
    logger.shutdown()
