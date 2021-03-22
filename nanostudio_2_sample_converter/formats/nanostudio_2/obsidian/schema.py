"""
Obsidian schema. Used to define defaults for a new instrument patch
Note: no public documentation exists for Obsidian instrument in NanoStudio 2.
"""
ROOT = {
    "tag": "Root",
    "default_settings": [
        {"attribute": "FileVersion", "key": "file_version", "default": "1"},
        {"attribute": "V", "key": "v", "default": "3"},  # Unknown what this means
        {"attribute": "Tags", "key": "tags", "default": "603979776"},
        {"attribute": "Oct", "key": "oct", "default": "4"},
    ],
}

VOICE = {
    "tag": "Voice",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "2"},  # Unknown what this means
        {"attribute": "Poly", "key": "polyphony", "default": "12"},
        {"attribute": "Uni", "key": "unison_voices", "default": "1"},
        {"attribute": "UDtn", "key": "unison_detune", "default": "0"},
        {"attribute": "USte", "key": "unison_stereo", "default": "0"},
        {"attribute": "GLeg", "key": "glide_legato", "default": "On"},
        {"attribute": "GTim", "key": "glide_time", "default": "0"},
    ],
}

OSCILLATOR_GROUP = {
    "tag": "Osc",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "Type", "key": "type", "default": "Split 3"},
        {"attribute": "LL1", "key": "layer_low_1", "default": "0"},
        {"attribute": "LL2", "key": "layer_low_2", "default": "0"},
        {"attribute": "S2L1", "key": "split_2_low_1", "default": "0.5"},
        {"attribute": "S3L1", "key": "split_3_low_1", "default": "0.5"},
        {"attribute": "S3L2", "key": "split_3_low_2", "default": "0.75"},
        {"attribute": "LX1", "key": "layer_crossfade_1", "default": "0"},
        {"attribute": "LX2", "key": "layer_crossfade_2", "default": "0"},
    ],
}

OSCILLATOR = {
    "tag": "Osc",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "En", "key": "enabled", "default": "On"},
        {"attribute": "Type", "key": "type", "default": "Sample"},
        {"attribute": "Trn", "key": "transpose", "default": "0"},
        {"attribute": "Dtn", "key": "detune", "default": "0"},
        {"attribute": "KeyT", "key": "key_track", "default": "1"},
        {"attribute": "Lev", "key": "level", "default": "1"},
        {"attribute": "Pan", "key": "pan", "default": "0.5"},
        {"attribute": "FMix", "key": "filter_mix", "default": "0"},
        {"attribute": "Ring", "key": "ring_modulation_osc_2", "default": "0"},
        {"attribute": "Widt", "key": "width", "default": "0.5"},
        {"attribute": "POff", "key": "phase_offset", "default": "0"},
    ],
}

ANALOG = {
    "tag": "Anlg",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "Wave", "key": "waveform", "default": "Saw"},
        {"attribute": "Sync", "key": "oscillator_sync", "default": "OFF"},
        {"attribute": "PWM", "key": "pulse_wave_modulation", "default": "0"},
        {"attribute": "SRat", "key": "sync_ratio", "default": "0"},
        {"attribute": "SShp", "key": "sync_hardness", "default": "0.5"},
    ],
}

WAVETABLE = {
    "tag": "Wave",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "Mode", "key": "", "default": "Crossfade"},
        {"attribute": "Pos", "key": "position", "default": "0"},
        {"attribute": "Dtn", "key": "detune", "default": "0.5"},
    ],
}

WAVETABLE_TABLE = {
    "tag": "WT",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "Name", "key": "name", "default": "Simple/Sin-Tri-Saw"},
    ],
}

PHASE_DISTORTION = {
    "tag": "PD",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "Wave", "key": "waveform", "default": "Saw"},
        {"attribute": "PD", "key": "phase_distortion", "default": "0.5"},
    ],
}

FREQUENCY_MODULATION = {
    "tag": "FM",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
    ],
}

FM_OPERATOR_GROUP = {
    "tag": "OP",
    "default_settings": [],
}

FM_OPERATOR = {
    "tag": "O",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},
        {"attribute": "Wave", "key": "waveform", "default": "Sine"},
        {"attribute": "FrqO", "key": "detune", "default": "0"},
        {"attribute": "Rat", "key": "frequency_ratio", "default": "10000"},
    ],
}

FM_CONNECTIONS = {
    "tag": "Con",
    "default_settings": [],
}

FM_OPERATOR_CONNECTION = {
    "tag": "O",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "Amt", "key": "send_amount", "default": "0"},
    ],
}

