from ctr.util.data_stream import DataStream

from ctr.util.blockutil import labelBlock


class TAG2:
    "A class representing the TAG2 (tags) block in a MSBP file"

    def __init__(self, data: DataStream = None) -> None:
        self.tags: dict = {}
        self.data: DataStream = data
        self.tag2Block: labelBlock = labelBlock(self.tags, data)

    def readTags(self, entries, index):
        # Get the amount of parameters then its indexes
        numberOfTagParameters = self.data.read_uint16()
        tagParameterIndexes = []
        for _ in range(numberOfTagParameters):
            parameterIndex = self.data.read_uint16()
            tagParameterIndexes.append(parameterIndex)
        tag = self.data.read_string_nt()
        entries[index] = {"Tag": tag, "parameterIndexes": tagParameterIndexes}

    def read(self):
        """Reads the TAG2 section from a data stream"""
        self.tag2Block.read(self.readTags, hasExtraData=False)
        return self.data
