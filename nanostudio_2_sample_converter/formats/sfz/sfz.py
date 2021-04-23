"""
Sfz conversion functions
Note: schema taken from sfzformat.com
"""
import os
import shutil
from pathlib import Path
from lxml import etree as ET
from pretty_midi.utilities import key_name_to_key_number
from nanostudio_2_sample_converter.formats.sfz.schema import (
    SFZ,
    HEADERS,
    OPCODES,
    HEADERS_XPATH,
    KEY_OPCODES,
    TRANSPOSE_OPCODES,
    RENAME_OPCODE_ALIASES,
    KEY,
    LO_KEY,
    HI_KEY,
    PITCH_KEYCENTER,
    TRANSPOSE,
    NOTE_OFFSET,
    OCTAVE_OFFSET,
    DEFAULT_PATH,
    SAMPLE,
    OFFSET,
    END,
    LOOP_START,
    LOOP_END,
    SAMPLE_EDIT_OPCODES,
)
from nanostudio_2_sample_converter.formats.sfz.exceptions import (
    SfzDestinationException,
    SfzUserCancelOperation,
    SfzDoesNotExistException,
    AudioFileDoesNotExistException,
)
from nanostudio_2_sample_converter.formats.sfz.utils.audio import (
    Audio,
    add_loop_to_audio_data,
    write_audio_file,
)


