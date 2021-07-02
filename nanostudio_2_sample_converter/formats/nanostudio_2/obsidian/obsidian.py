"""
Obsidian patch functions
Note: no public documentation exists for Obsidian instrument in NanoStudio 2.
"""
import xml.dom.minidom
from lxml import etree as ET
from nanostudio_2_sample_converter.formats.nanostudio_2.obsidian.schema import (
    ROOT,
    VOICE,
    OSCILLATOR_GROUP,
    OSCILLATOR,
    ANALOG,
    WAVETABLE,
    WAVETABLE_TABLE,
    PHASE_DISTORTION,
    FREQUENCY_MODULATION,
    FM_OPERATOR_GROUP,
    FM_OPERATOR,
    FM_CONNECTIONS,
    FM_OPERATOR_CONNECTION,
    NANO_SAW,
    NOISE,
    SAMPLER,
    SAMPLER_ZONE_GROUP,
    SAMPLER_ZONE,
    FILTER_GROUP,
    FILTER,
    ENVELOPE_GROUP,
    ENVELOPE,
    LFO_GROUP,
    LFO,
    MOD_MATRIX,
    CONTROL,
    UI,
    UI_CONTROL,
    EFFECTS,
    MULTI_EFEECTS,
    DELAY,
    REVERB,
    MACROS,
)
from nanostudio_2_sample_converter.formats.nanostudio_2.utils import (
    create_xml,
    create_numeric_suffix,
)


class Obsidian:
    def __init__(self, oscillator_group=None):
        self.xml = Obsidian.create_default_xml(self, oscillator_group)
        self.xml_string = Obsidian.create_output_xml(self.xml)

    @staticmethod
    def create_oscillator_group(
        split_3_low_1=None, split_3_low_2=None, sampler_list=None
    ):
        analog = create_xml(schema=ANALOG)
        wavetable_table = create_xml(schema=WAVETABLE_TABLE)
        wavetable = create_xml(schema=WAVETABLE, children=[wavetable_table])
        phase_distortion = create_xml(schema=PHASE_DISTORTION)
        operator_list = [
            create_xml(schema=FM_OPERATOR, tag_suffix=create_numeric_suffix(o))
            for o in list(range(1, 4))
        ]
        operator = create_xml(schema=FM_OPERATOR_GROUP, children=operator_list)
        operator_connection_suffix_list = [
            "11",
            "12",
            "13",
            "22",
            "23",
            "1O",
            "2O",
            "3O",
        ]
        operator_connection_list = []
        for connection in operator_connection_suffix_list:
            envelope = create_xml(schema=ENVELOPE)
            operator_connection_point = create_xml(
                schema=FM_OPERATOR_CONNECTION,
                tag_suffix=connection,
                children=[envelope],
            )
            operator_connection_list.append(operator_connection_point)
        operator_connection = create_xml(
            schema=FM_CONNECTIONS, children=operator_connection_list
        )
        frequency_modulation = create_xml(
            schema=FREQUENCY_MODULATION, children=[operator, operator_connection]
        )
        nano_saw = create_xml(schema=NANO_SAW)
        noise = create_xml(schema=NOISE)
        oscillator_range = list(range(0, 3))
        oscillator_list = []
        for oscillator_id in oscillator_range:
            settings = {}
            zones = []
            if sampler_list and oscillator_id < len(sampler_list):
                zones_settings_list = sampler_list[oscillator_id]
                for zone_settings in zones_settings_list:
                    sampler_zone = create_xml(
                        schema=SAMPLER_ZONE, settings=zone_settings
                    )
                    zones.append(sampler_zone)
            else:
                zones = None
            zone_group = create_xml(
                schema=SAMPLER_ZONE_GROUP, children=zones if zones else None
            )
            sampler = create_xml(
                schema=SAMPLER, settings=settings, children=[zone_group]
            )
            oscillator = create_xml(
                schema=OSCILLATOR,
                tag_suffix=create_numeric_suffix(oscillator_id),
                children=[
                    analog,
                    wavetable,
                    phase_distortion,
                    frequency_modulation,
                    nano_saw,
                    noise,
                    sampler,
                ],
                copy=True,
            )
            oscillator_list.append(oscillator)
        settings = {}
        if split_3_low_1:
            settings["split_3_low_1"] = split_3_low_1
        if split_3_low_2:
            settings["split_3_low_2"] = split_3_low_2
        return create_xml(
            schema=OSCILLATOR_GROUP, settings=settings, children=oscillator_list
        )

    def create_default_xml(self, oscillator_group):
        oscillator_group = (
            oscillator_group if oscillator_group else self.create_oscillator_group()
        )
        filter_list = [
            create_xml(schema=FILTER, tag_suffix=create_numeric_suffix(f))
            for f in list(range(1, 4))
        ]
        filter_group = create_xml(schema=FILTER_GROUP, children=filter_list)
        envelope_list = ["A", "F", "P", "4", "5"]
        envelope_list = [
            create_xml(schema=ENVELOPE, tag_suffix=e) for e in envelope_list
        ]
        envelope_group = create_xml(schema=ENVELOPE_GROUP, children=envelope_list)
        lfo_list = [
            create_xml(schema=LFO, tag_suffix=create_numeric_suffix(lfo))
            for lfo in list(range(1, 6))
        ]
        lfo_group = create_xml(schema=LFO_GROUP, children=lfo_list)
        control_list = [
            create_xml(schema=CONTROL, tag_suffix=create_numeric_suffix(c, 2))
            for c in list(range(0, 24))
        ]
        ui_control_list = [
            create_xml(schema=UI_CONTROL, tag_suffix=create_numeric_suffix(c, 2))
            for c in list(range(0, 10))
        ]
        user_interface = create_xml(schema=UI, children=ui_control_list)
        mod_matrix = create_xml(
            schema=MOD_MATRIX, children=control_list + [user_interface]
        )
        voice = create_xml(
            schema=VOICE,
            children=[
                oscillator_group,
                filter_group,
                envelope_group,
                lfo_group,
                mod_matrix,
            ],
        )
        multi_effects = create_xml(schema=MULTI_EFEECTS)
        delay = create_xml(schema=DELAY)
        reverb = create_xml(schema=REVERB)
        effects = create_xml(schema=EFFECTS, children=[multi_effects, delay, reverb])
        macros = create_xml(schema=MACROS)
        return create_xml(schema=ROOT, children=[voice, effects, macros])

    @staticmethod
    def create_output_xml(xml_data):
        xml_string = ET.tostring(xml_data)
        pretty_xml_string = xml.dom.minidom.parseString(xml_string).toprettyxml()
        return pretty_xml_string

    def import_package_xml(self, xml_path):
        self.xml = ET.parse(xml_path)
        self.xml_string = self.create_output_xml(self.xml)
