from ctr.util.data_stream import DataStream

from ctr.util.blockutil import labelBlock


class ALI2:
    "A class representing a ALI2 block (attribute lists) block in a MSBP file "

    def __init__(self, data: DataStream = None) -> None:
        self.attributeLists = {}
        self.data: DataStream = data

    def read(self):
        """Reads the ALI2 section from a data stream"""
        # TODO: Move code to one for loop so its less cluttered
        self.sectionSize = self.data.read_int32()

        # Skip padding
        self.data.read_bytes(8)
        relativeStart = self.data.tell()
        self.numberOfLists = self.data.read_int32()

        listCount = 0
        startOffsets = []

        # Get the attribute list start offsets
        for _ in range(self.numberOfLists):
            startOffsets.append(self.data.read_uint32())

        # Loop through each start offset, then loop through the attribute list item offsets and append it to a new list
        for offset in startOffsets:
            listItemOffsets = []
            attributeList = []
            self.data.seek(relativeStart)
            self.data.seek(offset, 1)

            # Offsets for list items are stored relative to the number of offsets
            # This is the exact same as regular label blocks
            relativeListItemStart = self.data.tell()

            amountOfItems = self.data.read_uint32()
            for _ in range(amountOfItems):
                listItemOffsets.append(self.data.read_uint32())

            for startListItemOffset in listItemOffsets:
                # Seek to the relative start offset then read each item
                self.data.seek(relativeListItemStart)
                self.data.seek(startListItemOffset, 1)
                listItem = self.data.read_string_nt()
                attributeList.append(listItem)

            self.attributeLists[listCount] = attributeList
            listCount += 1

        labelBlock.seekToEndOfSection(
            relativeStart, self.sectionSize, self.data)
        return self.data
