# Copyright 2018 Martin Bammer. All Rights Reserved.
# Licensed under MIT license.

"""Implements lightweight and fast logging."""

from __future__ import absolute_import

import sys


__all__ = [ 'Logger', 'GetLogger', 'LogInit', 'Shutdown', 'domains',
            'NOLOG', 'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG',
            'EXCEPTION', 'LOG2SYM', 'LOG2SSYM', 'LVL2COL', 'NORMAL',
            'OptimizeAst', 'Optimize', 'OptimizeObj', 'OptimizeFile', 'WritePycFile' ]

__author__ = 'Martin Bammer (mrbm74@gmail.com)'
__status__  = "beta"

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

LOG2SYM = {FATAL : "FATAL  ", ERROR : "ERROR  ", WARNING : "WARNING",
           INFO : "INFO   ", DEBUG : "DEBUG  "}

from fastlogging.fastlogging import NORMAL, LVL2COL, domains, Logger, GetLogger, LogInit, Shutdown
from fastlogging.optimize import OptimizeAst, Optimize, OptimizeObj, OptimizeFile, WritePycFile
