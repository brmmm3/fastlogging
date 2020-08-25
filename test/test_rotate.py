
import os

from fastlogging import LogInit


def RemoveLogs():
    for i in range(10):
        fileName = "test_rotate.log"
        if i > 0:
            fileName += f".{i}"
        if os.path.exists(fileName):
            os.remove(fileName)


def test_rotate():
    RemoveLogs()
    logger = LogInit(pathName="test_rotate.log", console=False, maxSize=81920, backupCnt=10)
    for i in range(2000):
        logger.error("printing line: %d", i)
    logger.stop()
    assert os.path.exists("test_rotate.log")
    assert os.path.getsize("test_rotate.log") == 24948
    assert os.path.exists("test_rotate.log.1")
    assert os.path.getsize("test_rotate.log.1") == 81942
    RemoveLogs()
