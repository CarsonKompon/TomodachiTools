from ctr.util.data_stream import DataStream
from ctr.util.write_stream import WriteStream
from ctr.util.serialize import JsonSerialize

"""
Indirect Parameter Entry
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x04  |   float  | Rotation
 0x04  |  0x08  |  vector2 | Scale (32-bit float, 32-bit float)
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
        self.scale = data.read_vector2()

        return data
    
    def write(self, data: WriteStream) -> WriteStream:
        """Writes the IndirectParameter section to a data stream"""

        # Write the rotation as a 32-bit float
        data.write_float(self.rotation)

        # Write the scale as two 32-bit floats
        data.write_vector2(self.scale)

        return data

    def __str__(self) -> str:
        j = JsonSerialize()
        j.add("rotation", self.rotation)
        j.add("scale", self.scale)
        return j.serialize()
    
