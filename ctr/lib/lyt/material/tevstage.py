from ctr.util.data_stream import DataStream
from ctr.util.write_stream import WriteStream
from ctr.util.serialize import JsonSerialize

"""
Tev Stage Entry
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x01  |   byte  | RGB Mode
 0x01  |  0x01  |   byte  | Alpha Mode
 0x02  |  0x02  |  ?????? | Unknown. In flyte this isn't even stored in a variable, but it's still read to advance the seeker (as a uint16).
===================
"""

class TevStage:

    rgbMode: int = None
    alphaMode: int = None
    unknown: int = None

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)
    
    def read(self, data: DataStream) -> DataStream:
        """Reads the TevStage section from a material data stream"""

        # Read in each mode as a single byte
        self.rgbMode = data.read_bytes(1)
        self.alphaMode = data.read_bytes(1)

        # Read in the unknown value as a uint16
        self.unknown = data.read_uint16()

        return data
    
    def write(self, data: WriteStream) -> WriteStream:
        """Writes the TevStage section to a data stream"""

        # Write each mode as a single byte
        data.write_bytes(self.rgbMode)
        data.write_bytes(self.alphaMode)

        # Write the unknown value as a uint16
        data.write_uint16(self.unknown)

        return data

    def __str__(self) -> str:
        j = JsonSerialize()
        j.add("rgbMode", self.rgbMode)
        j.add("alphaMode", self.alphaMode)
        j.add("unknown", self.unknown)
        return j.serialize()