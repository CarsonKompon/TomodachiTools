from ctr.util.data_stream import DataStream

from ctr.util.blockutil import block

class CLB1:
    "A class representing the color labels block in a MSBP files"

    def __init__(self, data: DataStream = None) -> None:
        self.entries: dict
        self.data: DataStream = data
        self.clb1Block: block = block(data)

    def read(self):
        """Reads the CLB1 section from a data stream"""
        self.entries = self.clb1Block.read(overSeeking=True)
         # Seek to the end of the section
        return self.data

       
