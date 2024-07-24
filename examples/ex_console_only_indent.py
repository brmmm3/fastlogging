
from fastlogging import LogInit, DEBUG


def A():
    logger.info("A()")


def B():
    logger.info("B()")
    A()


def C():
    logger.info("C()")
    B()


if __name__ == "__main__":
    logger = LogInit("root", DEBUG, console=True, indent=(0, 1, 5), colors=True)
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    A()
    B()
    C()
    logger.fatal("This is a fatal message.")
    logger.shutdown()
