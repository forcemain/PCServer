#! -*- coding: utf-8 -*-


from server.common.shortcut import uuid4


class Task(object):
    def __init__(self, target):
        self.tid = uuid4()
        self.target = target
        self.send_value = None

    def next(self):
        return self.target.send(self.send_value)
