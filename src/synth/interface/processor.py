
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
        """
        while self.interface_pipe.poll():
            msg_type, payload = self.interface_pipe.recv()
            if msg_type == MessageType.NEW_BUFFER:
                self.buffers[payload.id] = payload
            elif msg_type == MessageType.EXTEND_BUFFER:
                self.buffers[payload[0]].size += payload[1]
            elif msg_type == MessageType.REQUEST_REPONSES:
                self.process_responses(payload)

    def correct_val(self, val):
        return int(max(-VAL_LIMIT, min(VAL_LIMIT, val * self.volume)))

    def process_responses(self, responses):
        ## DEBUG
        inner_begin_time = time.time()
        times = [inner_begin_time]
        ## END DEBUG

        data = [0] * self.period_size
        for buf_id in responses:
            i = 0
            for part in self.buffers[buf_id].read(responses[buf_id]):
                data[i] += part
                i += 1

            times.append(time.time())   ## DEBUG

        ## DEBUG
        if time.time() - inner_begin_time >= 0.001000:
            logger.debug("bollocks: {:.6f}".format(time.time() - inner_begin_time))
            for i in range(len(times) - 1):
                logger.debug("- {} took {:.6f}".format(i, times[i + 1] - times[i]))
        ## END DEBUG

        data = [self.correct_val(x) for x in data]
        self.alsa_data_queue.put(struct.pack(
                "<{}h".format(self.period_size),
                *data
            )
        )

        self.waiting_for_response = False

    def run(self):
        begin_time = time.time()
        # i = 0
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

            self.interface_pipe.send(requests)
            self.waiting_for_response = True

            # i += 1
            # if i >= 100:
            #     logger.debug("Took {:.6f}s over {} periods".format((time.time() - begin_time) / i, i))
            #     i = 0
            #     begin_time = time.time()

def run_processor(*args):
    processor = AudioProcessor(*args)
    processor.run()
