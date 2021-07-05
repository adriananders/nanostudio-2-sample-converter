""" NanoStudio 2 Sample Converter setup """
import distutils.cmd
import distutils.log
import os
import subprocess
import setuptools.command.build_py
import setuptools.command.install
from setuptools import setup

sources = ["./setup.py", "./nanostudio_2_sample_converter", "./tests"]


class PylintCommand(distutils.cmd.Command):
    """A custom command to run Pylint on all Python source files."""

    description = "run Pylint on Python source files"
    user_options = [
        # The format is (long option, short option, description).
        ("pylint-rcfile=", None, "path to Pylint config file"),
    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.pylint_rcfile = "standard.rc"

    def finalize_options(self):
        """Post-process options."""
        if self.pylint_rcfile:
            assert os.path.exists(self.pylint_rcfile), (
                "Pylint config file %s does not exist." % self.pylint_rcfile
            )

    def run(self):
        """Run command."""
        command = ["pylint"]
        if self.pylint_rcfile:
            command.append("--rcfile=%s" % self.pylint_rcfile)
        command = command + sources
        self.announce("Running command: %s" % str(command), level=distutils.log.INFO)
        subprocess.check_call(command)


class BlackCommand(distutils.cmd.Command):
    """A custom command to run Python Black on all Python source files."""

    description = "run Black on Python source files"
    user_options = [
        # The format is (long option, short option, description).
        ("black-config=", None, "path to black config file"),
    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.black_config_file = ""

    def finalize_options(self):
        """Post-process options."""
        if self.black_config_file:
            assert os.path.exists(self.black_config_file), (
                "black config file %s does not exist." % self.black_config_file
            )

    def run(self):
        """Run command."""
        command = ["black"]
        if self.black_config_file:
            command.append("--config=%s" % self.black_config_file)
        command = command + sources
        self.announce("Running command: %s" % str(command), level=distutils.log.INFO)
        subprocess.check_call(command)


class BuildPyCommand(setuptools.command.build_py.build_py):
    """Custom build command."""

    def run(self):
        setuptools.command.build_py.build_py.run(self)


class InstallPyCommand(setuptools.command.install.install):
    """Custom install command."""

    def run(self):
        pip_process = ["pip", "install", "-r"]
        subprocess.check_call(pip_process + ["./requirements.txt"])
        subprocess.check_call(pip_process + ["./test_requirements.txt"])
        setuptools.command.install.install.run(self)


setup(
    name="nanostudio_2_sample_converter",
    version="0.0.1",
    packages=[
        "nanostudio_2_sample_converter",
        "nanostudio_2_sample_converter.utils",
        "nanostudio_2_sample_converter.formats",
        "nanostudio_2_sample_converter.formats.nanostudio_2",
        "nanostudio_2_sample_converter.formats.nanostudio_2.obsidian",
        "nanostudio_2_sample_converter.formats.sfz",
        "nanostudio_2_sample_converter.formats.sfz.utils",
        "nanostudio_2_sample_converter.formats.sfz.utils.wave_chunk_parser_extended",
    ],
    python_requires=">=3",
    entry_points={
        "console_scripts": ["ns2samplconv=nanostudio_2_sample_converter.converter:main"]
    },
    cmdclass={
        "format": BlackCommand,
        "build_py": BuildPyCommand,
        "install": InstallPyCommand,
        "lint": PylintCommand,
    },
    test_suite="tests",
    url="https://github.com/adriananders/nanostudio-2-sample-converter",
    license="MIT",
    author="Adrian Anders",
    author_email="realaanders@gmail.com",
    description="sfz -> NanoStudio 2 Obsidian patch converter",
)
