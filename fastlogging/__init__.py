
import sys

if sys.version_info[0] > 2:
    from fastlogging.fastlogging import ( Logger, GetLogger, LogInit, Shutdown,
                                          LOG_FATAL, LOG_ERROR, LOG_WARNING, LOG_INFO, LOG_DEBUG,
                                          LOG2SYM, LOG2SSYM, LVL2COL, WR_DIRECT, WR_THREAD )
    from fastlogging.optimize import OptimizeAst, optimize, optimize_obj, optimize_file, write_pyc_file
else:
    from fastlogging import ( Logger, GetLogger, LogInit, Shutdown,
                              LOG_FATAL, LOG_ERROR, LOG_WARNING, LOG_INFO, LOG_DEBUG,
                              LOG2SYM, LOG2SSYM, LVL2COL, WR_DIRECT, WR_THREAD )
    from optimize import OptimizeAst, optimize, optimize_obj, optimize_file, write_pyc_file
