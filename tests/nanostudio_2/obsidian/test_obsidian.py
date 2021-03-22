from nanostudio_2_sample_converter.formats.nanostudio_2.obsidian.obsidian import (
    create_default_obsidian_instrument,
)


class TestObisidian:
    def test_create_default_obsidian_instrument(self):
        obsidian = create_default_obsidian_instrument()
        with open("./obsidian/Package.obs", "r") as sample_default:
            assert sample_default.read() == obsidian
