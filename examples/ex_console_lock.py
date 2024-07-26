from threading import Lock

from fastlogging import LogInit

logger1 = LogInit(console=True, colors=True, consoleLock=None) # This is fine

logger1.debug("Hello")
logger1.info("Hello")
logger1.warning("Hello")
logger1.error("Hello")
logger1.fatal("Hello")
logger1.exception("Hello")

lock = Lock()

logger2 = LogInit(console=True, colors=True, consoleLock=lock) # This is nolonger fine
#logger2 = LogInit(console=True, colors=True, consoleLock=False) # Same result as the line from above

logger2.debug("Hello") # Exception __exit__
logger2.info("Hello")
logger2.warning("Hello")
logger2.error("Hello")
logger2.fatal("Hello")
logger2.exception("Hello")
