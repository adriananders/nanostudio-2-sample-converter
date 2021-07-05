# pylint: disable=too-many-instance-attributes, too-many-nested-blocks
"""
Sfz conversion functions
Note: schema taken from sfzformat.com
"""
import os
import re
import shutil
from copy import deepcopy
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
    LO_VEL,
    HI_VEL,
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
    GROUP,
    CONTROL,
    REGION,
    DIRECTION,
    LOOP_MODE,
)
from nanostudio_2_sample_converter.formats.sfz.exceptions import (
    SfzDestinationException,
    SfzUserCancelOperation,
    SfzDoesNotExistException,
    AudioFileDoesNotExistException,
    DirectoryExistsException,
)
from nanostudio_2_sample_converter.formats.sfz.utils.audio import (
    Audio,
    add_loop_to_audio_data,
    write_audio_file,
    check_if_audio_has_loops,
)
from nanostudio_2_sample_converter.formats.nanostudio_2.obsidian.obsidian import (
    Obsidian,
)


class Sfz:
    def __init__(self, sfz_file_path, destination_directory, extension):
        self.extension = extension
        self.max_velocity_zones = 3
        self.sfz_file_path = sfz_file_path
        if not os.path.exists(self.sfz_file_path):
            raise SfzDoesNotExistException(f"{sfz_file_path} does not exist.")
        self.sfz_parent_path = Path(sfz_file_path).parent.absolute()
        self.patch_name = (
            ".".join(os.path.basename(self.sfz_file_path).split(".")[:-1])
            + f".{self.extension}"
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
        self.ns2_xml = self.__xml_to_obs()

    @staticmethod
    def __remove_comment_filter(line):
        return not line.startswith("//")

    @staticmethod
    def __convert_list_to_string_single_space(line_list):
        line_string = " ".join(line_list)
        return " ".join(line_string.split())

    @staticmethod
    def __split_attribute_strings(sfz_string, sfz_list):
        for character in sfz_string:
            if character == "<" or sfz_list[-1][-1] == ">":
                sfz_list.append(character)
            elif character == "=":
                prior_list_item = sfz_list[-1]
                prior_space_index = prior_list_item.rfind(" ", 0)
                if prior_space_index != -1:
                    attribute_key_string = prior_list_item[prior_space_index + 1 :]
                    sfz_list[-1] = prior_list_item[:prior_space_index]
                    sfz_list.append(attribute_key_string)
                sfz_list[-1] += character
            else:
                sfz_list[-1] += character
        return sfz_list

    def __encapsulate_headers_as_xml_elements(self, sfz_string):
        sfz_list = self.__split_attribute_strings(sfz_string, [])
        sfz_list = [item.strip() for item in sfz_list]
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
                if parent is not None:
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
        compiled_regex = re.compile("([a-zA-Z#]+)([0-9]+)")
        key_tuple = compiled_regex.match(string).groups()
        return str(
            key_name_to_key_number(key_tuple[0].upper()) + (int(key_tuple[1]) * 12)
        )

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

    def __add_high_low_velocities(self, sfz_xml):
        for element in sfz_xml.iter():
            if element.tag == GROUP["header"]:
                velocity_opcodes = self.__find_valid_opcodes(element, [LO_VEL, HI_VEL])
                if LO_VEL not in velocity_opcodes.keys():
                    velocity_opcodes[LO_VEL] = "0"
                if HI_VEL not in velocity_opcodes.keys():
                    velocity_opcodes[HI_VEL] = "127"
                self.__update_xml_attributes(element, velocity_opcodes)

    @staticmethod
    def is_ranges_overlap(min_max_1, min_max_2):
        range_1 = range(int(min_max_1[0]), int(min_max_1[1]) + 1)
        range_2 = range(int(min_max_2[0]), int(min_max_2[1]) + 1)
        return len(list(set(range_1) & set(range_2))) > 0

    def __remove_velocity_overlap(self, sfz_xml):
        for element in sfz_xml.iter():
            if element.tag == GROUP["header"]:
                velocity = self.__find_valid_opcodes(element, [LO_VEL, HI_VEL])
                for element_compared in sfz_xml.iter():
                    velocity_compared = self.__find_valid_opcodes(
                        element_compared, [LO_VEL, HI_VEL]
                    )
                    if (
                        element_compared.tag == GROUP["header"]
                        and element_compared != element
                        and self.is_ranges_overlap(
                            [velocity[LO_VEL], velocity[HI_VEL]],
                            [velocity_compared[LO_VEL], velocity_compared[HI_VEL]],
                        )
                    ):
                        element_compared.getparent().remove(element_compared)

    def __reduce_to_three_max_velocity_zones(self, sfz_xml):
        velocity_zone_running_count = 0
        for element in sfz_xml.iter():
            if element.tag == GROUP["header"]:
                if velocity_zone_running_count > self.max_velocity_zones - 1:
                    element.getparent().remove(element)
                velocity_zone_running_count += 1

    def __fill_to_min_max_velocity(self, sfz_xml):
        velocity_zone_running_count = 0
        header = GROUP["header"]
        velocity_zone_count = sfz_xml.xpath(f"count(//{header})") - 1
        for element in sfz_xml.iter():
            if element.tag == header:
                velocity = self.__find_valid_opcodes(element, [LO_VEL, HI_VEL])
                if velocity_zone_running_count == 0 and velocity[LO_VEL] != "0":
                    velocity[LO_VEL] = "0"
                if (
                    velocity_zone_running_count == velocity_zone_count
                    and velocity[HI_VEL] != "127"
                ):
                    velocity[HI_VEL] = "127"
                self.__update_xml_attributes(element, velocity)
                velocity_zone_running_count += 1

    # Required because NS2 has a hard limit of 32 zones per velocity layer. This is common between obs and slt.
    @staticmethod
    def __reduce_regions(sfz_xml):
        region = REGION["header"]
        group = GROUP["header"]
        max_ns2_samples = 32
        for element in sfz_xml.iter():
            if element.tag == group:
                region_count = element.xpath(f"count(.//{region})")
                if region_count > max_ns2_samples:
                    region_index = 1
                    for child in element.iter():
                        if child.tag == region:
                            if region_index > max_ns2_samples:
                                element.remove(child)
                            region_index += 1

    @staticmethod
    def __remove_control_between_groups_and_regions(sfz_xml):
        control = CONTROL["header"]
        group = GROUP["header"]
        for element in sfz_xml.iter():
            if element.tag == control:
                group_count = element.xpath(f"count(.//{group})")
                if group_count == 0:
                    parent = element.getparent()
                    children = element.getchildren()
                    for child in children:
                        parent.append(child)
                    parent.remove(element)

    @staticmethod
    def __get_lo_vel(elem):
        return int(elem.get(LO_VEL))

    @staticmethod
    def __get_hi_vel(elem):
        return int(elem.get(HI_VEL))

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
        if os.path.isdir(self.destination_directory):
            raise DirectoryExistsException(
                f"{self.destination_directory} already exists. Please delete and try again."
            )
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
                if extension.lower() == "wav":
                    with open(file_path, "rb") as file:
                        if check_if_audio_has_loops(file):
                            sample_opcode[LOOP_MODE] = "loop_continuous"
                self.__update_xml_attributes(element, sample_opcode)
                self.__pop_xml_attributes(element, edit_opcodes)

    def __update_sample_to_basename(self):
        for element in self.sfz_xml.iter():
            sample_opcode = self.__find_valid_opcodes(element, [SAMPLE])
            if sample_opcode:
                sample_opcode[SAMPLE] = os.path.basename(sample_opcode[SAMPLE])
                self.__update_xml_attributes(element, sample_opcode)

    def __sfz_to_xml(self):
        with open(self.sfz_file_path, "r", encoding="utf-8", errors="ignore") as reader:
            sfz_lines = reader.readlines()
        sfz_string = self.__convert_list_to_string_single_space(
            list(filter(self.__remove_comment_filter, sfz_lines))
        )
        sfz_string = (
            "<root>"
            + self.__encapsulate_headers_as_xml_elements(sfz_string)
            + "</root>"
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
        self.__add_high_low_velocities(sfz_xml)
        self.__remove_velocity_overlap(sfz_xml)
        self.__reduce_to_three_max_velocity_zones(sfz_xml)
        self.__fill_to_min_max_velocity(sfz_xml)
        self.__remove_control_between_groups_and_regions(sfz_xml)
        self.__reduce_regions(sfz_xml)
        return sfz_xml

    def __get_split_3_level_1(self):
        header = GROUP["header"]
        for element in self.sfz_xml.iter():
            if element.tag == header:
                velocity = self.__find_valid_opcodes(element, [HI_VEL])
                return str(int(velocity[HI_VEL]) / 127)
        return None

    def __get_split_3_level_2(self, split_3_level_1):
        velocity_zone_running_count = 0
        header = GROUP["header"]
        velocity_zone_count = self.sfz_xml.xpath(f"count(//{header})") - 1
        for element in self.sfz_xml.iter():
            if element.tag == header:
                velocity = self.__find_valid_opcodes(element, [LO_VEL])
                if velocity_zone_running_count == velocity_zone_count:
                    split_3_level_2 = str(int(velocity[LO_VEL]) / 127)
                    return (
                        split_3_level_2
                        if split_3_level_2 > split_3_level_1
                        else split_3_level_1
                    )
        return None

    @staticmethod
    def __convert_element_to_settings_dictionary(element, schema):
        attributes = deepcopy(element.attrib)
        if DIRECTION in attributes.keys():
            attributes[DIRECTION] = attributes[DIRECTION].capitalize()
        if LOOP_MODE in attributes.keys():
            attributes[LOOP_MODE] = (
                "On" if attributes[LOOP_MODE] == "loop_continuous" else "Off"
            )
        settings_dictionary = {}
        for (key, value) in attributes.items():
            opcode_rename = schema["obsidian_opcode_rename"]
            if key in opcode_rename.keys():
                settings_dictionary[opcode_rename[key]] = value
        return settings_dictionary

    def __create_sampler_list(self):
        header = GROUP["header"]
        sampler_list = []
        for element in self.sfz_xml.iter():
            if element.tag == header:
                sampler_zones = []
                for region in list(element):
                    zone_settings = self.__convert_element_to_settings_dictionary(
                        element=region, schema=REGION
                    )
                    sampler_zones.append(zone_settings)
                sampler_list.append(sampler_zones)
        return sampler_list

    def __xml_to_obs(self):
        split_3_level_1 = self.__get_split_3_level_1()
        split_3_level_2 = self.__get_split_3_level_2(split_3_level_1)

        sampler_list = self.__create_sampler_list()
        oscillator_group = Obsidian().create_oscillator_group(
            split_3_level_1=split_3_level_1,
            split_3_level_2=split_3_level_2,
            sampler_list=sampler_list,
        )
        obsidian = Obsidian(oscillator_group)
        return obsidian.xml_string

    def export(self):
        destination_file_path = os.path.join(
            self.destination_directory, "Package." + self.extension
        )
        with open(destination_file_path, "w") as destination_file:
            destination_file.write(self.ns2_xml)
