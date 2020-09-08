
class PlaybackNote:
    def __init__(self, chan, val):
        self.chan = chan
        self.val = val
        self.playing = False

    def play(self, synth):
        synth.noteon(self.chan, self.val, 100)
        self.playing = True

    def stop(self, synth):
        synth.noteoff(self.chan, self.val)
        self.playing = False

    def conflicts_with(self, b):
        return self.playing and self.val == b.val and self.chan == b.chan
