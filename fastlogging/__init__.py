
import sys

if sys.version_info[0] > 2:
    from fastlogging.fastlogging import ( Logger, GetLogger, LogInit, WR_DIRECT, WR_THREAD,
                                          LOG_FATAL, LOG_ERROR, LOG_WARNING, LOG_INFO, LOG_DEBUG,
                                          LOG2SYM, LOG2SSYM, LVL2COL )
else:
    from fastlogging import ( Logger, GetLogger, LogInit, WR_DIRECT, WR_THREAD,
                              LOG_FATAL, LOG_ERROR, LOG_WARNING, LOG_INFO, LOG_DEBUG,
                              LOG2SYM, LOG2SSYM, LVL2COL )

