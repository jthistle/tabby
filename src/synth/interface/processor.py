
import time
import struct
from threading import Thread

from util.logger import logger
from .message import MessageType

VAL_LIMIT = (1 << 15) - 1


class AudioProcessor:
    def __init__(self, period_size, interface_pipe, alsa_data_queue):
        self.period_size = period_size
        self.interface_pipe = interface_pipe
        self.alsa_data_queue = alsa_data_queue
        self.buffers = []
        self.volume = 1

    def buf_by_id(self, buf_id):
        for buf in self.buffers:
            if buf.id == buf_id:
                return buf
        return None

    def read_buffers(self):
        """
        Expect payloads in format:
            for NEW_BUFFER:  buffer object
            for EXTEND_BUFFER:  (buffer id, size change)
            for REMOVE_BUFFER:  not implemented
        """
        while self.interface_pipe.poll():
            msg_type, payload = self.interface_pipe.recv()
            if msg_type == MessageType.NEW_BUFFER:
                self.buffers.append(payload)
            elif msg_type == MessageType.EXTEND_BUFFER:
                self.buf_by_id(payload[0]).size += payload[1]

    def correct_val(self, val):
        return int(max(-VAL_LIMIT, min(VAL_LIMIT, val * self.volume)))

    def run(self):
        begin_time = time.time()
        while True:
            self.read_buffers()

            if len(self.buffers) == 0:
                time.sleep(0.001)
                continue

            data = [0] * self.period_size
            for buffer in self.buffers:
                if buffer.finished:
                    continue

                i = 0
                buf_period = buffer.read(self.period_size)
                for part in buf_period:
                    data[i] += part
                    i += 1

            data = [self.correct_val(x) for x in data]
            self.alsa_data_queue.put(struct.pack(
                    "<{}h".format(self.period_size),
                    *data
                )
            )

def run_processor(*args):
    processor = AudioProcessor(*args)
    processor.run()
