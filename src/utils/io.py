"""Input/output and logging tools"""

from datetime import datetime as dt
import logging
import logging.handlers
import os
import sys
import tarfile
from typing import Union


LOG = None
SOURCE_DIR = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
LOG_DIR = os.path.join(SOURCE_DIR, "logs")
DEFAULT_LOG_FORMAT_STR = ("%(name)s|%(levelname)s|%(process)d:%(thread)d|"
                          "%(filename)s:%(lineno)d|%(funcName)s: "
                          "%(message)s")
DEFAULT_LOGGER_NAME = "MLC"
LOG_RECORD_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
LOG_LEVEL = logging.DEBUG if os.getenv("DEBUG", "") else logging.INFO


def _generate_log_filename() -> str:
    return f"{LOG_DIR}/mlc_{int(dt.utcnow().timestamp())}.log"


def _compress_logs(log_dir: str) -> None:
    # TODO: `os.listdir` loads everything into memory. Make more efficient
    #       by walking
    filenames = filter(lambda name: name.lower().endswith(".log"),
                       os.listdir(log_dir))
    filenames = [os.path.join(log_dir, filename) for filename in filenames]

    # TODO: dead code. Keeping in case we want to implement old log purging
    # Sort by creation time
    # filenames = list(reversed(sorted(
    #     filenames, key=lambda filename: os.stat(filename).st_ctime)))

    for filename in filenames:
        compressed_filename = f"{filename}.tar.gz"
        # Compress each log file
        with tarfile.open(compressed_filename, mode="w") as tar_file:
            tar_file.add(filename)
        # Remove the old file
        os.remove(filename)


# pylint: disable=too-many-arguments
def _set_up_logger(use_stdout: bool = True,
                   use_file: Union[bool, str] = True,
                   use_syslog: bool = True,
                   log_level=logging.DEBUG,
                   logger_name: str = DEFAULT_LOGGER_NAME,
                   log_format: str = DEFAULT_LOG_FORMAT_STR) -> None:
    # pylint: disable=global-statement
    global LOG

    LOG = logging.getLogger(logger_name)
    LOG.setLevel(log_level)
    formatter = logging.Formatter(log_format, LOG_RECORD_DATETIME_FORMAT)

    if use_stdout:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(log_level)
        LOG.addHandler(handler)

    log_filename = None
    if use_file is True:
        log_filename = _generate_log_filename()
    elif use_file:
        log_filename = use_file

    if log_filename:
        # Ensure directory where logs will be written to is created
        os.makedirs(LOG_DIR, mode=0o750, exist_ok=True)

        handler = logging.FileHandler(log_filename)
        handler.setFormatter(formatter)
        handler.setLevel(log_level)
        LOG.addHandler(handler)

    if use_syslog:
        platform = sys.platform.lower()
        if platform.endswith("nux") or platform.endswith("nix"):
            handler = logging.handlers.SysLogHandler(address="/dev/log")
        elif hasattr(logging.handlers, "NTEventLogHandler"):
            handler = logging.handlers.NTEventLogHandler(logger_name)
        else:
            handler = None

        if handler:
            handler.setFormatter(formatter)
            handler.setLevel(log_level)
            LOG.addHandler(handler)


def eprint(*args, **kwargs) -> None:
    """Print to stderr. This isn't fast, so don't use it if performance
    matters
    """
    kwargs = kwargs or {}
    kwargs["file"] = kwargs.get("file", sys.stderr)
    print(*args, **kwargs)


try:
    _compress_logs(LOG_DIR)
except (OSError, ValueError) as exc:
    eprint(f"Failed to compress log files in '{LOG_DIR}': {exc}")

_set_up_logger(log_level=LOG_LEVEL)


if __name__ == "__main__":
    def main():
        LOG.debug("Test DEBUG message")
        LOG.info("Test INFO message")
        LOG.warning("Test WARNING message")
        LOG.error("Test ERROR message")

    main()
