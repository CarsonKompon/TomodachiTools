from ctr.util.data_stream import DataStream
from ctr.lib.lms.common.lmsBlocks import lmsLabelBlock


class CLB1:
    """A class representing a CLB1 block"""

    def __init__(self, data: DataStream = None) -> None:
        self.data = data
        self.labelBlock = lmsLabelBlock(self.data)
        self.entries: dict = self.labelBlock.entries
