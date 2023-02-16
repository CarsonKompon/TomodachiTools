from ....util.data_stream import DataStream

"""
Tev Stage Entry
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x01  |   byte  | RGB Mode
 0x01  |  0x01  |   byte  | Alpha Mode
 0x02  |  0x04  |  ?????? | Unknown. In flyte this isn't even stored in a variable, but it's still read to advance the seeker (as a uint16).
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
