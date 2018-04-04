# Copyright 2018 Martin Bammer. All Rights Reserved.
# Licensed under MIT license.

"""Implements lightweight and fast logging."""

import os
import sys
import atexit
import time
import traceback
from collections import deque
from threading import Thread, Timer, Event

# Log-Levels
CRITICAL = 50
FATAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10

LOG2SYM = {FATAL : "FATAL  ", ERROR : "ERROR  ", WARNING : "WARNING",
           INFO : "INFO   ", DEBUG : "DEBUG  "}

LOG2SSYM = {FATAL : "FAT", ERROR : "ERR", WARNING : "WRN",
            INFO : "INF", DEBUG : "DBG"}

try:
    from colorama import init as initColorama, Fore, Style
    initColorama()
    NORMAL = Style.RESET_ALL
    BRIGHT = Style.BRIGHT
    WHITE = Fore.WHITE
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    GREEN = Fore.GREEN
    BRIGHTRED = BRIGHT + RED
    BRIGHTYELLOW = BRIGHT + YELLOW
    BRIGHTGREEN = BRIGHT + GREEN

    LVL2COL = {FATAL : BRIGHTRED, ERROR : RED, WARNING : BRIGHTYELLOW,
               INFO: BRIGHTGREEN, DEBUG: WHITE}
except ImportError:
    NORMAL = ""
    BRIGHTRED = ""

    LVL2COL = {FATAL : "", ERROR : "", WARNING : "", INFO : "", DEBUG : ""}


def Shutdown(now=True):
    for logger in tuple(domains.values()):
        logger.shutdown(now)


atexit.register(Shutdown)


domains = {}            # Dictionary holding all Logger instances for the configured domains


class LastMessage(object):

    def __init__(self, key, cnt, entry):
        self.key = None
        self.cnt = 1
        self.entry = None


class CommonConfig(object):

    def __init__(self, queue, evtQueue, evtRotate, maxSize, backupCnt):
        self.queue = queue
        self.evtQueue = evtQueue
        self.evtRotate = evtRotate
        self.maxSize = maxSize
        self.backupCnt = backupCnt


class ConsoleLogger(Thread):

    def __init__(self):
        self.name = "LogConsoleThread"
        self.daemon = True
        self.queue = deque()
        self.evtQueue = Event()
        self.stdOut = sys.stdout
        self.stdErr = sys.stderr

    def append(self, message):
        self.queue.append(message)
        self.evtQueue.set()

    def run(self):
        while True:
            try:
                entry = self.queue.popleft()
                if entry is None:
                    break
            except:
                self.evtQueue.wait()
                self.evtQueue.clear()
                continue
            print(entry[1], file=self.stdOut if entry[0] < ERROR else self.stdErr)


