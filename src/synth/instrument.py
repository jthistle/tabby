
import os
import simpleaudio as sa

from util.logger import logger
from lib.notenames import name_to_val
from .conversion import data_to_samples, samples_to_data
from .repitch import change_pitch_semitones
from .const import SAMPLE_RATE


def data_from_file(file):
    wave_obj = sa.WaveObject.from_wave_file(file)
    data = wave_obj.audio_data
    return data


class Instrument:
    def __init__(self, directory):
        logger.info("Load instrument from {}".format(directory))
        self.samples = {}
        for entry in filter(lambda x: x.is_file(), os.scandir(directory)):
            note = entry.name[:-4]
            path = entry.path
            data = data_from_file(path)
            samples = data_to_samples(data)
            self.samples[name_to_val(note)] = samples
        logger.info("Finished loading {}".format(directory))

    def get_note(self, note, length = None):
        """
        Get the samples for a note. length is the length of the note in seconds (useful for optimization).
        Returns the samples list.
        """
        use = None
        for val in sorted(self.samples.keys()):
            if val > note:
                break
            use = val

        if use is None:
            return None

        samples_to_use = self.samples[use]
        if length is not None:
            sample_count = int(length * SAMPLE_RATE)
            if sample_count < len(samples_to_use):
                samples_to_use = samples_to_use[:sample_count]

        pitch_diff = note - use
        final = change_pitch_semitones(samples_to_use, pitch_diff)
        return final
