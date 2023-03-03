from ctr.util.data_stream import DataStream
from ctr.util.write_stream import WriteStream
from ctr.util.bit import extract_bits
from ctr.util.serialize import JsonSerialize

from ctr.lib.lyt.layoutbase import LayoutBase

"""
PAN1 (Pane 1)
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

class Pan1(LayoutBase):
    """A PAN1 section in a CTR file"""

    isVisible: bool = None
    influencedAlpha: bool = None
    locationAdjustment: bool = None

    origin: int = None
    alpha: int = None
    ignorePartsMagnify: bool = None
    adjustToPartsBounds: bool = None

    dataString: str = None
    position: tuple[float, float, float] = None
    rotation: tuple[float, float, float] = None
    scale: tuple[float, float] = None
    width: float = None
    height: float = None

    originalSectionSize: int = None

    def __init__(self, data: DataStream = None):
        super().__init__()
        self.type = "Panel"
        if data is not None:
            self.read(data)

    def read(self, data: DataStream) -> DataStream:
        """Reads the PAN1 section from a data stream"""

        # Store the start offset of the section
        startPos = data.tell() - 4

        # Read in the section size as a 32-bit unsigned integer
        self.originalSectionSize = data.read_uint32()

        # Read in the flags as a single byte and determine the boolean values from it
        flags = data.read_uint8()
        self.isVisible = extract_bits(flags, 1, 0) == 1
        self.influencedAlpha = extract_bits(flags, 1, 1) == 1
        self.locationAdjustment = extract_bits(flags, 1, 2) == 1

        # Read in the origin, alpha, and magflags as single bytes
        self.origin = data.read_uint8()
        self.alpha = data.read_uint8()
        magFlags = data.read_uint8()

        # Determine the boolean values from the magflags
        self.ignorePartsMagnify = extract_bits(magFlags, 1, 0)
        self.adjustToPartsBounds = extract_bits(magFlags, 1, 1)

        # Read in the name as a string of length 0x10
        self.name = data.read_string(0x10).replace("\0", "")

        # Read in the data as a string of length 0x8
        self.dataString = data.read_string(0x8).replace("\0", "")

        # Read in the position and rotation as vector3s
        self.position = data.read_vector3()
        self.rotation = data.read_vector3()

        # Read in the height and width as 32-bit floats (In that order)
        self.height = data.read_float()
        self.width = data.read_float()

        # Seek to the end of the section
        data.seek(startPos + 0x4C)

        return data
    
    def write(self, data: WriteStream) -> WriteStream:
        """Writes the PAN1 section to a data stream"""

        # Store the start offset of the section
        startPos = data.tell()

        # Write the signature
        data.write_string("pan1")

        # Write the section size (same every time)
        data.write_uint32(0x4C)

        # Write the flags
        flags = 0
        if self.isVisible:
            flags = flags | 0b00000001
        if self.influencedAlpha:
            flags = flags | 0b00000010
        if self.locationAdjustment:
            flags = flags | 0b00000100
        data.write_uint8(flags)

        # Write the origin, alpha, and panemagflags
        data.write_uint8(self.origin)
        data.write_uint8(self.alpha)

        # Write the magflags
        magFlags = 0
        if self.ignorePartsMagnify:
            magFlags = magFlags | 0b00000001
        if self.adjustToPartsBounds:
            magFlags = magFlags | 0b00000010
        data.write_uint8(magFlags)

        # Write the name
        data.write_string(self.name, 0x10)

        # Write the data
        data.write_string(self.dataString, 0x8)

        # Write the position and rotation
        data.write_vector3(self.position)
        data.write_vector3(self.rotation)

        # Write the height and width
        data.write_float(self.height)
        data.write_float(self.width)

        # Seek to the end of the section
        data.seek(startPos + 0x4C)

        return data
    
    def __str__(self) -> str:
        j = JsonSerialize(super().__str__())
        j.add("isVisible", self.isVisible)
        j.add("influencedAlpha", self.influencedAlpha)
        j.add("locationAdjustment", self.locationAdjustment)
        j.add("origin", self.origin)
        j.add("alpha", self.alpha)
        j.add("ignorePartsMagnify", self.ignorePartsMagnify)
        j.add("adjustToPartsBounds", self.adjustToPartsBounds)
        j.add("dataString", self.dataString)
        j.add("position", self.position)
        j.add("rotation", self.rotation)
        j.add("scale", self.scale)
        j.add("width", self.width)
        j.add("height", self.height)
        return j.serialize()


class Bnd1(Pan1):

    def __init__(self, data: DataStream = None):
        super().__init__(data)
        self.type = "Bounding Box"
        if data is not None:
            self.read(data)
