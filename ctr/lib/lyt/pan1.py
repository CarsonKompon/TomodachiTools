from ctr.util.data_stream import DataStream
from ctr.util.bit import extract_bits

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

    flags: int = None
    isVisible: bool = None
    influencedAlpha: bool = None
    locationAdjustment: bool = None

    origin: int = None
    alpha: int = None
    magFlags: int = None
    ignorePartsMagnify: bool = None
    adjustToPartsBounds: bool = None

    name: str = None
    position: tuple[float, float, float] = None
    rotation: tuple[float, float, float] = None
    scale: tuple[float, float] = None
    width: float = None
    height: float = None

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)

    def read(self, data: DataStream) -> DataStream:
        """Reads the PAN1 section from a data stream"""

        # Store the start offset of the section
        startPos = data.tell() - 4

        # Read in the section size as a 32-bit unsigned integer
        sectionSize = data.read_uint32()

        # Read in the flags as a single byte and determine the boolean values from it
        self.flags = data.read_uint8()
        self.isVisible = extract_bits(self.flags, 1, 0)
        self.influencedAlpha = extract_bits(self.flags, 1, 1)
        self.locationAdjustment = extract_bits(self.flags, 1, 2)

        # Read in the origin, alpha, and panemagflags as single bytes
        self.origin = data.read_uint8()
        self.alpha = data.read_uint8()
        self.magFlags = data.read_uint8()

        # Determine the boolean values from the panemagflags
        self.ignorePartsMagnify = extract_bits(self.magFlags, 1, 0)
        self.adjustToPartsBounds = extract_bits(self.magFlags, 1, 1)

        # Read in the name as a string of length 0x18
        self.name = data.read_string(0x18).replace("\0", "")

        # Read in the position and rotation as vector3s
        self.position = data.read_vector3()
        self.rotation = data.read_vector3()

        # Read in the height and width as 32-bit floats (In that order)
        self.height = data.read_float()
        self.width = data.read_float()

        # Seek to the end of the section
        data.seek(startPos + sectionSize)

        return data
    
    def __str__(self) -> str:
        json = "{"
        json += f'"flags": {self.flags},'
        json += f'"isVisible": {self.isVisible},'
        json += f'"influencedAlpha": {self.influencedAlpha},'
        json += f'"locationAdjustment": {self.locationAdjustment},'
        json += f'"origin": {self.origin},'
        json += f'"alpha": {self.alpha},'
        json += f'"magFlags": {self.magFlags},'
        json += f'"ignorePartsMagnify": {self.ignorePartsMagnify},'
        json += f'"adjustToPartsBounds": {self.adjustToPartsBounds},'
        json += f'"name": "{self.name}",'
        json += f'"position": {self.position},'
        json += f'"rotation": {self.rotation},'
        json += f'"height": {self.height},'
        json += f'"width": {self.width}'
        json += "}"
        return json

class Bnd1(Pan1):

    def __init__(self, data: DataStream = None):
        super().__init__(data)
        self.layoutType = "Bounding Box"
        if data is not None:
            self.read(data)
