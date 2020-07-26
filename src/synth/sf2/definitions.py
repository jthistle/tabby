
from enum import Enum


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
