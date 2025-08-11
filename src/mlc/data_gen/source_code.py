"""Source code data type(s)"""

from enum import auto

from mlc.data_gen.data_type_base import DataTypeBase


class SourceCodeDataType(DataTypeBase):
    """Source code (plaintext) data type/format"""

    # TODO: how to handle encodings for interpreted plaintext data types?
    ASM_ARM = auto()
    ASM_MIPS = auto()
    ASM_PPC = auto()
    ASM_X86 = auto()
    ASP = auto()
    ASPX = auto()
    BATCH = auto()
    # Unsure if we'll be able to distringuish between header and source
    # (unlikely, but maybe if certain patterns that show up in headers rather
    # than source files (or vice versa) are enough to impact the ciphertext
    # or compressed text enough for the model to understand).
    C_HEADER = auto()
    C_SOURCE = auto()
    # Command file (older Windows scripts)
    COM = auto()
    CPP_HEADER = auto()
    CPP_SOURCE = auto()
    CSHARP = auto()
    CSS = auto()
    GO = auto()
    HTML = auto()
    JAVA = auto()
    JAVASCRIPT = auto()
    PERL = auto()
    PY = auto()
    RUBY = auto()
    RSS = auto()
    RUST = auto()
    SHELL = auto()
    SWIFT = auto()
    TYPESCRIPT = auto()
    # Not distinguishing between various *nix shells (yet?)
    UNIX_SHELL = auto()
    XHTML = auto()
    # TODO: much more

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Source code data types not yet supported")
