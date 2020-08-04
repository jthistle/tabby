
import synth.sf2.decode as decode
from .definitions import SFSampleLink


class Sample:
    def __init__(self, name, data, loop: (int), sample_rate, pitch, pitch_correction, sample_type, link = 0):
        self.name = name
        self.data = data
        self.loop = loop
        self.sample_rate = sample_rate
        self.pitch = pitch
        self.pitch_correction = pitch_correction
        self.type = sample_type
        self.link = link

    @classmethod
    def from_raw(cls, smpl, sample_data):
        # Soundfont 2.01 spec, 7.10
        name = decode.ascii_str(smpl[:20])

        if name == "EOS":
            return None

        start = decode.DWORD(smpl[20:24])
        end = decode.DWORD(smpl[24:28])

        data = sample_data[start * 2:end * 2]

        start_loop = decode.DWORD(smpl[28:32])
        end_loop = decode.DWORD(smpl[32:36])

        loop = (start_loop - start, end_loop - start)

        sample_rate = decode.DWORD(smpl[36:40])
        if sample_rate > 50000 or sample_rate < 400:
            logger.warn("Warning: sample {} has unusual sample rate of {}".format(name, sample_rate))

        by_original_pitch = decode.BYTE(smpl[40:41])
        pitch_correction = ord(decode.CHAR(smpl[41:42]))

        sample_link = decode.WORD(smpl[42:44])
        sample_type = SFSampleLink(decode.WORD(smpl[44:46]))

        return cls(name, data, loop, sample_rate, by_original_pitch, pitch_correction, sample_type, sample_link)

    @property
    def num_samples(self):
        # Works for mono... TODO stereo?
        return len(self.data) // 2

    @property
    def is_mono(self):
        return self.type == SFSampleLink.monoSample

    def __str__(self):
        return "Sample '{}' of length {:.2f}s ({} samples), looping ({},{}), fs {}Hz, pitch {} ({:+d}), type {}".format(
            self.name, self.num_samples / self.sample_rate, self.num_samples, *self.loop, self.sample_rate, self.pitch, self.pitch_correction, self.type
        )
