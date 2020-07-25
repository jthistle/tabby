
import math

def interpolate(a, b, t):
    # Linear interpolation is good enough
    return a + (b - a) * t


def change_pitch(samples, rate):
    """
    Change the pitch of a samples array, returning a new samples array with the pitch changed.
    """
    LIMIT = (1 << 15) - 1

    index = 0
    finished = []
    while index < len(samples) - math.ceil(rate):
        i = int(index);
        frac = index - i;
        s1 = samples[i];
        s2 = samples[i + math.ceil(rate)];
        val = int(interpolate(s1, s2, frac))

        # Apply clipping
        val = max(-LIMIT, min(LIMIT, val))

        finished.append(val)
        index += rate

    return finished


def change_pitch_semitones(samples, semitones):
    ratio = 2 ** (semitones / 12)
    return change_pitch(samples, ratio)
