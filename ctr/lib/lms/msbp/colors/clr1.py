from util.data_stream import DataStream

from util.blockutil import block

class CLR1:
    "A class representing a CLR1, color RGBA data block"

    def __init__(self, data: DataStream = None):
        self.data = data
        self.clr1Block = block(data)
        self.colors = []

    def read(self) -> None:
        """Reads the CLR1 section from a data stream"""
        self.sectionSize = self.data.read_int32()

        # Skip padding
        self.data.read_bytes(8)
        self.numberOfColors = self.data.read_int32()

        for _ in range(self.numberOfColors):
            color = self.data.read_color_rgba8()
            self.colors.append(color)

        self.clr1Block.seekToEndOfSection(self.data)
        return self.data


