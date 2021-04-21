import pytest
from nanostudio_2_sample_converter.formats.nanostudio_2.obsidian.obsidian import (
    Obsidian,
)


class TestObisidian:
    def test_init(self):
        obsidian = Obsidian().xml_string
        with open("./sample-files/Package.obs", "r") as sample_default:
            expected = sample_default.read()
            assert expected == obsidian


pytest.main()
