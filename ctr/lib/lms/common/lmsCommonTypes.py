from ctr.util.data_stream import DataStream


class label:
    """A class that represents a label"""

    def __init__(self, d: DataStream):
        self.data: DataStream = d
        labelLength: int = self.data.read_uint8()
        self.label: str = self.data.read_string(labelLength)
        self.itemIndex: int = self.data.read_uint32()


class dataOffsetEntry:
    """A class that represents a data offset entry"""

    def __init__(self, d: DataStream):
        self.data: DataStream = d
        self.labelCount: int = self.data.read_uint32()
        self.offset: int = self.data.read_uint32()


class itemOffsetEntry:
    """A class that represents an item offset entry"""

    def __init__(self, d: DataStream):
        self.data: DataStream = d
        self.offset: int = self.data.read_uint32()


class color:
    """A class that represents a color"""

    def __init__(self, d: DataStream):
        self.data: DataStream = d
        self.color: tuple = self.data.read_color_rgba8()


class attribute:
    """A class that represents an attribute"""

    def __init__(self, d: DataStream):
        self.data: DataStream = d
        self.type: int = self.data.read_uint8()
        self.data.read_bytes(1)
        self.listIndex: int = self.data.read_uint16()
        self.offset: int = self.data.read_uint32()


class attributeList:
    """A class that represents an attribute list"""

    def __init__(self, d: DataStream):
        self.data: DataStream = d
        self.list: list[str] = []
        itemOffsets: list[int] = []
        relativeStart = self.data.tell()
        itemCount = self.data.read_uint32()
        for _ in range(itemCount):
            itemOffsets.append(self.data.read_uint32())
        for offset in itemOffsets:
            self.data.seek(relativeStart)
            self.data.seek(offset, 1)
            listItem = self.data.read_string_nt()
            self.list.append(listItem)


class tagGroup:
    """A class that represents a tag group"""

    def __init__(self, d: DataStream):
        self.data: DataStream = d
        self.tagCount: int = self.data.read_uint16()
        self.tagIndexes: list[int] = []
        for _ in range(self.tagCount):
            index = self.data.read_uint16()
            self.tagIndexes.append(index)
        self.groupName: str = self.data.read_string_nt()


class tag:
    """A class that represents a tag"""

    def __init__(self, d: DataStream):
        self.data: DataStream = d
        self.parameterCount: int = self.data.read_uint16()
        self.parameterIndexes: list[int] = []
        for _ in range(self.parameterCount):
            parameterIndex: int = self.data.read_uint16()
            self.parameterIndexes.append(parameterIndex)
        self.name: str = self.data.read_string_nt()


class tagParameter:
    """A class that represents a tag parameter"""

    def __init__(self, d: DataStream):
        self.data: DataStream = d
        self.type: int = self.data.read_uint8()
        if self.type != 9:
            self.parameterName: str = self.data.read_string_nt()
        else:
            self.data.read_bytes(1)
            self.ListItemIndexes: list[int] = []
            self.ListItemCount: int = self.data.read_uint16()
            for _ in range(self.ListItemCount):
                index = self.data.read_uint16()
                self.ListItemIndexes.append(index)
            self.parameterName: str = self.data.read_string_nt()


class tagList:
    def __init__(self, d: DataStream):
        """A class that represents a tag list"""
        self.data: DataStream = d
        self.item: str = self.data.read_string_nt()


class style:
    """A class that represents a style"""

    def __init__(self, d: DataStream):
        self.data: DataStream = d
        self.regionWidth: int = self.data.read_uint32()
        self.lineNumber: int = self.data.read_uint32()
        self.fontIndex: int = self.data.read_uint32()
        self.baseColorIndex: tuple = self.data.read_color_rgba8()


class contentInfo:
    def __init__(self, d: DataStream):
        """A class that represents content info"""
        self.data: DataStream = d
        self.sourceFile: str = self.data.read_string_nt()
