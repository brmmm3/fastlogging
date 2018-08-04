
import time

from fastlogging import LogInit, DEBUG


if __name__ == "__main__":
    addr = "127.0.0.1"
    port = 12345
    logger = LogInit(pathName="C:/temp/server.log", level=DEBUG, console=False, colors=True, server=(addr, port))
    logger.info("Logging started.")
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    time.sleep(15)
    logger.info("Shutdown logging.")
    logger.shutdown()
