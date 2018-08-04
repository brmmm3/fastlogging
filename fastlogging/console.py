# -*- coding: utf-8 -*-
# Copyright 2018 Martin Bammer. All Rights Reserved.
# Licensed under MIT license.

"""Console logger."""

import sys
from collections import deque
from threading import Thread, Event

from . import ERROR


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
        queue_popleft = self.queue.popleft
        evtQueue = self.evtQueue
        while True:
            try:
                entry = queue_popleft()
                if entry is None:
                    break
            except:
                evtQueue.wait()
                evtQueue.clear()
                continue
            print(entry[1], file=self.stdOut if entry[0] < ERROR else self.stdErr)
