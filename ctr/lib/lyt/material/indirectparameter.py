from ....util.data_stream import DataStream

"""
Indirect Parameter Entry
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x08  |   float  | Rotation
 0x08  |  0x10  |  vector2 | Scale (32-bit float, 32-bit float)
===================
"""

class IndirectParameter:

    rotation: float = None
    scale: tuple[float, float] = None

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)
    
    def read(self, data: DataStream) -> DataStream:
        """Reads the IndirectParameter section from a material data stream"""

        # Read in the rotation as a 32-bit float
        self.rotation = data.read_float()

        # Read in the scale as two 32-bit floats
        self.scale = (data.read_float(), data.read_float())

        return data
