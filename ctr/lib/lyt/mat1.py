from ...util.data_stream import DataStream
from ...util.bit import extract_bits

from .material.texmap import TexMap
from .material.texsrt import TexSRT
from .material.texcoordgen import TexCoordGen
from .material.tevstage import TevStage
from .material.alphacompare import AlphaCompare
from .material.blendmode import BlendMode
from .material.indirectparameter import IndirectParameter
from .material.projectiontexgenparam import ProjectionTexGenParam
from .material.fontshadowparameter import FontShadowParameter

"""
MAT1 (Materials 1)
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x14  |  string  | Material Name
 0x14  |  0x04  |  rgba8   | Tev Color
 0x18  |  0x18  | rgba8[6] | Tev Constant Colors
 0x30  |  0x04  |  uint32  | Flags bitfield:
       |        |          | - Bits 0-1: TexMap Count
       |        |          | - Bits 2-3: TexMtx Count
       |        |          | - Bits 4-5: TexCoordGen Count
       |        |          | - Bits 6-8: TevStage Count
       |        |          | - Bit 9: Has Alpha Compare
       |        |          | - Bit 10: Has Blend Mode
       |        |          | - Bit 11: Use Texture Only
===================
"""

class Mat1Material:

    name: str = ""
    tevColor: list[int] = None
    tevConstantColors: list[list[int]] = None
    flags: int = None

    texMapCount: int = None
    texMtxCount: int = None
    texCoordGenCount: int = None
    tevStageCount: int = None
    hasAlphaCompare: bool = None
    hasBlendMode: bool = None
    useTextureOnly: bool = None
    separateBlendMode: bool = None
    hasIndParam: bool = None
    projTextGenParamCount: int = None
    hasFontShadowParam: bool = None

    texMaps: list[TexMap] = None
    texSRTs: list[TexSRT] = None
    texCoords: list[TexCoordGen] = None
    tevStages: list[TevStage] = None
    alphaCompare: AlphaCompare = None
    blendModeBlend: BlendMode = None
    blendModeLogic: BlendMode = None
    indParam: IndirectParameter = None
    projTextGenParam: list[ProjectionTexGenParam] = None
    fontShadowParam: FontShadowParameter = None

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)
        
    def read(self, data: DataStream) -> DataStream:

        # Read the first 20 bytes to get the material name
        self.name = data.read_string(0x14).replace("\0", "")

        # Read the next 4 bytes to get the flags
        tevColor = data.read_color_rgba8()

        # Read the 6 constant colors
        tevConstantColors = []
        for i in range(6):
            tevConstantColors.append(data.read_color_rgba8())
        
        # Read the next 4 bytes to get the flags
        self.flags = data.read_uint32()

        # Extract the info from the flags
        self.texMapCount = extract_bits(self.flags, 2, 0)
        self.texMtxCount = extract_bits(self.flags, 2, 2)
        self.texCoordGenCount = extract_bits(self.flags, 2, 4)
        self.tevStageCount = extract_bits(self.flags, 2, 6)
        self.hasAlphaCompare = extract_bits(self.flags, 1, 9) == 1
        self.hasBlendMode = extract_bits(self.flags, 1, 10) == 1
        self.useTextureOnly = extract_bits(self.flags, 1, 11) == 1
        self.separateBlendMode = extract_bits(self.flags, 1, 12) == 1
        self.hasIndParam = extract_bits(self.flags, 1, 14) == 1
        self.projTextGenParamCount = extract_bits(self.flags, 2, 15)
        self.hasFontShadowParam = extract_bits(self.flags, 1, 17) == 1

        # Loop through each texture map
        self.texMaps = []
        for i in range(self.texMapCount):
            # Read the texture map
            texMap = TexMap(data)
            data = texMap.read(data)
            self.texMaps.append(texMap)

class Mat1:
    """A MAT1 section in a CTR file"""

    sectionSize: int = None
    materialCount: int = None
    sectionOffsets: list[int] = None
    materials: list[Mat1Material] = None

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)

    def read(self, data: DataStream) -> DataStream:
        """Reads the MAT1 section from a data stream"""

        # Save the start position
        startPos = data.tell() - 4

        # Read the first 4 bytes to get the section size
        self.sectionSize = data.read_uint32()

        # Read the next 4 bytes to get the texture count
        self.materialCount = data.read_uint32()

        # All offsets are relative to the start of the section
        curPos = data.tell()

        # Loop through each material
        self.sectionOffsets = []
        for i in range(self.materialCount):
            # Read the next 4 bytes to get the section offset
            self.sectionOffsets.append(data.read_uint32())
        
        # Loop through each section offset
        self.materials = []
        for offset in self.sectionOffsets:
            # Seek to the offset
            data.seek(startPos + offset)
            # Read the material
            material = Mat1Material(data)
            data = material.read(data)
        
        # Seek to the end of the section
        data.seek(startPos + self.sectionSize)

        return data