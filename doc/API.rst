API
===

Log levels
----------

::

 EXCEPTION Log exception messages. In addition to the message text the exception info
           (output of traceback.format_exc) is logged.
 FATAL     Log fatal/critical messages. Default color is bright red.
 CRITICAL  Same as FATAL.
 ERROR     Log also error messages. Default color is red.
 WARNING   Log also warning messages. Default color is bright yellow.
 INFO      Log also info messages. Default color is bright green.
 DEBUG     Log also debug messages. Default color is white.
 NOTSET    All messages are logged.

Mappings
--------

::

 LOG2SYM      A dictionary which maps the integer severity value to a string.
 LOG2SSYM     A dictionary which maps the integer severity value to a short string.
 LVL2COL      A dictionary which maps the integer severity to a color.

Global fastlogging members
--------------------------

::

 domains                A dictionary holding all Logger instances for the configured domains.
 Colors                 A class which contains the color codes (if colorama is installed).
 Shutdown               Global shutdown method. Will be called when Python exits.
 Rotate                 Perform a log rotate for all log files.
 Logger                 The logger class.
 Remove                 Remove a log domain.
 GetLogger              Create a new log domain.
 LogInit                Create initial log domain. Has to be called first!

class Logger
------------

Logging class object. It contains the following static member variables::

 domains                A dictionary holding all Logger instances for the configured domains.
 backlog                The last 1000 log messages (and module internal exceptions), (default None).
 dateFmt                The date and time format for the log messages.
 cbMessageKey           Custom log message key calculation callback function to identify same successive messages.
                        Default is None which means to use the default algorithm.
                        The function signature of the function needs to be cbMessageKey(self, entry) where
                        ::self :: is the Logger class instance and
 cbFormatter            Custom log messages formatter callback function.
                        Set (if a callable is supplied) or clear (if None is supplied) the function for formatting the message.
 cbWriter               Custom log messages writer callback function.
                        Set (if a callable is supplied) or clear (if None is supplied) the function to call after writing
                        log messages to the log file.
 colors                 Enable/Disable colored logging to console (default False).
 compress = None        A tuple with compressor instance and file extension (dfeault None).
 useThreads             Write log messages in main thread (False) or in background thread (True).
 encoding               Encoding to use for log files.
 sameMsgTimeout         Timeout for same log messages in a row (default 30.0 seconds).
 sameMsgCountMax        Maximum counter value for same log messages in a row (default 1000).
 thrConsoleLogger       Console logger thread instance.
 console                Default value for logging to console (set in LogInit).
 indent                 Log message indent settings. Tuple with (offset, inc, max) (default None).
 consoleLock            An optional lock for console logging, if log messages come from different threads (default None).

``stopNetwork()``
^^^^^^^^^^^^^^^^^

Stop network support.

``setLevel(level)``
^^^^^^^^^^^^^^^^^^^

Set logging level.

``setConsole(console)``
^^^^^^^^^^^^^^^^^^^^^^^

Enable/disable logging to console.

``setBacklog(size)``
^^^^^^^^^^^^^^^^^^^^

If size > 0 then enable log message history and set buffer size.
If size = 0 then disable log message history.

``logEntry(self, log_time, domain, level, msg, kwargs)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Force logging a custom message.

::

 log_time  Custom log message time (float value). By default fastlogging uses the time.time() function when
           logging a message. But if the message comes from a source with a changing delay, e.g. from another
           computer, then it makes sense to use the time value provided by the source.
 domain    Log domain.
 level     Log level.
 msg       Message text.
 kwargs    Dictionary with extra keyword arguments for controlling the output, like exc_info, console, color.

``log(self, level, msg, *args, **kwargs)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Force logging a custom message.

::

 level     Log level.
 msg       Message format string.
 args      Tuple with arguments for the format string.
 kwargs    Dictionary with extra keyword arguments for controlling the output, like exc_info, console, color.

``debug(self, msg, *args, **kwargs)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Log debug message.

``info(self, msg, *args, **kwargs)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Log info message.

``warning(self, msg, *args, **kwargs)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Log warning message.

``error(self, msg, *args, **kwargs)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Log error message.

``fatal(self, msg, *args, **kwargs)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Log fatal/critical message.

``exception(self, msg, *args, **kwargs)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Log an error message including the current exception (output of traceback.format_exc).

``stop(now=False)``
^^^^^^^^^^^^^^^^^^^

Stop the logger thread.

::

 now    If True all pending log message are dropped. If False all pending message will be logged.

``join()``
^^^^^^^^^^

Wait for the logger thread to finish.

``shutdown(now=False)``
^^^^^^^^^^^^^^^^^^^^^^^

This method first calls stop then join. for parameter **now** see method **stop()**.

``flush()``
^^^^^^^^^^^

Write all pending messages to disk and send all pending messages to log server.

``rotate(bWait=False)``
^^^^^^^^^^^^^^^^^^^^^^^

Rotate the log file for this Logger instance.

::

 bWait   Wait until rotating is done. This is only needed if background threads for logging are used.

LogInit(domain=None, level=NOTSET, pathName=None, maxSize=0, backupCnt=0, console=False, colors=False, compress=None, useThreads=False, encoding=None, backlog=0, indent=None, server=None, connect=None, consoleLock=None)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

