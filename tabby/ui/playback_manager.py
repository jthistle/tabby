
import re
import time

from lib.notenames import name_to_val
from threading import Thread, Lock


NOTE_VAL_FINDER = re.compile(r"\d+", re.I)


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


class PlaybackManager:
    def __init__(self, synth):
        self.synth = synth
        self.notes = []
        self.notes_lock = Lock()

        self.sfid = self.synth.sfload("/home/james/Downloads/GeneralUserGS/GeneralUserGS.sf2")
        self.synth.program_select(0, self.sfid, 0, 24)

    def play_chord(self, chord):
        bar = chord.parent
        tuning = bar.tuning
        vals = []
        last_str_val = -1
        offset = 2
        for string in range(bar.nstrings):
            string_val = name_to_val(tuning.at(string), req_octave=False)
            if string_val <= last_str_val:
                offset += 1
            last_str_val = string_val

            note = chord.get_note(string)
            if note is None:
                continue
            note_val_find = NOTE_VAL_FINDER.match(note.value)
            if note_val_find is None:
                continue
            note_val = int(note_val_find.group(0).strip())

            vals.append(string_val + offset * 12 + note_val)

        chord_playback_notes = []
        self.notes_lock.acquire()
        for val in vals:
            new_note = PlaybackNote(0, val)

            for i in range(len(self.notes) - 1, -1, -1):
                note = self.notes[i]
                if note.conflicts_with(new_note):
                    note.stop(self.synth)
                    del self.notes[i]

            new_note.play(self.synth)
            self.notes.append(new_note)
            chord_playback_notes.append(new_note)

        self.notes_lock.release()

        Thread(target=self.start_noteoff_thread, args=(chord_playback_notes,)).start()

    def start_noteoff_thread(self, notes):
        time.sleep(1)
        for note in notes:
            if note.playing:
                note.stop(self.synth)
                del self.notes[self.notes.index(note)]
