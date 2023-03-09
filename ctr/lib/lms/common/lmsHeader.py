
from ctr.lib.lms.common.lmsExceptions import (lmsInvalidBOM,
                                              lmsInvalidEncoding,
                                              lmsInvalidHeader,
                                              lmsInvalidRevision)
from ctr.util.data_stream import DataStream


class lmsBinaryHeader:
    """A class that represents a binary file-header for the following files from the LMS library:
      - MSBT (Message Studio Binary Text)
      - MSBP (Message Studio Binary Project)
      - MSBF (Message Studio Binary Flow) 
    """

    def __init__(self, data: DataStream):
        self.data: DataStream = data
        self.magic: str = self.data.read_string(8)
        self.byteOrderMark = 'little' if self.data.read_bytes(
            2) == b'\xFF\xFE' else 'big'
        self.data.read_bytes(2)
        self.messageEncoding: int
        messageEncodingNumber: int = self.data.read_uint8()
        match messageEncodingNumber:
            case 0:
                self.messageEncoding = "UTF-8"
            case 1:
                self.messageEncoding = "UTF-16"
            case 2:
                self.messageEncoding = "UTF-32"

        self.revision: int = self.data.read_uint8()
        self.blockCount: int = self.data.read_uint32()
        self.fileSize: int = self.data.read_uint32()
        self.data.read_bytes(10)

        # Exception handling
        if self.magic != "MsgPrjBn":
            raise lmsInvalidHeader(
                f"Invalid header, expected 'MsgPrjBn' got '{self.magic}'")
        if self.byteOrderMark != "little":
            raise lmsInvalidBOM(
                f"Invalid BOM, expected 'little' got '{self.byteOrderMark}'")
        if self.revision != 3:
            raise lmsInvalidRevision(
                f"Invalid revision, expected '3', got '{self.revision}'")
        if self.messageEncoding != "UTF-8":
            raise lmsInvalidEncoding(
                f"Invalid revision, expected 'UTF-8', got '{self.messageEncoding}'")
