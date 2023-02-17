from ctr.util.data_stream import DataStream


class CLR1:
    "A class representing a CLR1, color RGBA data block"

    def __init__(self, data: DataStream = None):
        self.colors = []
        if data is not None:
            self.read(data)

    def read(self, data: DataStream) -> None:
        """Reads the CLR1 section from a data stream"""
        self.sectionSize = data.read_int32()

        # Skip padding
        data.read_bytes(8)
        self.numberOfColors = data.read_int32()

        for _ in range(self.numberOfColors):
            color = data.read_color_rgba8()
            self.colors.append(color)

        # Seek to the end of the section
        data.read_bytes(4)
        return data


