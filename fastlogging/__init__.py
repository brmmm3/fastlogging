# The MIT License (MIT)
# 
# Copyright (c) <2024> <Martin Bammer, mrbm74 at gmail dot com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Implements lightweight and fast logging."""

from fastlogging.fastlogging import Colors, domains, Logger, GetLogger, LogInit, Remove, Rotate, Shutdown, \
    CRITICAL, FATAL, ERROR, WARNING, WARN, INFO, DEBUG, NOTSET, EXCEPTION, LOG2SYM, LOG2SSYM, LVL2COL
from fastlogging.optimize import OptimizeAst, Optimize, OptimizeObj, OptimizeFile, WritePycFile


__all__ = ['Colors', 'domains', 'Logger', 'GetLogger', 'LogInit', 'Remove', 'Rotate', 'Shutdown',
           'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET',
           'EXCEPTION', 'LOG2SYM', 'LOG2SSYM', 'LVL2COL',
           'OptimizeAst', 'Optimize', 'OptimizeObj', 'OptimizeFile', 'WritePycFile']

__author__ = 'Martin Bammer (mrbm74@gmail.com)'
__status__ = "beta"

