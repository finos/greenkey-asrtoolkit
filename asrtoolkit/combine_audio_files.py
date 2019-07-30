#!/usr/bin/env python
"""
Script for splitting audio files using a transcript with start/stop times
"""
import argparse
import logging
import os
import operator
from functools import reduce

from asrtoolkit.data_structures.time_aligned_text import time_aligned_text
from asrtoolkit.data_structures.audio_file import audio_file, combine_audio
from asrtoolkit.file_utils.script_input_validation import valid_input_file
from asrtoolkit.file_utils.name_cleaners import strip_extension

LOGGER = logging.getLogger(__name__)

def check_transcript(transcript):
    if valid_input_file(transcript):
        return time_aligned_text(input_data=transcript)
    else:
        LOGGER.error("Invalid transcript file {}".format(transcript))


def check_audio_file(audio_file_name):
    if valid_input_file(audio_file_name, ["mp3", "sph", "wav", "au", "raw"]):
        return audio_file(audio_file_name)
    else:
        LOGGER.error("Invalid audio file {}".format(audio_file_name))


def check_transcript_segment(segment):
    if not hasattr(segment, 'start'):
        LOGGER.error("Transcript segment doesn't include the start time, segment: {}".format(segment))


def combine_transcripts(transcripts, output_file_name):
    # Get one list of segments
    out_transcript = reduce(operator.add, transcripts)
    out_transcript.location = os.path.join(strip_extension(output_file_name) + '.' +
                                           out_transcript.file_extension)
    out_transcript.write(out_transcript.location)


def main():
    """
    Combine audio files using their transcript files
    """
    parser = argparse.ArgumentParser(
        description=
        '''Combine a audio files using segments from their transcript files. For this utility, transcript files must contain start/stop times.
   Lists of transcripts and audio files must be ordered identically, meaning the first audio file's
transcript is the first transcript.
        '''
    )
    parser.add_argument('--output_file',
                        default='output.wav',
                        required=True,
                        help='Name of output file')
    parser.add_argument('--audio_files',
                        metavar='audio_files',
                        type=str,
                        nargs='+',
                        required=True,
                        help='List of input audio files')
    parser.add_argument('--transcripts',
                        metavar='transcripts',
                        type=str,
                        nargs='+',
                        required=True,
                        help='List of transcripts')
    parser.add_argument('--renormalize',
                        default=False,
                        action='store_true',
                        help='Renormalize files to undo sox normalizing by 1/num_audio_files. Useful when combined audio has little overlap')
    # Sending audio through tanh could be helpful if there are significant transient audio signals

    args = parser.parse_args()
    if len(args.audio_files) != len(args.transcripts):
        LOGGER.error("The number of audio files, {}, must be equal to the number of transcripts, {}".format( 
                      len(args.audio_files), len(ags.transcripts) ))

    [ check_audio_file( _ ) for _ in args.audio_files ]
    transcripts = [ check_transcript( _ ) for _ in args.transcripts ]
    
    [ check_transcript_segment( _ ) for transcript in transcripts for _ in transcript.segments ]

    combine_transcripts(transcripts, args.output_file)
    combine_audio(args.audio_files, args.output_file, args.renormalize)


if __name__ == "__main__":
    main()
