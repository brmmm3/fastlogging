# -*- coding: utf-8 -*-
# Copyright 2018 Martin Bammer. All Rights Reserved.
# Licensed under MIT license.

"""Console logger."""

import sys
from collections import deque
from threading import Thread, Event

from fastlogging import ERROR


class ConsoleLogger(Thread):

    def __init__(self):
        super(ConsoleLogger, self).__init__()
        self.name = "LogConsoleThread"
        self.daemon = True
        self.queue = deque()
        self.evtQueue = Event()
        self.stdOut = sys.stdout
        self.stdErr = sys.stderr

    def append(self, message):
        self.queue.append(message)
        self.evtQueue.set()

    def run(self):
        while True:
            try:
                entry = self.queue.popleft()
                if entry is None:
                    break
            except:
                self.evtQueue.wait()
                self.evtQueue.clear()
                continue
            print(entry[1], file=self.stdOut if entry[0] < ERROR else self.stdErr)
