from ctr.util.data_stream import DataStream
from ctr.lib.lms.common.lmsBlocks import lmsItemBlock
from ctr.lib.lms.common.lmsCommonTypes import contentInfo


class CTI1:
    """A class representing CTI1 block"""

    def __init__(self, data: DataStream = None) -> None:
        self.data: DataStream = data
        self.cti1Block: lmsItemBlock = lmsItemBlock(self.data, contentInfo)
        self.contentInfo: list[contentInfo] = self.cti1Block.entries