class Sfz:
    def __init__(self, sfz_file_path, destination_directory, extension="obs"):
        self.sfz_file_path = sfz_file_path
        if not os.path.exists(self.sfz_file_path):
            raise SfzDoesNotExistException(f"{sfz_file_path} does not exist.")
        self.sfz_parent_path = Path(sfz_file_path).parent.absolute()
        self.patch_name = (
            ".".join(os.path.basename(self.sfz_file_path).split(".")[:-1])
            + f".{extension}"
        )
        if not destination_directory:
            raise SfzDestinationException(
                "Destination directory path must be specified."
            )
        self.destination_directory = os.path.join(
            destination_directory, self.patch_name
        )
        self.__create_destination_directory()
        self.sfz_xml = self.__sfz_to_xml()
        self.__copy_audio_files()
        self.__convert_audio_files_to_ns_audio_files()
        self.__update_sample_to_basename()

    @staticmethod
    def __remove_comment_filter(line):
        return not line.startswith("//")

    @staticmethod
    def __convert_list_to_string_single_space(line_list):
        line_string = " ".join(line_list)
        return " ".join(line_string.split())

    @staticmethod
    def __encapsulate_headers_as_xml_elements(sfz_string):
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

    @staticmethod
    def __remove_unsupported_headers(sfz_xml):
        for element in sfz_xml:
            if element.tag not in HEADERS:
                sfz_xml.remove(element)

    @staticmethod
    def __pop_xml_attributes(element, attribute_list):
        for attribute in attribute_list:
            element.attrib.pop(attribute)

    def __remove_unsupported_opcodes(self, sfz_xml):
        for element in sfz_xml:
            invalid_opcodes = self.__find_invalid_opcodes(element, OPCODES)
            self.__pop_xml_attributes(element, invalid_opcodes)

    def __get_opcodes(self, tag):
        return [header for header in SFZ if tag == header["header"]][0]["opcodes"]

    @staticmethod
    def __find_invalid_opcodes(element, opcodes):
        return {
            key: value for (key, value) in element.attrib.items() if key not in opcodes
        }

    @staticmethod
    def __find_valid_opcodes(element, opcodes):
        return {key: value for (key, value) in element.attrib.items() if key in opcodes}

    @staticmethod
    def __merge_dictionaries(dictionary_1, dictionary_2):
        return {**dictionary_1, **dictionary_2}

    @staticmethod
    def __update_xml_attributes(xml, attributes):
        for (key, value) in attributes.items():
            xml.attrib[key] = value

    def __distribute_opcodes_down_to_correct_level(
        self, sfz_xml, distribution_attributes
    ):
        merged_attributes = self.__merge_dictionaries(
            sfz_xml.attrib, distribution_attributes
        )
        self.__update_xml_attributes(sfz_xml, merged_attributes)
        header_opcodes = self.__get_opcodes(sfz_xml.tag)
        invalid_header_opcodes = self.__find_invalid_opcodes(sfz_xml, header_opcodes)
        if len(sfz_xml):
            invalid_opcodes = self.__find_invalid_opcodes(sfz_xml, header_opcodes)
            self.__pop_xml_attributes(sfz_xml, invalid_opcodes)
            for child in sfz_xml:
                self.__distribute_opcodes_down_to_correct_level(
                    child, invalid_header_opcodes
                )

    def __aggregate_opcodes_up_to_correct_level(self, sfz_xml):
        for index, xpath in enumerate(HEADERS_XPATH):
            header = HEADERS[index]
            header_opcodes = self.__get_opcodes(header)
            for element in sfz_xml.findall(xpath):
                invalid_header_opcodes = self.__find_invalid_opcodes(
                    element, header_opcodes
                )
                parent = element.getparent()
                if parent:
                    merged_attributes = self.__merge_dictionaries(
                        parent.attrib, invalid_header_opcodes
                    )
                    self.__update_xml_attributes(parent, merged_attributes)
                invalid_opcodes = self.__find_invalid_opcodes(element, header_opcodes)
                self.__pop_xml_attributes(element, invalid_opcodes)

    @staticmethod
    def __flatten_xml_child(xml, index):
        for child in xml[index]:
            xml.append(child)
        xml.remove(xml[index])

    @staticmethod
    def __fill_missing_parent_headers(sfz_xml):
        for header in HEADERS:
            header_count = sum(1 for _ in sfz_xml.iter(header))
            if not header_count:
                new_node = ET.Element(header)
                children = sfz_xml[:]
                for child in children:
                    new_node.append(child)
                sfz_xml.append(new_node)

    def __move_headers_into_hierachies(self, sfz_xml):
        for header in HEADERS:
            parent_index = -1
            index_offset = 0
            for index, elem in enumerate(sfz_xml):
                if elem.tag == header:
                    if parent_index >= 0:
                        sfz_xml[parent_index].append(elem)
                        index_offset = index_offset + 1
                else:
                    parent_index = index - index_offset
        self.__fill_missing_parent_headers(sfz_xml)
        return sfz_xml[0]  # drops "root" parent element

    @staticmethod
    def __convert_key_string_to_key_number(string):
        if string[0].isdigit():
            return string
        return key_name_to_key_number(string)

    def __convert_opcodes_key_string_to_key_number(self, sfz_xml):
        for header in HEADERS:
            for element in sfz_xml.iter(header):
                key_opcodes = self.__find_valid_opcodes(element, KEY_OPCODES)
                key_opcodes = {
                    key: self.__convert_key_string_to_key_number(value)
                    for (key, value) in key_opcodes.items()
                }
                self.__update_xml_attributes(element, key_opcodes)

    def __consolidate_opcode_aliases(self, sfz_xml):
        for header in HEADERS:
            for element in sfz_xml.iter(header):
                old_name_opcodes = self.__find_valid_opcodes(
                    element, RENAME_OPCODE_ALIASES.keys()
                )
                new_name_opcodes = {
                    RENAME_OPCODE_ALIASES[key]: value
                    for (key, value) in old_name_opcodes.items()
                }
                self.__update_xml_attributes(element, new_name_opcodes)
                self.__pop_xml_attributes(element, old_name_opcodes)

    def __convert_key_to_lo_hi_pitch_keycenter(self, sfz_xml):
        for element in sfz_xml.iter():
            key_opcodes = self.__find_valid_opcodes(element, KEY_OPCODES)
            if key_opcodes:
                if KEY in key_opcodes:
                    key_value = key_opcodes[KEY]
                    replacement_opcodes = {}
                    if not LO_KEY in key_opcodes:
                        replacement_opcodes[LO_KEY] = key_value
                    if not HI_KEY in key_opcodes:
                        replacement_opcodes[HI_KEY] = key_value
                    if not PITCH_KEYCENTER in key_opcodes:
                        replacement_opcodes[PITCH_KEYCENTER] = key_value
                    self.__update_xml_attributes(element, replacement_opcodes)
                    self.__pop_xml_attributes(element, {KEY: key_opcodes[KEY]})

    def __apply_transpose_to_pitch_keys(self, sfz_xml):
        for element in sfz_xml.iter():
            transpose_opcodes = self.__find_valid_opcodes(element, TRANSPOSE_OPCODES)
            key_opcodes = self.__find_valid_opcodes(element, KEY)
            if transpose_opcodes and key_opcodes:
                transpose_amount = 0
                if transpose_opcodes[OCTAVE_OFFSET]:
                    transpose_amount = transpose_opcodes[OCTAVE_OFFSET] * 12
                if transpose_opcodes[NOTE_OFFSET]:
                    transpose_amount += transpose_opcodes[NOTE_OFFSET]
                if transpose_opcodes[TRANSPOSE]:
                    transpose_amount += transpose_opcodes[TRANSPOSE]
                key_opcodes = {
                    key: value + transpose_amount
                    for (key, value) in key_opcodes.items()
                }
            self.__update_xml_attributes(element, key_opcodes)
            self.__pop_xml_attributes(element, transpose_opcodes)

    def __append_default_path_to_sample_opcodes(self, sfz_xml):
        for element in sfz_xml.iter():
            sample_opcode = self.__find_valid_opcodes(element, [SAMPLE])
            default_path_opcode = self.__find_valid_opcodes(element, [DEFAULT_PATH])
            if sample_opcode and default_path_opcode:
                sample = {
                    SAMPLE: default_path_opcode[DEFAULT_PATH] + sample_opcode[SAMPLE]
                }
                self.__update_xml_attributes(element, sample)
                self.__pop_xml_attributes(element, default_path_opcode)

    def __input_yes_no_binary_choice(self, input_question, yes_response, no_response):
        print(input_question)
        response = input()
        if response.lower() == "y":
            yes_response()
        elif response.lower() == "n":
            no_response()
        else:
            self.__input_yes_no_binary_choice(
                "Input not recognized, please try again", yes_response, no_response
            )

    def __raise_user_cancel(self):
        raise SfzUserCancelOperation("SFZ conversion operation cancelled.")

    def __pass(self):
        pass

    def __create_destination_directory(self):
        os.makedirs(self.destination_directory)

    def __copy_audio_files(self):
        for element in self.sfz_xml.iter():
            sample_opcode = self.__find_valid_opcodes(element, [SAMPLE])
            if sample_opcode:
                sample_path = sample_opcode[SAMPLE].replace("\\", "/")
                if not os.path.exists(sample_path):
                    sample_path = os.path.join(self.sfz_parent_path, sample_path)
                    if not os.path.exists(sample_path):
                        raise AudioFileDoesNotExistException(
                            f"{sample_path} does not exist."
                        )
                file_name = os.path.basename(sample_path)
                destination_file = os.path.join(self.destination_directory, file_name)
                print(f"Copying {sample_path} to {destination_file}")
                if os.path.exists(destination_file):
                    question = f"{destination_file} already exists. Do you wish to overwrite? (y/n)"
                    self.__input_yes_no_binary_choice(
                        question, self.__pass, self.__raise_user_cancel
                    )
                shutil.copyfile(sample_path, destination_file)
                sample_opcode[SAMPLE] = destination_file
                self.__update_xml_attributes(element, sample_opcode)

    def __convert_audio_files_to_ns_audio_files(self):
        for element in self.sfz_xml.iter():
            sample_opcode = self.__find_valid_opcodes(element, [SAMPLE])
            edit_opcodes = self.__find_valid_opcodes(element, SAMPLE_EDIT_OPCODES)
            if sample_opcode:
                file_path = sample_opcode[SAMPLE]
                extension = file_path.split(".")[-1]
                if extension.lower() != "wav" and (
                    LOOP_START in edit_opcodes.keys() or LOOP_END in edit_opcodes.keys()
                ):
                    print(f"Converting {file_path} to wav to handle loop editing")
                    destination = ".".join(file_path.split(".")[:-1]) + ".wav"
                    Audio(file_path).export(destination)
                    os.remove(file_path)
                    file_path = destination
                    sample_opcode[SAMPLE] = file_path
                offset = None
                end = None
                if OFFSET in edit_opcodes.keys():
                    offset = int(edit_opcodes[OFFSET])
                if END in edit_opcodes.keys():
                    end = int(edit_opcodes[END])
                if offset or end:
                    audio = Audio(file_path)
                    audio.crop_audio(offset, end)
                    audio.export(file_path)
                if LOOP_START in edit_opcodes.keys() or LOOP_END in edit_opcodes.keys():
                    loop_start = (
                        int(edit_opcodes[LOOP_START]) - offset
                        if offset
                        else int(edit_opcodes[LOOP_START])
                    )
                    loop_end = (
                        int(edit_opcodes[LOOP_END]) - offset
                        if offset
                        else int(edit_opcodes[LOOP_END])
                    )
                    with open(file_path, "rb") as file:
                        data = add_loop_to_audio_data(file, loop_start, loop_end)
                    write_audio_file(data, file_path)
                self.__update_xml_attributes(element, sample_opcode)
                self.__pop_xml_attributes(element, edit_opcodes)

    def __update_sample_to_basename(self):
        for element in self.sfz_xml.iter():
            sample_opcode = self.__find_valid_opcodes(element, [SAMPLE])
            if sample_opcode:
                sample_opcode[SAMPLE] = os.path.basename(sample_opcode[SAMPLE])
                self.__update_xml_attributes(element, sample_opcode)

    def __sfz_to_xml(self):
        with open(self.sfz_file_path, "r") as reader:
            sfz_lines = reader.readlines()
        sfz_string = Sfz.__convert_list_to_string_single_space(
            list(filter(Sfz.__remove_comment_filter, sfz_lines))
        )
        sfz_string = (
            "<root>" + Sfz.__encapsulate_headers_as_xml_elements(sfz_string) + "</root>"
        )
        sfz_xml = ET.fromstring(sfz_string)
        self.__remove_unsupported_headers(sfz_xml)
        self.__remove_unsupported_opcodes(sfz_xml)
        self.__convert_opcodes_key_string_to_key_number(sfz_xml)
        self.__consolidate_opcode_aliases(sfz_xml)
        self.__convert_key_to_lo_hi_pitch_keycenter(sfz_xml)
        sfz_xml = self.__move_headers_into_hierachies(sfz_xml)
        self.__distribute_opcodes_down_to_correct_level(sfz_xml, {})
        self.__aggregate_opcodes_up_to_correct_level(sfz_xml)
        self.__apply_transpose_to_pitch_keys(sfz_xml)
        self.__append_default_path_to_sample_opcodes(sfz_xml)
        return sfz_xml
