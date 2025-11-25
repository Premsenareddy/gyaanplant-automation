# core/logger.py
import logging
import os

_LOGGER_NAME = "gyaanplant"
_LOG_LEVEL = logging.INFO

def _configure_root_logger() -> logging.Logger:
    logger = logging.getLogger(_LOGGER_NAME)
    if logger.handlers:
        return logger  # already configured

    logger.setLevel(_LOG_LEVEL)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(_LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    logger.propagate = False
    return logger

def get_logger(name: str | None = None) -> logging.Logger:
    root = _configure_root_logger()
    return root if name is None else root.getChild(name)

