from ctr.util.data_stream import DataStream
from ctr.util.write_stream import WriteStream
from ctr.util.serialize import JsonSerialize

from ctr.lib.lyt.layoutbase import LayoutBase

"""
GRP1 (Group 1)
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x04  |  string  | Signature (grp1)
 0x04  |  0x04  |  uint32  | Section Size
 0x08  |  0x10  |  string  | Group Name
 0x18  |  0x02  |  uint16  | Pane Count = N
 0x1A  |  0x02  |  uint16  | Padding?
 0x1C  | N*0x10 | string[] | Pane References
===================
"""

class Grp1(LayoutBase):
    """A GRP1 section in a CTR file"""

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
        paneCount = data.read_uint16()
        data.read_uint16() # Padding?

        # Root group never has any entries
        if paneCount > 0:
            self.entries = []
            for _ in range(paneCount):
                self.entries.append(data.read_string(0x10).replace("\0", ""))
        
        # Seek to the end of the section
        data.seek(startPos + sectionSize)

        return data
    
    def write(self, data: WriteStream) -> WriteStream:
        """Writes the GRP1 section to a data stream"""

        # Store the start offset of the section
        startPos = data.tell()

        # Write the section header
        data.write_string("grp1")

        # Write the section size (placeholder)
        data.write_uint32(0)

        # Write the name
        data.write_string(self.name, 0x10)

        # Write the pane count
        if self.entries is None:
            data.write_uint16(0)
        else:
            data.write_uint16(len(self.entries))

        # Write the padding
        data.write_uint16(0)

        # Write the pane references
        if self.entries is not None:
            for entry in self.entries:
                data.write_string(entry, 0x10)
        
        # Write the section size
        sectionSize = data.tell() - startPos
        data.seek(startPos + 4)
        data.write_uint32(sectionSize)

        # Seek to the end of the section
        data.seek(startPos + sectionSize)

        return data
    
    def __str__(self) -> str:
        j = JsonSerialize(super().__str__())
        j.add("entries", self.entries)
        return j.serialize()