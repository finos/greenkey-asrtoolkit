#!/usr/bin/env python
"""
Creates asrtoolkit
"""
from setuptools import find_packages, setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

with open("README.md") as f:
    long_description = f.read()

setup(
    name="asrtoolkit",
    version="0.2.0",
    description=
    "The GreenKey ASRToolkit provides tools for automatic speech recognition (ASR) file conversion and corpora organization.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/finos-voice/greenkey-asrtoolkit",
    author="Matthew Goldey",
    author_email="mgoldey@greenkeytech.com",
    install_requires=required,
    extras_require={"dev": ["pandas"]},
    keywords="asr speech recognition greenkey word error rate",
    entry_points={
        "console_scripts": [
            "convert_transcript = asrtoolkit.convert_transcript:main",
            "clean_formatting=asrtoolkit.clean_formatting:main",
            "prepare_audio_corpora=asrtoolkit.prepare_audio_corpora:main",
            "degrade_audio_file=asrtoolkit.degrade_audio_file:main",
            "wer=asrtoolkit.wer:main",
            "split_audio_file=asrtoolkit.split_audio_file:main",
            "combine_audio_files=asrtoolkit.combine_audio_files:main",
            "extract_excel_spreadsheets=asrtoolkit.extract_excel_spreadsheets:main",
        ]
    },
    license="Apache v2",
    packages=find_packages(),
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
