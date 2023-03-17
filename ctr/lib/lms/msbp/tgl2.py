from ctr.util.data_stream import DataStream
from ctr.lib.lms.common.lmsBlocks import lmsItemBlock
from ctr.lib.lms.common.lmsCommonTypes import tagList


class TGL2:
    """A class representing a TGL2 block"""

    def __init__(self, data: DataStream = None) -> None:
        self.data: DataStream = data
        self.tgl2Block: lmsItemBlock = lmsItemBlock(self.data, tagList)
        self.tagList: list[str] = self.tgl2Block.entries
