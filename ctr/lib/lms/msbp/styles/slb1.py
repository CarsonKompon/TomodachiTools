from ctr.util.data_stream import DataStream
from ctr.util.blockutil import labelBlock

from ctr.lib.lms.msbp.styles.syl3 import SYL3


class SLB1:
    "A class representing the SLB1 (style labels) block in a MSBP file"

    def __init__(self, data: DataStream = None) -> None:
        self.entries: dict = {}
        self.data: DataStream = data
        self.slb1Block: labelBlock = labelBlock(self.entries, data)

    def readLabelData(self, entries, index):
        labelLength = self.data.read_uint8()
        try:
            label = self.data.read_string(labelLength)
        except:
            return
        index = self.data.read_uint32()
        entries[index] = {"Label": label, "Index": index}

    def read(self):
        """Reads the SLB1 section from a data stream"""
        self.slb1Block.read(self.readLabelData, overSeeking=True)
        # Seek to the end of the section
        return self.data

    def combine(self, syl3Data: SYL3) -> dict:
        """Combines labela and style data into one dict"""
        for i, key in enumerate(self.entries):
            self.entries[key]["Style Data"] = {"Region Width": syl3Data.styles[i][i]["Region width"],
                                               "Line number": syl3Data.styles[i][i]["Line number"],
                                               "Font index": syl3Data.styles[i][i]["Font index"],
                                               "Base color index": syl3Data.styles[i][i]["Base color index"]}
        return self.entries
