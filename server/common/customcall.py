#! -*- coding: utf-8 -*-


class BaseCall(object):
    def __init__(self):
        self.task = None
        self.scheduler = None

    def handle(self):
        pass


class ForkTaskCall(BaseCall):
    def __init__(self, target):
        self.target = target
        super(ForkTaskCall, self).__init__()

    def handle(self):
        task = self.scheduler.spawn_one(self.target)
        self.scheduler.put_to_queue(task)


class CanReadCall(BaseCall):
    def __init__(self, socket):
        self.socket = socket
        super(CanReadCall, self).__init__()

    def handle(self):
        self.scheduler.wait_read(self.socket, self.task)


class CanWriteCall(BaseCall):
    def __init__(self, socket):
        self.socket = socket
        super(CanWriteCall, self).__init__()

    def handle(self):
        self.scheduler.wait_write(self.socket, self.task)

