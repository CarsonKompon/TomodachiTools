from enum import IntEnum

from ctr.util.data_stream import DataStream
from ctr.util.serialize import JsonSerialize

"""
USD1 (User Data 1?)
===================
Offset |  Size  |    Type    | Description
-------+--------+----------+------------
 0x00  |  0x04  |   string   | Signature (txl1)
 0x04  |  0x04  |   uint32   | Section Size
 0x08  |  0x02  |   uint16   | Number of Entries = N
 0x0A  |  0x02  |   uint16   | Unknown (It could also be that Number of Entries is a uint32)
 0x0C  |  ????  | usdentry[] | User Data Entries. Size is determined by the entries themselves
===================

USD1Entry (User Data 1 Entry?)
===================
Offset |  Size  |    Type    | Description
-------+--------+----------+------------
 0x00  |  0x04  |   uint32   | Name Offset (Relative to the start of this entry)
 0x04  |  0x04  |   uint32   | Data Offset (Relative to the start of this entry)
 0x08  |  0x02  |   uint16   | Setting
 0x0A  |  0x01  |   uint8    | Type (0 = String, 1 = Int, 2 = Float)
 0x0B  |  0x01  |   uint8    | Unknown
===================
The value is then read from the data offset. The data offset is relative to the start of the entry.
If the type is zero, then the value is a string and setting is the length of the string.
If the type is one, then the value is an int and setting is the number of ints to read into an array.
If the type is two, then the value is a float and setting is the number of floats to read into an array.
"""

class UsdDataType(IntEnum):
    STRING = 0
    INT = 1
    FLOAT = 2

class Usd1:
    """A USD1 section in a CTR file"""

    entryCount: int = None
    entries: list["Usd1Entry"] = []

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)

    def read(self, data: DataStream) -> DataStream:
        """Reads the TXL1 section from a data stream"""

        # Save the start position
        startPos = data.tell() - 4

        # Read the first 4 bytes to get the section size
        sectionSize = data.read_uint32()

        # Read the next 2 bytes to get the entry count
        self.entryCount = data.read_uint16()
        data.read_uint16() # Unknown

        # Read in the entries
        self.entries = []
        for _ in range(self.entryCount):
            entry = Usd1Entry()
            data = entry.read(data)
            self.entries.append(entry)
        
        # Seek to the end of the section
        data.seek(startPos + sectionSize)

        return data
    
    def __str__(self) -> str:
        j = JsonSerialize()
        j.add("entryCount", self.entryCount)
        j.add("entries", self.entries)
        return j.serialize()

class Usd1Entry:
    """A USD1 entry in a USD1 section within a CTR"""

    nameOffset: int = None
    name: str = None
    dataOffset: int = None
    setting: int = None
    type: UsdDataType = None
    unkown: bytes = None

    value: str or list[int or float] = None

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)

    def read(self, data: DataStream) -> DataStream:
        """Reads the TXL1 section from a data stream"""

        # Save the start position
        startPos = data.tell()

        # Read the first 4 bytes to get the name offset
        self.nameOffset = data.read_uint32()

        # Read a string at the name offset
        self.name = data.read_string_nt_from(startPos + self.nameOffset)

        # Read the next 4 bytes to get the data offset
        self.dataOffset = data.read_uint32()

        # Read the next 2 bytes to get the setting
        self.setting = data.read_uint16()

        # Read the next byte to get the type
        self.type = UsdDataType(data.read_uint8())

        # Read the next byte to get the unknown
        self.unknown = data.read_bytes(1)

        # Read the value(s) based on the type
        match self.type:
            case 0:
                self.value = data.read_string_from(startPos + self.dataOffset, self.setting)
            case 1:
                self.value = []
                for _ in range(self.setting):
                    self.value.append(data.read_int32_from(startPos + self.dataOffset))
            case 2:
                self.value = []
                for _ in range(self.setting):
                    self.value.append(data.read_float_from(startPos + self.dataOffset))

        return data
    
    def image_exists(self, name: str) -> bool:
        """Returns true if the image exists in the TXL1"""
        return name in self.strings
    
    def __str__(self) -> str:
        j = JsonSerialize()
        # j.add("nameOffset", self.nameOffset)
        j.add("name", self.name)
        # j.add("dataOffset", self.dataOffset)
        # j.add("setting", self.setting)
        j.add("type", self.type, True)
        # j.add("unknown", self.unknown)
        j.add("value", self.value)
        return j.serialize()