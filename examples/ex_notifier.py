
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
    hdlr.setLevel(logging.INFO)

    log.addHandler(hdlr)
    log.info('And just like that, you get notified about all your errors!')
