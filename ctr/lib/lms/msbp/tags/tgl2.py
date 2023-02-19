from ctr.util.data_stream import DataStream

from ctr.util.blockutil import labelBlock


class TGL2:
    "A class representing the TGL2 (tag lists) block in a MSBP file"

    def __init__(self, data: DataStream = None) -> None:
        self.lists: list = {}
        self.data: DataStream = data
        self.tag2Block: labelBlock = labelBlock(self.lists, data)

    def readLists(self, entries, index):
        entries[index] = self.data.read_string_nt()

    def read(self):
        """Reads the TGL2 section from a data stream"""
        self.tag2Block.read(self.readLists, hasExtraData=False)
        return self.data
