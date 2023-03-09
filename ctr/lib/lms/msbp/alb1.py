from ctr.util.data_stream import DataStream
from ctr.lib.lms.common.lmsBlocks import lmsLabelBlock


class ALB1:
    """A class representing an ALB1 block"""

    def __init__(self, data: DataStream = None):
        self.data = data
        self.block: lmsLabelBlock = lmsLabelBlock(self.data)
        self.entries: dict = self.block.entries