NANO_SAW = {
    "tag": "NS",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "Mix", "key": "mix", "default": "1"},
        {"attribute": "FlOf", "key": "falloff", "default": "0"},
        {"attribute": "Dtn", "key": "detune", "default": "0"},
        {"attribute": "Sprd", "key": "spread", "default": "0"},
    ],
}

NOISE = {
    "tag": "Nois",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "Type", "key": "type", "default": "White"},
        {"attribute": "Deci", "key": "decimate", "default": "0"},
        {"attribute": "Cut", "key": "cutoff", "default": "0.5"},
        {"attribute": "Q", "key": "resonance", "default": "0"},
    ],
}

SAMPLER = {
    "tag": "Samp",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
    ],
}

SAMPLER_ZONE_GROUP = {
    "tag": "Zones",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
    ],
}

SAMPLER_ZONE = {
    "tag": "Zone",
    "default_settings": [
        {"attribute": "File", "key": "file_name", "default": ""},
        {"attribute": "Root", "key": "root_key", "default": "0"},
        {"attribute": "Lo", "key": "minimum_key", "default": "0"},
        {"attribute": "Hi", "key": "maximum_key", "default": "0"},
        {"attribute": "Tune", "key": "tune", "default": "0"},
        {"attribute": "Vol", "key": "level", "default": "1"},
        {"attribute": "Pan", "key": "pan", "default": "0.5"},
        {"attribute": "Dir", "key": "playback_direction", "default": "Forward"},
        {"attribute": "Loop", "key": "loop_mode", "default": "Off"},
    ],
}

FILTER_GROUP = {
    "tag": "Filt",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "O1BP", "key": "oscillator_1_bypass", "default": "OFF"},
        {"attribute": "Rout", "key": "filter_routing", "default": "PARALLEL"},
    ],
}

FILTER = {
    "tag": "F",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "En", "key": "enabled", "default": "Off"},
        {"attribute": "Type", "key": "type", "default": "LP 12-A"},
        {"attribute": "CutO", "key": "cutoff", "default": "1"},
        {"attribute": "Q", "key": "resonance", "default": "0"},
        {"attribute": "SGan", "key": "eq_gain", "default": "0"},
        {"attribute": "FVwl", "key": "formant_vowel", "default": "0.5"},
        {"attribute": "CMix", "key": "comb_filter_mix", "default": "1"},
        {"attribute": "WSGn", "key": "waveshaper_lo_fi_mix", "default": "0.5"},
        {"attribute": "Drv", "key": "drive", "default": "0"},
        {"attribute": "KeyT", "key": "key_tracking", "default": "1"},
        {"attribute": "OGn", "key": "output_gain", "default": "1"},
        {"attribute": "Pan", "key": "pan", "default": "0.5"},
    ],
}

ENVELOPE_GROUP = {
    "tag": "Env",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
    ],
}

ENVELOPE = {
    "tag": "Env",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "2"},  # Unknown what this means
        {"attribute": "Type", "key": "type", "default": "ADSR"},
        {"attribute": "A", "key": "attack", "default": "0"},
        {"attribute": "D", "key": "decay", "default": "0"},
        {"attribute": "Brk", "key": "ad_break", "default": "0"},
        {"attribute": "S", "key": "sustain", "default": "1"},
        {"attribute": "D2", "key": "ad_decay_2", "default": "0"},
        {"attribute": "R", "key": "release", "default": "0"},
        {"attribute": "Levl", "key": "envelope_level", "default": "1"},
        {"attribute": "Dly", "key": "delay", "default": "0"},
        {"attribute": "SLv", "key": "bipolar_attack_level", "default": "0"},
        {"attribute": "RLv", "key": "bipolar_release_level", "default": "0"},
        {"attribute": "AC", "key": "adsr_attack_curve", "default": "2"},
        {"attribute": "SC", "key": "adsr_sustain_curve", "default": "2"},
        {"attribute": "DC", "key": "adsr_decay_curve", "default": "2"},
        {"attribute": "RC", "key": "adsr_release_curve", "default": "2"},
        {"attribute": "VTim", "key": "velocity_time", "default": "0"},
        {"attribute": "VLev", "key": "velocity_level", "default": "0"},
        {"attribute": "KCtr", "key": "key_center", "default": "24"},
        {"attribute": "KTim", "key": "key_time", "default": "0"},
        {"attribute": "KLev", "key": "key_level", "default": "0"},
    ],
}

LFO_GROUP = {
    "tag": "LFO",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
    ],
}

