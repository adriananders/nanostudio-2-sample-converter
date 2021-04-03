"""
Obsidian patch functions
Note: schema taken from sfzformat.com
"""
import xml.etree.ElementTree as ET
from nanostudio_2_sample_converter.formats.sfz.schema import SFZ, HEADERS


class Sfz:
    def __init__(self):
        self.schema = SFZ
        self.headers = HEADERS

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

    def remove_invalid_headers(self, sfz_xml):
        for opcode in sfz_xml:
            if opcode.tag not in self.headers:
                sfz_xml.remove(opcode)

    @staticmethod
    def move_headers_into_hierachies(sfz_xml):
        for header in HEADERS:
            parent_index = -1
            child_element_list = []
            element_removal_list = []
            for index, elem in enumerate(sfz_xml):
                if elem.tag == header:
                    child_element_list.append(elem)
                    element_removal_list.append(elem)
                else:
                    for child in child_element_list:
                        sfz_xml[parent_index].append(child)
                    parent_index = index
                    child_element_list = []
            for child in element_removal_list:
                sfz_xml.remove(child)
        for child in sfz_xml[0]:
            sfz_xml.append(child)
        sfz_xml.remove(sfz_xml[0])
        for header in HEADERS:
            header_count = 0
            for child in sfz_xml.iter(header):
                header_count += 1
            if not header_count:
                new_node = ET.Element(header)
                children = sfz_xml[:]
                for child in children:
                    new_node.append(child)
                    sfz_xml.remove(child)
                sfz_xml.append(new_node)
        return sfz_xml[0]

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
        self.remove_invalid_headers(sfz_xml)
        sfz_xml = self.move_headers_into_hierachies(sfz_xml)
        return sfz_xml
