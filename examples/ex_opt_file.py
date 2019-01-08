
from fastlogging import LogInit, INFO, OptimizeFile


logger = LogInit(console=True)

optBar = OptimizeFile(globals(), "opt_test.py", "logger", remove=INFO)
optBar.bar()
