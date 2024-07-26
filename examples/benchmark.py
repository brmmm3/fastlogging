
import os
import sys
import time
import logging.handlers

import simplejson as json
import shutil
from fastlogging import FATAL, ERROR, WARNING, INFO, DEBUG, LogInit, LOG2SSYM, OptimizeObj

MB = 1024 * 1024

tmpDirName = "C:\\temp" if os.name == 'nt' else "/tmp"


# noinspection PyShadowingNames
def LoggingWork(logger, message, cnt):
    t1 = time.time()
    for i in range(cnt):
        logger.fatal("Fatal %d %s", i, message)
        logger.error("Error %d %s", i, message)
        logger.warning("Warning %d %s", i, message)
        logger.info("Info %d %s", i, message)
        logger.debug("Debug %d %s", i, message)
        logger.fatal("Fatal %d %s", i, message)
        logger.error("Error %d %s", i, message)
        logger.warning("Warning %d %s", i, message)
        logger.info("Info %d %s", i, message)
        logger.debug("Debug %d %s", i, message)
        logger.fatal("Fatal %d %s", i, message)
        logger.error("Error %d %s", i, message)
        logger.warning("Warning %d %s", i, message)
        logger.info("Info %d %s", i, message)
        logger.debug("Debug %d %s", i, message)
        # noinspection PyBroadException
        try:
            # noinspection PyUnusedLocal
            x = 1 / 0
        except:
            logger.exception("EXCEPTION")
    dt = time.time() - t1
    print("  dt: %.3f" % dt)


# noinspection PyShadowingNames
def DoLogging(cnt, message, level=logging.DEBUG, fileName=None, bRotate=False):
    title = [LOG2SSYM[level], "FILE" if fileName else "NO FILE"]
    if bRotate:
        title.append("ROTATE")
    if fileName:
        key = "LOGGING_" + "_".join(title)
        dirName = os.path.join(tmpDirName, key)
        if os.path.exists(dirName):
            shutil.rmtree(dirName)
        os.makedirs(dirName)
        pathName = os.path.join(dirName, fileName)
        if bRotate:
            logHandler = logging.handlers.RotatingFileHandler(pathName, mode='a', maxBytes=MB, backupCount=8)
        else:
            logHandler = logging.FileHandler(pathName)
    else:
        logHandler = logging.NullHandler()
    logFormatter = logging.Formatter('%(asctime)-15s %(name)s %(levelname)-8.8s %(message)s', "%Y.%m.%d %H:%M:%S")
    logHandler.setFormatter(logFormatter)
    logHandler.setLevel(level)
    logger = logging.getLogger('root')
    logger.addHandler(logHandler)
    logger.setLevel(level)
    print("logging:", ", ".join(title))
    t1 = time.time()
    LoggingWork(logger, message, cnt)
    logHandler.close()
    dt = time.time() - t1
    print("  total: %.3f" % dt)
    return dt


# noinspection PyShadowingNames
def DoFastLogging(cnt, message, level=DEBUG, fileName=None, bRotate=False, bThreads=False, compress=None, cbOptimized=None, prefix=None):
    title = []
    if prefix:
        title.append(prefix.upper())
    title.append(LOG2SSYM[level])
    title.append("FILE" if fileName else "NO FILE")
    if bRotate:
        title.append("ROTATE")
        size = MB
        count = 8
    else:
        size = 0
        count = 0
    title.append("THREADS" if bThreads else "DIRECT")
    if compress:
        title.append("COMPRESS")
    if cbOptimized:
        title.append("OPTIMIZED")
    if fileName:
        key = "FAST_" + "_".join(title)
        dirName = os.path.join(tmpDirName, key)
        if os.path.exists(dirName):
            shutil.rmtree(dirName)
        os.makedirs(dirName)
        pathName = os.path.join(dirName, fileName)
    else:
        pathName = None
    print("fastlogging:", ", ".join(title))
    t1 = time.time()
    logger = LogInit("main", level, pathName, size, count, False, False, useThreads=bThreads, compress=compress)
    if cbOptimized is None:
        LoggingWork(logger, message, cnt)
    else:
        cbOptimized(logger, message, cnt)
    logger.shutdown()
    dt = time.time() - t1
    print("  total: %.3f" % dt)
    return dt


if __name__ == "__main__":
    import zstandard as zstd
    ZC = zstd.ZstdCompressor(level=14)
    cnt = 5000
    print("cnt:", cnt)
    fileName = "logging.log"
    fastFileName = "logging.log"
    htmlTemplate = open("../doc/benchmarks/template.html").read()
    shortMessage = "Message"
    longMessage = "Message Message Message Message Message Message Message Message Message Message Message Message Message"
    # Benchmark fastlogging module without threads
    for title, name, message, fileName, bRotate in (("No log file short", "nolog_short", shortMessage, None, False),
                                                    ("Log file short", "log_short", shortMessage, "logging.log", False),
                                                    ("Rotating log file short", "rotate_short", shortMessage, "logging.log", True),
                                                    ("No log file long", "nolog_long", longMessage, None, False),
                                                    ("Log file long", "log_long", longMessage, "logging.log", False),
                                                    ("Rotating log file long", "rotate_long", longMessage, "logging.log", True)):
        print("#", title)
        dtAll = {"TITLE": title}
        for level in (DEBUG, INFO, WARNING, ERROR, FATAL):
            dts = [DoLogging(cnt, message, level, fileName, bRotate),
                   DoFastLogging(cnt, message, level, fileName, bRotate),
                   DoFastLogging(cnt, message, level, fileName, bRotate, True)]
            # Benchmark fastlogging module with AST optimization constants to values conversion
            LoggingWorkOptCst = OptimizeObj(globals(), LoggingWork, "logger", optimize=level, const2value=True)
            dts.append(DoFastLogging(cnt, message, level, fileName, bRotate, cbOptimized=LoggingWorkOptCst, prefix="CONST2VALUE"))
            # Benchmark fastlogging module with AST optimization level
            LoggingWorkOpt = OptimizeObj(globals(), LoggingWork, "logger", optimize=level)
            dts.append(DoFastLogging(cnt, message, level, fileName, bRotate, cbOptimized=LoggingWorkOpt))
            # Benchmark fastlogging module with AST optimization remove
            LoggingWorkOptRem = OptimizeObj(globals(), LoggingWork, "logger", remove=level)
            dts.append(DoFastLogging(cnt, message, level, fileName, bRotate, cbOptimized=LoggingWorkOptRem, prefix="REMOVE"))
            dtAll[LOG2SSYM[level]] = ", ".join(["%.4f" % dt for dt in dts])
        fileName = "../doc/benchmarks/%s_%s_%s." % (sys.platform, sys.version.split(" ")[0].replace(".", "_"), name)
        with open("%s.dat" % fileName, "w") as F:
            F.write(json.dumps(dtAll))
        with open("%s.html" % fileName, "w") as F:
            F.write(htmlTemplate % dtAll)
    # Benchmark fastlogging module with threads
    DoFastLogging(cnt, message, FATAL, fastFileName, bThreads=True)
