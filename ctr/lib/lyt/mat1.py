from ctr.util.data_stream import DataStream
from ctr.util.bit import extract_bits
from ctr.util.serialize import JsonSerialize

from ctr.lib.lyt.material.texmap import TexMap
from ctr.lib.lyt.material.texsrt import TexSRT
from ctr.lib.lyt.material.texcoordgen import TexCoordGen
from ctr.lib.lyt.material.tevstage import TevStage
from ctr.lib.lyt.material.alphacompare import AlphaCompare
from ctr.lib.lyt.material.blendmode import BlendMode
from ctr.lib.lyt.material.indirectparameter import IndirectParameter
from ctr.lib.lyt.material.projectiontexgenparam import ProjectionTexGenParam
from ctr.lib.lyt.material.fontshadowparameter import FontShadowParameter

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
        print(self.name)

        # Read the next few bytes to get the tev color
        self.tevColor = data.read_color_rgba8()

        # Read the 6 constant colors
        self.tevConstantColors = []
        for _ in range(6):
            self.tevConstantColors.append(data.read_color_rgba8())
        
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
        for _ in range(self.texMapCount):
            # Read the texture map
            texMap = TexMap()
            data = texMap.read(data)
            self.texMaps.append(texMap)
        
        # Loop through each texture SRT
        self.texSRTs = []
        for _ in range(self.texMtxCount):
            # Read the texture SRT
            texSRT = TexSRT()
            data = texSRT.read(data)
            self.texSRTs.append(texSRT)
        
        # Loop through each texture coordinate
        self.texCoords = []
        for _ in range(self.texCoordGenCount):
            # Read the texture coordinate
            texCoord = TexCoordGen()
            data = texCoord.read(data)
            self.texCoords.append(texCoord)
        
        # Loop through each tev stage
        self.tevStages = []
        for _ in range(self.tevStageCount):
            # Read the tev stage
            tevStage = TevStage()
            data = tevStage.read(data)
            self.tevStages.append(tevStage)
        
        # Read the alpha compare
        if self.hasAlphaCompare:
            self.alphaCompare = AlphaCompare()
            data = self.alphaCompare.read(data)
        
        # Read the blend mode
        if self.hasBlendMode:
            self.blendModeBlend = BlendMode()
            data = self.blendModeBlend.read(data)
        
        # Read the logic blend mode
        if self.separateBlendMode:
            self.blendModeLogic = BlendMode()
            data = self.blendModeLogic.read(data)
        
        # Read the indirect parameter
        if self.hasIndParam:
            self.indParam = IndirectParameter()
            data = self.indParam.read(data)
        
        # Read the projection texture generation parameters
        self.projTextGenParam = []
        for _ in range(self.projTextGenParamCount):
            # Read the projection texture generation parameter
            projTextGenParam = ProjectionTexGenParam()
            data = projTextGenParam.read(data)
            self.projTextGenParam.append(projTextGenParam)
        
        # Read the font shadow parameter
        if self.hasFontShadowParam:
            self.fontShadowParam = FontShadowParameter()
            data = self.fontShadowParam.read(data)
        
        # Return the data stream
        return data
    
    def __str__(self) -> str:
        j = JsonSerialize()
        j.add("name", self.name)
        j.add("tevColor", self.tevColor)
        j.add("tevConstantColors", self.tevConstantColors)
        # j.add("flags", self.flags)
        j.add("texMapCount", self.texMapCount)
        j.add("texMtxCount", self.texMtxCount)
        j.add("texCoordGenCount", self.texCoordGenCount)
        j.add("tevStageCount", self.tevStageCount)
        j.add("hasAlphaCompare", self.hasAlphaCompare)
        j.add("hasBlendMode", self.hasBlendMode)
        j.add("useTextureOnly", self.useTextureOnly)
        j.add("separateBlendMode", self.separateBlendMode)
        j.add("hasIndParam", self.hasIndParam)
        j.add("projTextGenParamCount", self.projTextGenParamCount)
        j.add("hasFontShadowParam", self.hasFontShadowParam)
        j.add("texMaps", self.texMaps)
        j.add("texSRTs", self.texSRTs)
        j.add("texCoords", self.texCoords)
        j.add("tevStages", self.tevStages)
        j.add("alphaCompare", self.alphaCompare)
        j.add("blendModeBlend", self.blendModeBlend)
        j.add("blendModeLogic", self.blendModeLogic)
        j.add("indParam", self.indParam)
        j.add("projTextGenParam", self.projTextGenParam)
        j.add("fontShadowParam", self.fontShadowParam)
        return j.serialize()
        

class Mat1:
    """A MAT1 section in a CTR file"""

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
        sectionSize = data.read_uint32()

        # Read the next 4 bytes to get the texture count
        self.materialCount = data.read_uint32()

        # Loop through each material
        self.sectionOffsets = []
        for _ in range(self.materialCount):
            # Read the next 4 bytes to get the section offset
            self.sectionOffsets.append(data.read_uint32())
        
        # Loop through each section offset
        self.materials = []
        for offset in self.sectionOffsets:
            # Seek to the offset
            data.seek(startPos + offset)
            # Read the material
            material = Mat1Material()
            self.materials.append(material)
            data = material.read(data)
        
        # Seek to the end of the section
        data.seek(startPos + sectionSize)

        return data
    
    def get_material_name_from_index(self, index: int) -> str:
        """Gets the material name from an index"""
        return self.materials[index].name

    def __str__(self) -> str:
        j = JsonSerialize()
        j.add("materials", self.materials)
        return j.serialize()