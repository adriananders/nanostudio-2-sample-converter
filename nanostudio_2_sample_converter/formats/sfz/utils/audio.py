# pylint: disable=protected-access
from pydub.audio_segment import AudioSegment
from nanostudio_2_sample_converter.formats.sfz.utils.wave_chunk_parser_extended.chunks_extended import (
    RiffChunkExtended,
    SampleChunk,
)
from nanostudio_2_sample_converter.formats.sfz.exceptions import (
    FfmpegNotInstalledException,
)

MANUFACTURER_ID = 0
PRODUCT_ID = 0
MIDI_UNITY_NOTE = 60
MIDI_PITCH_FRACTION = 0
SMPTE_FORMAT = 0
SMPTE_OFFSET = 0
NUMBER_OF_SAMPLE_LOOPS = 1
SAMPLER_DATA = 0
CUE_POINT_ID = 0
LOOP_TYPE = 0
LOOP_FRACTION = 0
LOOP_PLAY_COUNT = 0


class Audio:
    def __init__(self, path):
        self.path = path
        self.format = path.split(".")[-1]
        try:
            self.audio = AudioSegment.from_file(path, self.format)
        except FileNotFoundError as exception:
            if exception.filename == "ffprobe":
                raise FfmpegNotInstalledException(
                    "ffmpeg or libav is required to read audio from non-wave files. "
                    "Please download and install from ffmpeg.org or libav.org then try again."
                ) from exception
        self.sample_rate = self.audio.frame_rate

    def crop_audio(self, start=0, end=None):
        samples = self.audio.get_array_of_samples()
        samples = samples[start:end]
        self.audio = self.audio._spawn(samples)

    def export(self, destination):
        destination_format = destination.split(".")[-1]
        self.audio.export(destination, format=destination_format)


def add_loop_to_audio_data(file, loop_start, loop_end):
    riff_chunk = RiffChunkExtended.from_file(file)
    format_chunk = riff_chunk.sub_chunks[RiffChunkExtended.CHUNK_FORMAT]
    data_chunk = riff_chunk.sub_chunks[RiffChunkExtended.CHUNK_DATA]
    sample_rate = format_chunk.sample_rate
    sample_period = int((1 / sample_rate) * 1000000000)
    sample_chunk = SampleChunk(
        MANUFACTURER_ID,
        PRODUCT_ID,
        sample_period,
        MIDI_UNITY_NOTE,
        MIDI_PITCH_FRACTION,
        SMPTE_FORMAT,
        SMPTE_OFFSET,
        NUMBER_OF_SAMPLE_LOOPS,
        SAMPLER_DATA,
        CUE_POINT_ID,
        LOOP_TYPE,
        loop_start,
        loop_end,
        LOOP_FRACTION,
        LOOP_PLAY_COUNT,
    )
    chunks = {
        RiffChunkExtended.CHUNK_FORMAT: format_chunk,
        RiffChunkExtended.CHUNK_DATA: data_chunk,
        RiffChunkExtended.CHUNK_SAMPLE: sample_chunk,
    }
    return RiffChunkExtended(chunks).to_bytes()


def write_audio_file(data, file_path):
    with open(file_path, "wb") as file:
        file.write(data)
