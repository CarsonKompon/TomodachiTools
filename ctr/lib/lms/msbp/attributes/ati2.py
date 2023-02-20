from ctr.util.data_stream import DataStream

from ctr.util.blockutil import labelBlock


class ATI2:
    "A class representing the attribute information block "

    def __init__(self, data: DataStream = None) -> None:
        self.attributes = {}
        self.data: DataStream = data

    def read(self):
        """Reads the ATI2 section from a data stream"""
        self.sectionSize = self.data.read_int32()

        # Skip padding
        self.data.read_bytes(8)
        relativeStart = self.data.tell()
        self.numberOfAttributes = self.data.read_int32()

        attributeCount = 0
        for _ in range(self.numberOfAttributes):
            attributeType = self.data.read_uint8()
            self.data.read_bytes(1)
            listIndex = self.data.read_uint16()
            offset = self.data.read_int32()
            attributeCount += 1

            self.attributes[attributeCount] = {
                "type": attributeType, "listIndex": listIndex}

        labelBlock.seekToEndOfSection(
            relativeStart, self.sectionSize, self.data)
        return self.data
