
import alsaaudio as aa
from util.logger import logger

def run_alsa(cfg, data_queue):
    pcm = aa.PCM(rate=cfg.sample_rate, channels=cfg.channels, periodsize=cfg.period_size)

    while True:
        part = data_queue.get()
        pcm.write(part)
