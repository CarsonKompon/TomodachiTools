from ctr.util.data_stream import DataStream

from ctr.util.blockutil import labelBlock


class CTI1:
    "A class representing the CTI1 (project content info) block in a MSBP file"

    def __init__(self, data: DataStream = None) -> None:
        self.info: dict = {}
        self.data: DataStream = data
        self.cti1block: labelBlock = labelBlock(self.info, data)

    def readInfo(self, entries, index):
        entries[index] = self.data.read_string_nt()

    def read(self):
        """Reads the CTI1 section from a data stream"""
        self.cti1block.read(self.readInfo, hasExtraData=False)
        return self.data
