from ctr.util.data_stream import DataStream
from ctr.lib.lms.common.lmsBlocks import lmsItemBlock
from ctr.lib.lms.common.lmsCommonTypes import tag


class TAG2:
    """A class representing a TAG2 block"""

    def __init__(self, data: DataStream = None):
        self.data: DataStream = data
        self.tag2Block: lmsItemBlock = lmsItemBlock(self.data, tag)
        self.tags: list[tag] = self.tag2Block.entries
