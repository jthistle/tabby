
from util.logger import logger

from multiprocessing import Queue


class AudioBuffer:
    is_custom = False

    def __init__(self, _id, size, immortal, loop: (int, int)):
        self.id = _id
        self.size = size
        self.immortal = immortal
        self.offset = 0
        if loop is not None:
            self.loop_start, self.loop_end = loop
        self.do_loop = loop is not None

    def get_request(self, size):
        loop_start = loop_end = None
        if not self.do_loop:
            loop_start = loop_end = -1
        else:
            loop_start = self.loop_start
            loop_end = self.loop_end
        return (False, self.id, size, self.offset, loop_start, loop_end)

    def end_loop(self):
        self.do_loop = False

    def read(self, response, size):
        tot = 0
        for x in response:
            yield x
            self.offset += 1
            tot += 1
            if not self.do_loop:
                continue
            if self.offset == self.loop_end:
                self.offset = self.loop_start

        for i in range(size - tot):
            yield 0

    @property
    def finished(self):
        return self.offset >= self.size


class CustomBuffer:
    is_custom = True
    id = None
    finished = False
    immortal = False

    def __init__(self, looping):
        self.looping = looping

    def get_request(self, size):
        return (True, self.id, size, self.looping)

    def read(self, response, size):
        for x in response:
            yield x

        for i in range(size - len(response)):
            self.finished = True
            yield 0

    def end_loop(self):
        self.looping = False
