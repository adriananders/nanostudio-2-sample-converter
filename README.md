# nanostudio-2-sample-converter
Python 3 SFZ to NanoStudio 2 patch converter compatible with MacOS and Windows.

## Installation
1. Install dependencies

    ### Python
    #### MacOS
    Follow Instructions to install [Homebrew](https://brew.sh/).
    ```brew update && brew install python```
    #### Windows
    1. Download Python installer from [python.org](https://www.python.org/).
    2. Install. Be sure to select "Add Python to path" during installation as well as disable path length limit.
   
    ### ffmpeg
    #### MacOS
    ```brew install ffmpeg```
    #### Windows
    1. Download the latest Windows binary from [ffmpeg.org](http://ffmpeg.org/).
    2. Unzip and move contents of bin to "C:\Program Files\ffmpeg".
    3. Add ffmpeg to path.
        1. Open Start Menu.
        2. Type "Edit Environment Variables".
        3. Click on "Edit Environment Variables For Your Account".
        4. In Edit Environment Variables, you will see two boxes. In system variables box find and select "path" variables.
        5. Click "Edit".
        6. In window pop up, click "New".
        7. Type "C:\Program Files\ffmpeg", then click OK twice to save your changes.
    

2. Install ns2samplconv command
    1. Clone or download nanostudio-2-sample-converter package from GitHub. Unzip if downloaded.
    2. In Terminal (MacOS) or Command Prompt (Windows) navigate to the nanostudio-2-sample-converter package folder.
    3. Run ```python setup.py install```. This will install ns2samplconv to your path and be accessible as a terminal command.
    4. Restart Terminal or Command Prompt before first usage.
    
## Usage
```ns2samplconv --source path/of/sfz/patch --destination path/of/destination/directory```

```ns2samplconv --help```

## Notes

- Currently, only [SFZ](https://sfzformat.com/) is supported as a source format. Unlikely that other formats will be supported due to the ubiquity of converters to SFZ. Here are some options to convert to SFZ:
    ### Commercial
    1. [Awave Studio](https://www.fmjsoft.com/awavestudio.html#main) - ***Recommended*** - Windows Only, although works fine under Wine for MacOS (<=10.14).
    2. [Extreme Sample Converter](https://extranslator.com/index.php?page=exsc) - Windows Only, have not tested under Wine for MacOS.
    ### Freeware or Open Source
    1. [EXS2SFZ](https://www.bjoernbojahr.de/exs2sfz.html) - Windows & MacOS - [EXS24](https://support.apple.com/en-us/HT211115) to SFZ.
    2. [TX2SFZ](https://www.kvraudio.com/product/awave-studio-by-fmj-software/news) - Windows Only, have not tested under Wine for MacOS. [TX16Wx](https://www.tx16wx.com/) to SFZ.
    3. [AudioKit - exs2sfz script](https://github.com/AudioKit/SamplerDemo/blob/master/Sounds/exs2sfz.py) - Python module
    4. [sfZed](http://audio.clockbeat.com/sfZed.html) - Windows Only - SFZ Editor that can also convert [SF2](https://en.wikipedia.org/wiki/SoundFont).
    5. [FreePats-Tools](https://github.com/freepats/freepats-tools) - Python module - createSFZ.py converts SF2 to SFZ.


- Currently only NanoStudio 2's [Obsidian](https://www.blipinteractive.co.uk/nanostudio2/user-manual/Obsidian.html) is supported as a destination format. Support for [Slate](https://www.blipinteractive.co.uk/nanostudio2/user-manual/Slate.html) is on the roadmap, but there is no planned date for this release.

- Currently the converter only maps the SFZ samples and attributes directly tied to the samples (such as looping), but does not try to convert other SFZ attributes such as envelope and filter settings. This is for several reasons:
    1. Prioritization of a fast release of basic features over infrequently used features of the format.
    2. Many of the [opcode](https://sfzformat.com/opcodes/) settings of SFZ don't translate neatly to NanoStudio 2's filters and envelopes. It would have required a much larger amount of development for a minimal lift in conversion results.
    3. Reduce the surface area for bugs and other defects due to the semi-structured nature of SFZ format itself.
    
- Python ffmpeg is required for audio file manipulation to insert loop points into the SFZ audio files since some SFZ files specify loop points via the file itself rather than embedded within the audio file.
- Due to inherent limitations of NanoStudio 2, truncation of some patch details may occur:
    1. Velocity Layers greater than 3 will be truncated down to the first three in order to fit within the 3 layer limit of NanoStudio 2 patches.
    2. Sample key maps that are greater than 32 will be truncated down to the first 32 in order to fit within the 32 zone limit of NanoStudio 2 patches.
    
- As mentioned in the MIT license, this software is provided as-is without warranty. Although care is taken to prevent damage to the original SFZ and audio files, please back up originals to a separate location prior to use. In addition it is recommended you specify a destination location not currently in use for other purposes to minimize the chance of data loss.
