from ctr.util.data_stream import DataStream
from ctr.lib.lms.common.lmsBlocks import lmsDataBlock
from ctr.lib.lms.common.lmsCommonTypes import color


class CLR1:
    """A class representing a CLR1 block"""

    def __init__(self, data: DataStream = None):
        self.data: DataStream = data
        self.block: lmsDataBlock = lmsDataBlock(self.data, color)
        self.colors: list = self.block.entries
