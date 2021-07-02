# pylint: disable=unnecessary-pass
class ConverterSourceException(Exception):
    """
    Indicates the source argument is missing.
    """

    pass


class ConverterSourceExtensionException(Exception):
    """
    Indicates the source argument's extension is missing.
    """

    pass


class ConverterUnsupportedSourceFormatException(Exception):
    """
    Indicates the source argument's extension is not supported currently.
    """

    pass


class ConverterDestinationException(Exception):
    """
    Indicates the destination argument is missing.
    """

    pass


class ConverterUnsupportedDestinationFormatException(Exception):
    """
    Indicates the format argument is not supported currently.
    """

    pass
