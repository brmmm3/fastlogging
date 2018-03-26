# Copyright 2018 Martin Bammer. All Rights Reserved.
# Licensed under MIT license.

"""Implements lightweight and fast logging."""

__author__ = 'Martin Bammer (mrbm74@gmail.com)'

import os
import sys
import atexit
import time
import traceback
from collections import deque
from threading import Thread, Timer, Event

# Log-Levels
LOG_FATAL = 50
LOG_ERROR = 40
LOG_WARNING = 30
LOG_INFO = 20
LOG_DEBUG = 10

LOG2SYM = { LOG_FATAL : "FATAL  ", LOG_ERROR : "ERROR  ", LOG_WARNING : "WARNING",
            LOG_INFO : "INFO   ", LOG_DEBUG : "DEBUG  " }

LOG2SSYM = { LOG_FATAL : "FAT", LOG_ERROR : "ERR", LOG_WARNING : "WRN",
             LOG_INFO : "INF", LOG_DEBUG : "DBG" }

try:
    from colorama import Fore, Style

    NORMAL = Style.RESET_ALL
    BRIGHT = Style.BRIGHT
    WHITE = Fore.WHITE
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    GREEN = Fore.GREEN
    BRIGHTRED = BRIGHT + RED
    BRIGHTYELLOW = BRIGHT + YELLOW
    BRIGHTGREEN = BRIGHT + GREEN

    LVL2COL = { LOG_FATAL : BRIGHTRED, LOG_ERROR : RED, LOG_WARNING : BRIGHTYELLOW,
                LOG_INFO: BRIGHTGREEN, LOG_DEBUG: WHITE }
except ImportError:
    NORMAL = ""
    BRIGHTRED = ""

    LVL2COL = { LOG_FATAL : "", LOG_ERROR : "", LOG_WARNING : "", LOG_INFO: "",  LOG_DEBUG: "" }

WR_DIRECT = 0
WR_THREAD = 1


def shutdown(now = False):
    for logger in Logger.domains.values():
        logger.shutdown(now)


atexit.register(shutdown)


class LastMessage:
    key = None
    cnt = 1
    entry = None


