from ctr.util.data_stream import DataStream
from ctr.lib.lms.common.lmsBlocks import lmsItemBlock
from ctr.lib.lms.common.lmsCommonTypes import attributeList


class ALI2:
    """A class representing a ALI2 block block"""

    def __init__(self, data: DataStream = None) -> None:
        self.data: DataStream = data
        self.block: lmsItemBlock = lmsItemBlock(self.data, attributeList)
        self.attributeLists: list[attributeList] = self.block.entries
