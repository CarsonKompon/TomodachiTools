from ctr.util.data_stream import DataStream
from ctr.util.serialize import JsonSerialize

from ctr.lib.lyt.pan1 import Pan1

"""
PIC1 (Picture 1)
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x04  |  string  | Signature (pic1)
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
 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Same as PAN1
 0x4C  |  0x02  |  uint16  | Buffer Length
 0x4E  |  0x02  |  uint16  | String Length
 0x50  |  0x02  |  uint16  | Material Index
 0x52  |  0x02  |  uint16  | Font Number
 0x54  |  0x01  |   byte   | Another Origin
 0x55  |  0x01  |   byte   | Alignment
 0x56  |  0x02  |  ??????  | Unknown
 0x58  |  0x04  |  uint32  | Text Offset
 0x5C  |  0x04  |  rgba8   | Top Color
 0x60  |  0x04  |  rgba8   | Bottom Color
 0x64  |  0x04  |  float   | Size X
 0x68  |  0x04  |  float   | Size Y
 0x6C  |  0x04  |  float   | Character Size
 0x70  |  0x04  |  float   | Line Size
"""

class Txt1(Pan1):

    bufferLength: int = None
    stringLength: int = None
    materialId: int = None
    fontNum: int = None
    anotherOrigin: int = None
    alignment: int = None

    unknown: bytes = None
    textOffset: int = None
    topColor: tuple[int, int, int, int] = None
    bottomColor: tuple[int, int, int, int] = None
    sizeX: float = None
    sizeY: float = None
    characterSize: float = None
    lineSize: float = None

    string: str = None

    def __init__(self, data: DataStream = None):
        self.type = "Text Box"
        if data is not None:
            self.read(data)

    def read(self, data: DataStream) -> DataStream:
        data = super().read(data)

        # Save the start of the section
        startPos = data.tell() - 0x4C

        # Read unsigned 16-bit integers
        self.bufferLength = data.read_uint16()
        self.stringLength = data.read_uint16()
        self.materialId = data.read_uint16()
        self.fontNum = data.read_uint16()

        # Read single bytes
        self.anotherOrigin = data.read_bytes(1)
        self.alignment = data.read_bytes(1)

        # Read unknown bytes
        self.unknown = data.read_bytes(0x2)

        # Read unsigned 32-bit integer
        self.textOffset = data.read_uint32()

        # Read RGBA8 colors
        self.topColor = data.read_color_rgba8()
        self.bottomColor = data.read_color_rgba8()

        # Read 32-bit floats
        self.sizeX = data.read_float()
        self.sizeY = data.read_float()
        self.characterSize = data.read_float()
        self.lineSize = data.read_float()

        # Read string
        if self.stringLength != 0:
            data.seek(startPos + self.textOffset)
            self.string = data.read_string(self.stringLength)
        
        # Seek to the end of the section
        data.seek(startPos + self.sectionSize)

        return data

    def __str__(self):
        j = JsonSerialize()
        # j.add("bufferLength", self.bufferLength)
        # j.add("stringLength", self.stringLength)
        j.add("materialId", self.materialId)
        j.add("fontNum", self.fontNum)
        j.add("anotherOrigin", self.anotherOrigin)
        j.add("alignment", self.alignment)
        j.add("unknown", self.unknown)
        # j.add("textOffset", self.textOffset)
        j.add("topColor", self.topColor)
        j.add("bottomColor", self.bottomColor)
        j.add("sizeX", self.sizeX)
        j.add("sizeY", self.sizeY)
        j.add("characterSize", self.characterSize)
        j.add("lineSize", self.lineSize)
        j.add("string", self.string)
        return j.serialize()