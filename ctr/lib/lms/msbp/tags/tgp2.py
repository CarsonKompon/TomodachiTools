from ctr.util.data_stream import DataStream

from ctr.util.blockutil import labelBlock


class TGP2:
    "A class representing the TGP2 (tag parameter) block in a MSBP file"

    def __init__(self, data: DataStream = None) -> None:
        self.parameters: dict = {}
        self.data: DataStream = data
        self.tag2Block: labelBlock = labelBlock(self.parameters, data)

    def readParameters(self, entries, index):
        listItemIndexes = []
        parameterType = self.data.read_uint8()
        if parameterType != 9:
            parameter = self.data.read_string_nt()
        # Handling TGL2 indexes
        else:
            # Skip padding
            self.data.read_bytes(1)
            # Read the amount of list items
            numberOfListItems = self.data.read_uint16()
            for _ in range(numberOfListItems):
                # Append them to a list, items that are not type 9 are displayed with an empty array
                index = self.data.read_uint16()
                listItemIndexes.append(index)
            parameter = self.data.read_string_nt()
        
        if listItemIndexes == []:
            entries[index] = {"parameter": parameter, "type": parameterType}
        else:
            entries[index] = {"parameter": parameter, "type": parameterType,
                             "listItemIndexes": listItemIndexes}
    

    def read(self):
        """Reads the TGP2 section from a data stream"""
        self.tag2Block.read(self.readParameters, hasExtraData=False)
        return self.data
