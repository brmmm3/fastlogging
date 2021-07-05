import time
from fastlogging import LogInit

start = time.time()
logger = LogInit(pathName="/tmp/example1.log", console=True, maxSize=819200, backupCnt=10)

for i in range(1000):
    logger.error("printing line: %s", i)

end = time.time()
print(end - start)
