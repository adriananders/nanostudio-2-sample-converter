from unittest import TestCase
from nanostudio_2_sample_converter.utils.utils import create_parser, create_args
from nanostudio_2_sample_converter.utils.exceptions import (
    ConverterSourceException,
    ConverterSourceExtensionException,
    ConverterUnsupportedSourceFormatException,
    ConverterDestinationException,
    ConverterUnsupportedDestinationFormatException,
)


class TestValidateArgs(TestCase):
    def setUp(self):
        self.parser = create_parser()

    def test_source_not_provided(self):
        args = self.parser.parse_args([])
        with self.assertRaises(ConverterSourceException) as context:
            create_args(args)
        self.assertEqual(
            "Error! Please specify required --source argument.",
            context.exception.args[0],
        )

    def test_source_no_extension(self):
        args = self.parser.parse_args(["--source", "test"])
        with self.assertRaises(ConverterSourceExtensionException) as context:
            create_args(args)
        self.assertEqual(
            "Error! Source path does not contain an extension. Must specify a specific source file.",
            context.exception.args[0],
        )

    def test_source_unsupported_extension(self):
        args = self.parser.parse_args(["--source", "test.tst"])
        with self.assertRaises(ConverterUnsupportedSourceFormatException) as context:
            create_args(args)
        self.assertEqual(
            "Error! Source format tst is not supported. Currently supported formats: sfz.",
            context.exception.args[0],
        )

    def test_destination_not_provided(self):
        args = self.parser.parse_args(["--source", "test.SFZ"])
        with self.assertRaises(ConverterDestinationException) as context:
            create_args(args)
        self.assertEqual(
            "Error! Please specify required --destination argument.",
            context.exception.args[0],
        )

    def test_destination_unsupported_extension(self):
        args = self.parser.parse_args(
            [
                "--source",
                "test.sfz",
                "--destination",
                "destinationDir",
                "--format",
                "blh",
            ]
        )
        with self.assertRaises(
            ConverterUnsupportedDestinationFormatException
        ) as context:
            create_args(args)
        self.assertEqual(
            "Error! Destination format blh is not supported. Currently supported formats: obs.",
            context.exception.args[0],
        )

    def test_valid_args_no_format(self):
        args = self.parser.parse_args(
            ["--source", "test.sfz", "--destination", "destinationDir"]
        )
        response = create_args(args)
        self.assertEqual(
            {
                "destination": "destinationDir",
                "destination_format": "obs",
                "source": "test.sfz",
            },
            response,
        )

    def test_valid_args_with_format(self):
        args = self.parser.parse_args(
            [
                "--source",
                "test.sfz",
                "--destination",
                "destinationDir",
                "--format",
                "obs",
            ]
        )
        response = create_args(args)
        self.assertEqual(
            {
                "destination": "destinationDir",
                "destination_format": "obs",
                "source": "test.sfz",
            },
            response,
        )
