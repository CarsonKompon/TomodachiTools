from ctr.util.data_stream import DataStream
from ctr.util.blockutil import labelBlock

from ctr.lib.lms.msbp.tags.tag2 import TAG2
from ctr.lib.lms.msbp.tags.tgp2 import TGP2
from ctr.lib.lms.msbp.tags.tgl2 import TGL2


class TGG2:
    "A class representing the TGGP (tag group) block in a MSBP file"

    def __init__(self, data: DataStream = None) -> None:
        self.groups: dict = {}
        self.data: DataStream = data
        self.tgg2Block: labelBlock = labelBlock(self.groups, data)

    def readGroups(self, entries, groupIndex):
        numberOfTags = self.data.read_uint16()
        tagIndexes = []
        for _ in range(numberOfTags):
            # Get the index
            index = self.data.read_uint16()
            tagIndexes.append(index)
        # Get the tag group name
        tagGroup = self.data.read_string_nt()
        entries[groupIndex] = {"Group": tagGroup,  "tagIndexes": tagIndexes}

    def read(self):
        """Reads the TGG2 section from a data stream"""
        self.tgg2Block.read(self.readGroups, hasExtraData=False)
        return self.data
