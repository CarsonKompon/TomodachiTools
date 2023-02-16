from ....util.data_stream import DataStream

"""
Font Shadow Parameter Entry
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x01  |   byte   | Black - Red Value
 0x01  |  0x01  |   byte   | Black - Green Value
 0x02  |  0x01  |   byte   | Black - Blue Value
 0x03  |  0x01  |   byte   | White - Red Value
 0x04  |  0x01  |   byte   | White - Green Value
 0x05  |  0x01  |   byte   | White - Blue Value
 0x06  |  0x01  |   byte   | White - Alpha Value
 0x06  |  0x01  |   byte   | Unknown byte that's read in but not stored in flyte
===================
"""

class FontShadowParameter:

    blackRed: int = None
    blackGreen: int = None
    blackBlue: int = None
    whiteRed: int = None
    whiteGreen: int = None
    whiteBlue: int = None
    whiteAlpha: int = None

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)
    
    def read(self, data: DataStream) -> DataStream:
        """Reads the FontShadowParameter section from a material data stream"""

        # Read in each value as a single byte
        self.blackRed = data.read_bytes(1)
        self.blackGreen = data.read_bytes(1)
        self.blackBlue = data.read_bytes(1)
        self.whiteRed = data.read_bytes(1)
        self.whiteGreen = data.read_bytes(1)
        self.whiteBlue = data.read_bytes(1)
        self.whiteAlpha = data.read_bytes(1)

        return data