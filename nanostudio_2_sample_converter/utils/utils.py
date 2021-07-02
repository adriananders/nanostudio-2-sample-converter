import argparse
from nanostudio_2_sample_converter.utils.exceptions import (
    ConverterSourceException,
    ConverterSourceExtensionException,
    ConverterUnsupportedSourceFormatException,
    ConverterDestinationException,
    ConverterUnsupportedDestinationFormatException,
)

SUPPORTED_SOURCE_FORMATS = ["sfz"]
SUPPORTED_DESTINATION_FORMATS = ["obs"]


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="source file path - required")
    parser.add_argument("--destination", help="destination directory path - required")
    parser.add_argument(
        "--format", help="destination file format - optional - defaults to obs"
    )
    return parser


def validate_args(args):
    source = args.source
    if not source:
        raise ConverterSourceException(
            "Error! Please specify required --source argument."
        )
    source_format_index = source.rfind(".")
    if source_format_index == -1:
        raise ConverterSourceExtensionException(
            "Error! Source path does not contain an extension. Must specify a specific source file."
        )
    source_format = source[source_format_index + 1 :].lower()
    if source_format not in SUPPORTED_SOURCE_FORMATS:
        error = (
            "Error! Source format "
            + source_format
            + " is not supported. Currently supported formats: "
            + ",".join(SUPPORTED_SOURCE_FORMATS)
            + "."
        )
        raise ConverterUnsupportedSourceFormatException(error)
    destination = args.destination
    if not destination:
        raise ConverterDestinationException(
            "Error! Please specify required --destination argument."
        )
    destination_format = args.format.lower() if args.format else "obs"
    if destination_format not in SUPPORTED_DESTINATION_FORMATS:
        error = (
            "Error! Destination format "
            + destination_format
            + " is not supported. Currently supported formats: "
            + ",".join(SUPPORTED_DESTINATION_FORMATS)
            + "."
        )
        raise ConverterUnsupportedDestinationFormatException(error)
    return True
