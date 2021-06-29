from nanostudio_2_sample_converter.formats.nanostudio_2.obsidian.schema import (
    SAMPLER_ZONE,
    OSCILLATOR_GROUP,
    VOICE,
)

KEY = "key"
LO_KEY = "lokey"
HI_KEY = "hikey"
LO_VEL = "lovel"
HI_VEL = "hivel"
PITCH_KEYCENTER = "pitch_keycenter"
TRANSPOSE = "transpose"
NOTE_OFFSET = "note_offset"
OCTAVE_OFFSET = "octave_offset"
DEFAULT_PATH = "default_path"
SAMPLE = "sample"
OFFSET = "offset"
END = "end"
LOOP_START = "loop_start"
LOOP_END = "loop_end"
DIRECTION = "direction"
LOOP_MODE = "loop_mode"

KEY_OPCODES = [KEY, LO_KEY, HI_KEY, PITCH_KEYCENTER]
TRANSPOSE_OPCODES = [TRANSPOSE, NOTE_OFFSET, OCTAVE_OFFSET]
SAMPLE_EDIT_OPCODES = [OFFSET, END, LOOP_START, LOOP_END]

RENAME_OPCODE_ALIASES = {
    "loopmode": LOOP_MODE,
    "loopstart": LOOP_START,
    "loopend": LOOP_END,
    "pitch": "tune",
}

REGION = {
    "header": "region",
    "obsidian_tag": SAMPLER_ZONE["tag"],
    "obsidian_opcode_rename": {
        PITCH_KEYCENTER: "root_key",
        LO_KEY: "minimum_key",
        HI_KEY: "maximum_key",
        DIRECTION: "playback_direction",
        SAMPLE: "file_name",
        LOOP_MODE: "loop_mode",
    },
    "obsidian_opcode_remove": [
        KEY,
        TRANSPOSE,
        OCTAVE_OFFSET,
        NOTE_OFFSET,
        DEFAULT_PATH,
        OFFSET,
        END,
        LOOP_START,
        LOOP_END,
    ],
    "opcodes": [
        KEY,
        LO_KEY,
        HI_KEY,
        TRANSPOSE,
        DEFAULT_PATH,
        "direction",
        OFFSET,
        END,
        LOOP_MODE,
        LOOP_START,
        LOOP_END,
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
        LO_VEL,
        HI_VEL,
    ],
    "opcodes": [LO_VEL, HI_VEL, "tune", "pitch"],
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
