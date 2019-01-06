An efficient and lightweight logging module
===========================================

The ``fastlogging`` module is a faster and more lightweight version of the standard logging module.
The default logging module comes with a full load of features which are not always required.
The high complexity makes the logging module slow. The ``fastlogging`` module is much smaller and has less features with the benefit of a more than **5 times faster** logging.
It comes with the following features:

 - (colored, if colorama is installed) logging to console
 - logging to file (maximum file size with rotating/history feature can be configured)
 - old log files can be compressed (the compression algorithm can be configured)
 - count same successive messages within a 30s time frame and log only once the message with the counted value.
 - log domains
 - log to different files
 - writing to log files is done in (per file) background threads, if configured
 - configure callback function for custom detection of same successive log messages
 - configure callback function for custom message formatter
 - configure callback function for custom log writer

**API**
=======

``Log levels``
""""""""""""""

::

 EXCEPTION Log exception messages. In addition to the message text the exception info
           (output of traceback.format_exc) is logged.
 CRITICAL  Same as FATAL.
 FATAL     Log also fatal/critical messages. Default color is bright red.
 ERROR     Log also error messages. Default color is red.
 WARNING   Log also warning messages. Default color is bright yellow.
 INFO      Log also info messages. Default color is bright green.
 DEBUG     Log also debug messages. Default color is white.
 NOTSET    All messages are logged.

``Mappings``
************

::

 LOG2SYM      A dictionary which maps the integer severity value to a string.
 LOG2SSYM     A dictionary which maps the integer severity value to a short string.
 LVL2COL      A dictionary which maps the integer severity to a color.

``class Logger``
""""""""""""""""

Logging class object. It contains the following static member variables::

 domains                A dictionary holding all Logger instances for the configured domains.
 backlog                The last 1000 log messages (and internal exceptions).
 dateFmt                The date and time format for the log messages.
 cbMessageKey           Custom log message key calculation callback function to identify same successive messages.
 cbFormatter            Custom log messages formatter callback function.
 cbWriter               Custom log messages writer callback function
 stdOut                 Destination file descriptor sys.stdout
 stdErr = sys.stderr
 colors = False          # Enable/Disable colored logging to console
 compress = None         # ( CompressorInstance, CompressedFileExtension )
 write = WR_DIRECT       # Write log messages in main thread or in background thread
 encoding = None
 sameMsgTimeout = 30.0   # Timeout for same log messages in a row
 sameMsgCountMax = 1000  # Maximum counter value for same log messages in a row

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

``setSameMessageLimits(timeout, countMax)``
"""""""""""""""""""""""""""""""""""""""""""

Set limits for same successive log messages.

**timeout** is the time frame 

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

Log fatal/critical message.

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
