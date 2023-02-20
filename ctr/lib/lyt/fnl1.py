from ctr.util.data_stream import DataStream
from ctr.util.write_stream import WriteStream
from ctr.util.serialize import JsonSerialize

"""
FNL1 (Font List 1)
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x04  |  string  | Signature (fnl1)
 0x04  |  0x04  |  uint32  | Section Size
 0x08  |  0x04  |  uint32  | Font Count = N
 0x0C  | N*0x04 | uint32[] | Font Name Offsets (Relative to the start of this array)
===================
Notes: Some libs such as "flyte" read 2 uint16s at offset 0x08 and mark the second variable as "unknown"
"""

class Fnl1:
    """A FNL1 section in a CTR file"""

    fontCount: int = None
    strings: list[str] = []

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)

    def read(self, data: DataStream) -> DataStream:
        """Reads the FNL1 section from a data stream"""

        # Save the start position
        startPos = data.tell() - 4

        # Read the first 4 bytes to get the section size
        sectionSize = data.read_uint32()

        # Read the next 4 bytes to get the texture count
        self.fontCount = data.read_uint32()

        # All offsets are relative to the start of the section
        curPos = data.tell()

        # Loop through each texture offset
        self.strings = []
        for i in range(self.fontCount):
            # Read the next 4 bytes to get the texture offset
            offset = data.read_uint32()
            # Add the string from the curPos + offset (Equivalent of C#'s ReadStringNTFrom)
            self.strings.append(data.read_string_nt_from(curPos + offset))
        
        # Seek to the end of the section
        data.seek(startPos + sectionSize)

        return data
    
    def write(self, data: WriteStream) -> WriteStream:
        """Writes the FNL1 section to a data stream"""

        # Save the start position
        startPos = data.tell()

        # Write the signature
        data.write_string("fnl1")

        # Write the section size (Temporary value that will be overwritten later)
        data.write_uint32(0)

        # Write the font count
        data.write_uint32(self.fontCount)

        # Store section start
        sectionStart = data.tell()

        # Write the font name offsets (Temporary values that will be overwritten later)
        for i in range(self.fontCount):
            data.write_uint32(0)

        # Write the font names
        fontNameOffsets = []
        for i in range(self.fontCount):
            fontNameOffsets.append(data.tell() - sectionStart)
            data.write_string_nt(self.strings[i])
        
        # Calculate the section size
        sectionSize = data.tell() - startPos

        # Write the font name offsets
        for i in range(self.fontCount):
            data.seek(startPos + 0xC + (i * 4))
            data.write_uint32(fontNameOffsets[i])

        # Write the section size
        data.seek(startPos + 4)
        data.write_uint32(sectionSize)

        # Seek to the end of the section
        data.seek(startPos + sectionSize)

        return data
    
    def __str__(self) -> str:
        j = JsonSerialize()
        j.add("fontCount", self.fontCount)
        j.add("strings", self.strings)
        return j.serialize()

