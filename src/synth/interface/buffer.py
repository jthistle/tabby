
from util.logger import logger

from multiprocessing import Queue


class AudioBuffer:
    def __init__(self, _id, size, immortal):
        self.id = _id
        self.size = size
        self.immortal = immortal
        self.offset = 0

    def get_request(self, size):
        return (self.id, self.offset, size)

    def read(self, response):
        tot = 0
        for x in response:
            yield x
            tot += 1

        self.offset += tot
        for i in range(len(response) - tot):
            yield 0

    @property
    def finished(self):
        return self.offset >= self.size
