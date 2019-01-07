
import os
import time

from fastlogging import LogInit

addr = "127.0.0.1"
port = 12345
pathName = "C:/temp/server.log" if os.name == 'nt' else "/tmp/server.log"
logger = LogInit(pathName=pathName, server=(addr, port))
logger.info("Logging started.")
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
time.sleep(15)
logger.info("Shutdown logging.")
logger.shutdown()
