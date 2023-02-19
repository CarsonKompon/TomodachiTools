from ctr.util.data_stream import DataStream

from ctr.util.blockutil import labelBlock


class SYL3:
    "A class representing the SYL3 (styles) block in a MSBP file"

    def __init__(self, data: DataStream = None) -> None:
        self.styles: list = []
        self.data: DataStream = data

    def read(self) -> None:
        """Reads the SYL3 section from a data stream"""
        self.sectionSize = self.data.read_int32()

        self.data.read_bytes(8)
        relativeStart = self.data.tell()
        self.numberOfStyles = self.data.read_int32()

        styleIndex = 0
        for _ in range(self.numberOfStyles):
            entry = {}
            regionWidth = self.data.read_uint32()
            lineNum = self.data.read_uint32()
            fontIndex = self.data.read_uint32()
            baseColorIndex = self.data.read_color_rgba8()
            entry[styleIndex] = {"Region width":
                                 regionWidth, "Line number": lineNum,
                                 "Font index": fontIndex, "Base color index": baseColorIndex}
            self.styles.append(entry)
            styleIndex += 1
        labelBlock.seekToEndOfSection(
            relativeStart, self.sectionSize, self.data)
        return self.data
