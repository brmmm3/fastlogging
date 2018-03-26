
import time
import logging.handlers
from fastlogging import LOG_DEBUG, WR_THREAD, LogInit

MB = 1024 * 1024

def LogWarning(msg):
    logger.warning(msg)


if __name__ == "__main__":
    from colorama import init
    #import zstd
    #ZC = zstd.ZstdCompressor()
    init()
    cnt = 2000
    t1 = time.time()
    logger = LogInit("main", LOG_DEBUG, "/tmp/fast_example.log", MB, 8, False, False, write = WR_THREAD)#, ( ZC, ".zstd" ))
    #logger.info("Hello World", status = ST_IDLE)
    #logger.debug("Debug Message", status = ST_MASTER_BUSY)
    #logger.fatal("Fatal Message", status = ST_WORKER_IDLE)
    #logger.error("Error Message", status = ST_MASTER_BUSY)
    for i in range(cnt):
        logger.warning("Warning %d Message" % i)
        logger.info("Info Message %d" % i)
        logger.fatal("Fatal Error %d" % i)
        logger.info("Info %d Info" % i)
        logger.warning("Warning %d Message" % i)
        logger.info("Info Message %d" % i)
        logger.fatal("Fatal Error %d" % i)
        logger.info("Info %d Info" % i)
        logger.warning("Warning %d Message" % i)
        logger.info("Info Message %d" % i)
        logger.fatal("Fatal Error %d" % i)
        logger.info("Info %d Info" % i)
        logger.warning("Warning %d Message" % i)
        logger.info("Info Message %d" % i)
        logger.fatal("Fatal Error %d" % i)
        logger.info("Info %d Info" % i)
        logger.warning("Warning %d Message" % i)
        logger.info("Info Message %d" % i)
        logger.fatal("Fatal Error %d" % i)
        logger.info("Info %d Info" % i)
        try:
            x = 1 / 0
        except:
            logger.exception("EXCEPTION")
    logger.info("Info Message")
    #LogWarning("Warning Message")
    #LogWarning("Warning Message")
    #LogWarning("Warning Message")
    #LogWarning("Warning Message")
    #LogWarning("Warning Message")
    print(time.time() - t1)
    logger.shutdown()
    print(time.time() - t1)
    t1 = time.time()
    logHandler = logging.handlers.RotatingFileHandler("/tmp/logging_example.log", mode = 'a', maxBytes = MB, backupCount = 8, encoding = None, delay = 0)
    logFormatter = logging.Formatter('%(asctime)-15s %(name)s %(levelname)-8.8s %(message)s', "%Y.%m.%d %H:%M:%S")
    logHandler.setFormatter(logFormatter)
    logHandler.setLevel(logging.DEBUG)
    logger = logging.getLogger('root')
    logger.addHandler(logHandler)
    logger.setLevel(logging.DEBUG)
    for i in range(cnt):
        logger.warning("Warning %d Message" % i)
        logger.info("Info Message %d" % i)
        logger.fatal("Fatal Error %d" % i)
        logger.info("Info %d Info" % i)
        logger.warning("Warning %d Message" % i)
        logger.info("Info Message %d" % i)
        logger.fatal("Fatal Error %d" % i)
        logger.info("Info %d Info" % i)
        logger.warning("Warning %d Message" % i)
        logger.info("Info Message %d" % i)
        logger.fatal("Fatal Error %d" % i)
        logger.info("Info %d Info" % i)
        logger.warning("Warning %d Message" % i)
        logger.info("Info Message %d" % i)
        logger.fatal("Fatal Error %d" % i)
        logger.info("Info %d Info" % i)
        logger.warning("Warning %d Message" % i)
        logger.info("Info Message %d" % i)
        logger.fatal("Fatal Error %d" % i)
        logger.info("Info %d Info" % i)
        try:
            x = 1 / 0
        except:
            logger.exception("EXCEPTION")
    logger.info("Info Message")
    print(time.time() - t1)

