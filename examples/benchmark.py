
import os
import time
import logging.handlers
from fastlogging import FATAL, DEBUG, LogInit, optimize_obj

MB = 1024 * 1024


def LoggingWork(logger, cnt):
    t1 = time.time()
    for i in range(cnt):
        logger.warning("Warning %d Message", i)
        logger.info("Info Message %d", i)
        logger.debug("Fatal Error %d", i)
        logger.info("Info %d Info", i)
        logger.warning("Warning %d Message", i)
        logger.info("Info Message %d", i)
        logger.debug("Fatal Error %d", i)
        logger.info("Info %d Info", i)
        logger.warning("Warning %d Message", i)
        logger.info("Info Message %d", i)
        logger.debug("Fatal Error %d", i)
        logger.info("Info %d Info", i)
        logger.warning("Warning %d Message", i)
        logger.info("Info Message %d", i)
        logger.debug("Fatal Error %d", i)
        logger.info("Info %d Info", i)
        logger.warning("Warning %d Message", i)
        logger.info("Info Message %d", i)
        logger.debug("Fatal Error %d", i)
        logger.info("Info %d Info", i)
        try:
            x = 1 / 0
        except:
            logger.exception("EXCEPTION")
    logger.info("Info Message")
    print(cnt, time.time() - t1)


def DoLogging(title, logger, cnt):
    for fileName in os.listdir("/tmp"):
        if "logging.log" in fileName:
            os.remove(os.path.join("/tmp", fileName))
    print("logging:", title)
    t1 = time.time()
    LoggingWork(logger, cnt)
    print("FINISHED", time.time() - t1)
    print()


def DoFastLogging(title, logger, cnt, cbDoLogging):
    for fileName in os.listdir("/tmp"):
        if "fastlogging.log" in fileName:
            os.remove(os.path.join("/tmp", fileName))
    print("fastlogging:", title)
    t1 = time.time()
    cbDoLogging(logger, cnt)
    logger.shutdown()
    print("FINISHED", time.time() - t1)
    print()


if __name__ == "__main__":
    import zstd
    ZC = zstd.ZstdCompressor()
    cnt = 5000
    logHandler = logging.handlers.RotatingFileHandler("/tmp/logging.log", mode = 'a', maxBytes = MB, backupCount = 8, encoding = None, delay = 0)
    logFormatter = logging.Formatter('%(asctime)-15s %(name)s %(levelname)-8.8s %(message)s', "%Y.%m.%d %H:%M:%S")
    logHandler.setFormatter(logFormatter)
    logHandler.setLevel(logging.DEBUG)
    logger = logging.getLogger('root')
    logger.addHandler(logHandler)
    logger.setLevel(logging.DEBUG)
    #DoLogging("ROTATE", logger, cnt)
    logger.setLevel(logging.FATAL)
    DoLogging("ROTATE, FATAL", logger, cnt)
    #
    logger = LogInit()
    logger.setLevel(FATAL)
    DoFastLogging("NO FILE, DIRECT, FATAL", logger, cnt, LoggingWork)
    sys.exit(0)
    logger = LogInit()
    DoFastLogging("NO FILE, DIRECT", logger, cnt, LoggingWork)
    logger = LogInit(useThreads = True)
    DoFastLogging("NO FILE, THREADED", logger, cnt, LoggingWork)
    logger = LogInit("main", DEBUG, "/tmp/fastlogging.log")
    DoFastLogging("FILE DIRECT", logger, cnt, LoggingWork)
    logger = LogInit("main", DEBUG, "/tmp/fastlogging.log", write = WR_THREAD)
    DoFastLogging("FILE THREADED", logger, cnt, LoggingWork)
    logger = LogInit("main", DEBUG, "/tmp/fastlogging.log", MB, 8)
    DoFastLogging("ROTATE DIRECT", logger, cnt, LoggingWork)
    logger = LogInit("main", DEBUG, "/tmp/fastlogging.log", MB, 8, False, False, write = WR_THREAD)#, ( ZC, ".zstd" ))
    DoFastLogging("ROTATE THREADED", logger, cnt, LoggingWork)
    logger = LogInit("main", DEBUG, "/tmp/fastlogging.log", MB, 8, False, False, write = WR_THREAD, compress = ( ZC, ".zstd" ))
    DoFastLogging("ROTATE COMPRESSED THREADED", logger, cnt, LoggingWork)
    LoggingWorkOpt = optimize_obj(LoggingWork, "logger", FATAL)
    logger = LogInit()
    logger.setLevel(FATAL)
    DoFastLogging("NO FILE, DIRECT, FATAL, OPTIMIZED", logger, cnt, LoggingWorkOpt)
    logger = LogInit()
    DoFastLogging("NO FILE, DIRECT, OPTIMIZED", logger, cnt, LoggingWorkOpt)
    logger = LogInit("main", DEBUG, "/tmp/fastlogging.log", MB, 8)
    DoFastLogging("ROTATE DIRECT, OPTIMIZED", logger, cnt, LoggingWorkOpt)

