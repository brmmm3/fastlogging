
import sys
import fastlogging

logger = fastlogging.LogInit(console=True, stderr=sys.stdout)


def multilevel_logging():
    logger.debug("Debug Level 1")
    logger.info("Info Level 1")
    logger.warning("Warning Level 1")
    logger.error("Error Level 1")
    branch1 = True
    if branch1:
        logger.debug("Debug Level 2")
        logger.info("Info Level 2")
        logger.warning("Warning Level 2")
        logger.error("Error Level 2")


if __name__ == "__main__":
    print("Raw multilevel_logging:")
    multilevel_logging()

    print("Optimized multilevel_logging:")
    opt_multilevel_logging = fastlogging.OptimizeObj(globals(), multilevel_logging, "logger", remove=fastlogging.INFO)
    opt_multilevel_logging()
