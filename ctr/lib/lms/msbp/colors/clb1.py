from ctr.util.data_stream import DataStream
from ctr.util.blockutil import labelBlock

from ctr.lib.lms.msbp.colors.clr1 import CLR1


class CLB1:
    "A class representing the color labels block in a MSBP files"

    def __init__(self, data: DataStream = None) -> None:
        self.entries: dict = {}
        self.data: DataStream = data
        self.clb1Block: labelBlock = labelBlock(self.entries, data)

    def readLabelData(self, entries, index):
        labelLength = self.data.read_uint8()
        try:
            label = self.data.read_string(labelLength)
        except:
            return
        index = self.data.read_uint32()
        entries[index] = {"Label": label, "Index": index}

    def read(self):
        """Reads the CLB1 section from a data stream"""
        self.clb1Block.read(self.readLabelData, overSeeking=True)
        # Seek to the end of the section
        return self.data

    def combine(self, clr1Data: CLR1) -> dict:
        """Combines label and color data into one dict"""
        for i, key in enumerate(self.entries):
            self.entries[key]["Color"] = {"R": clr1Data.colors[i][0],
                                          "G": clr1Data.colors[i][1],
                                          "B": clr1Data.colors[i][2],
                                          "A": clr1Data.colors[i][3]}
        return self.entries
