import xml.etree.ElementTree as ET
import xml.dom.minidom
import pytest
from nanostudio_2_sample_converter.formats.sfz.sfz import (
    Sfz,
)
from tests.sfz.manifest import EXAMPLES


class TestSfz:
    def test_sfz_to_xml(self):
        for example in EXAMPLES:
            with open(example["xml"]) as sample_file:
                sample = sample_file.read()
                sample = " ".join(sample.split())
            sample_xml = ET.fromstring(sample)
            sample_xml_string = ET.tostring(sample_xml).decode("utf-8")
            sample_xml_string = sample_xml_string.replace("> <", "><")
            sample_xml_pretty = xml.dom.minidom.parseString(
                sample_xml_string
            ).toprettyxml()
            sfz_xml = Sfz().sfz_to_xml(example["sfz"])
            sfz_xml_string = ET.tostring(sfz_xml).decode("utf-8")
            sfz_xml_pretty = xml.dom.minidom.parseString(sfz_xml_string).toprettyxml()
            assert sample_xml_pretty == sfz_xml_pretty


pytest.main()
