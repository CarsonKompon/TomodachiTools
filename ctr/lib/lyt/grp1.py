from ctr.util.data_stream import DataStream
from ctr.util.serialize import JsonSerialize

from ctr.lib.lyt.layoutbase import LayoutBase

"""
GRP1 (Group 1)
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x04  |  string  | Signature (pan1)
 0x04  |  0x04  |  uint32  | Section Size
 0x08  |  0x01  |  uint8   | Flags (Bit 0: Visible, Bit 1: Influenced Alpha, Bit 2: Location Adjustment)
 0x09  |  0x01  |  uint8   | Origin
 0x0A  |  0x01  |  uint8   | Alpha
 0x0B  |  0x01  |  uint8   | Padding
 0x0C  |  0x10  |  string  | Pane Name
 0x1C  |  0x08  |  string  | Data
 0x24  |  0x0C  |  vector3 | Translation (three 32-bit floats)
 0x30  |  0x0C  |  vector3 | Rotation (three 32-bit floats)
 0x3C  |  0x08  |  vector2 | Scale (two 32-bit floats)
 0x44  |  0x04  |  uint32  | Height
 0x48  |  0x04  |  uint32  | Width
===================
"""

class Grp1(LayoutBase):
    """A GRP1 section in a CTR file"""

    paneCount: int = None
    entries: list[str] = None

    def __init__(self, data: DataStream = None):
        super().__init__()
        self.type = "Group"
        if data is not None:
            self.read(data)

    def read(self, data: DataStream) -> DataStream:
        """Reads the GRP1 section from a data stream"""

        # Store the start offset of the section
        startPos = data.tell() - 4

        sectionSize = data.read_uint32()
        self.name = data.read_string(0x10).replace("\0", "")
        self.paneCount = data.read_uint16()
        data.read_uint16() # Padding?

        # Root group never has any entries
        if self.paneCount > 0:
            self.entries = []
            for _ in range(self.paneCount):
                self.entries.append(data.read_string(0x10).replace("\0", ""))
        
        # Seek to the end of the section
        data.seek(startPos + sectionSize)

        return data
    
    def __str__(self) -> str:
        j = JsonSerialize(super().__str__())
        j.add("paneCount", self.paneCount)
        j.add("entries", self.entries)
        return j.serialize()