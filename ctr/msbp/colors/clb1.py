from util.data_stream import DataStream


class CLB1:
    "A class repersenting the color labels block in a MSBP files"

    def __init__(self, data: DataStream = None) -> None:
        self.entries = {}
        if data is not None:
            self.read(data)

    def read(self, data: DataStream):
        """Reads the CLB1 section from a data stream"""
        self.sectionSize = data.read_int32()

        # Skip padding
        data.read_bytes(8)

        # Save where the offsets are relative for seeking later
        relativeStart = data.tell()

        # This is always constant (0x1D) no matter if they're less colors
        # It is unknown to why this is th case
        self.numberOfHashEntries = data.read_int32()

        hashOffsets = []
        data.read_bytes(4)

        for _ in range(self.numberOfHashEntries):
            hashOffsets.append(data.read_uint32())
            data.read_bytes(4)

        for offset in hashOffsets:
            data.seek(relativeStart)
            # The last offset often leads to the ATI2 block when it is not supposed to (unknown why)
            # Subtracitng the by 9 will give us the offset as usual
            offset = offset if hashOffsets.index(
                offset) != len(hashOffsets) - 1 else offset - 9

            data.seek(offset, 1)
            labelLength = data.read_uint8()
            label = data.read_string(labelLength)
            colorIndex = data.read_uint8()

            self.entries[colorIndex] = label

         # Seek to the end of the section
        data.read_bytes(8)
        return data

       
