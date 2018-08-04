
from fastlogging import GetLogger

if __name__ == "__main__":
    logger = GetLogger()
    logger.debug("This is a debug message.")
    logger.rotate()
    logger.fatal("This is a fatal message.")
    logger.shutdown()
