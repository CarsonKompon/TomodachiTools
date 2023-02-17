from ctr.util.data_stream import DataStream

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

    sectionSize: int = None
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
        self.sectionSize = data.read_uint32()

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
        data.seek(startPos + self.sectionSize)

        return data

