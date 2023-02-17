from enum import IntEnum

from ctr.util.data_stream import DataStream

"""
Texture Map Entry
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x02  |  uint16  | Texture Index
 0x02  |  0x01  |   byte   | Bitfield (Bit 0-1 Wrap S: 0 = Clamp, 1 = Repeat, 2 = Mirror | Bit 2-3 Min Filter: 0 = Near, 1 = Linear)
 0x03  |  0x01  |   byte   | Bitfield (Bit 0-1 Wrap T: 0 = Clamp, 1 = Repeat, 2 = Mirror | Bit 2-3 Mag Filter: 0 = Near, 1 = Linear)
===================
"""

# Wrap Mode Enum
class WrapMode(IntEnum):
    CLAMP = 0,
    REPEAT = 1,
    MIRROR = 2

# Filter Mode Enum
class FilterMode(IntEnum):
    NEAREST = 0,
    LINEAR = 1

class TexMap:

    textureIndex: int = None
    wrapModeS: WrapMode = WrapMode.CLAMP
    wrapModeT: WrapMode = WrapMode.CLAMP
    filterModeMin: FilterMode = FilterMode.NEAREST
    filterModeMag: FilterMode = FilterMode.NEAREST

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)
    
    def read(self, data: DataStream) -> DataStream:
        """Reads the TexMap section from a material data stream"""

        # Read the first 2 bytes to get the texture index
        self.textureIndex = data.read_uint16()

        # Read in the next 2 bytes to determine the wrap and filter modes
        sVal = data.read_bytes(1)
        tVal = data.read_bytes(1)

        # Determine the wrap and filter modes
        self.wrapModeS = sVal & 0x3
        self.filterModeMin = (sVal >> 2) & 0x3

        self.wrapModeT = tVal & 0x3
        self.filterModeMag = (tVal >> 2) & 0x3

        return data