class Logger(object):
    domains = {}
    backlog = deque(maxlen = 1000)
    dateFmt = "%y.%m.%d %H:%M:%S"
    cbMessageKey = None
    cbFormatter = None
    cbWriter = None
    colors = False
    compress = None     # ( CompressorInstance, CompressedFileExtension )
    write = WR_DIRECT
    encoding = None

    def __init__(self, domain, level, pathName, maxSize, backupCnt, console):
        if (maxSize < 0) or (backupCnt < 0) or ((maxSize > 0) and (backupCnt == 0)):
            raise ValueError("Invalid maxSize or backupCnt")
        self.__domain = domain
        self.__level = level
        self.queue = deque()
        self.evtQueue = Event()
        self.evtRotate = Event()
        self._lastMsg = LastMessage()
        self.pathName = pathName
        self.F = None
        self.buf = []
        self.size = 0
        self.pos = 0
        self.maxSize = maxSize
        self.backupCnt = backupCnt
        self.__console = console
        self.__thrTimer = None
        self.__thrLogger = None
        self.__stopped = False
        if pathName is None:
            pass
        elif os.path.isdir(os.path.dirname(pathName)):
            for logger in Logger.domains.values():
                if pathName == logger.pathName:
                    self.queue = logger.queue
                    self.evtQueue = logger.evtQueue
                    self.evtRotate = logger.evtRotate
                    self.maxSize = logger.maxSize
                    self.backupCnt = logger.backupCnt
                    break
            else:
                self.F = open(pathName, "a", encoding = Logger.encoding)
                self.pos = self.F.tell()
                if Logger.write == WR_THREAD:
                    self.__thrLogger = Thread(target = self.__logThread, daemon = True, name = "LogThread")
                    self.__thrLogger.start()
        else:
            raise ValueError("Invalid path %s" % pathName)

    @property
    def stopped(self):
        return self.__stopped

    @property
    def domain(self):
        return self.__domain

    @property
    def level(self):
        return self.__level

    def setLevel(self, level):
        self.__level = level

    @staticmethod
    def setBacklog(size):
        Logger.backlog = deque(Logger.backlog, maxlen = size)

    @staticmethod
    def setMessageKey(cbMessageKey):
        Logger.cbMessageKey = cbMessageKey

    @staticmethod
    def setFormatter(cbFormatter):
        Logger.cbFormatter = cbFormatter

    @staticmethod
    def setWriter(cbWriter):
        Logger.cbWriter = cbWriter

    def __log(self, level, msg, args, kwargs):
        if self.stopped:
            raise RuntimeError("Logger already stopped")
        try:
            if args:
                msg = msg % args
        except:
            print("fastlogging.__log: Exception:", ( msg, args ), file = sys.stderr)
            traceback.print_exc()
            traceback.print_stack()
            return
        if Logger.write == WR_DIRECT:
            self.__logEntry(( time.time(), self.__domain, level, msg, kwargs ))
        else:
            self.queue.append((time.time(), self.__domain, level, msg, kwargs))
            self.evtQueue.set()

    def debug(self, msg, *args, **kwargs):
        if self.__level <= LOG_DEBUG:
            self.__log(LOG_DEBUG, msg, args, kwargs)

    def info(self, msg, *args, **kwargs):
        if self.__level <= LOG_INFO:
            self.__log(LOG_INFO, msg, args, kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.__level <= LOG_WARNING:
            self.__log(LOG_WARNING, msg, args, kwargs)

    def error(self, msg, *args, **kwargs):
        if self.__level <= LOG_ERROR:
            self.__log(LOG_ERROR, msg, args, kwargs)

    def fatal(self, msg, *args, **kwargs):
        if self.__level <= LOG_FATAL:
            self.__log(LOG_FATAL, msg, args, kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.__level <= LOG_FATAL:
            self.__log(LOG_FATAL, msg, args, kwargs)

    def exception(self, msg, *args, **kwargs):
        kwargs["exc_info"] = traceback.format_exc()
        self.__log(LOG_FATAL, msg, args, kwargs)

    @staticmethod
    def getBacklog(size = 0):
        if size < 0:
            raise ValueError("Invalid size")
        if size == 0:
            return Logger.backlog
        return list(Logger.backlog)[-size:]

    def stop(self, now = False):
        if not self.__thrTimer is None:
            self.__thrTimer.cancel()
            self.__thrTimer.join()
            self.__thrTimer = None
            self.__logMessage(self._lastMsg.key, self._lastMsg.entry, self._lastMsg.cnt)
        if now:
            self.queue.clear()
        self.queue.append(None)
        self.evtQueue.set()
        self.__stopped = True

    def join(self):
        if not self.__thrLogger is None:
            self.__thrLogger.join()
            self.__thrLogger = None
        del Logger.domains[self.__domain]

    def shutdown(self, now = False):
        self.stop(now)
        self.join()

    def rotate(self, logger = None):
        if logger is None:
            loggers = Logger.domains.values()
        else:
            loggers = [ logger ]
        signaled = set()
        for logger in loggers:
            if logger.evtRotate in signaled:
                continue
            signaled.add(logger)
            if Logger.write == WR_DIRECT:
                self.__rotate(logger)
            else:
                logger.evtRotate.set()
                logger.evtQueue.set()

    def __rotate(self, logger = None):
        self.__writePending(logger)
        logger.F.flush()
        logger.F.close()
        logger.pos = 0
        path_join = os.path.join
        pathName = logger.pathName
        dirName, logFileName = os.path.split(pathName)
        zExt = "" if Logger.compress is None else Logger.compress[1]
        fileNames = { fileName for fileName in os.listdir(dirName) if fileName.startswith(logFileName) }
        for cnt in range(self.backupCnt, 1, -1):
            srcFileName = "%s.%d%s" % (logFileName, cnt - 1, zExt)
            if srcFileName not in fileNames:
                continue
            os.replace(path_join(dirName, srcFileName), path_join(dirName, "%s.%d%s" % (logFileName, cnt, zExt)))
        dstFileName = "%s.1%s" % (logFileName, zExt)
        if Logger.compress is None:
            os.replace(pathName, path_join(dirName, dstFileName))
        else:
            with open(path_join(dirName, dstFileName), "wb") as Z:
                Z.write(Logger.compress[0].compress(open(pathName, "rb").read()))
            os.remove(pathName)
        logger.F = open(pathName, "a", encoding = Logger.encoding)

    @staticmethod
    def __writePending(logger):
        if logger.buf:
            if Logger.cbWriter is None:
                data = "".join(logger.buf)
                logger.F.write(data)
                logger.buf = []
                logger.size = 0
            else:
                Logger.cbWriter(logger)

    def __logWriteRotate(self, logger, message):
        logger.buf.append(message + "\n")
        size = len(message) + 1
        logger.size += size
        if logger.maxSize == 0:
            if (logger.size >= 65536) or (Logger.write == WR_DIRECT):
                self.__writePending(logger)
            return
        logger.pos += size
        if logger.pos < logger.maxSize:
            if Logger.write == WR_DIRECT:
                self.__writePending(logger)
            return
        self.__rotate(logger)

    def __logMessage(self, key, entry, cnt = 0):
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
            if not self.F is None:
                self.__logWriteRotate(self, message)
                console = self.__console
        except:
            traceback.print_exc()
            console = True
        if console or kwargs.get("console", False):
            F = sys.stdout if level < LOG_ERROR else sys.stderr
            if Logger.colors:
                if "color" in kwargs:
                    color = kwargs["color"]
                else:
                    color = LVL2COL.get(level, LOG_FATAL)
                print("%s%s%s" % (color, message, NORMAL), file = F)
            else:
                print(message, file = F)

    def __logEntry(self, entry):
        msg = entry[3]  # logTime, domain, level, msg, kwargs
        if Logger.cbMessageKey is None:
            key = msg
        else:
            key = Logger.cbMessageKey(self, entry)
        if (key == self._lastMsg.key) and (self._lastMsg.cnt < 1000):
            self._lastMsg.cnt += 1
            self._lastMsg.entry = entry
            if self.__thrTimer is None:
                self.__thrTimer = Timer(30.0, self.__logMessage, key, entry)
                self.__thrTimer.start()
        elif self.__thrTimer is None:
            self.__logMessage(key, entry)
        else:
            self.__thrTimer.cancel()
            self.__thrTimer.join()
            self.__thrTimer = None
            self.__logMessage(key, self._lastMsg.entry, self._lastMsg.cnt)
            self.__logMessage(key, entry)

    def __logThread(self):
        while True:
            try:
                entry = self.queue.popleft()
                if entry is None:
                    if not self.F is None:
                        if self.buf:
                            self.__writePending(self)
                        self.F.flush()
                        self.F.close()
                        self.F = None
                    break
            except:
                if not self.F is None and self.buf:
                    self.__writePending(self)
                self.evtQueue.wait()
                self.evtQueue.clear()
                if self.evtRotate.is_set():
                    self.evtRotate.clear()
                    self.__rotate(self)
                continue
            try:
                self.__logEntry(entry)
            except:
                errMsg = traceback.format_exc()
                Logger.backlog.append(errMsg)
                print("%s%s%s" % (BRIGHTRED, errMsg, NORMAL), file = sys.stderr)


def GetLogger(domain, level, pathName = None, maxSize = 0, backupCnt = 0, console = False):
    if not Logger.domains:
        raise ValueError("Call LogInit first")
    if domain is None:
        domain = "root"
    if domain in Logger.domains:
        logger = Logger.domains[domain]
        if not logger is None:
            logger.stop()
            logger.join()
        del Logger.domains[domain]
    logger = Logger.domains[domain] = Logger(domain, level, pathName, maxSize, backupCnt, console)
    return logger


def LogInit(domain, level, pathName = None, maxSize = 0, backupCnt = 0, console = False,
            colors = False, compress = None, write = WR_DIRECT, encoding = None):
    Logger.colors = colors
    Logger.compress = compress
    Logger.write = write
    Logger.encoding = encoding
    Logger.domains[domain] = None
    logger = GetLogger(domain, level, pathName, maxSize, backupCnt, console)
    if colors and (NORMAL == ""):
        logger.warning("Module colorama not installed! Colored log not available")
    return logger

