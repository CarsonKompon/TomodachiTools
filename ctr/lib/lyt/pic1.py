from ctr.util.data_stream import DataStream
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
 0x4C  |  0x04  |  rgba8   | Vertex Color Top Left
 0x50  |  0x04  |  rgba8   | Vertex Color Top Right
 0x54  |  0x04  |  rgba8   | Vertex Color Bottom Left
 0x58  |  0x04  |  rgba8   | Vertex Color Bottom Right
 0x5C  |  0x02  |  uint16  | Material ID
 0x5E  |  0x02  |  uint16  | Texture Coordinate Count = N
===================
    For each texture coordinate:
    Offset                     |  Size  |  Type   | Description
    ---------------------------+--------+---------+------------
    0x60 + (N-1) * 0x20 + 0x00 |  0x08  | vector2 | Top left texture coordinate (two 32-bit floats)
    0x60 + (N-1) * 0x20 + 0x08 |  0x08  | vector2 | Top right texture coordinate (two 32-bit floats)
    0x60 + (N-1) * 0x20 + 0x10 |  0x08  | vector2 | Bottom left texture coordinate (two 32-bit floats)
    0x60 + (N-1) * 0x20 + 0x18 |  0x08  | vector2 | Bottom right texture coordinate (two 32-bit floats)
"""

class Pic1(Pan1):

    vertexColorTopLeft: tuple[int, int, int, int] = None
    vertexColorTopRight: tuple[int, int, int, int] = None
    vertexColorBottomLeft: tuple[int, int, int, int] = None
    vertexColorBottomRight: tuple[int, int, int, int] = None
    materialId: int = None
    textureCoordCount: int = None
    textureCoords: list[list[tuple[float, float]]] = None

    def __init__(self, data: DataStream = None):
        super().__init__(data)
        self.layoutType = "Picture"
        if data is not None:
            self.read(data)
    
    def read(self, data: DataStream) -> DataStream:
        data = super().read(data)
        
        # Get the start position
        startPos = data.tell() - 0x4C

        # Read in the vertex colors
        self.vertexColorTopLeft = data.read_color_rgba8()
        self.vertexColorTopRight = data.read_color_rgba8()
        self.vertexColorBottomLeft = data.read_color_rgba8()
        self.vertexColorBottomRight = data.read_color_rgba8()

        # Read in the material ID and texture coordinate count as unsigned 16-bit integers
        self.materialId = data.read_uint16()
        self.textureCoordCount = data.read_uint16()

        # Read in the texture coordinates
        self.textureCoords = []
        for _ in range(self.textureCoordCount):
            coord = []
            for _ in range(4):
                coord.append(data.read_vector2())
            self.textureCoords.append(coord)
        
        # Seek to the end of the section
        data.seek(startPos + self.sectionSize)

        # Return the data stream
        return data

    def __str__(self) -> str:
        string = super().__str__() # Get parent string
        string = string[:-1] + "," # Remove the closing brace and add a comma
        string += "vertexColorTopLeft: " + str(self.vertexColorTopLeft) + ","
        string += "vertexColorTopRight: " + str(self.vertexColorTopRight) + ","
        string += "vertexColorBottomLeft: " + str(self.vertexColorBottomLeft) + ","
        string += "vertexColorBottomRight: " + str(self.vertexColorBottomRight) + ","
        string += "materialId: " + str(self.materialId) + ","
        string += "textureCoordCount: " + str(self.textureCoordCount) + ","
        string += "textureCoords: " + str(self.textureCoords) + "}"
        return string 
