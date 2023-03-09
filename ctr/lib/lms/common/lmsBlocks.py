from ctr.util.data_stream import DataStream
from ctr.lib.lms.common.lmsCommonTypes import label, dataOffsetEntry, itemOffsetEntry


class lmsBlockHeader:
    """A class that represents the header of a LMS block"""

    def __init__(self, data: DataStream):
        self.data: DataStream = data
        self.blockSize: int = self.data.read_uint32()
        self.data.read_bytes(8)
        self.relativeStart: int = self.data.tell()
        self.numberOfEntries: int = self.data.read_uint32()

    def seekToEndOfSection(self) -> None:
        """Function for seeking to the end of the section"""
        self.data.seek(self.relativeStart)
        self.data.seek(self.blockSize, 1)
        byte = self.data.read_bytes(1)
        while byte == b"\xab":
            byte = self.data.read_bytes(1)
        self.data.seek(self.data.tell() - 1)


class lmsDataBlock(lmsBlockHeader):
    """A class that represents a data block
    The following blocks are considered as data

    CLR1 (MSBP)
    ATI2 (MSBP)
    SYL3 (MSBP)
    """

    def __init__(self, data: DataStream, entryType):
        super().__init__(data)
        self.entries: list = []
        for _ in range(self.numberOfEntries):
            entry: entryType = entryType(self.data)
            self.entries.append(entry)
        self.seekToEndOfSection()


class lmsItemBlock(lmsBlockHeader):
    """A class that represents an item block
    The following blocks are considered as item

    ALI2 (MSBP)
    TXT2 (MSBT)
    TAG2 (MSBP)
    TGP2 (MSBP)
    TGP2 (MSBP)
    CTI1 (MSBP)
    """

    def __init__(self, data: DataStream, entryType):
        super().__init__(data)
        self.entries: list = []
        self.entryType = entryType

        itemOffsets: list[int] = []
        for _ in range(self.numberOfEntries):
            itemData: itemOffsetEntry = itemOffsetEntry(self.data)
            itemOffsets.append(itemData)

        for itemData in itemOffsets:
            self.data.seek(self.relativeStart)
            self.data.seek(itemData.offset, 1)
            entry: entryType = entryType(self.data)
            self.entries.append(entry)

        self.seekToEndOfSection()


class lmsLabelBlock(lmsBlockHeader):
    """A class that represents a label block. 
    The following blocks are considered as label:

      - LBL1 (MSBT)
      - CLB1 (MSBP)
      - ALB1 (MSBP)
      - SLB1 (MSBP)
      - FEN1 (MSBF)
    """

    def __init__(self, data: DataStream):
        super().__init__(data)
        self.entries: list[label] = []

        dataEntries: list[dataOffsetEntry] = []
        for _ in range(self.numberOfEntries):
            entry: dataOffsetEntry = dataOffsetEntry(self.data)
            dataEntries.append(entry)

        for entry in dataEntries:
            self.data.seek(self.relativeStart)
            self.data.seek(entry.offset, 1)
            for _ in range(entry.labelCount):
                labelData: label = label(self.data)
                self.entries.append(labelData)
        
        self.seekToEndOfSection()
