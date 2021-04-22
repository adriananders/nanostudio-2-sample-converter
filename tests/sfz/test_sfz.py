from unittest import TestCase
from unittest.mock import patch
import xml.etree.ElementTree as ET
import xml.dom.minidom
import os
from nanostudio_2_sample_converter.formats.sfz.sfz import (
    Sfz,
)
from nanostudio_2_sample_converter.formats.sfz.exceptions import (
    SfzDestinationException,
    SfzUserCancelOperation,
    SfzDoesNotExistException,
)
from tests.sfz.manifest import EXAMPLES

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
SFZ_PATH = os.path.join(DIR_PATH, "sample-files/examples/sfz/example_1.sfz")


class TestSfz(TestCase):
    def test_sfz_does_not_exist(self):
        with self.assertRaises(SfzDoesNotExistException) as context:
            Sfz("test_does_not_exist", None)
        self.assertEqual(
            "test_does_not_exist does not exist.", context.exception.args[0]
        )

    def test_destination_is_empty(self):
        with self.assertRaises(SfzDestinationException) as context:
            Sfz(SFZ_PATH, None)
        self.assertEqual(
            "Destination directory path must be specified.", context.exception.args[0]
        )

    def test_destination_is_equal_to_sfz_parent(self):
        sfz_parent = os.path.join(DIR_PATH, "sample-files/examples/sfz/")
        with self.assertRaises(SfzDestinationException) as context:
            Sfz(SFZ_PATH, sfz_parent)
        self.assertIn("must be different than the SFZ", context.exception.args[0])

    def test_destination_existing_path_user_cancelled(self):
        user_input = ["n"]
        with patch("builtins.input", side_effect=user_input):
            with self.assertRaises(SfzUserCancelOperation) as context:
                Sfz(SFZ_PATH, DIR_PATH)
            self.assertEqual(
                "SFZ conversion operation cancelled.", context.exception.args[0]
            )

    def test_destination_existing_path_user_accepted(self):
        user_input = ["y"]
        with patch("builtins.input", side_effect=user_input):
            sfz = Sfz(SFZ_PATH, DIR_PATH)
            self.assertEqual(DIR_PATH, sfz.destination_directory)

    @patch(
        "nanostudio_2_sample_converter.formats.sfz.sfz.Sfz._Sfz__create_destination_directory"
    )
    def test_sfz_to_xml(self, mock_create_destination_directory):
        mock_create_destination_directory.return_value = None
        for example in EXAMPLES:
            xml_path = os.path.join(DIR_PATH, example["xml"])
            sfz_path = os.path.join(DIR_PATH, example["sfz"])
            with open(xml_path) as sample_file:
                sample = sample_file.read()
                sample = " ".join(sample.split())
            sample_xml = ET.fromstring(sample)
            sample_xml_string = ET.tostring(sample_xml).decode("utf-8")
            sample_xml_string = sample_xml_string.replace("> <", "><")
            sample_xml_pretty = xml.dom.minidom.parseString(
                sample_xml_string
            ).toprettyxml()
            sfz = Sfz(sfz_path, "test_destination")
            sfz_xml_string = ET.tostring(sfz.sfz_xml).decode("utf-8")
            sfz_xml_pretty = xml.dom.minidom.parseString(sfz_xml_string).toprettyxml()
            self.assertTrue(mock_create_destination_directory.called)
            self.assertEqual(sample_xml_pretty, sfz_xml_pretty)
