# Copyright 2018 Martin Bammer. All Rights Reserved.
# Licensed under MIT license.

"""Implements lightweight and fast logging."""

import sys


__all__ = [ 'Logger', 'GetLogger', 'LogInit', 'Shutdown',
            'NOLOG', 'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG',
            'EXCEPTION', 'LOG2SYM', 'LOG2SSYM', 'LVL2COL',
            'OptimizeAst', 'Optimize', 'OptimizeObj', 'OptimizeFile', 'WritePycFile' ]

__author__ = 'Martin Bammer (mrbm74@gmail.com)'
__status__  = "alpha"

# Log-Levels
NOLOG = 100
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
EXCEPTION = ERROR

LOG2SSYM = {FATAL : "FAT", ERROR : "ERR", WARNING : "WRN",
            INFO : "INF", DEBUG : "DBG"}

LOG2SYM = {FATAL : "FATAL", ERROR : "ERROR", WARNING : "WARNING",
           INFO : "INFO", DEBUG : "DEBUG"}

LOG2SYM = {FATAL : "FATAL  ", ERROR : "ERROR  ", WARNING : "WARNING",
           INFO : "INFO   ", DEBUG : "DEBUG  "}


if sys.version_info[0] > 2:
    from fastlogging.fastlogging import LVL2COL, Logger, GetLogger, LogInit, Shutdown
    from fastlogging.optimize import OptimizeAst, Optimize, OptimizeObj, OptimizeFile, WritePycFile
else:
    from fastlogging import LVL2COL, Logger, GetLogger, LogInit, Shutdown
    from optimize import OptimizeAst, Optimize, OptimizeObj, OptimizeFile, WritePycFile
