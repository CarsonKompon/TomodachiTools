from enum import IntEnum
from ctr.lib.lyt.pan1 import Pan1

from ctr.util.data_stream import DataStream

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
    materialIdx: int = None
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
        if data is not None:
            self.read(data)
        self.layoutType = "Text Box"

    def read(self, data: DataStream) -> DataStream:

        # Save the start of the section
        startPos = data.tell() - 0x4C

        # Read unsigned 16-bit integers
        self.bufferLength = data.read_uint16()
        self.stringLength = data.read_uint16()
        self.materialIdx = data.read_uint16()
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
        self.sizeX = data.read_float32()
        self.sizeY = data.read_float32()
        self.characterSize = data.read_float32()
        self.lineSize = data.read_float32()

        # Read string
        if self.stringLength != 0:
            data.seek(startPos + self.textOffset)
            self.string = data.read_string(self.stringLength)
        
        # Seek to the end of the section
        data.seek(startPos + self.sectionSize)

        return data

    def __str__(self):
        string = "{"
        string += f"bufferLength: {self.bufferLength}, "
        string += f"stringLength: {self.stringLength}, "
        string += f"materialIdx: {self.materialIdx}, "
        string += f"fontNum: {self.fontNum}, "
        string += f"anotherOrigin: {self.anotherOrigin}, "
        string += f"alignment: {self.alignment}, "
        string += f"unknown: {self.unknown}, "
        string += f"textOffset: {self.textOffset}, "
        string += f"topColor: {self.topColor}, "
        string += f"bottomColor: {self.bottomColor}, "
        string += f"sizeX: {self.sizeX}, "
        string += f"sizeY: {self.sizeY}, "
        string += f"characterSize: {self.characterSize}, "
        string += f"lineSize: {self.lineSize}, "
        string += f"string: {self.string}"
        string += "}"
        return string