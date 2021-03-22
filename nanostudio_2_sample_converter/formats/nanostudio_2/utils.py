"""
NanoStudio 2 Utility functions
"""
import xml.etree.ElementTree as ET


def coalesce_parameter(settings, key, default_value):
    return settings[key] if settings and settings[key] else default_value


def set_xml_attribute(element, attribute, settings, key, default_value):
    element.set(attribute, coalesce_parameter(settings, key, default_value))


def create_xml(schema, tag_suffix="", settings=None, children=None):
    tag = schema["tag"] + tag_suffix
    default_settings = schema["default_settings"]
    element = ET.Element(tag)
    for default_setting in default_settings:
        set_xml_attribute(
            element=element,
            attribute=default_setting["attribute"],
            settings=settings,
            key=default_setting["key"],
            default_value=default_setting["default"],
        )
    if children:
        for child in children:
            element.append(child)
    return element


def create_numeric_suffix(number, fill=1):
    return str(number).zfill(fill)
