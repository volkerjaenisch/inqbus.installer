from itertools import count
import os
import time


class TaskMixin(object):

    def runtask(self, func):
        self.task_file_name = 'fabric_tasks.txt'
        try:
            if time.time() - os.path.getmtime(self.task_file_name) > 1800:
                self.clear()
            with open(self.task_file_name, 'r') as _file:
                self.finished_tasks = _file.readlines()
        except OSError:
            self.clear()
            self.finished_tasks = []
        if self.finished(func.name):
            print('Task "' + func.name +
                  '" is already done! Skipping')
        else:
            func.install()
            self.finish(func.name)

    def task_out(self, task):
        return task + '\n'

    def clear(self):
        with open(self.task_file_name, 'w') as _file:
            _file.write("")

    def finished(self, task):
        return self.task_out(task) in self.finished_tasks

    def finish(self, task):
        with open(self.task_file_name, 'a') as _file:
            _file.write(self.task_out(task))
