
from .definitions import SFGenerator, rangesType
from .modulator import Modulator


SF_GEN_DEFAULTS = {
    SFGenerator.startAddrsOffset: 0,
    SFGenerator.endAddrsOffset: 0,
    SFGenerator.startloopAddrsOffset: 0,
    SFGenerator.endloopAddrsOffset: 0,
    SFGenerator.startAddrsCoarseOffset: 0,
    SFGenerator.modLfoToPitch: 0,
    SFGenerator.vibLfoToPitch: 0,
    SFGenerator.modEnvToPitch: 0,
    SFGenerator.initialFilterFc: 13500,
    SFGenerator.initialFilterQ: 0,
    SFGenerator.modLfoToFilterFc: 0,
    SFGenerator.modEnvToFilterFc: 0,
    SFGenerator.endAddrsCoarseOffset: 0,
    SFGenerator.modLfoToVolume: 0,
    SFGenerator.chorusEffectsSend: 0,
    SFGenerator.reverbEffectsSend: 0,
    SFGenerator.pan: 0,
    SFGenerator.delayModLFO: -12000,
    SFGenerator.freqModLFO: 0,
    SFGenerator.delayVibLFO: -12000,
    SFGenerator.freqVibLFO: 0,
    SFGenerator.delayModEnv: -12000,
    SFGenerator.attackModEnv: -12000,
    SFGenerator.holdModEnv: -12000,
    SFGenerator.decayModEnv: -12000,
    SFGenerator.sustainModEnv: 0,
    SFGenerator.releaseModEnv: -12000,
    SFGenerator.keynumToModEnvHold: 0,
    SFGenerator.keynumToModEnvDecay: 0,
    SFGenerator.delayVolEnv: -12000,
    SFGenerator.attackVolEnv: -12000,
    SFGenerator.holdVolEnv: -12000,
    SFGenerator.decayVolEnv: -12000,
    SFGenerator.sustainVolEnv: 0,
    SFGenerator.releaseVolEnv: -12000,
    SFGenerator.keynumToVolEnvHold: 0,
    SFGenerator.keynumToVolEnvDecay: 0,
    SFGenerator.keyRange: rangesType.from_hilo(0, 127),
    SFGenerator.velRange: rangesType.from_hilo(0, 127),
    SFGenerator.startloopAddrsCoarseOffset: 0,
    SFGenerator.keynum: -1,
    SFGenerator.velocity: -1,
    SFGenerator.initialAttenuation: 0,
    SFGenerator.endloopAddrsCoarseOffset: 0,
    SFGenerator.coarseTune: 0,
    SFGenerator.fineTune: 0,
    SFGenerator.sampleModes: 0,
    SFGenerator.scaleTuning: 100,
    SFGenerator.exclusiveClass: 0,
    SFGenerator.overridingRootKey: -1,
}


# Soundfont 2.01 spec, 8.4
DEFAULT_MODULATORS = [
    # 8.4.1  MIDI Note-On Velocity to Initial Attenuation
    Modulator.from_default_def(0x0502, SFGenerator.initialAttenuation, 960, 0x0, 0),
    # 8.4.2  MIDI Note-On Velocity to Filter Cutoff
    Modulator.from_default_def(0x0102, SFGenerator.initialFilterFc, -2400, 0x0, 0),
    # 8.4.3  MIDI Channel Pressure to Vibrato LFO Pitch Depth
    Modulator.from_default_def(0x000D, SFGenerator.vibLfoToPitch, 50, 0x0, 0),  # TODO 50/cents per max excursion?
    # 8.4.4  MIDI Continuous Controller 1 to Vibrato LFO Pitch Depth
    Modulator.from_default_def(0x0081, SFGenerator.vibLfoToPitch, 50, 0x0, 0),
    # 8.4.5  MIDI Continuous Controller 7 to Initial Attenuation
    Modulator.from_default_def(0x0582, SFGenerator.initialAttenuation, 960, 0x0, 0),
    # 8.4.6  MIDI Continuous Controller 10 to Pan Position
    Modulator.from_default_def(0x028A, SFGenerator.pan, 1000, 0x0, 0),
    # 8.4.7  MIDI Continuous Controller 11 to Initial Attenuation
    Modulator.from_default_def(0x058B, SFGenerator.initialAttenuation, 960, 0x0, 0),
    # 8.4.8  MIDI Continuous Controller 91 to Reverb Effects Send
    Modulator.from_default_def(0x00DB, SFGenerator.reverbEffectsSend, 200, 0x0, 0),
    # 8.4.9  MIDI Continuous Controller 93 to Chorus Effects Send
    Modulator.from_default_def(0x00DD, SFGenerator.chorusEffectsSend, 200, 0x0, 0),
    # 8.4.10  MIDI Pitch Wheel to Initial Pitch Controlled by MIDI Pitch Wheel Sensitivity
    # Modulator.from_default_def(0x020E, SFGenerator.initialPit, 200, 0x0, 0),
]
