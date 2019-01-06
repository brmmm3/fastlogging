
import os
import time

from fastlogging import LogInit, DEBUG


if __name__ == "__main__":
    addr = "127.0.0.1"
    port = 12345
    pathName = "C:/temp/fastlogging.log" if os.name == 'nt' else "/tmp/fastlogging.log"
    logger = LogInit(level=DEBUG, pathName=pathName, server=(addr, port))
    logger.info("Waiting 100s for connections...")
    time.sleep(100)
    logger.shutdown()
