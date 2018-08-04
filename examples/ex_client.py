
import os
import time

from fastlogging import LogInit, DEBUG


if __name__ == "__main__":
    addr = "127.0.0.1"
    port = 12345
    logger = LogInit(level=DEBUG, console=False, colors=True, connect=(addr, port, "HELLO%d" % os.getpid()))
    for i in range(100000):
        logger.debug("This is a DBG message %d." % i)
        logger.info("This is an INF message %d." % i)
        logger.warning("This is a WRN message %d." % i)
    time.sleep(10.0)
    logger.shutdown()
