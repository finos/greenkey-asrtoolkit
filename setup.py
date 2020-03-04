#!/usr/bin/env python
"""
Creates asrtoolkit
"""
from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()


def install_deps():
    """
    Reads requirements.txt and preprocess it
    to be feed into setuptools.

    This is the only possible way (we found)
    how requirements.txt can be reused in setup.py
    using dependencies from private github repositories.

    Links must be appendend by `-{StringWithAtLeastOneNumber}`
    or something like that, so e.g. `-9231` works as well as
    `1.1.0`. This is ignored by the setuptools, but has to be there.

    Warnings:
        to make pip respect the links, you have to use
        `--process-dependency-links` switch. So e.g.:
        `pip install --process-dependency-links {git-url}`

    Returns:
         list of packages and dependency links.
    """
    default = open("requirements.txt", "r").readlines()
    new_pkgs = []
    links = []
    for resource in default:
        if "http" in resource:
            pkg = resource.split("#")[-1]
            links.append(resource.strip() + "-9876543210")
            new_pkgs.append(pkg.replace("egg=", "").rstrip())
        else:
            new_pkgs.append(resource.strip())
    return new_pkgs, links


pkgs, new_links = install_deps()
dev_pkgs = open("requirements-dev.txt",'r').readlines()

setup(
    name="asrtoolkit",
    version="0.2.1",
    description=
    "The GreenKey ASRToolkit provides tools for automatic speech recognition (ASR) file conversion and corpora organization.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/finos-voice/greenkey-asrtoolkit",
    author="Matthew Goldey",
    author_email="mgoldey@greenkeytech.com",
    install_requires=pkgs,
    extras_require={"dev": dev_pkgs},
    dependency_links=new_links,
    keywords="asr speech recognition greenkey gk word error rate",
    entry_points={
        "console_scripts": [
            "align_json=asrtoolkit.align_json:main",
            "clean_formatting=asrtoolkit.clean_formatting:main",
            "combine_audio_files=asrtoolkit.combine_audio_files:main",
            "convert_transcript = asrtoolkit.convert_transcript:main",
            "degrade_audio_file=asrtoolkit.degrade_audio_file:main",
            "extract_excel_spreadsheets=asrtoolkit.extract_excel_spreadsheets:main",
            "prepare_audio_corpora=asrtoolkit.prepare_audio_corpora:main",
            "split_audio_file=asrtoolkit.split_audio_file:main",
            "wer=asrtoolkit.wer:main",
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
