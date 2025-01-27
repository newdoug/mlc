"""Document data types"""

from enum import auto

try:
    from .data_type_base import DataTypeBase
except (ImportError, ModuleNotFoundError):
    from data_gen.data_type_base import DataTypeBase


class DocumentDataType(DataTypeBase):
    """Document (mostly plaintext) data type/format"""
    ASCIIDOC = auto()
    EPUB = auto()
    # HOCON is a superset of .properties and .json, so leaving that off
    MARKDOWN = auto()
    MS_DOC = auto()
    MS_DOCX = auto()
    # TODO: there are more book formats (at least one I can't remember right
    #       now)
    MOBI = auto()
    PDF = auto()
    PLIST = auto()
    PROPERTIES = auto()
    RTF = auto()
    # TODO: much more

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Document data types not yet supported")
