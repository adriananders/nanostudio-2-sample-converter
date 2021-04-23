import os
from unittest import TestCase
from nanostudio_2_sample_converter.formats.sfz.utils.audio import (
    Audio,
    add_loop_to_audio_data,
)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

FILE_PATH = os.path.join(DIR_PATH, "./wave_chunk_parser_extended/files/tone.wav")


class TestAudio(TestCase):
    def test_crop_audio(self):
        start = 10000
        end = 20000
        audio = Audio(FILE_PATH)
        self.assertEqual(len(audio.audio.raw_data), 75172)
        audio.crop_audio(start, end)
        self.assertEqual(len(audio.audio.raw_data), 20000)


class TestLoop(TestCase):
    def test_add_loop_to_audio_data(self):
        with open(FILE_PATH, "rb") as file:
            result = add_loop_to_audio_data(file, 10000, 20000)
        expected_smpl_binary = (
            b"smpl<\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x93X\x00\x00<\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10'\x00\x00 N\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        self.assertEqual(result[75216:], expected_smpl_binary)
        self.assertEqual(len(result), 75284)
