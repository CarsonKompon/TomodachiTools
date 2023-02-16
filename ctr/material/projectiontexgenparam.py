from ..util.data_stream import DataStream

"""
Projection Tex Gen Param Entry
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x10  |  vector2 | Position (32-bit float, 32-bit float)
 0x10  |  0x10  |  vector2 | Scale (32-bit float, 32-bit float)
 0x20  |  0x01  |   byte   | Flags (bit 0: isFittingLayoutSize, bit 1: isFittingPaneSize, bit 2: isAdjustProjectionSR)
 0x21  |  0x03  |  ??????  | Unknown. In flyte it's not stored in a variable, but a comment simply says "padding" next to it
===================
"""

class ProjectionTexGenParam:

    position: tuple[float, float] = None
    scale: tuple[float, float] = None

    isFittingLayoutSize: bool = None
    isFittingPaneSize: bool = None
    isAdjustProjectionSR: bool = None

    padding: int = None

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)
    
    def read(self, data: DataStream) -> DataStream:
        """Reads the ProjectionTexGenParam section from a material data stream"""

        # Read in the position and scale as vectors consiting of two 32-bit floats each
        self.position = (data.read_float(), data.read_float())
        self.scale = (data.read_float(), data.read_float())

        # Read in the flags as a byte
        flags = data.read_bytes(1)

        # Determine the boolean values from the flags
        self.isFittingLayoutSize = bool(flags & 0x01)
        self.isFittingPaneSize = bool(flags & 0x02)
        self.isAdjustProjectionSR = bool(flags & 0x03)

        # Read in the padding as 3 bytes
        self.padding = data.read_bytes(3)

        return data
