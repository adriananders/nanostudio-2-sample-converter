# pylint: disable=too-many-instance-attributes, too-many-arguments
from typing import List
from parameterized import parameterized
import pytest
from pytest import raises
import numpy as np
from wave_chunk_parser.exceptions import (
    InvalidHeaderException,
)
from wave_chunk_parser.chunks import (
    FormatChunk,
    DataChunk,
    WaveFormat,
)
from nanostudio_2_sample_converter.formats.sfz.utils.wave_chunk_parser_extended.chunks_extended import (
    SampleChunk,
    RiffChunkExtended,
)


class TestSampleChunk:
    @parameterized.expand(
        [
            (
                "./files/tone.wav",
                75216,
                0,
                0,
                22675,
                60,
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                37485,
                37585,
                0,
                0,
            )
        ]
    )
    def test_read_valid_format_chunk(
        self,
        file_name: str,
        chunk_offset: int,
        expected_manufacturer: int,
        expected_product: int,
        expected_sample_period: int,
        expected_midi_unity_note: int,
        expected_midi_pitch_fraction: int,
        expected_smpte_format: int,
        expected_smpte_offset: int,
        expected_number_of_sample_loops: int,
        expected_sampler_data: int,
        expected_first_cue_point_id: int,
        expected_first_loop_type: int,
        expected_first_loop_start: int,
        expected_first_loop_end: int,
        expected_first_loop_fraction: int,
        expected_first_loop_play_count: int,
    ):
        """
        Valid sample chunks can be read from a file.
        """

        # Arrange

        with open(file_name, "rb") as file:

            # Act

            chunk: SampleChunk = SampleChunk.from_file(file, chunk_offset)

            # Assert

            assert chunk is not None
            assert chunk.get_name == b"smpl"
            assert chunk.manufacturer == expected_manufacturer
            assert chunk.product == expected_product
            assert chunk.sample_period == expected_sample_period
            assert chunk.midi_unity_note == expected_midi_unity_note
            assert chunk.midi_pitch_fraction == expected_midi_pitch_fraction
            assert chunk.smpte_format == expected_smpte_format
            assert chunk.smpte_offset == expected_smpte_offset
            assert chunk.number_of_sample_loops == expected_number_of_sample_loops
            assert chunk.sampler_data == expected_sampler_data
            assert chunk.first_cue_point_id == expected_first_cue_point_id
            assert chunk.first_loop_type == expected_first_loop_type
            assert chunk.first_loop_start == expected_first_loop_start
            assert chunk.first_loop_end == expected_first_loop_end
            assert chunk.first_loop_fraction == expected_first_loop_fraction
            assert chunk.first_loop_play_count == expected_first_loop_play_count

    @parameterized.expand(
        [
            (
                "./files/tone.wav",
                36,
            )
        ]
    )
    def test_read_wrong_chunk(self, file_name: str, chunk_offset: int):
        """
        An appropriate error is raised if the wrong chunk is read.
        """

        # Arrange

        with open(file_name, "rb") as file:

            # Act

            with raises(InvalidHeaderException) as context:
                SampleChunk.from_file(file, chunk_offset)

                # Assert

                assert context.exception in "Sample chunk must start with fmt"

    @parameterized.expand(
        [
            (
                0,
                0,
                22675,
                60,
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                37485,
                37585,
                0,
                0,
                b"smpl<\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x93X\x00\x00<\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00m\x92\x00\x00"
                b"\xd1\x92\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
            )
        ]
    )
    def test_encode_chunk(
        self,
        manufacturer: int,
        product: int,
        sample_period: int,
        midi_unity_note: int,
        midi_pitch_fraction: int,
        smpte_format: int,
        smpte_offset: int,
        number_of_sample_loops: int,
        sampler_data: int,
        first_cue_point_id: int,
        first_loop_type: int,
        first_loop_start: int,
        first_loop_end: int,
        first_loop_fraction: int,
        first_loop_play_count: int,
        expected_bytes: bytes,
    ):
        """
        The sample chunk encodes correctly.
        """

        # Arrage

        chunk = SampleChunk(
            manufacturer,
            product,
            sample_period,
            midi_unity_note,
            midi_pitch_fraction,
            smpte_format,
            smpte_offset,
            number_of_sample_loops,
            sampler_data,
            first_cue_point_id,
            first_loop_type,
            first_loop_start,
            first_loop_end,
            first_loop_fraction,
            first_loop_play_count,
        )

        # Act

        converted = chunk.to_bytes()

        # Assert

        assert converted == expected_bytes


class TestRiffChunkExtended:
    @parameterized.expand(
        [
            ("./files/tone.wav", [b"fmt ", b"data", b"smpl"]),
        ]
    )
    def test_read_valid_wave(self, file_name: str, expected_chunks: List[str]):
        """
        Read valid wave files with smpl chunk.
        """

        # Arrange

        with open(file_name, "rb") as file:

            # Act

            chunk = RiffChunkExtended.from_file(file)

            # Assert

            assert chunk is not None
            assert chunk.get_name == b"WAVE"
            assert chunk.sub_chunks is not None
            for expected_chunk in expected_chunks:
                assert expected_chunk in chunk.sub_chunks

    def test_encode_wave(self):
        """
        A WAVE file with smpl chunk can be encoded.
        """

        # Arrange

        chunks = {}

        chunks[RiffChunkExtended.CHUNK_FORMAT] = FormatChunk(
            WaveFormat.PCM, False, 1, 44100, 16
        )

        chunks[RiffChunkExtended.CHUNK_SAMPLE] = SampleChunk(
            0,
            0,
            22675,
            60,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            37485,
            37585,
            0,
            0,
        )

        with open("./files/tone.wav", "rb") as in_file:
            samples = np.memmap(
                in_file, dtype=np.dtype("<i2"), mode="c", shape=(37586, 1), offset=44
            )

        chunks[RiffChunkExtended.CHUNK_DATA] = DataChunk(samples)

        riff = RiffChunkExtended(chunks)

        with open("./files/tone.wav", "rb") as expected_file:
            expected_blob = expected_file.read()

        #  Act

        blob = riff.to_bytes()

        # Assert

        assert blob is not None
        assert blob == expected_blob


pytest.main()
