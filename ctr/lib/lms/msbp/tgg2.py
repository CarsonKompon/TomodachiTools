from ctr.util.data_stream import DataStream
from ctr.lib.lms.common.lmsBlocks import lmsItemBlock
from ctr.lib.lms.common.lmsCommonTypes import tagGroup


class TGG2:
    """A class representing a TGG2 block"""

    def __init__(self, data: DataStream = None):
        self.data: DataStream = data
        self.tgg2Block: lmsItemBlock = lmsItemBlock(self.data, tagGroup)
        self.tagGroups: list[tagGroup] = self.tgg2Block.entries
