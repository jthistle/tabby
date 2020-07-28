
from .sf2.soundfont import Soundfont
from .interface import AudioInterface

class Synthesizer:
    sfont = None
    preset = None

    def __init__(self):
        self.interface = AudioInterface()

    def load_soundfont(self, path):
        self.sfont = Soundfont(path)

    def use_preset(self, bank, number):
        for preset in self.sfont.presets:
            if preset.bank == bank and preset.preset_num == number:
                self.preset = preset
                break


    def __str__(self):
        return "Synthesizer, using soundfont:\n{}\nand preset {}".format(
            self.sfont, self.preset
        )
