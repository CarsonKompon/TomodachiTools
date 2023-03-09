from ctr.util.data_stream import DataStream
from ctr.lib.lms.common.lmsBlocks import lmsDataBlock
from ctr.lib.lms.common.lmsCommonTypes import style


class SYL3:
    """A class representing a SYL3 block"""

    def __init__(self, data: DataStream = None):
        self.data: DataStream = data
        self.block: lmsDataBlock = lmsDataBlock(self.data, style)
        self.styles: list[style] = self.block.entries
