from ....util.data_stream import DataStream

"""
Texture Matrix Entry
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x08  |  vector2 | Translation (32-bit float, 32-bit float)
 0x08  |  0x04  |   float  | Rotation
 0x0C  |  0x08  |  vector2 | Scale (32-bit float, 32-bit float)
===================
"""

class TexSRT:

    translation: tuple[float, float] = None
    rotation: float = None
    scale: tuple[float, float] = None

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)
    
    def read(self, data: DataStream) -> DataStream:
        """Reads the TexMap section from a material data stream"""

        # Read in each value as a 32-bit float
        self.translation = (data.read_float(), data.read_float())
        self.rotation = data.read_float()
        self.scale = (data.read_float(), data.read_float())

        return data
    
    # TODO: Implement write methods with a WriteStream class
    # def write(self, data: DataStream) -> DataStream:
    #     """Writes the TexMap section to a data stream"""

    #     # Write each value as a 32-bit float
    #     data.write_float(self.x)
    #     data.write_float(self.y)
    #     data.write_float(self.rotation)
    #     data.write_float(self.scaleX)
    #     data.write_float(self.scaleY)

    #     return data

