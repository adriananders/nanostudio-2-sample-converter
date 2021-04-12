"""
Obsidian patch functions
Note: schema taken from sfzformat.com
"""
from lxml import etree as ET
from pretty_midi.utilities import key_name_to_key_number
from nanostudio_2_sample_converter.formats.sfz.schema import (
    SFZ,
    HEADERS,
    OPCODES,
    HEADERS_XPATH,
    KEY_OPCODES,
    RENAME_OPCODE_ALIASES,
)


class Sfz:
    def __init__(self):
        self.schema = SFZ
        self.headers = HEADERS
        self.headers_xpath = HEADERS_XPATH
        self.opcodes = OPCODES
        self.key_opcodes = KEY_OPCODES
        self.rename_opcode_aliases = RENAME_OPCODE_ALIASES

    @staticmethod
    def remove_comment_filter(line):
        return not line.startswith("//")

    @staticmethod
    def convert_list_to_string_single_space(line_list):
        line_string = " ".join(line_list)
        return " ".join(line_string.split())

    @staticmethod
    def encapsulate_headers_as_xml_elements(sfz_string):
        sfz_list = sfz_string.split()
        sfz_range = [
            {"start": index}
            for index, statement in enumerate(sfz_list)
            if statement.startswith("<") and statement.endswith(">")
        ]
        for index, block in enumerate(sfz_range):
            block["end"] = (
                sfz_range[index + 1]["start"]
                if index + 1 < len(sfz_range)
                else len(sfz_list)
            )
        block_sfz_list = []
        for block in sfz_range:
            block_items = sfz_list[block["start"] : block["end"]]
            block_items[0] = block_items[0].replace(">", "")
            block_items = [
                item.replace("=", '="') + '"' if "=" in item else item
                for item in block_items
            ]
            block_sfz_list.append(" ".join(block_items) + "/>")
        return "".join(block_sfz_list)

    def remove_unsupported_headers(self, sfz_xml):
        for element in sfz_xml:
            if element.tag not in self.headers:
                sfz_xml.remove(element)

    @staticmethod
    def pop_xml_attributes(element, attribute_list):
        for attribute in attribute_list:
            element.attrib.pop(attribute)

    def remove_unsupported_opcodes(self, sfz_xml):
        for element in sfz_xml:
            invalid_opcodes = self.find_invalid_opcodes(element, self.opcodes)
            self.pop_xml_attributes(element, invalid_opcodes)

    def get_opcodes(self, tag):
        return [header for header in self.schema if tag == header["header"]][0][
            "opcodes"
        ]

    @staticmethod
    def find_invalid_opcodes(element, opcodes):
        return {
            key: value for (key, value) in element.attrib.items() if key not in opcodes
        }

    @staticmethod
    def find_valid_opcodes(element, opcodes):
        return {key: value for (key, value) in element.attrib.items() if key in opcodes}

    @staticmethod
    def merge_dictionaries(dictionary_1, dictionary_2):
        return {**dictionary_1, **dictionary_2}

    @staticmethod
    def update_xml_attributes(xml, attributes):
        for (key, value) in attributes.items():
            xml.attrib[key] = value

    def distribute_opcodes_down_to_correct_level(
        self, sfz_xml, distribution_attributes
    ):
        merged_attributes = self.merge_dictionaries(
            sfz_xml.attrib, distribution_attributes
        )
        self.update_xml_attributes(sfz_xml, merged_attributes)
        header_opcodes = self.get_opcodes(sfz_xml.tag)
        invalid_header_opcodes = self.find_invalid_opcodes(sfz_xml, header_opcodes)
        if len(sfz_xml):
            invalid_opcodes = self.find_invalid_opcodes(sfz_xml, header_opcodes)
            self.pop_xml_attributes(sfz_xml, invalid_opcodes)
            for child in sfz_xml:
                self.distribute_opcodes_down_to_correct_level(
                    child, invalid_header_opcodes
                )

    def aggregate_opcodes_up_to_correct_level(self, sfz_xml):
        for index, xpath in enumerate(self.headers_xpath):
            header = self.headers[index]
            header_opcodes = self.get_opcodes(header)
            for element in sfz_xml.findall(xpath):
                invalid_header_opcodes = self.find_invalid_opcodes(
                    element, header_opcodes
                )
                parent = element.getparent()
                if parent:
                    merged_attributes = self.merge_dictionaries(
                        parent.attrib, invalid_header_opcodes
                    )
                    self.update_xml_attributes(parent, merged_attributes)
                invalid_opcodes = self.find_invalid_opcodes(element, header_opcodes)
                self.pop_xml_attributes(element, invalid_opcodes)

    @staticmethod
    def flatten_xml_child(xml, index):
        for child in xml[index]:
            xml.append(child)
        xml.remove(xml[index])

    def fill_missing_parent_headers(self, sfz_xml):
        for header in self.headers:
            header_count = sum(1 for _ in sfz_xml.iter(header))
            if not header_count:
                new_node = ET.Element(header)
                children = sfz_xml[:]
                for child in children:
                    new_node.append(child)
                sfz_xml.append(new_node)

    def move_headers_into_hierachies(self, sfz_xml):
        for header in self.headers:
            parent_index = -1
            index_offset = 0
            for index, elem in enumerate(sfz_xml):
                if elem.tag == header:
                    if parent_index >= 0:
                        sfz_xml[parent_index].append(elem)
                        index_offset = index_offset + 1
                else:
                    parent_index = index - index_offset
        self.fill_missing_parent_headers(sfz_xml)
        return sfz_xml[0]  # drops "root" parent element

    @staticmethod
    def convert_key_string_to_key_number(string):
        if string[0].isdigit():
            return string
        return key_name_to_key_number(string)

    def convert_opcodes_key_string_to_key_number(self, sfz_xml):
        for header in HEADERS:
            for element in sfz_xml.iter(header):
                key_opcodes = self.find_valid_opcodes(element, self.key_opcodes)
                key_opcodes = {
                    key: self.convert_key_string_to_key_number(value)
                    for (key, value) in key_opcodes.items()
                }
                self.update_xml_attributes(element, key_opcodes)

    def consolidate_opcode_aliases(self, sfz_xml):
        for header in HEADERS:
            for element in sfz_xml.iter(header):
                old_name_opcodes = self.find_valid_opcodes(
                    element, self.rename_opcode_aliases.keys()
                )
                new_name_opcodes = {
                    self.rename_opcode_aliases[key]: value
                    for (key, value) in old_name_opcodes.items()
                }
                self.update_xml_attributes(element, new_name_opcodes)
                self.pop_xml_attributes(element, old_name_opcodes)

    def sfz_to_xml(self, sfz_file_path):
        with open(sfz_file_path, "r") as reader:
            sfz_lines = reader.readlines()
        sfz_string = Sfz.convert_list_to_string_single_space(
            list(filter(Sfz.remove_comment_filter, sfz_lines))
        )
        sfz_string = (
            "<root>" + Sfz.encapsulate_headers_as_xml_elements(sfz_string) + "</root>"
        )
        sfz_xml = ET.fromstring(sfz_string)
        self.remove_unsupported_headers(sfz_xml)
        self.remove_unsupported_opcodes(sfz_xml)
        self.convert_opcodes_key_string_to_key_number(sfz_xml)
        self.consolidate_opcode_aliases(sfz_xml)
        sfz_xml = self.move_headers_into_hierachies(sfz_xml)
        self.distribute_opcodes_down_to_correct_level(sfz_xml, {})
        self.aggregate_opcodes_up_to_correct_level(sfz_xml)
        return sfz_xml
