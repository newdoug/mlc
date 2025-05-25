"""Source code data type(s)"""

from enum import auto

from mlc.data_gen.data_type_base import DataTypeBase


class SourceCodeDataType(DataTypeBase):
    """Source code (plaintext) data type/format"""
    # TODO: how to handle encodings for interpreted plaintext data types?
    BATCH = auto()
    # Unsure if we'll be able to distringuish between header and source
    # (unlikely, but maybe if certain patterns that show up in headers rather
    # than source files (or vice versa) are enough to impact the ciphertext
    # or compressed text enough for the model to understand).
    C_HEADER = auto()
    C_SOURCE = auto()
    CPP_HEADER = auto()
    CPP_SOURCE = auto()
    GO = auto()
    JAVA = auto()
    JAVASCRIPT = auto()
    PERL = auto()
    PY = auto()
    RUBY = auto()
    RUST = auto()
    # Not distinguishing between various *nix shells (yet?)
    UNIX_SHELL = auto()
    # TODO: much more

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Source code data types not yet supported")
