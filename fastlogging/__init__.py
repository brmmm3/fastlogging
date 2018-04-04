# Copyright 2018 Martin Bammer. All Rights Reserved.
# Licensed under MIT license.

"""Implements lightweight and fast logging."""

__all__ = [ 'Logger', 'GetLogger', 'LogInit', 'Shutdown',
            'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG',
            'LOG2SYM', 'LOG2SSYM', 'LVL2COL',
            'OptimizeAst', 'optimize', 'optimize_obj', 'optimize_file', 'write_pyc_file' ]

__author__ = 'Martin Bammer (mrbm74@gmail.com)'
__status__  = "alpha"

import sys

if sys.version_info[0] > 2:
    from fastlogging.fastlogging import ( Logger, GetLogger, LogInit, Shutdown,
                                          CRITICAL, FATAL, ERROR, WARNING, INFO, DEBUG,
                                          LOG2SYM, LOG2SSYM, LVL2COL )
    from fastlogging.optimize import OptimizeAst, optimize, optimize_obj, optimize_file, write_pyc_file
else:
    from fastlogging import ( Logger, GetLogger, LogInit, Shutdown,
                              CRITICAL, FATAL, ERROR, WARNING, INFO, DEBUG,
                              LOG2SYM, LOG2SSYM, LVL2COL )
    from optimize import OptimizeAst, optimize, optimize_obj, optimize_file, write_pyc_file
