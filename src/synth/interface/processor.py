
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
        self.buffers = {}
        self.volume = 1

        self.waiting_for_response = False

    def read_buffers(self):
        """
        Expect payloads in format:
            for NEW_BUFFER:  buffer object
            for EXTEND_BUFFER:  (buffer id, size change)
            for REMOVE_BUFFER:  not implemented
            for REQUEST_REPONSES: { buffer id: buffer data }
            for END_LOOP: buffer id
        """
        while self.interface_pipe.poll():
            msg_type, payload = self.interface_pipe.recv()
            if msg_type == MessageType.NEW_BUFFER:
                self.buffers[payload.id] = payload
            elif msg_type == MessageType.EXTEND_BUFFER:
                self.buffers[payload[0]].size += payload[1]
            elif msg_type == MessageType.REQUEST_REPONSES:
                self.process_responses(payload)
            elif msg_type == MessageType.END_LOOP:
                self.buffers[payload].end_loop()

    def correct_val(self, val):
        return int(max(-VAL_LIMIT, min(VAL_LIMIT, val * self.volume)))

    def process_responses(self, responses):
        data = [0] * self.period_size
        for buf_id in responses:
            i = 0
            for part in self.buffers[buf_id].read(responses[buf_id]):
                data[i] += part
                i += 1

        data = [self.correct_val(x) for x in data]
        self.alsa_data_queue.put(struct.pack(
                "<{}h".format(self.period_size),
                *data
            )
        )

        self.waiting_for_response = False

        # Take the time to delete a single buffer if we think we can get away
        # with it, in order to free up memory
        if self.alsa_data_queue.full():
            for buf_id in self.buffers:
                buf = self.buffers[buf_id]
                if buf.finished and not buf.immortal:
                    self.interface_pipe.send((MessageType.DELETE_BUFFER, buf_id))
                    del self.buffers[buf_id]
                    break

    def run(self):
        begin_time = time.time()
        while True:
            self.read_buffers()

            if len(self.buffers) == 0:
                time.sleep(0.001)
                continue

            if self.waiting_for_response:
                continue

            requests = []
            for buffer in self.buffers.values():
                if buffer.finished:
                    continue

                requests.append(buffer.get_request(self.period_size))

            self.interface_pipe.send((MessageType.REQUEST_REPONSES, requests))
            self.waiting_for_response = True


def run_processor(*args):
    processor = AudioProcessor(*args)
    processor.run()
