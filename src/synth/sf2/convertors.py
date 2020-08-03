
from math import log2


MIN = -0x7fff
MAX =  0x7fff


def hertz_to_cents(hz):
    global MIN, MAX
    if hz == 0:
        return MIN
    return min(MAX, 1200 * log2(hz / 8.176))


def cents_to_hertz(cts):
    global MIN
    if cts == MIN:
        return 0

    return 2 ** (cts / 1200) * 8.176


def secs_to_timecents(s):
    global MIN, MAX
    if s == 0:
        return MIN
    return min(MAX, 1200 * log2(s))


def timecents_to_secs(tcts):
    global MIN
    if cts == MIN:
        return 0

    return 2 ** (tcts / 1200)

