from ctr.util.data_stream import DataStream
from ctr.util.write_stream import WriteStream
from ctr.util.serialize import JsonSerialize

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

    textureNames: list[str] = []

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
        textureCount = data.read_uint32()

        # All offsets are relative to the start of the section
        curPos = data.tell()

        # Loop through each texture offset
        self.textureNames = []
        for i in range(textureCount):
            # Read the next 4 bytes to get the texture offset
            offset = data.read_uint32()
            # Add the string from the curPos + offset (Equivalent of C#'s ReadStringNTFrom)
            self.textureNames.append(data.read_string_nt_from(curPos + offset))
        
        # Seek to the end of the section
        data.seek(startPos + sectionSize)

        return data
    
    def write(self, data: WriteStream) -> WriteStream:
        """Writes the TXL1 section to a data stream"""

        # Save the start position
        startPos = data.tell()

        # Write the signature
        data.write_string("txl1")

        # Write the section size (Placeholder)
        data.write_uint32(0)

        # Write the texture count
        data.write_uint32(len(self.textureNames))

        # Write the texture offsets (Placeholder)
        for i in range(len(self.textureNames)):
            data.write_uint32(0)

        # Write the texture names
        textureOffsets = []
        for i in range(len(self.textureNames)):
            textureOffsets.append(data.tell() - startPos)
            data.write_string_nt(self.textureNames[i])
        
        # Calculate the section size
        sectionSize = data.tell() - startPos

        # Write the texture offsets
        for i in range(len(textureOffsets)):
            data.seek(startPos + 0x0C + (i * 4))
            data.write_uint32(textureOffsets[i])

        # Write the section size
        data.seek(startPos + 4)
        data.write_uint32(sectionSize)

        # Seek to the end of the section
        data.seek(startPos + sectionSize)

        return data
    
    def image_exists(self, name: str) -> bool:
        """Returns true if the image exists in the TXL1"""
        return name in self.textureNames
    
    def __str__(self) -> str:
        j = JsonSerialize()
        j.add("textureNames", self.textureNames)
        return j.serialize()

