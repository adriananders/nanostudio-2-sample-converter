from unittest import TestCase
from unittest.mock import patch
import xml.etree.ElementTree as ET
import xml.dom.minidom
import os
import shutil
from nanostudio_2_sample_converter.formats.sfz.utils.audio import Audio
from nanostudio_2_sample_converter.formats.sfz.sfz import (
    Sfz,
)
from nanostudio_2_sample_converter.formats.sfz.exceptions import (
    SfzDestinationException,
    SfzDoesNotExistException,
)
from tests.sfz.manifest import EXAMPLES

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
SFZ_PATH = os.path.join(DIR_PATH, "sample-files/examples/sfz/example_2.sfz")
DESTINATION_PATH = os.path.join(DIR_PATH, "sample-files/examples/obsidian/actual")
DESTINATION_PATCH = os.path.join(DESTINATION_PATH, "example_2.obs")
DESTINATION_PATCH_PACKAGE = os.path.join(DESTINATION_PATCH, "Package.obs")


class TestSfz(TestCase):
    def test_sfz_does_not_exist(self):
        with self.assertRaises(SfzDoesNotExistException) as context:
            Sfz("test_does_not_exist", None, "obs")
        self.assertEqual(
            "test_does_not_exist does not exist.", context.exception.args[0]
        )

    def test_destination_is_empty(self):
        with self.assertRaises(SfzDestinationException) as context:
            Sfz(SFZ_PATH, None, "obs")
        self.assertEqual(
            "Destination directory path must be specified.", context.exception.args[0]
        )

    @patch(
        "nanostudio_2_sample_converter.formats.sfz.sfz.Sfz._Sfz__create_destination_directory"
    )
    @patch("nanostudio_2_sample_converter.formats.sfz.sfz.Sfz._Sfz__copy_audio_files")
    @patch(
        "nanostudio_2_sample_converter.formats.sfz.sfz.Sfz._Sfz__convert_audio_files_to_ns_audio_files"
    )
    @patch(
        "nanostudio_2_sample_converter.formats.sfz.sfz.Sfz._Sfz__update_sample_to_basename"
    )
    def test_sfz_to_xml(
        self, mock_update, mock_convert, mock_copy, mock_create_destination_directory
    ):
        mock_create_destination_directory.return_value = None
        mock_update.return_value = None
        mock_convert.return_value = None
        mock_copy.return_value = None
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
            sfz = Sfz(sfz_path, "test_destination", "obs")
            sfz_xml_string = ET.tostring(sfz.sfz_xml).decode("utf-8")
            sfz_xml_pretty = xml.dom.minidom.parseString(sfz_xml_string).toprettyxml()
            self.assertTrue(mock_create_destination_directory.called)
            self.assertEqual(sample_xml_pretty, sfz_xml_pretty)

    def test_full(self):
        if os.path.exists(DESTINATION_PATCH):
            shutil.rmtree(DESTINATION_PATCH)
        self.assertFalse(os.path.exists(DESTINATION_PATCH))
        sfz = Sfz(SFZ_PATH, DESTINATION_PATH, "obs")
        self.assertTrue(os.path.exists(DESTINATION_PATCH))
        sfz.export_obs()
        with open(DESTINATION_PATCH_PACKAGE) as sample_file:
            sample = sample_file.read()
            sample = " ".join(sample.split())
        sample_xml = ET.fromstring(sample)
        sample_xml_string = ET.tostring(sample_xml).decode("utf-8")
        sample_xml_string = sample_xml_string.replace("> <", "><")
        sample_xml_pretty = xml.dom.minidom.parseString(
            sample_xml_string
        ).toprettyxml()
        obs_xml_pretty = xml.dom.minidom.parseString(sfz.obs_xml).toprettyxml()
        self.assertEqual(sample_xml_pretty.replace("\n", "").replace("\t", ""),
                         obs_xml_pretty.replace("\n", "").replace("\t", ""))
        files = [
            "mf-taiko-v1.ogg",
            "mf-taiko-v2.wav",
            "mf-taiko-v3.wav",
            "mf-taiko-v4.ogg",
        ]
        files = [os.path.join(DESTINATION_PATCH, file) for file in files]
        files_length = [217984, 80000, 189824, 408960]
        for index, file in enumerate(files):
            self.assertTrue(os.path.exists(file))
            self.assertEqual(
                files_length[index], len(Audio(file).audio.get_array_of_samples())
            )

        with open(files[1], "rb") as open_file:
            expected_smpl_binary = (
                b"smpl<\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x93X\x00\x00<\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000u\x00\x00@\x9c\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00"
            )
            smpl_binary = open_file.read()
            self.assertIn(expected_smpl_binary, smpl_binary)

