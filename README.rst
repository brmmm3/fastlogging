An efficient and lightweight logging module
===========================================

A faster a more lightweight version of the standard logging module in Python.
The standard version comes with a full load of features which are not always required.
The high complexity makes the logging module slow. The fastlogging module is much smaller
and has less features with the benefit of a more than 5 times faster logging.
It comes with the following features:

 - (colored) logging to console
 - logging to file (maximum file size with rotating/history feature can be configured)
 - old log files can be compressed (the compression algorithm can be configured)
 - count same successive messages within a 30s time frame and log only once the message with the counted value.
 - log domains
 - log to different files
 - writing to log files is done in background thread
 - configure custom detection of same successive message
 - configure custom message formatter
 - configure additional custom log writer

**API**
=======


``Log levels``
""""""""""""""

 ``LOG_FATAL    Log a fatal/critical message. Default color is bright red.``

 ``LOG_ERROR    Log an error message. Default color is red.``

 ``LOG_WARNING  Log a warning message. Default color is bright yellow.``

 ``LOG_INFO     Log an info message. Default color is bright green.``

 ``LOG_DEBUG    Log a debug message. Default color is white.``

 ``LOG2SYM      A dictionary which maps the integer severity value to a string.``

 ``LVL2COL      A dictionary which maps the integer severity to a color.``

``class Logger``
""""""""""""""""

Logging class object.

``setLevel(level)``
"""""""""""""""""""

Set logging. level.

``setMessageKey(cbMessageKey)``
"""""""""""""""""""""""""""""""

Set (if a callable is supplied) or clear (if None is supplied) the function for calculating
a message key. The key is used to identify same messages. If this function is not set a default
algorithm is used.

 The function signatur of **cbMessageKey** needs to be **cbMessageKey(self, entry)** where 

``setFormatter(cbFormatter)``
"""""""""""""""""""""""""""""

Set (if a callable is supplied) or clear (if None is supplied) the function for formatting the message.

``setWriter(cbWriter)``
"""""""""""""""""""""""

Set (if a callable is supplied) or clear (if None is supplied) the function to call after writing
log messages to the log file.

``debug(self, msg, *args, **kwargs)``
"""""""""""""""""""""""""""""""""""""

Log debug message.

``info(self, msg, *args, **kwargs)``
""""""""""""""""""""""""""""""""""""

Log info message.

``warning(self, msg, *args, **kwargs)``
"""""""""""""""""""""""""""""""""""""""

Log warning message.

``error(self, msg, *args, **kwargs)``
"""""""""""""""""""""""""""""""""""""

Log error message.

``fatal(self, msg, *args, **kwargs)``
"""""""""""""""""""""""""""""""""""""

Log fata/critical message.

``exception(self, msg, *args, **kwargs)``
"""""""""""""""""""""""""""""""""""""""""

Log an error message including the current exception.

``getBacklog()``
""""""""""""""""

Get the backlog, the last 10000 messages as a deque object.

``stop(now = False)``
"""""""""""""""""""""

Stop the logger thread.

 **now** if **True** all pending log message are dropped. If **False** all pending message will be logged.

``join()``
""""""""""

Wait for the logger thread to finish.

``close(now = False)``
""""""""""""""""""""""

This method first calls stop then join.

 **now** if **True** all pending log message are dropped. If **False** all pending message will be logged.

``LogInit(domain, level, pathName = None, maxSize = 0, backupCnt = 0, console = False, colors = False)``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
LogInit has to be called first to get the initial logger instance. Global default settings will be set.

 **domain** is the logging domain. 

 **level**

 **pathName**

 **maxSize**

 **backupCnt**

 **console**

 **colors**

``GetLogger(domain, level, pathName = None, maxSize = 0, backupCnt = 0, console = False)``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
