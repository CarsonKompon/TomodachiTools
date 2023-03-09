from ctr.util.data_stream import DataStream
from ctr.lib.lms.common.lmsBlocks import lmsDataBlock
from ctr.lib.lms.common.lmsCommonTypes import attribute


class ATI2:
    """A class that represents an ATI2 block"""

    def __init__(self, data: DataStream = None) -> None:
        self.data: DataStream = data
        self.block: lmsDataBlock = lmsDataBlock(self.data, attribute)
        self.attributes: list[attribute] = self.block.entries
