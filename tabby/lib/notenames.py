
"""
Midi pitch values:
    A0 has value 21
    C8 has value 108
"""

NAME_TO_VAL = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
}

def name_to_val(name, req_octave = True):
    """Given a note name (e.g. Bb4) return the MIDI key value associated
    with the note.

    If req_octave is False, then the note name must not include an octave,
    (i.e. Bb is valid, but Bb4 is not). The value returned will then be
    contained to one octave (specified by the offset).
    """
    name = name.upper()
    note = name[0]
    mod = None
    octave = 0
    offset = 12

    if req_octave:
        if name[1] in ("#", "B"):
            mod = name[1]
            octave = int(name[2:])
        else:
            octave = int(name[1:])
    else:
        if len(name) > 1 and name[1] in ("#", "B"):
            mod = name[1]
            octave = int(name[2:])

    val = NAME_TO_VAL[note]
    if mod == "#":
        val += 1
    elif mod == "B":
        val -= 1

    val += octave * 12
    val += offset
    return val
