"""Executable data types"""

from enum import auto

from mlc.data_gen.data_type_base import DataTypeBase


class ExecutableDataType(DataTypeBase):
    """Executable data types/formats"""
    NIX_ELF = auto()
    NIX_LIB_A = auto()
    NIX_LIB_SO = auto()
    NIX_OBJ = auto()
    WINDOWS_DLL = auto()
    # Doubt DLL vs EXE will be distinguishable
    WINDOWS_EXE = auto()
    WINDOWS_LIB = auto()
    WINDOWS_OBJ = auto()

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Executable data types not yet supported")
