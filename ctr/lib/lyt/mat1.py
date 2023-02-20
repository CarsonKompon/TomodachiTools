from ctr.util.data_stream import DataStream
from ctr.util.write_stream import WriteStream
from ctr.util.bit import extract_bits, insert_bits
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
==================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x04  |  string  | Signature (mat1)
 0x04  |  0x04  |  uint32  | Section Size
 0x08  |  0x04  |  uint32  | Material Count = N
 0x0C  | N*0x04 | uint32[] | Material Entry Offsets (Relative to the start of this section)

Then material entries follow:

MAT1 Entry (Material Entry 1)
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

class Mat1:
    """A MAT1 section in a CTR file"""

    sectionOffsets: list[int] = None
    materials: list["Mat1Material"] = None

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
        materialCount = data.read_uint32()

        # Loop through each material
        self.sectionOffsets = []
        for _ in range(materialCount):
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
    
    def write(self, data: WriteStream) -> WriteStream:
        
        # Save the start position
        startPos = data.tell()

        # Write the signature
        data.write_string("mat1")

        # Write the section size (placeholder)
        data.write_uint32(0)

        # Write the material count
        data.write_uint32(len(self.materials))

        # Write the material entry offsets (placeholder)
        for _ in range(len(self.materials)):
            data.write_uint32(0)

        # Write the material entries
        materialOffsets = []
        for material in self.materials:
            materialOffsets.append(data.tell() - startPos)
            data = material.write(data)
        
        # Calculate the section size
        sectionSize = data.tell() - startPos

        # Write the material entry offsets
        for i in range(len(self.materials)):
            data.seek(startPos + 8 + (i * 4))
            data.write_uint32(materialOffsets[i])
        
        # Write the section size
        data.seek(startPos + 4)
        data.write_uint32(sectionSize)

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

