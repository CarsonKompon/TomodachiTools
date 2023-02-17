from util.data_stream import DataStream

class block:
    # TODO: Support data parsing
    "A class representing a block in a MSBP file"
    def __init__(self, data: DataStream):
        self.data = data
        self.entries: dict
    
    def read(self, overSeeking=False):
        """Reads a block from a self.data stream"""
        self.sectionSize = self.data.read_int32()
        # Skip padding
        self.data.read_bytes(8)
        # Save where the offsets are relative for seeking later
        relativeStart = self.data.tell()
        self.numberOfHashEntries = self.data.read_int32()

        self.data.read_bytes(4)
        
        self.entries = self.readLabelBlock(relativeStart, self.numberOfHashEntries, overSeeking=overSeeking)

        self.seekToEndOfSection(self.data)
        
        return self.entries

    def getHashOffsets(self, numberOfEntries: int) -> list:
        hashOffsets = []
        for _ in range(0, numberOfEntries):
            hashOffsets.append(self.data.read_uint32())
            self.data.read_bytes(4)
        return hashOffsets
    
    def seekToEndOfSection(self, data: DataStream):
        byte = data.read_bytes(1)
        while byte == b"\xab":
            byte = data.read_bytes(1)
        data.seek(data.tell() - 1)

    def readLabelBlock(self, relativeStart: int, numberOfEntries: int, overSeeking=False) -> dict:
        entries = []
        hashOffsets = self.getHashOffsets(numberOfEntries)
        for offset in hashOffsets:
            self.data.seek(relativeStart)
            if overSeeking:
                offset = offset if hashOffsets.index(
                    offset) != len(hashOffsets) - 1 else offset - 9

            self.data.seek(offset, 1)
            labelLength = self.data.read_uint8()

            # Sometimes a unicode decode error will occur when the stream 
            # goes past the bounds of the block, a simple try except will do for now
            try:
                label = self.data.read_string(labelLength)
            except UnicodeDecodeError:
                break
            index = self.data.read_uint32()
            entry = {}
            entry[label] = {"Offset": offset, "Index": index}
            entries.append(entry)
        
        return entries
