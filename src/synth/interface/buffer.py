
from util.logger import logger

from multiprocessing import Queue


class AudioBuffer:
    def __init__(self, _id, size, pipe):
        self.id = _id
        self.size = size
        self.pipe = pipe
        self.offset = 0

    def read(self, size):
        self.pipe.send((self.id, self.offset, size))
        self.pipe.poll(timeout=None)
        tot = 0
        for x in self.pipe.recv():
            yield x
            tot += 1

        self.offset += tot
        for i in range(size - tot):
            yield 0

    @property
    def finished(self):
        return self.offset >= self.size
