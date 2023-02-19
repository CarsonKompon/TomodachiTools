from ctr.util.data_stream import DataStream

from ctr.util.blockutil import labelBlock


class ALB1:
    "A class representing the attribute labels block in a MSBP file"

    def __init__(self, data: DataStream = None) -> None:
        self.entries = {}
        self.data: DataStream = data
        self.alb1Block: labelBlock = labelBlock(self.entries, data)

    def readLabelData(self, entries, index):
        labelLength = self.data.read_uint8()
        try:
            label = self.data.read_string(labelLength)
        except:
            return
        index = self.data.read_uint32()
        entries[index] = {"Label": label}

    def read(self):
        """Reads the ALB1 section from a data stream"""
        self.entries = self.alb1Block.read(self.readLabelData)
        return self.data
