
from enum import Enum


class rangesType:
    def __init__(self, val: int):
        self.byLo = val & 0b11111111
        self.byHi = val >> 8

    @classmethod
    def from_hilo(cls, lo, hi):
        final = cls(0)
        final.byLo = lo
        final.byHi = hi
        return final

    def contains(self, val):
        return val >= self.byLo and val <= self.byHi

    def __str__(self):
        return "rangesType: lo {} hi {}".format(self.byLo, self.byHi)


# Soundfont 2.01 spec, 8.1.2, number 54
# "0 indicates a sound reproduced with no loop, 1 indicates a sound which loops
# continuously, 2 is unused but should be interpreted as indicating no loop,
# and 3 indicates a sound which loops for the duration of key depression then
# proceeds to play the remainder of the sample."
class LoopType(Enum):
    NO_LOOP = 0
    CONT_LOOP = 1
    UNUSED_NO_LOOP = 2
    KEY_LOOP = 3


class sampleModes:
    def __init__(self, val):
        self.loop_type = LoopType(val & 0b11)

    def __str__(self):
        return "sampleModes: {}".format(self.loop_type)


class SFSampleLink(Enum):
    monoSample = 1
    rightSample = 2
    leftSample = 4
    linkedSample = 8
    RomMonoSample = 0x8001
    RomRightSample = 0x8002
    RomLeftSample = 0x8004
    RomLinkedSample = 0x8008


# Soundfont 2.01 spec, 8.1.3
class SFGenerator(Enum):
    startAddrsOffset = 0
    endAddrsOffset = 1
    startloopAddrsOffset = 2
    endloopAddrsOffset = 3
    startAddrsCoarseOffset = 4
    modLfoToPitch = 5
    vibLfoToPitch = 6
    modEnvToPitch = 7
    initialFilterFc = 8
    initialFilterQ = 9
    modLfoToFilterFc = 10
    modEnvToFilterFc = 11
    endAddrsCoarseOffset = 12
    modLfoToVolume = 13
    chorusEffectsSend = 15
    reverbEffectsSend = 16
    pan = 17
    delayModLFO = 21
    freqModLFO = 22
    delayVibLFO = 23
    freqVibLFO = 24
    delayModEnv = 25
    attackModEnv = 26
    holdModEnv = 27
    decayModEnv = 28
    sustainModEnv = 29
    releaseModEnv = 30
    keynumToModEnvHold = 31
    keynumToModEnvDecay = 32
    delayVolEnv = 33
    attackVolEnv = 34
    holdVolEnv = 35
    decayVolEnv = 36
    sustainVolEnv = 37
    releaseVolEnv = 38
    keynumToVolEnvHold = 39
    keynumToVolEnvDecay = 40
    instrument = 41
    keyRange = 43
    velRange = 44
    startloopAddrsCoarseOffset = 45
    keynum = 46
    velocity = 47
    initialAttenuation = 48
    endloopAddrsCoarseOffset = 50
    coarseTune = 51
    fineTune = 52
    sampleID = 53
    sampleModes = 54
    scaleTuning = 56
    exclusiveClass = 57
    overridingRootKey = 58


# Soundfont 2.01 spec, 7.5
class genAmountType(Enum):
    rangesType = 1
    SHORT = 2
    WORD = 3
    sampleModes = 4


# Soundfont 2.01 spec, 8.1.3
# Assume SHORT if not listed
GEN_AMOUNT_TYPE_MAP = {
    genAmountType.rangesType: [
        SFGenerator.keyRange,
        SFGenerator.velRange,
    ],
    # I don't think any of these exist. It's really hard to tell from what
    # the spec says, due to its ambiguity.
    genAmountType.WORD: [],
    genAmountType.sampleModes: [
        SFGenerator.sampleModes
    ]
}

def get_gen_amount_type(generator):
    for tp in GEN_AMOUNT_TYPE_MAP:
        if generator in GEN_AMOUNT_TYPE_MAP[tp]:
            return tp
    return genAmountType.SHORT


class SFModPolarity(Enum):
    unipolar = 0
    bipolar = 1


class SFModDirection(Enum):
    positive = 0
    negative = 1


class SFModType(Enum):
    linear = 0
    concave = 1
    convex = 2
    switch = 3


class SFGeneralController(Enum):
    invalid = -1
    noController = 0
    noteOnVel = 2
    noteOnKeyNum = 3
    polyPressure = 10
    channelPressure = 13
    pitchWheel = 14
    pitchWheelSens = 16
    link = 127


class SFTransform(Enum):
    linear = 0
    absoluteValue = 2
