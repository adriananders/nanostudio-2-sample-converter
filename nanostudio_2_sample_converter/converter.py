from nanostudio_2_sample_converter.formats.sfz.sfz import Sfz
from nanostudio_2_sample_converter.utils.utils import create_parser, create_args


def main():
    parser = create_parser()
    args = create_args(parser.parse_args())
    if args:
        convert(args)


def convert(args):
    sample_patch = Sfz(args["source"], args["destination"], args["destination_format"])
    sample_patch.export()
    print("Success! Sample patch has been saved to " + args['destination'] + ".")
