from ctr.util.data_stream import DataStream
from ctr.util.write_stream import WriteStream
from ctr.util.serialize import JsonSerialize

"""
Alpha Compare Entry
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x01  |   byte  | Compare Mode
 0x01  |  0x04  |  float  | Reference Alpha
 0x05  |  0x03  |  ?????  | Unknown. In flyte this isn't even stored in a variable, but it's still read to advance the seeker.
===================
"""

class AlphaCompare:

    compareMode: int = None
    referenceAlpha: int = None
    unknown: int = None

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)
    
    def read(self, data: DataStream) -> DataStream:
        """Reads the AlphaCompare section from a material data stream"""

        # Read in the compare mode as a byte
        self.compareMode = data.read_bytes(1)

        # Read in the reference alpha as a 32-bit float
        self.referenceAlpha = data.read_float()

        # Read the unknown bytes
        self.unknown = data.read_bytes(0x3)

        return data
    
    def write(self, data: WriteStream) -> WriteStream:
        """Writes the AlphaCompare section to a data stream"""

        # Write the compare mode as a byte
        data.write_bytes(self.compareMode)

        # Write the reference alpha as a 32-bit float
        data.write_float(self.referenceAlpha)

        # Write the unknown bytes
        data.write_bytes(self.unknown, 0x3)

        return data
    
    def __str__(self) -> str:
        j = JsonSerialize()
        j.add("compareMode", self.compareMode)
        j.add("referenceAlpha", self.referenceAlpha)
        j.add("unknown", self.unknown)
        return j.serialize()