LFO = {
    "tag": "LFO",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "Type", "key": "type", "default": "Sine"},
        {"attribute": "Rt", "key": "rate_time", "default": "4"},
        {"attribute": "RtBt", "key": "rate_beats_numerator", "default": "1"},
        {"attribute": "BRt", "key": "rate_beats_denominator_or_hz", "default": "Hz"},
        {"attribute": "Sync", "key": "rate_sync", "default": "OFF"},
        {"attribute": "OutT", "key": "output", "default": "BIPOLAR"},
        {"attribute": "Atk", "key": "attack", "default": "0"},
        {"attribute": "Ampl", "key": "level", "default": "0"},
        {"attribute": "PhOf", "key": "phase_offset", "default": "0"},
        {"attribute": "Crv", "key": "curve", "default": "0.5"},
        {"attribute": "SqCv", "key": "square_curve", "default": "0"},
        {"attribute": "Warp", "key": "warp", "default": "0.5"},
        {"attribute": "Qtz", "key": "quantization", "default": "0"},
        {"attribute": "RPtn", "key": "random_loop_pattern", "default": "8"},
        {"attribute": "RLen", "key": "random_loop_length", "default": "2"},
    ],
}

MOD_MATRIX = {
    "tag": "Mod",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "2"},  # Unknown what this means
    ],
}

CONTROL = {
    "tag": "C",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "3"},  # Unknown what this means
        {"attribute": "Src", "key": "source", "default": "None"},
        {"attribute": "Dest", "key": "destination", "default": "None"},
        {"attribute": "DstP", "key": "destination_parameter", "default": "---"},
        {"attribute": "Sca", "key": "multiplier", "default": "None"},
        {"attribute": "Dept", "key": "depth", "default": "100"},
    ],
}

UI = {
    "tag": "UI",
    "default_settings": [],
}

UI_CONTROL = {
    "tag": "C",
    "default_settings": [
        {"attribute": "Name", "key": "name", "default": ""},
    ],
}

EFFECTS = {
    "tag": "FX",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "En", "key": "enabled", "default": "0"},
        {
            "attribute": "Ord",
            "key": "ord",
            "default": "131328",
        },  # Unknown what this means
    ],
}

MULTI_EFEECTS = {
    "tag": "MFX",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "Type", "key": "type", "default": "Chorus 1"},
        {"attribute": "En", "key": "enabled", "default": "0"},
        {"attribute": "Rat", "key": "ratio", "default": "0.25"},
        {"attribute": "Dep", "key": "depth", "default": "0.5"},
        {"attribute": "Dly", "key": "delay", "default": "0.5"},
        {"attribute": "FB", "key": "feedback", "default": "0"},
        {"attribute": "Wid", "key": "width", "default": "0.5"},
        {"attribute": "Mix", "key": "mix", "default": "1"},
    ],
}

DELAY = {
    "tag": "Dly",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "En", "key": "enabled", "default": "0"},
        {"attribute": "Type", "key": "type", "default": "Stereo"},
        {"attribute": "DTim", "key": "delay_time_seconds", "default": "0.5"},
        {"attribute": "TNum", "key": "delay_time_numerator", "default": "1"},
        {"attribute": "TDen", "key": "delay_time_denominator", "default": "sec"},
        {"attribute": "EQCt", "key": "equalizer", "default": "0.5"},
        {"attribute": "FB", "key": "feedback", "default": "0"},
        {"attribute": "Mix", "key": "mix", "default": "0.33"},
    ],
}

REVERB = {
    "tag": "Rev",
    "default_settings": [
        {"attribute": "V", "key": "v", "default": "1"},  # Unknown what this means
        {"attribute": "Type", "key": "type", "default": "Small Room 1"},
        {"attribute": "En", "key": "enabled", "default": "0"},
        {"attribute": "LCut", "key": "low_cut", "default": "0.25"},
        {"attribute": "HCut", "key": "high_cut", "default": "0.25"},
        {"attribute": "Decy", "key": "decay", "default": "0.5"},
        {"attribute": "HDmp", "key": "damping", "default": "0.25"},
        {"attribute": "Mix", "key": "mix", "default": "0.25"},
    ],
}

MACROS = {
    "tag": "Autm",
    "default_settings": [
        {"attribute": "C01", "key": "pitch_bend", "default": "0.5"},
        {"attribute": "C02", "key": "xy_pad_x", "default": "0"},
        {"attribute": "C03", "key": "xy_pad_y", "default": "0"},
        {"attribute": "C04", "key": "knob_1", "default": "0"},
        {"attribute": "C05", "key": "knob_2", "default": "0"},
        {"attribute": "C06", "key": "knob_3", "default": "0"},
        {"attribute": "C07", "key": "knob_4", "default": "0"},
        {"attribute": "C08", "key": "knob_5", "default": "0"},
        {"attribute": "C09", "key": "knob_6", "default": "0"},
        {"attribute": "C10", "key": "knob_7", "default": "0"},
        {"attribute": "C11", "key": "knob_8", "default": "0"},
    ],
}
