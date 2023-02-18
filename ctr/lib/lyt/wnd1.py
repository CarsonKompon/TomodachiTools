from ctr.util.data_stream import DataStream
from ctr.lib.lyt.pan1 import Pan1
from ctr.lib.lyt.mat1 import Mat1

"""
WND1 (Window 1)
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
 0x4C                   |  0x04  | float  | Content Overflow Left
 0x50                   |  0x04  | float  | Content Overflow Right
 0x54                   |  0x04  | float  | Content Overflow Top
 0x58                   |  0x04  | float  | Content Overflow Bottom
 0x5C                   |  0x01  | uint8  | Frame Count = A
 0x5D                   |  0x01  | uint8  | Flag
 0x5E                   |  0x02  | uint16 | Padding (?)
 0x60                   |  0x04  | uint32 | Window Content Offset
 0x64                   |  0x04  | uint32 | Window Frame Offset
 0x68                   |  0x04  | rgba8  | Top Left Color
 0x6C                   |  0x04  | rgba8  | Top Right Color
 0x70                   |  0x04  | rgba8  | Bottom Left Color
 0x74                   |  0x04  | rgba8  | Bottom Right Color
 0x78                   |  0x02  | uint16 | Material Index
 0x7A                   |  0x01  | uint8  | Texture Coordinate Count = N
 0x7B                   |  0x01  | uint8  | Padding (?)
 0x7C                   |  0x04  | uint32 | Material Name Offset
 0x80                   | N*0x20 | uvset  | UV Sets
 0x80 + N*0x20          | A*0x04 | uint32 | Frame Offsets
 0x80 + N*0x20 + A*0x04 | A*0x04 | uint32 | Frames
===================
    For each frame:
    Offset |  Size  |  Type  | Description
    -------+--------+--------+------------
     0x00  |  0x02  | uint16 | Material Index
     0x02  |  0x01  | uint8  | Flip Type
     0x03  |  0x08  |  byte  | Unknown
"""

class Wnd1(Pan1):

    contentOverflowLeft: float = None
    contentOverflowRight: float = None
    contentOverflowTop: float = None
    contentOverflowBottom: float = None
    frameCount: int = None
    flag: int = None
    padding: int = None

    windowContentOffset: int = None
    windowFrameOffset: int = None
    colorTopLeft: tuple[int, int, int, int] = None
    colorTopRight: tuple[int, int, int, int] = None
    colorBottomLeft: tuple[int, int, int, int] = None
    colorBottomRight: tuple[int, int, int, int] = None
    materialId: int = None
    textureCoordCount: int = None

    materialName: str = None
    materialList: Mat1 = None

    textureCoords: list[tuple] = None
    frameOffsets: list[int] = None
    frames: list["WND1Frame"] = None

    def __init__(self, materials, data: DataStream = None):
        super().__init__(data)
        self.materialList = materials
        self.layoutType = "Window"
        if data is not None:
            self.read(data)
    
    def read(self, data: DataStream) -> DataStream:
        data = super().read(data)

        # Store the start pos
        startPos = data.tell() - 0x4C
        
        # Read the content overflow values as 32-bit floats
        self.contentOverflowLeft = data.read_float()
        self.contentOverflowRight = data.read_float()
        self.contentOverflowTop = data.read_float()
        self.contentOverflowBottom = data.read_float()
        
        # Read the frame count and flag in as single bytes
        self.frameCount = data.read_uint8()
        self.flag = data.read_uint8()

        # Read the padding in as a 16-bit int
        self.padding = data.read_uint16()

        # Read the window content and frame offsets as 32-bit uints
        self.windowContentOffset = data.read_uint32()
        self.windowFrameOffset = data.read_uint32()

        # Read the vertex colors as 32-bit RGBA8 values
        self.colorTopLeft = data.read_color_rgba8()
        self.colorTopRight = data.read_color_rgba8()
        self.colorBottomLeft = data.read_color_rgba8()
        self.colorBottomRight = data.read_color_rgba8()

        # Read the material ID as a 16-bit uint
        self.materialId = data.read_uint16()

        # Read the texture coordinate count as an 8-bit uint
        self.textureCoordCount = data.read_uint8()

        data.read_bytes(1) # Padding

        # Read the texture coordinates
        self.textureCoords = []
        for _ in range(self.textureCoordCount):
            self.textureCoords.append(data.read_uv_coord_set())
        
        # Read the window frame offsets
        data.seek(startPos + self.windowFrameOffset)
        self.frameOffsets = []
        for _ in range(self.frameCount):
            self.frameOffsets.append(data.read_uint32())
        
        # Read the window frames
        self.frames = []
        for offset in self.frameOffsets:
            data.seek(startPos + offset)
            frame = WND1Frame()
            data = frame.read(data)
            self.frames.append(frame)

        self.materialName = self.materialList.get_material_name_from_index(self.materialId)

        data.seek(startPos + self.sectionSize)
        
        return data

    def __str__(self) -> str:
        string = super().__str__() # Get parent string
        string = string[:-1] + "," # Remove the closing brace and add a comma
        string += f"contentOverflowLeft={self.contentOverflowLeft},"
        string += f"contentOverflowRight={self.contentOverflowRight},"
        string += f"contentOverflowTop={self.contentOverflowTop},"
        string += f"contentOverflowBottom={self.contentOverflowBottom},"
        string += f"frameCount={self.frameCount},"
        string += f"flag={self.flag},"
        string += f"padding={self.padding},"
        string += f"windowContentOffset={self.windowContentOffset},"
        string += f"windowFrameOffset={self.windowFrameOffset},"
        string += f"colorTopLeft={self.colorTopLeft},"
        string += f"colorTopRight={self.colorTopRight},"
        string += f"colorBottomLeft={self.colorBottomLeft},"
        string += f"colorBottomRight={self.colorBottomRight},"
        string += f"materialId={self.materialId},"
        string += f"textureCoordCount={self.textureCoordCount},"
        string += f"materialName={self.materialName},"
        string += f"textureCoords={self.textureCoords},"
        string += f"frameOffsets={self.frameOffsets},"
        string += f"frames={self.frames}"
        string += "}" # Add the closing brace
        return string 

class WND1Frame():

    materialIndex: int = None
    flipType: int = None
    unknown: int = None

    def read(self, data: DataStream) -> DataStream:
        
        # Read the material index and flip type
        self.materialIndex = data.read_uint16()
        self.flipType = data.read_uint8()
        self.unknown = data.read_uint8()
        
        return data