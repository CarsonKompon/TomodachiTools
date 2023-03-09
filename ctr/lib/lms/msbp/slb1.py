from ctr.util.data_stream import DataStream
from ctr.lib.lms.common.lmsBlocks import lmsLabelBlock


class SLB1:
    """A class representing a SLB1 block"""

    def __init__(self, data: DataStream = None) -> None:
        self.data = data
        self.block: lmsLabelBlock = lmsLabelBlock(self.data)
        self.entries: dict = self.block.entries
