
import math
# import alsaaudio as aa
import time
import struct
from threading import Thread, Lock
from multiprocessing import Process, Queue, Pipe, Manager

from util.logger import logger
from .processor import run_processor
from .alsa import run_alsa
from .buffer import AudioBuffer
from .message import MessageType


class AudioInterface:
    def __init__(self, config, max_latency=0.2, use_buffering=False):
        # Format by default is signed 16-bit LE
        self.cfg = config
        self.frame_size = 2     # bytes

        self.use_buffering = use_buffering
        self.target_latency = 0.01      # only valid with use_buffering = True
        self.init_buffer_samples = int(self.cfg.sample_rate * self.target_latency)
        self.max_latency = max_latency

        self.buffer_pipes = []
        self.raw_buffers = {}
        self.raw_buffers_mutex = Lock()
        self.last = 0

        self.halted = False

        # Playback process
        # Queue size = max latency / length of period
        queue_size = int(self.max_latency / self.cfg.period_length)
        self.playback_pipe, playback_rec = Pipe()
        alsa_data_queue = Queue(maxsize=queue_size)
        self.playback_thread = Process(target=run_processor, args=(self.cfg.period_size, playback_rec, alsa_data_queue))

        # ALSA relay
        self.alsa_thread = Process(target=run_alsa, args=(self.cfg, alsa_data_queue))

        # Communication with AudioBuffers under playback process
        self.read_buffers_thread = Thread(target=self.start_read_buffers_thread)

        self.playback_thread.start()
        self.alsa_thread.start()
        self.read_buffers_thread.start()

        # Run some zeros through the system to prevent underruns on initial playback
        blank = [0] * self.cfg.sample_rate
        self.play(blank, 1)
        time.sleep(1)

    def __do_extend(self, start_point, buf_id, buffer, buf_size, channel_ratio):
        chunk_size = self.init_buffer_samples * 2
        while start_point < buf_size:
            xtnd = 0
            for i in range(start_point, min(start_point + chunk_size, buf_size)):
                for j in range(channel_ratio):
                    self.raw_buffers[buf_id].append(buffer[i])
                    xtnd += 1
            self.playback_pipe.send((MessageType.EXTEND_BUFFER, (buf_id, xtnd)))
            start_point += chunk_size

    def play(self, buffer, channels = 2, loop = None, immortal = False):
        """
        Play a buffer, which should be given as a list of frames. bytes-like objects
        are also accepted. channels specifies the number of channels of the buffer to
        be played, and must be a power of two and >= 1, and must be <= the audio config
        number of channels for this interface. If `immortal` is specified, the buffer
        will not be deleted upon finishing, allowing you to extend it or restart it.
        This comes with the responsibility of making sure not all the memory is used up
        by immortal buffers.
        """
        assert not self.halted

        # buffer should be given as a list of frames where possible
        if type(buffer) == bytes:
            buffer = struct.unpack("<h", buffer)

        buf_size = len(buffer)
        start_point = buf_size if not self.use_buffering else min(self.init_buffer_samples, buf_size)
        channel_ratio = self.cfg.channels // channels

        # We create an initial buffer up to a start point determined by the target latency
        new_data = []
        for i in range(start_point):
            for j in range(channel_ratio):
                new_data.append(buffer[i])

        self.last += 1
        loop = None if loop is None else tuple([x * channel_ratio for x in loop])
        buf = AudioBuffer(self.last, len(new_data), immortal, loop)

        self.raw_buffers_mutex.acquire()
        self.raw_buffers[self.last] = new_data
        self.raw_buffers_mutex.release()

        self.playback_pipe.send((MessageType.NEW_BUFFER, buf))

        # Now the buffer has been added to the playback processor, we can start extending it
        # with chunks while the first bit of it is playing back. Hopefully we can outpace it.
        if self.use_buffering:
            self.__do_extend(start_point, self.last, buffer, buf_size, channel_ratio)

        return self.last

    def extend(self, buffer_id, buffer, channels = 2):
        assert not self.halted

        # buffer should be given as a list of frames where possible
        if type(buffer) == bytes:
            buffer = struct.unpack("<h", buffer)

        buf_size = len(buffer)
        channel_ratio = self.cfg.channels // channels

        self.__do_extend(0, buffer_id, buffer, buf_size, channel_ratio)

        return buffer_id

    def end_loop(self, buffer_id):
        self.playback_pipe.send((MessageType.END_LOOP, buffer_id))

    def start_read_buffers_thread(self):
        """
        Expect requests from the playback pipe in the format (message type, payload),
        where payload is _ for each message type:
            for REQUEST_RESPONSES:
                [(buffer id, offset, size)]
            for DELETE_BUFFER:
                buffer id
        """
        backlog = []
        while True:
            if self.halted:
                break
            req = None
            if not self.playback_pipe.poll() and len(backlog) > 0:
                req = backlog[0]
                del backlog[0]
            else:
                self.playback_pipe.poll(timeout=None)
                try:
                    req = self.playback_pipe.recv()
                except EOFError:
                    # Probably need to halt
                    continue

            msg_type, payload = req
            if msg_type == MessageType.REQUEST_REPONSES:
                resp = {}
                for buf_id, offset, size, loop_start, loop_end in payload:
                    uses_loop = loop_start != -1 and loop_end != -1
                    if not uses_loop:
                        resp[buf_id] = self.raw_buffers[buf_id][offset:offset + size]
                        continue

                    remaining = size
                    resp[buf_id] = []
                    while remaining > 0:
                        chunk_size = min(remaining, min(size, loop_end - offset))
                        resp[buf_id] += self.raw_buffers[buf_id][offset:offset + chunk_size]
                        remaining -= chunk_size
                        offset = loop_start

                self.playback_pipe.send((MessageType.REQUEST_REPONSES, resp))
            elif msg_type == MessageType.DELETE_BUFFER:
                # 0.01s is a completely arbitrary number - we just don't want
                # deleting buffers to hold up the much more important job of
                # sending off buffer data to the processor.
                if not self.raw_buffers_mutex.acquire(timeout=0.01):
                    self.backlog.append(req)
                else:
                    del self.raw_buffers[payload]
                    self.raw_buffers_mutex.release()

    def halt(self):
        self.halted = True
        self.playback_thread.kill()
        self.alsa_thread.kill()
        self.read_buffers_thread.join()

        del self.raw_buffers
