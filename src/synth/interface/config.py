
class AudioConfig:
    def __init__(self, sample_rate=44100, channels=2, period_size=32):
        self.sample_rate = sample_rate  # Hz
        self.channels = channels
        self.period_size = period_size  # frames

        self.period_length = self.period_size / (self.channels * self.sample_rate)

    def __str__(self):
        return "AudioConfig: fs {}Hz, {} chan, period size {} frames".format(self.sample_rate, self.channels, self.period_size)
