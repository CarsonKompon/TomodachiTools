from ctr.util.data_stream import DataStream

from ctr.util.blockutil import block

class ALB1:
    "A class representing the attribute labels block in a MSBP file"

    def __init__(self, data: DataStream = None) -> None:
        self.entries = {}
        self.data: DataStream = data
        self.alb1Block: block = block(data)

    def read(self):
        """Reads the ALB1 section from a data stream"""
        self.entries = self.alb1Block.read()
        return self.data
