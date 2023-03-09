from ctr.util.data_stream import DataStream
from ctr.lib.lms.common.lmsBlocks import lmsItemBlock
from ctr.lib.lms.common.lmsCommonTypes import tagParameter


class TGP2:
    """A class representing a TGP2 block"""

    def __init__(self, data: DataStream = None) -> None:
        self.data: DataStream = data
        self.tgp2block: lmsItemBlock = lmsItemBlock(self.data, tagParameter)
        self.tagParameters: list[tagParameter] = self.tgp2block.entries
