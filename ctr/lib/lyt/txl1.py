from ctr.util.data_stream import DataStream

"""
TXL1 (Texture List 1)
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x04  |  string  | Signature (txl1)
 0x04  |  0x04  |  uint32  | Section Size
 0x08  |  0x04  |  uint32  | Texture Count = N
 0x0C  | N*0x04 | uint32[] | Texture Name Offsets (Relative to the start of this array)
===================
Notes: Some libs such as "flyte" read 2 uint16s at offset 0x08 and mark the second variable as "unknown"
"""

class Txl1:
    """A TXL1 section in a CTR file"""

    textureCount: int = None
    strings: list[str] = []

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)

    def read(self, data: DataStream) -> DataStream:
        """Reads the TXL1 section from a data stream"""

        # Save the start position
        startPos = data.tell() - 4

        # Read the first 4 bytes to get the section size
        sectionSize = data.read_uint32()

        # Read the next 4 bytes to get the texture count
        self.textureCount = data.read_uint32()

        # All offsets are relative to the start of the section
        curPos = data.tell()

        # Loop through each texture offset
        self.strings = []
        for i in range(self.textureCount):
            # Read the next 4 bytes to get the texture offset
            offset = data.read_uint32()
            # Add the string from the curPos + offset (Equivalent of C#'s ReadStringNTFrom)
            self.strings.append(data.read_string_nt_from(curPos + offset))
        
        # Seek to the end of the section
        data.seek(startPos + sectionSize)

        return data
    
    def image_exists(self, name: str) -> bool:
        """Returns true if the image exists in the TXL1"""
        return name in self.strings
    
    def __str__(self) -> str:
        string = "{"
        string += f"textureCount: {self.textureCount},"
        string += f"strings: {self.strings}"
        string += "}"
        return string

