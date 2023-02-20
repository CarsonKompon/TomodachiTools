from enum import IntEnum

from ctr.util.data_stream import DataStream
from ctr.util.write_stream import WriteStream
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

    entries: list["Usd1Entry"] = []

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)

    def read(self, data: DataStream) -> DataStream:
        """Reads the USD1 section from a data stream"""

        # Save the start position
        startPos = data.tell() - 4

        # Read the first 4 bytes to get the section size
        sectionSize = data.read_uint32()

        # Read the next 2 bytes to get the entry count
        entryCount = data.read_uint16()
        data.read_uint16() # Unknown

        # Read in the entries
        self.entries = []
        for _ in range(entryCount):
            entry = Usd1Entry()
            data = entry.read(data)
            self.entries.append(entry)
        
        # Seek to the end of the section
        data.seek(startPos + sectionSize)

        return data
    
    def write(self, data: WriteStream) -> WriteStream:
        """Writes a USD section to a data stream"""

        # Save the start position
        startPos = data.tell()

        # Write the signature
        data.write_string("txl1")

        # Write the section size (0 for now)
        data.write_uint32(0)

        # Write the entry count
        data.write_uint16(len(self.entries))
        data.write_uint16(0) # Unknown

        # Write the entries
        for entry in self.entries:
            entry.write(data)
        
        # Calculate the section size
        sectionSize = data.tell() - startPos

        # Seek back to the section size and write it
        data.seek(startPos + 4)
        data.write_uint32(sectionSize)

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

    name: str = None
    type: UsdDataType = None
    unkown: bytes = None

    value: str or list[int or float] = None

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)

    def read(self, data: DataStream) -> DataStream:
        """Reads the USD1 entry within a USD1 section from a data stream"""

        # Save the start position
        startPos = data.tell()

        # Read the first 4 bytes to get the name offset
        nameOffset = data.read_uint32()

        # Read a string at the name offset
        self.name = data.read_string_nt_from(startPos + nameOffset)

        # Read the next 4 bytes to get the data offset
        dataOffset = data.read_uint32()

        # Read the next 2 bytes to get the setting
        setting = data.read_uint16()

        # Read the next byte to get the type
        self.type = UsdDataType(data.read_uint8())

        # Read the next byte to get the unknown
        self.unknown = data.read_bytes(1)

        # Read the value(s) based on the type
        match self.type:
            case 0:
                self.value = data.read_string_from(startPos + dataOffset, setting)
            case 1:
                self.value = []
                for _ in range(setting):
                    self.value.append(data.read_int32_from(startPos + dataOffset))
            case 2:
                self.value = []
                for _ in range(setting):
                    self.value.append(data.read_float_from(startPos + dataOffset))

        return data

    def write(self, data: WriteStream) -> WriteStream:
        """Writes the USD1 entry within a USD1 section to a data stream"""

        # Save the start position
        startPos = data.tell()

        # Write the name offset (0 for now)
        data.write_uint32(0)

        # Write the name

        # Write the data offset (0 for now)
        data.write_uint32(0)

        # Write the setting (Length of the array or string)
        data.write_uint16(len(self.value))

        # Write the type
        data.write_uint8(self.type.value)

        # Write the unknown
        data.write_bytes(self.unknown, 1)

        # Write the value(s) based on the type
        dataOffset = data.tell() - startPos
        match self.type:
            case UsdDataType.STRING:
                data.write_string(self.value)
            case UsdDataType.INT:
                data.write_int32(self.value[0])
            case UsdDataType.FLOAT:
                data.write_float(self.value[0])
            
        # Write the name
        nameOffset = data.tell() - startPos
        data.write_string_nt(self.name)

        # Calculate the section size
        sectionSize = data.tell() - startPos

        # Write the name offset
        data.seek(startPos)
        data.write_uint32(nameOffset)

        # Write the data offset
        data.seek(startPos + 4)
        data.write_uint32(dataOffset)

        # Seek to the end of the entry
        data.seek(startPos + sectionSize)

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