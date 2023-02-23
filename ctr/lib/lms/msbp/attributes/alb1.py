from util.data_stream import DataStream


class ALB1:
    "A class repersenting the color labels block in a MSBP files"

    def __init__(self, data: DataStream = None) -> None:
        self.entries = {}
        if data is not None:
            self.read(data)

    def read(self, data: DataStream):
        """Reads the ALB1 section from a data stream"""
        self.sectionSize = data.read_int32()

        data.read_bytes(8)

        relativeStart = data.tell()

        self.numberOfHashEntries = data.read_int32()

        hashOffsets = []
        data.read_bytes(4)

        for _ in range(self.numberOfHashEntries):
            hashOffsets.append(data.read_uint32())
            data.read_bytes(4)
        count = 0
        for offset in hashOffsets:
            print(count, offset)
            count += 1
            data.seek(relativeStart)
           
            data.seek(offset, 1)
            labelLength = data.read_uint8()

            try:
                label = data.read_string(labelLength)
            except UnicodeDecodeError:
                print(label)

            colorIndex = data.read_uint8()
           
            self.entries[f"E{count}"] = label

         # Seek to the end of the section
        data.read_bytes(8)
        return data

       
