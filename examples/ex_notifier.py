
import fastlogging as logging
from notifiers import get_notifier
from notifiers.logging import NotificationHandler


if __name__ == "__main__":
    log = logging.LogInit(console=True, colors=True)
    defaults = get_notifier("gmail").defaults
    defaults["to"] = input("ToMail:")
    defaults["username"] = input("User:")
    defaults["password"] = input("PW:")
    hdlr = NotificationHandler('gmail', defaults=defaults)
    log.addHandler(hdlr)
    # Set log handler specific log level
    hdlr.setLevel(logging.WARN)
    # Set console specific log level (optional). If not set, the global log level will do the filtering.
    log.setConsoleLevel(logging.WARN)
    # Set global log level.
    # Note: If global log level is higher than the log level of a log handler or the console then messages
    # will be filtered nevertheless
    log.setLevel(logging.INFO)
    log.info('And just like that, you get notified about all your infos!')
    log.warning('And just like that, you get notified about all your warnings!')
