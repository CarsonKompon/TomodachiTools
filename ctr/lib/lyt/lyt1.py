from enum import IntEnum

from ctr.util.data_stream import DataStream

"""
LYT1 (Layout 1)
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x04  |  string  | Signature (lyt1)
 0x04  |  0x04  |  uint32  | Section Size
 0x08  |  0x04  |  uint32  | Origin Type (0 = Classic, 1 = Normal)
 0x0C  |  0x08  |  vector2 | Canvas Size (uint32, uint32)
===================
Notes: Some libs such as "flyte" read 2 uint16s at offset 0x08 and mark the second variable as "unknown"
"""

# Origin Type Enum
class OriginType(IntEnum):
    CLASSIC = 0
    NORMAL = 1

# Lyt1 Class
class Lyt1:
    """A LYT1 section in a CTR file"""

    originType: OriginType = OriginType.CLASSIC
    canvasSize: tuple[int, int] = (0, 0)

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)

    def read(self, data: DataStream) -> DataStream:
        """Reads the LYT1 section from a data stream"""

        # Save the start position
        startPos = data.tell() - 4

        # Read the first 4 bytes to get the section size
        sectionSize = data.read_uint32()

        # Read the next 4 bytes to get the origin type
        self.originType = data.read_uint32()

        # Read the next 8 bytes to get the x and y floats for the canvas size
        self.canvasSize = data.read_vector2()

        # Seek to the end of the section
        data.seek(startPos + sectionSize)

        return data
    
    def __str__(self) -> str:
        json = "{"
        json += f'"originType": {self.originType},'
        json += f'"canvasSize": {self.canvasSize}'
        json += "}"
        return json