class Mat1Material:

    name: str = ""
    tevColor: list[int] = None
    tevConstantColors: list[list[int]] = None

    useTextureOnly: bool = None

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

        # Read the next few bytes to get the tev color
        self.tevColor = data.read_color_rgba8()

        # Read the 6 constant colors
        self.tevConstantColors = []
        for _ in range(6):
            self.tevConstantColors.append(data.read_color_rgba8())
        
        # Read the next 4 bytes to get the flags
        flags = data.read_uint32()

        # Extract the info from the flags
        texMapCount = extract_bits(flags, 2, 0)
        texMtxCount = extract_bits(flags, 2, 2)
        texCoordGenCount = extract_bits(flags, 2, 4)
        tevStageCount = extract_bits(flags, 2, 6)
        hasAlphaCompare = extract_bits(flags, 1, 9) == 1
        hasBlendMode = extract_bits(flags, 1, 10) == 1
        self.useTextureOnly = extract_bits(flags, 1, 11) == 1
        separateBlendMode = extract_bits(flags, 1, 12) == 1
        hasIndParam = extract_bits(flags, 1, 14) == 1
        projTextGenParamCount = extract_bits(flags, 2, 15)
        hasFontShadowParam = extract_bits(flags, 1, 17) == 1

        # Loop through each texture map
        self.texMaps = []
        for _ in range(texMapCount):
            # Read the texture map
            texMap = TexMap()
            data = texMap.read(data)
            self.texMaps.append(texMap)
        
        # Loop through each texture SRT
        self.texSRTs = []
        for _ in range(texMtxCount):
            # Read the texture SRT
            texSRT = TexSRT()
            data = texSRT.read(data)
            self.texSRTs.append(texSRT)
        
        # Loop through each texture coordinate
        self.texCoords = []
        for _ in range(texCoordGenCount):
            # Read the texture coordinate
            texCoord = TexCoordGen()
            data = texCoord.read(data)
            self.texCoords.append(texCoord)
        
        # Loop through each tev stage
        self.tevStages = []
        for _ in range(tevStageCount):
            # Read the tev stage
            tevStage = TevStage()
            data = tevStage.read(data)
            self.tevStages.append(tevStage)
        
        # Read the alpha compare
        if hasAlphaCompare:
            self.alphaCompare = AlphaCompare()
            data = self.alphaCompare.read(data)
        
        # Read the blend mode
        if hasBlendMode:
            self.blendModeBlend = BlendMode()
            data = self.blendModeBlend.read(data)
        
        # Read the logic blend mode
        if separateBlendMode:
            self.blendModeLogic = BlendMode()
            data = self.blendModeLogic.read(data)
        
        # Read the indirect parameter
        if hasIndParam:
            self.indParam = IndirectParameter()
            data = self.indParam.read(data)
        
        # Read the projection texture generation parameters
        self.projTextGenParam = []
        for _ in range(projTextGenParamCount):
            # Read the projection texture generation parameter
            projTextGenParam = ProjectionTexGenParam()
            data = projTextGenParam.read(data)
            self.projTextGenParam.append(projTextGenParam)
        
        # Read the font shadow parameter
        if hasFontShadowParam:
            self.fontShadowParam = FontShadowParameter()
            data = self.fontShadowParam.read(data)
        
        # Return the data stream
        return data
    
    def write(self, data: WriteStream) -> WriteStream:

        # Write the material name
        data.write_string(self.name, 0x14)

        # Write the tev color
        data.write_color_rgba8(self.tevColor)

        # Write the 6 constant colors
        for color in self.tevConstantColors:
            data.write_color_rgba8(color)
        
        # Write the flags
        flags = 0
        flags = insert_bits(flags, 0, len(self.texMaps), 2)
        flags = insert_bits(flags, 2, len(self.texSRTs), 2)
        flags = insert_bits(flags, 4, len(self.texCoords), 2)
        flags = insert_bits(flags, 6, len(self.tevStages), 2)
        flags = insert_bits(flags, 9, 1 if self.alphaCompare is not None else 0, 1)
        flags = insert_bits(flags, 10, 1 if self.blendModeBlend is not None else 0, 1)
        flags = insert_bits(flags, 11, 1 if self.useTextureOnly else 0, 1)
        flags = insert_bits(flags, 12, 1 if self.blendModeLogic is not None else 0, 1)
        flags = insert_bits(flags, 14, 1 if self.indParam is not None else 0, 1)
        flags = insert_bits(flags, 15, len(self.projTextGenParam), 2)
        flags = insert_bits(flags, 17, 1 if self.fontShadowParam is not None else 0, 1)
        data.write_uint32(flags)
        
        # Loop through each texture map
        for texMap in self.texMaps:
            # Write the texture map
            data = texMap.write(data)
        
        # Loop through each texture SRT
        for texSRT in self.texSRTs:
            # Write the texture SRT
            data = texSRT.write(data)
        
        # Loop through each texture coordinate
        for texCoord in self.texCoords:
            # Write the texture coordinate
            data = texCoord.write(data)
        
        # Loop through each tev stage
        for tevStage in self.tevStages:
            # Write the tev stage
            data = tevStage.write(data)
        
        # Write the alpha compare
        if self.alphaCompare is not None:
            data = self.alphaCompare.write(data)
        
        # Write the blend mode
        if self.blendModeBlend is not None:
            data = self.blendModeBlend.write(data)
        
        # Write the logic blend mode
        if self.blendModeLogic is not None:
            data = self.blendModeLogic.write(data)
        
        # Write the indirect parameter
        if self.indParam is not None:
            data = self.indParam.write(data)
        
        # Write the projection texture generation parameters
        for projTextGenParam in self.projTextGenParam:
            # Write the projection texture generation parameter
            data = projTextGenParam.write(data)
        
        # Write the font shadow parameter
        if self.fontShadowParam is not None:
            data = self.fontShadowParam.write(data)
        
        # Return the data stream
        return data

    
    def __str__(self) -> str:
        j = JsonSerialize()
        j.add("name", self.name)
        j.add("tevColor", self.tevColor)
        j.add("tevConstantColors", self.tevConstantColors)
        # j.add("flags", self.flags)
        j.add("useTextureOnly", self.useTextureOnly)
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
        