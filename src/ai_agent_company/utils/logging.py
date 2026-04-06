"""Logging utilities for the AI Agent Company."""

from __future__ import annotations

import logging
import sys


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a consistently-configured :class:`logging.Logger`.

    The returned logger writes to *stdout* using a simple timestamped
    format.  If a handler is already attached (e.g. in a test harness),
    a second handler is not added.

    Args:
        name: Logger name — typically ``__name__`` of the calling module.
        level: Logging level.  Defaults to :data:`logging.INFO`.

    Returns:
        A configured :class:`logging.Logger` instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