LogInit has to be called first to get the initial logger instance. Global default settings will be set.

::

 domain         Log domain. (default is root, if not provided).
 level          Log level (default NOTSET).
 pathName       Log file name (defaule None). If None no log file is created.
 maxSize        Maximum log file size. If >0 then log file rotating is activated (default 0).
 backupCnt      Size of log files history (default 0). This value is only considered when maxSize>0.
 console        Log to console (default False). This also sets the default value for GetLogger calls.
 colors         Enable/disable colored logging.
 compress       Tuple with compressor instance and extension for compressed log files (default None).
                If provided the backup log files will be compressed when rotating is done.
 useThreads     If True log messages are written in a background thread. Otherwise in the main thread.
 encoding       Encoding to use for log files.
 backlog        Queue with a copy of latest log messages, if configured.
 indent         Tuple with indent settings (offset, increment, max level), default is None.
                Indent log messages depending on the call stack depth, if configured.
 server         Tuple to create server socket for receiving log messages from other computers (default None).
                The tuple must contain at least 2 parameters address and port. All other parameters are optional and must be provided
                in the order shown below. If not provided the parameters have the default values as shown below.
                server = (address, port, maxMsgSize=4096, cbAccept=None, cbAuth=None, cbDecode=None)
                maxMsgSize  Size of receive buffer.
                cbAccept    Optional accept callback function. Function signature must be cbAccept(client, address).
                            client    Client socket.
                            address   Client address.
                cbAuth      Optional authentication function. Function signature must be cbAuth(self, client, address, message).
                            self      LoggingServer instance.
                            client    Client socket.
                            address   Client address.
                            message   Message for authentication.
                cbDecode    Optional message decoding/decryption function. Function signature must be cbDecode(prefix, message).
                            prefix    Name (or IP address if name could not be retrieved) of client computer.
                            message   Message which needs to be decoded/decrypted.
 connect        Tuple to connect to logging server for sending log messages to another computer (default None).
                The tuple must contain at least 2 parameters address and port. All other parameters are optional and must be provided
                in the order shown below. If not provided the parameters have the default values as shown below.
                connect = (address, port, clientName=None, maxMsgSize=4096, cbConnect=None, cbEncode=None)
                clientName  Name to send after successfully connecting to, and successfull authentication on, log server.
                maxMsgSize  Size of receive buffer.
                cbConnect   Optional authentication function. Function signature must be cbConnect(socket).
                            socket    Connection socket.
                cbEncode    Optional message encoding/encryption function. Function signature must be cbEncode(message).
                            message   Message to encode/encrypt.
 consoleLock    An optional lock for console output (default None). If several threads write log messages to the console at the same
                time the ensures that only 1 can write at the same time to avoid garbage on the console.

GetLogger(domain=None, level=NOTSET, pathName=None, maxSize=0, backupCnt=0, console=None, indent=True, server=None, connect=None)
---------------------------------------------------------------------------------------------------------------------------------

Create a new logger domain.

::

 domain         Log domain. (default is root, if not provided).
 level          Log level (default NOTSET).
 pathName       Log file name (defaule None).
 maxSize        Maximum log file size. If >0 then log file rotating is activated (default 0).
 backupCnt      Size of log files history (default 0). This value is only considered when maxSize>0.
 console        Log to console (default None). If value is None then the value provided in LogInit will be used.
 indent         Tuple with indent settings (offset, increment, max level), default is None.
                Indent log messages depending on the call stack depth, if configured.
 server         Tuple to create server socket for receiving log messages from other computers (default None).
                The tuple must contain at least 2 parameters address and port. All other parameters are optional and must be provided
                in the order shown below. If not provided the parameters have the default values as shown below.
                server = (address, port, maxMsgSize=4096, cbAccept=None, cbAuth=None, cbDecode=None)
                maxMsgSize  Size of receive buffer.
                cbAccept    Optional accept callback function. Function signature must be cbAccept(client, address).
                            client    Client socket.
                            address   Client address.
                cbAuth      Optional authentication function. Function signature must be cbAuth(self, client, address, message).
                            self      LoggingServer instance.
                            client    Client socket.
                            address   Client address.
                            message   Message for authentication.
                cbDecode    Optional message decoding/decryption function. Function signature must be cbDecode(prefix, message).
                            prefix    Name (or IP address if name could not be retrieved) of client computer.
                            message   Message which needs to be decoded/decrypted.
 connect        Tuple to connect to logging server for sending log messages to another computer (default None).
                The tuple must contain at least 2 parameters address and port. All other parameters are optional and must be provided
                in the order shown below. If not provided the parameters have the default values as shown below.
                connect = (address, port, clientName=None, maxMsgSize=4096, cbConnect=None, cbEncode=None)
                clientName  Name to send after successfully connecting to, and successfull authentication on, log server.
                maxMsgSize  Size of receive buffer.
                cbConnect   Optional authentication function. Function signature must be cbConnect(socket).
                            socket    Connection socket.
                cbEncode    Optional message encoding/encryption function. Function signature must be cbEncode(message).
                            message   Message to encode/encrypt.
