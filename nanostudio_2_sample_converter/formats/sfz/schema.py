from nanostudio_2_sample_converter.formats.nanostudio_2.obsidian.schema import (
    SAMPLER_ZONE,
    OSCILLATOR_GROUP,
    VOICE,
)

KEY = "key"
LO_KEY = "lokey"
HI_KEY = "hikey"
PITCH_KEYCENTER = "pitch_keycenter"
TRANSPOSE = "transpose"
NOTE_OFFSET = "note_offset"
OCTAVE_OFFSET = "octave_offset"
DEFAULT_PATH = "default_path"
SAMPLE = "sample"

KEY_OPCODES = [KEY, LO_KEY, HI_KEY, PITCH_KEYCENTER]
TRANSPOSE_OPCODES = [TRANSPOSE, NOTE_OFFSET, OCTAVE_OFFSET]

RENAME_OPCODE_ALIASES = {
    "loopmode": "loop_mode",
    "loopstart": "loop_start",
    "loopend": "loop_end",
    "pitch": "tune",
}

REGION = {
    "header": "region",
    "obsidian_tag": SAMPLER_ZONE["tag"],
    "obsidian_opcode_rename": {
        PITCH_KEYCENTER: "root_key",
        LO_KEY: "minimum_key",
        HI_KEY: "maximum_key",
        "direction": "playback_direction",
        SAMPLE: "file_name",
    },
    "obsidian_opcode_remove": [
        KEY,
        TRANSPOSE,
        OCTAVE_OFFSET,
        NOTE_OFFSET,
        DEFAULT_PATH,
        "offset",
        "end",
        "loop_start",
        "loop_end",
    ],
    "opcodes": [
        KEY,
        LO_KEY,
        HI_KEY,
        TRANSPOSE,
        DEFAULT_PATH,
        "direction",
        "offset",
        "end",
        "loop_mode",
        "loop_start",
        "loop_end",
        "loopmode",
        "loopstart",
        "loopend",
        SAMPLE,
        PITCH_KEYCENTER,
        OCTAVE_OFFSET,
        NOTE_OFFSET,
    ],
}

GROUP = {
    "header": "group",
    "obsidian_tag": "OscX",
    "obsidian_opcode_rename": {},
    "obsidian_opcode_remove": [
        "lovel",
        "hivel",
    ],
    "opcodes": ["lovel", "hivel", "tune", "pitch"],
}

GLOBAL = {
    "header": "global",
    "opcodes": [],
    "obsidian_tag": OSCILLATOR_GROUP["tag"],
    "obsidian_opcode_rename": {},
    "obsidian_opcode_remove": [],
}

CONTROL = {
    "header": "control",
    "opcodes": [],
    "obsidian_tag": VOICE["tag"],
    "obsidian_opcode_rename": {},
    "obsidian_opcode_remove": [],
}

SFZ = [REGION, GROUP, GLOBAL, CONTROL]
HEADER = "header"

HEADERS = [header[HEADER] for header in SFZ]
HEADERS_XPATH = [
    ".//" + "/".join(HEADERS[::-1][1 : index + 2]) for index in range(len(HEADERS) - 1)
][::-1]

OPCODES = REGION["opcodes"] + GROUP["opcodes"] + GLOBAL["opcodes"] + CONTROL["opcodes"]
