
import time

from fastlogging import LogInit, DEBUG


if __name__ == "__main__":
    addr = "127.0.0.1"
    port = 12345
    logger = LogInit(level = DEBUG, pathName = "C:/temp/fastlogging.log", server = (addr, port))
    logger.info("Waiting 10s for connections...")
    time.sleep(100)
    logger.shutdown()
