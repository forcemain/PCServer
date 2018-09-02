#! -*- coding: utf-8 -*-


import select


from Queue import Queue
from server.common.task import Task
from server.common.logger import Logger
from server.common.customcall import BaseCall


logger = Logger.get_logger(__name__)


class Scheduler(object):
    def __init__(self):
        self.task_queue = Queue()
        self.readable_dict = {}
        self.writeable_dict = {}

    def wait_read(self, socket, task):
        self.readable_dict[socket] = task

    def wait_write(self, socket, task):
        self.writeable_dict[socket] = task

    def spawn_one(self, target):
        task = Task(target)
        self.put_to_queue(task)

        return task

    def spawn_all(self, *targets):
        tasks = map(self.spawn_one, targets)

        return tasks

    def put_to_queue(self, task):
        self.task_queue.put(task)

    def ioloop(self, timeout):
        if self.readable_dict or self.writeable_dict:
            r_list, w_list, e_list = select.select(self.readable_dict, self.writeable_dict, [], timeout)
            for r in r_list:
                self.put_to_queue(self.readable_dict.get(r))
            for w in w_list:
                self.put_to_queue(self.writeable_dict.get(w))

    def main_ioloop(self):
        while True:
            self.ioloop(0)
            yield

    def main_loop(self):
        self.spawn_one(self.main_ioloop())
        while True:
            task = self.task_queue.get()
            try:
                result = task.next()
                if isinstance(result, BaseCall):
                    result.task = task
                    result.scheduler = self
                    result.handle()
                    continue
                logger.debug('task {0}#(yield {1}) hand over executive power to {2}'.format(task.target, result, self))
            except StopIteration:
                task.target.close()
                continue
            self.put_to_queue(task)

