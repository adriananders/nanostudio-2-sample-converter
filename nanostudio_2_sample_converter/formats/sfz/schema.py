REGION = {
    "header": "region",
    "opcodes": ["lokey", "hikey", "pitch_keycenter", "sample"],
}

GROUP = {
    "header": "group",
    "opcodes": ["sample", "loop_start", "loop_end", "loop_mode"],
}

GLOBAL = {"header": "global", "opcodes": []}

CONTROL = {
    "header": "control",
    "opcodes": ["octave_offset"],
}

SFZ = [REGION, GROUP, GLOBAL, CONTROL]
HEADER = "header"

HEADERS = [header[HEADER] for header in SFZ]