class Logger(object):

    backlog = None
    dateFmt = "%y.%m.%d %H:%M:%S"
    cbMessageKey = None     # Custom log messages key calculation callback function
    cbFormatter = None      # Custom log messages formatter callback function
    cbWriter = None         # Custom log messages writer callback function
    colors = False          # Enable/Disable colored logging to console
    compress = None         # ( CompressorInstance, CompressedFileExtension )
    useThreads = False      # Write log messages in main thread or in background thread
    encoding = None
    sameMsgTimeout = 30.0   # Timeout for same log messages in a row
    sameMsgCountMax = 1000  # Maximum counter value for same log messages in a row
    thrConsoleLogger = None

    def __init__(self, domain, level, pathName, maxSize, backupCnt, console):
        if (maxSize < 0) or (backupCnt < 0) or ((maxSize > 0) and (backupCnt == 0)):
            raise ValueError("Invalid maxSize or backupCnt")
        self.domain = domain
        self.level = level
        self.common = CommonConfig(deque(), Event(), Event(), maxSize, backupCnt)
        self._lastMsg = LastMessage(None, 1, None)
        self.pathName = pathName
        self.F = None
        self.buf = []
        self.size = 0
        self.pos = 0
        self.__console = console
        self.__thrTimer = None
        self.__thrLogger = None
        self.stopped = False
        if pathName is not None and os.path.isdir(os.path.dirname(pathName)):
            for logger in domains.values():
                if pathName == logger.pathName:
                    common = logger.common
                    self.common = CommonConfig(common.queue, common.evtQueue, common.evtRotate,
                                               common.maxSize, common.backupCnt)
                    break
            else:
                self.F = open(pathName, "a", encoding=Logger.encoding)
                self.pos = self.F.tell()
                if Logger.useThreads:
                    self.__thrLogger = Thread(target=self.__logThread, daemon=True,
                                              name="LogThread_%s" % domain)
                    self.__thrLogger.start()
        if Logger.useThreads and Logger.thrConsoleLogger is None:
            Logger.thrConsoleLogger = ConsoleLogger()
            Logger.thrConsoleLogger.start()

    def setLevel(self, level):
        self.level = level

    @staticmethod
    def setBacklog(size):
        if size > 0:
            Logger.backlog = deque(Logger.backlog, maxlen=size)
        else:
            Logger.backlog = None

    def __log(self, level, msg, args, kwargs):
        if self.stopped:
            raise RuntimeError("Logger already stopped")
        if args:
            msg = msg % args
        if not Logger.useThreads or self.__thrLogger is None:
            self.__logEntry((time.time(), self.domain, level, msg, kwargs))
        else:
            self.common.queue.append((time.time(), self.domain, level, msg, kwargs))
            self.common.evtQueue.set()

    def log(self, level, msg, *args, **kwargs):
        self.__log(level, msg, args, kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.level <= DEBUG:
            self.__log(DEBUG, msg, args, kwargs)

    def info(self, msg, *args, **kwargs):
        if self.level <= INFO:
            self.__log(INFO, msg, args, kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.level <= WARNING:
            self.__log(WARNING, msg, args, kwargs)

    def error(self, msg, *args, **kwargs):
        if self.level <= ERROR:
            self.__log(ERROR, msg, args, kwargs)

    def fatal(self, msg, *args, **kwargs):
        if self.level <= FATAL:
            self.__log(FATAL, msg, args, kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.level <= FATAL:
            self.__log(FATAL, msg, args, kwargs)

    def exception(self, msg, *args, **kwargs):
        kwargs["exc_info"] = traceback.format_exc()
        self.__log(FATAL, msg, args, kwargs)

    def stop(self, now=False):
        if self.__thrTimer is not None:
            self.__thrTimer.cancel()
            self.__thrTimer.join()
            self.__thrTimer = None
            self.__logMessage(self._lastMsg.key, self._lastMsg.entry, self._lastMsg.cnt)
        if now:
            self.common.queue.clear()
        self.common.queue.append(None)
        self.common.evtQueue.set()
        self.stopped = True

    def join(self):
        if self.__thrLogger is not None:
            self.__thrLogger.join()
            self.__thrLogger = None
        del domains[self.domain]
        if not domains and Logger.thrConsoleLogger is not None:
            Logger.thrConsoleLogger.append(None)
            Logger.thrConsoleLogger.join()
            Logger.thrConsoleLogger = None

    def shutdown(self, now=False):
        self.stop(now)
        self.join()

    def rotate(self, logger=None):
        if logger is None:
            loggers = domains.values()
        else:
            loggers = [logger]
        signaled = set()
        for logger in loggers:
            if logger.F is None or logger.common.evtRotate in signaled:
                continue
            signaled.add(logger)
            if Logger.useThreads:
                logger.common.evtRotate.set()
                logger.common.evtQueue.set()
            else:
                self.__rotate(logger)

    def __rotate(self, logger=None):
        self.__writePending(logger)
        logger.F.flush()
        logger.F.close()
        logger.pos = 0
        path_join = os.path.join
        pathName = logger.pathName
        dirName, logFileName = os.path.split(pathName)
        zExt = "" if Logger.compress is None else Logger.compress[1]
        fileNames = {fileName for fileName in os.listdir(dirName) if fileName.startswith(logFileName)}
        try:
            for cnt in range(self.common.backupCnt, 1, -1):
                srcFileName = "%s.%d%s" % (logFileName, cnt - 1, zExt)
                if srcFileName not in fileNames:
                    continue
                os.replace(path_join(dirName, srcFileName),
                           path_join(dirName, "%s.%d%s" % (logFileName, cnt, zExt)))
        except:
            pass
        dstFileName = "%s.1%s" % (logFileName, zExt)
        if Logger.compress is None:
            os.replace(pathName, path_join(dirName, dstFileName))
        else:
            with open(path_join(dirName, dstFileName), "wb") as Z:
                Z.write(Logger.compress[0].compress(open(pathName, "rb").read()))
            os.remove(pathName)
        logger.F = open(pathName, "a", encoding=Logger.encoding)

    @staticmethod
    def __writePending(logger):
        if logger.buf:
            if Logger.cbWriter is None:
                data = "".join(logger.buf)
                logger.F.write(data)
                del logger.buf[:]
                logger.size = 0
            else:
                Logger.cbWriter(logger)

    def __logMessage(self, key, entry, cnt=0):
        if Logger.backlog is not None:
            Logger.backlog.append(entry)
        logTime, _, level, msg, kwargs = entry # logTime, domain, level, msg, kwargs
        if Logger.cbFormatter is None:
            sTime = time.strftime(Logger.dateFmt, time.localtime(logTime))
            if "exc_info" in kwargs:
                message = "%s: %s: %s\n%s" % (sTime, LOG2SYM[level], msg, kwargs["exc_info"])
            else:
                message = "%s: %s: %s" % (sTime, LOG2SYM[level], msg)
        else:
            message = Logger.cbFormatter(self, entry)
        if cnt > 0:
            message = "%d times: %s" % (cnt, message)
        self._lastMsg.key = key
        self._lastMsg.cnt = 1
        self._lastMsg.entry = entry
        console = False
        try:
            if self.F is not None:
                self.buf.append(message + "\n")
                size = len(message) + 1
                self.size += size
                if self.common.maxSize == 0:
                    if (self.size >= 65536) or not Logger.useThreads:
                        self.__writePending(self)
                    return
                self.pos += size
                if self.pos < self.common.maxSize:
                    if not Logger.useThreads:
                        self.__writePending(self)
                    return
                console = self.__console
        except:
            errMsg = traceback.format_exc()
            if Logger.backlog is not None:
                Logger.backlog.append(errMsg)
            print("%s%s%s" % (BRIGHTRED, errMsg, NORMAL), file=sys.stderr)
        if console or self.__console or kwargs.get("console", False):
            if Logger.colors:
                if "color" in kwargs:
                    color = kwargs["color"]
                else:
                    color = LVL2COL.get(level, FATAL)
                message = "%s%s%s" % (color, message, NORMAL)
            if Logger.thrConsoleLogger is None:
                print(message, file=sys.stdout if level < ERROR else sys.stderr)
            else:
                Logger.thrConsoleLogger.append((level, message))

    def __logEntry(self, entry):
        # logTime, domain, level, msg, kwargs
        if Logger.cbMessageKey is None:
            key = entry[3]
        else:
            key = Logger.cbMessageKey(self, entry)
        _lastMsg = self._lastMsg
        if (key == _lastMsg.key) and (_lastMsg.cnt < Logger.sameMsgCountMax):
            _lastMsg.cnt += 1
            _lastMsg.entry = entry
            if self.__thrTimer is None:
                self.__thrTimer = Timer(Logger.sameMsgTimeout, self.__logMessage, key, entry)
                self.__thrTimer.start()
        elif self.__thrTimer is None:
            self.__logMessage(key, entry)
        else:
            self.__thrTimer.cancel()
            self.__thrTimer.join()
            self.__thrTimer = None
            self.__logMessage(key, _lastMsg.entry, _lastMsg.cnt)
            self.__logMessage(key, entry)

    def __logThread(self):
        while True:
            try:
                entry = self.common.queue.popleft()
                if entry is None:
                    if self.F is not None:
                        if self.buf:
                            self.__writePending(self)
                        self.F.flush()
                        self.F.close()
                        self.F = None
                    break
            except:
                if self.F is not None and self.buf:
                    self.__writePending(self)
                common = self.common
                common.evtQueue.wait()
                common.evtQueue.clear()
                if common.evtRotate.is_set():
                    common.evtRotate.clear()
                    self.__rotate(self)
                continue
            try:
                self.__logEntry(entry)
            except:
                errMsg = traceback.format_exc()
                if Logger.backlog is not None:
                    Logger.backlog.append(errMsg)
                print("%s%s%s" % (BRIGHTRED, errMsg, NORMAL), file=sys.stderr)


def GetLogger(domain=None, level=DEBUG, pathName=None, maxSize=0, backupCnt=0, console=False):
    if not domains:
        raise ValueError("Call LogInit first")
    if domain is None:
        domain = "root"
    if domain in domains:
        logger = domains[domain]
        if logger is not None:
            logger.stop()
            logger.join()
        del domains[domain]
    logger = domains[domain] = Logger(domain, level, pathName, maxSize, backupCnt, console)
    return logger


def LogInit(domain=None, level=DEBUG, pathName=None, maxSize=0, backupCnt=0, console=False,
            colors=False, compress=None, useThreads=False, encoding=None):
    if domain is None:
        domain = "root"
    Logger.colors = colors
    Logger.compress = compress
    Logger.useThreads = useThreads
    Logger.encoding = encoding
    domains[domain] = None
    logger = GetLogger(domain, level, pathName, maxSize, backupCnt, console)
    if colors and (NORMAL == ""):
        logger.warning("Module colorama not installed! Colored log not available")
    return logger

