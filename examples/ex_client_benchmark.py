
import time

from fastlogging import LogInit, DEBUG


if __name__ == "__main__":
    addr = "127.0.0.1"
    port = 12345
    logger = LogInit(level=DEBUG, console=False, colors=True, connect=(addr, port))
    t1 = time.time()
    for i in range(333333):
        s = str(i)
        logger.debug(s + "This is a debug message.")
        logger.info(s + "This is an info message.")
        logger.warning(s + "This is a warning message.")
    dt = time.time() - t1
    print(f"dt={dt} {999999 / dt:.2f} messages/s  after logging 999999 messages.")
    logger.flush()
    dt = time.time() - t1
    print(f"dt={dt} {999999 / dt:.2f} messages/s  after flush.")
    logger.shutdown()
    dt = time.time() - t1
    print(f"dt={dt} {999999 / dt:.2f} messages/s  after shutdown.")
