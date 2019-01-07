An efficient and feature-rich logging module
============================================

The ``fastlogging`` module is a faster replacement of the standard logging module.

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

The API is described `here <doc/API.rst>`_.
