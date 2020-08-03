
from enum import Enum


class EventType(Enum):
    NOTE_ON = 1
    NOTE_OFF = 1



class Event:
    def __init__(self, etype):
        self.type = etype


class EventNoteOn(Event):
    def __init__(self, midi_note, velocity):
        super().__init__(EventType.NOTE_ON)
        self.note = midi_note
        self.velocity = velocity


class EventNoteOff(Event):
    def __init__(self, midi_note):
        super().__init__(EventType.NOTE_OFF)
        self.note = midi_note
