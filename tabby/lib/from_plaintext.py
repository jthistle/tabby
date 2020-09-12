
import re
from enum import Enum


class LineType(Enum):
    UNKNOWN = 0
    STRING = 1
    TEXT = 2
    BREAK = 3



def from_plaintext(text):
    """Attempts to parse a plaintext tab `text` into a Tabby-readable tab object.
    Ill-formed tabs will cause it to raise an exception, as may certain edge cases.
    """
    model = {
        "meta": {
            "name": "Untitled",
            "api_version": 1,
        },
        "max_width": 100,
        "tab": [

        ]
    }

    tab = model["tab"]

    lines = text.split("\n")
    current_system = []
    last_text = False
    for line in lines:
        line_type, data = parse_line(line)

        if line_type == LineType.STRING:
            current_system.append(data)
        elif len(current_system) != 0:
            for bar in rectify_strings(current_system):
                tab.append(bar)
            current_system = []

        if line_type == LineType.TEXT:
            if last_text:
                tab[-1]["value"] += "\n" + data
            else:
                tab.append({
                    "type": "Text",
                    "value": data
                })
                last_text = True
        else:
            last_text = False

    return model


def string_has_anchor(string, n):
    try:
        string[n]
    except KeyError:
        return False
    return True


def explain(*msg):
    EXPLAIN = False
    if EXPLAIN:
        print(*msg)

def rectify_strings(system):
    """During the process of guessing what parts of a string are separate notes, inevitably we
    will end up with unequal numbers of notes on each string. This function attempts to remove
    all artefacts of this guessing, leaving bars with the same number of chords on each string.

    Expects `system` to be given as the format returned by `parse_string`.
    Returns the bars from the system passed in Tabby-readable format.
    """
    tuning_strings = []
    for string in system:
        tuning_strings.append(string.get("tuning"))
    tuning_strings.reverse()

    bars = []
    for i in range(len(system[0]["bars"])):
        bar = [x["bars"][i] for x in system]

        # Find the highest anchor point number in the bar
        max_anchor = max(*[n for s in bar for n in s])

        last_good = 0
        for anchor in range(max_anchor + 1):
            explain("\nAnchor point {}".format(anchor))
            good = True
            notes_at_anchor = 0
            for string in bar:
                if not string_has_anchor(string, anchor):
                    good = False
                else:
                    notes_at_anchor += 1
            if good:
                explain("All anchor points satisfied")
                last_good = anchor
                continue

            if notes_at_anchor == 0:
                explain("Anchor point is unused")
                continue

            _debug = 0
            explain("Not all strings have anchor point")
            for string in bar:
                if string_has_anchor(string, anchor):
                    note = string[anchor]
                    if note is not None:
                        if string[last_good] is not None:
                            explain("Oops! Overwriting note on string {}, anchor {}, bar {}".format(_debug, string, i))
                        string[last_good] = note
                        explain("Moving note '{}' from string {} to {}".format(note, _debug, last_good))
                    else:
                        explain("Deleting empty note string {}".format(_debug))
                    del string[anchor]
                _debug += 1

        # Debug
        for string in bar:
            acc = ""
            for note in string.values():
                if note is None:
                    acc += "-"
                else:
                    acc += note
            explain(acc)
        explain("end bar\n")

        chords = []
        bar_notes = [list(x.values()) for x in bar]
        for chord_num in range(len(bar_notes[0])):
            string_count = len(bar_notes)

            is_empty = True
            for string_num in range(string_count):
                string = bar_notes[string_num]
                try:
                    if string[chord_num] is not None:
                        is_empty = False
                except KeyError:
                    print("Encountered an error.")
                    print(string_num, chord_num)
                    print(bar_notes)
                    raise

            if is_empty:
                if len(chords) == 0 or chords[-1].get("type") != "EmptyChords":
                    chords.append({
                        "type": "EmptyChords",
                        "count": 1,
                    })
                else:
                    chords[-1]["count"] += 1
                continue

            chord_notes = []
            for string_num in range(string_count):
                string = bar_notes[string_num]
                chord_notes.append({
                    "type": "Note",
                    "value": string[chord_num] or "",
                    "string": string_count - string_num - 1,     # reverse string numbers
                })

            chords.append({
                "type": "Chord",
                "notes": chord_notes
            })

        bars.append({
            "type": "Bar",
            "chords": chords,
            "tuning": {
                "type": "Tuning",
                "strings": tuning_strings
            }
        })

    return bars




STRING_TUNING_RE = re.compile(r"^\s*([a-g#])\s*\|", re.I)

def parse_line(line):
    if line.strip() == "":
        return (LineType.BREAK, None)

    if STRING_TUNING_RE.match(line):
        return (LineType.STRING, parse_string(line))
    else:
        return (LineType.TEXT, line)



def parse_string(string):
    """Tries to work out which bits of a string are separate notes.

    Returns a dict of the form:
        {
            "tuning": str,
            "notes": {
                int: str    # anchor point: note value
            }
        }
    """
    str_start = STRING_TUNING_RE.match(string)
    tuning = str_start.group(1)

    beginning_size = len(str_start.group(0))

    bars = []
    cur_bar = {}
    acc = ""
    acc_begin = 0
    i = beginning_size + 1
    while i < len(string):
        char = string[i]
        if char == "|":
            bars.append(cur_bar)
            cur_bar = {}
            i += 2
            acc_begin = 0
            continue

        # Treat a space the same as a dash
        if char in ("-", " "):
            if acc != "":
                for note in parse_accumulated(acc):
                    cur_bar[acc_begin] = note
                    acc_begin += len(note)
            if string[i+1] != "|":
                cur_bar[acc_begin] = None
                acc_begin += 1
            acc = ""
        else:
            acc += char

        i += 1

    return {
        "tuning": tuning,
        "bars": bars
    }


def parse_accumulated(acc):
    try:
        int(acc)
    except ValueError:
        return parse_complex(acc)
    else:
        return parse_simple(acc)


def parse_simple(acc):
    """Parses a simple note (i.e. all numerals). This allows for situations where notes have been
    written with no gap, e.g. '456' -> ['4', '5', '6']. Note however that due to this ambiguity,
    '123' -> ['12', '3'].
    """
    current = []
    while acc != "":
        if int(acc) >= 25:
            # assume it was meant to be one note followed by another
            for i in range(2, len(acc) + 1):
                if int(acc[:i]) >= 25:
                    current.append(acc[:i-1])
                    acc = acc[i-1:]
                    break
        else:
            current.append(acc)
            acc = ""

    return current


def parse_complex(acc):
    """Parses a complex note (i.e. one containing symbols other than numbers), for example
    '4h5', '/8', '11p10'. Returns a list of notes, e.g. ['4', 'h5'], ['/8'], ['11', 'p10'].
    """
    current_pre = ""
    current_int = ""
    notes = []
    for char in acc:
        try:
            int(char)
        except ValueError:
            if current_int != "":
                parts = parse_simple(current_int)
                notes += [current_pre + parts[0], *parts[1:]]

                current_pre = ""
                current_int = ""

            current_pre += char
        else:
            current_int += char

    if current_int != "":
        parts = parse_simple(current_int)
        notes += [current_pre + parts[0], *parts[1:]]
    elif current_pre != "":
        try:
            notes[-1] += current_pre
        except IndexError:
            notes.append(current_pre)

    return notes

