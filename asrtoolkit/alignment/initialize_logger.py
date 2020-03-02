#!/usr/bin/env python3
"""
This file should be imported/called before any other modules that use any logging.
If any other modules that use logging are imported before this file,
then any calls to the logging module will not be formatted properly until after this module is loaded.
"""
import logging
import os
import sys

# Get logging level from the environment, if it is set
LOG_LEVEL_ENV = os.environ.get("LOG_LEVEL", "INFO").upper()


def initialize_logger(stream=sys.stderr):
    """
    Set logging level to the level specified in environment, or "INFO" if no valid value specified.
    """
    # Note, do NOT do any logging in this function until the "basicConfig" is set!
    unable_to_set_user_log_level = False

    try:
        logging_level = getattr(logging, LOG_LEVEL_ENV)
    except AttributeError:
        unable_to_set_user_log_level = True
        logging_level = logging.INFO

    logging.basicConfig(
        level=logging_level,
        format="%(levelname)-8s - %(asctime)s - %(name)s - %(message)s",
        stream=stream,
    )

    logging.info(
        'Logger initialized! Threshold set to "%s".',
        logging.getLevelName(logging_level),
    )

    if unable_to_set_user_log_level:
        logging.warning(
            "User attempted to set log level to %s, which is not a valid log level!",
            LOG_LEVEL_ENV,
        )
