from nanostudio_2_sample_converter.formats.nanostudio_2.obsidian.schema import (
    SAMPLER_ZONE,
    OSCILLATOR_GROUP,
    VOICE,
)

KEY_OPCODES = ["key", "lokey", "hikey", "pitch_keycenter"]
RENAME_OPCODE_ALIASES = {
    "loopmode": "loop_mode",
    "loopstart": "loop_start",
    "loopend": "loop_end",
}

REGION = {
    "header": "region",
    "obsidian_tag": SAMPLER_ZONE["tag"],
    "obsidian_opcode_rename": {
        "pitch_keycenter": "root_key",
        "lokey": "minimum_key",
        "hikey": "maximum_key",
        "direction": "playback_direction",
        "sample": "file_name",
    },
    "obsidian_opcode_remove": [
        "key",
        "transpose",
        "default_path",
        "offset",
        "end",
        "octave_offset",
    ],
    "opcodes": [
        "key",
        "lokey",
        "hikey",
        "tune",
        "transpose",
        "default_path",
        "direction",
        "offset",
        "end",
        "loop_mode",
        "loop_start",
        "loop_end",
        "loopmode",
        "loopstart",
        "loopend",
        "sample",
        "pitch_keycenter",
        "octave_offset",
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
    "opcodes": [
        "lovel",
        "hivel",
    ],
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
