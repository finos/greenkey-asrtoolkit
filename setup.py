#!/usr/bin/env python
"""
Creates asrtoolkit
"""
from setuptools import setup, find_packages

with open('requirements.txt') as f:
  required = f.read().splitlines()

setup(
  name='asrtoolkit',
  version='0.1',
  description='ASR toolkit for processing ',
  url='http://github.com/asrtool',
  author='Matthew Goldey',
  author_email='mgoldey@greenkeytech.com',
  install_requires=required,
  keywords="asr speech recognition greenkey word error rate",
  entry_points={
    'console_scripts':
      [
        'convert_transcript = asrtoolkit.convert_transcript:main',
        'clean_formatting=asrtoolkit.clean_formatting:main',
        'prepare_audio_corpora=asrtoolkit.prepare_audio_corpora:main',
        'degrade_audio_file=asrtoolkit.degrade_audio_file:main',
        'wer=asrtoolkit.wer:main',
      ]
  },
  license='Apache v2',
  packages=find_packages(),
  zip_safe=True
)
