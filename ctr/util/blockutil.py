from ctr.util.data_stream import DataStream


class labelBlock:
    # TODO: Support data parsing
    "A class representing a label block for the LMS library"

    def __init__(self, entries, data: DataStream):
        self.entries = entries
        self.data = data

        self.sectionSize = self.data.read_int32()
        self.data.read_bytes(8)
        self.relativeStart = self.data.tell()
        self.numberOfEntries = self.data.read_int32()

    def read(self, readFunction, overSeeking=False, hasExtraData=True) -> None:
        """Reads a block from a data stream. Uses a function for custom behaviour after each seek"""
        if hasExtraData == True:
            self.data.read_bytes(4)

        index = 0

        hashOffsets = self.getOffsets(
            self.numberOfEntries, hasExtraData=hasExtraData)
        for offset in hashOffsets:

            self.data.seek(self.relativeStart)
            if overSeeking:
                offset = offset if hashOffsets.index(
                    offset) != len(hashOffsets) - 1 else offset - 9

            self.data.seek(offset, 1)
            # Run the custom behaviour
            readFunction(self.entries, index)
            index += 1

        data = self.seekToEndOfSection(
            self.relativeStart, self.sectionSize, self.data)
        return self.entries

    def getOffsets(self, numberOfEntries: int, hasExtraData=True) -> list:
        """Function for appending all the offsets to each item in a block  into a list."""
        hashOffsets = []
        for _ in range(numberOfEntries):
            hashOffsets.append(self.data.read_uint32())
            # HasExtraData determines if a block
            if hasExtraData:
                self.data.read_bytes(4)

        return hashOffsets

    @staticmethod
    def seekToEndOfSection(relativeStart: int, sectionSize: int, data: DataStream) -> None:
        data.seek(relativeStart)
        data.seek(sectionSize, 1)
        byte = data.read_bytes(1)
        while byte == b"\xab":
            byte = data.read_bytes(1)
        data.seek(data.tell() - 1)

        return data
