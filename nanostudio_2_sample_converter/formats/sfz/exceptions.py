# pylint: disable=unnecessary-pass
class SfzDestinationException(Exception):
    """
    Indicates the sfz destination path is invalid.
    """

    pass


class SfzUserCancelOperation(Exception):
    """
    Indicates the user has cancelled the Sfz conversion operation.
    """

    pass


class SfzDoesNotExistException(Exception):
    """
    Indicates the sfz file specified does not exist.
    """

    pass


class AudioFileDoesNotExistException(Exception):
    """
    Indicates the audio file specified does not exist.
    """

    pass


class FfmpegNotInstalledException(Exception):
    """
    Indicates that ffmpeg is not installed.
    """

    pass


class DirectoryExistsException(Exception):
    """
    Indicates that specified destination already exists.
    """

    pass
