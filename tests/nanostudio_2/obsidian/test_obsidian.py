import os
from unittest import TestCase
from nanostudio_2_sample_converter.formats.nanostudio_2.obsidian.obsidian import (
    Obsidian,
)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class TestObisidian(TestCase):
    def test_init(self):
        obsidian = Obsidian().xml_string
        with open(
            os.path.join(DIR_PATH, "./sample-files/Package.obs"), "r"
        ) as sample_default:
            expected = sample_default.read()
            self.assertEqual(expected, obsidian)
