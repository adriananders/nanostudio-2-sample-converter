from nanostudio_2_sample_converter.formats.sfz.sfz import Sfz
from nanostudio_2_sample_converter.utils.utils import create_parser, validate_args


def main():
    parser = create_parser()
    args = parser.parse_args()
    if validate_args(args):
        convert(args)


def convert(args):
    sample_patch = Sfz(args.source, args.destination, args.destination_format)
    sample_patch.export()
    print("Success! Sample patch has been saved to " + args.destination + ".")
