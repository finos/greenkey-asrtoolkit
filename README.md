# GreenKey Automatic Speech Recognition (ASR) Toolkit

<img src="https://github.com/finos-voice/greenkey-voice-sdk/raw/master/logo/greenkey-logo.png" width="100" />

---

## The GreenKey ASRToolkit provides tools for file conversion and ASR corpora organization. These are intended to simplify the workflow for building, customizing, and analyzing ASR models, useful for scientists, engineers, and other technologists in speech recognition.


### convert_transcript 
```text
usage: convert_transcript [-h] input_file output_file

convert between text file formats

positional arguments:
  input_file   input file
  output_file  output file

optional arguments:
  -h, --help   show this help message and exit
```
This tool allows for easy conversion from STM files to TXT files and back. Other file formats will be added in the near future.

### wer
```text
usage: wer [-h] [--char-level] [--ignore-nsns]
           reference_file transcript_file

Compares a reference and transcript file and calculates word error rate (WER)
between these two files

positional arguments:
  reference_file   reference "truth" file
  transcript_file  transcript possibly containing errors

optional arguments:
  -h, --help       show this help message and exit
  --char-level     calculate character error rate instead of word error rate
  --ignore-nsns    ignore non silence noises like um, uh, etc.
```

### clean_formatting 
```text
usage: clean_formatting input_file1.txt input_file2.txt

remove formatting from text files

```
This script standardizes how abbreviations, numbers, and other formatted text is expressed so that ASR engines can easily use these files as training or testing data. Standardizing the formatting of output is essential for reproducible measurements of ASR accuracy.

### split_audio_file 
```text
usage: split_audio_file [-h] [--target-dir TARGET_DIR] audio_file transcript

Split an audio file using valid segments from a transcript file. For this
utility, transcript files must contain start/stop times.

positional arguments:
  audio_file            input audio file
  transcript            transcript

optional arguments:
  -h, --help            show this help message and exit
  --target-dir TARGET_DIR
                        Path to target directory
```

### prepare_audio_corpora
```text
usage: prepare_audio_corpora [-h] [--target-dir TARGET_DIR]
                             corpora [corpora ...]

Copy and organize specified corpora into a target directory. Training,
testing, and development sets will be created automatically if not already
defined.

positional arguments:
  corpora               Name of one or more directories in directory this
                        script is run

optional arguments:
  -h, --help            show this help message and exit
  --target-dir TARGET_DIR
                        Path to target directory
```
This script scrapes a list of directories for paired STM and SPH files. If `train`, `test`, and `dev` folders are present, these labels are used for the output folder. By default, a target directory of 'input-data' will be created. Note that filenames with hyphens will be sanitized to underscores and that audio files will be forced to single channel, 16 kHz, signed PCM format. If two channels are present, only the first will be used.

### degrade_audio_file 
```text
usage: degrade_audio_file input_file1.wav input_file2.wav

Degrade audio files to 8 kHz format similar to G711 codec
```
This script reduces audio quality of input audio files so that acoustic models can learn features from telephony with the G711 codec.

### Requirements

- Python 3.6 with `pip`

### Dependencies

To ensure your dependencies install correctly, we recommend that you upgrade your `setuptools` before proceeding further.

```sh
pip install --upgrade setuptools
```

Now you are ready to install with `pip`.

```sh
pip install -e .
```

## Contributing

### Code of Conduct

Please make sure you read and observe our [Code of Conduct].

### Pull Request process

1. Fork it
1. Create your feature branch (`git checkout -b feature/fooBar`)
1. Commit your changes (`git commit -am 'Add some fooBar'`)
1. Push to the branch (`git push origin feature/fooBar`)
1. Create a new Pull Request

## Authors

Original authors:

- [Matthew Goldey](https://github.com/mgoldey)

For all others who have aided this project, please see the [list of contributors].

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details.

<!-- Markdown link & img defs -->
