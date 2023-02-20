from ctr.util.data_stream import DataStream
from ctr.util.blockutil import labelBlock

from ctr.lib.lms.msbp.tags.tag2 import TAG2
from ctr.lib.lms.msbp.tags.tgp2 import TGP2
from ctr.lib.lms.msbp.tags.tgl2 import TGL2


class TGG2:
    "A class representing the TGGP (tag group) block in a MSBP file"

    def __init__(self, data: DataStream = None) -> None:
        self.groups: dict = {}
        self.data: DataStream = data
        self.tgg2Block: labelBlock = labelBlock(self.groups, data)

    def readGroups(self, entries, groupIndex):
        numberOfTags = self.data.read_uint16()
        tagIndexes = []
        for _ in range(numberOfTags):
            # Get the index
            index = self.data.read_uint16()
            tagIndexes.append(index)
        # Get the tag group name
        tagGroup = self.data.read_string_nt()
        entries[f"group{groupIndex}"] = {"Group": tagGroup,  "tagIndexes": tagIndexes}

    def read(self):
        """Reads the TGG2 section from a data stream"""
        self.tgg2Block.read(self.readGroups, hasExtraData=False)
        return self.data


    def combine(self, tag2Data: TAG2, tgp2Data: TGP2, tgl2Data: TGL2):
        tags = tag2Data.tags
        parameters = tgp2Data.parameters
        tagLists = tgl2Data.lists

        for parameterIndex in parameters:
            items = []
            for tagListIndex in parameters[parameterIndex]["listItemIndexes"]:
                items.append(tagLists[tagListIndex])
                parameters[parameterIndex]["tagListItems"] = items

                
        for tagIndex in tags:
            tags[tagIndex]["parameterMetaData"] = {}
            for parameterIndex in tags[tagIndex]["parameterIndexes"]:
                tags[tagIndex]["parameterMetaData"][parameterIndex] = parameters[parameterIndex]

        # Compile all the data into one and add it the groups

        for groupIndex in self.groups:
            self.groups[f"{groupIndex}"]["tagMetaData"] = {}
            for tagIndex in self.groups[groupIndex]["tagIndexes"]:
                self.groups[f"{groupIndex}"]["tagMetaData"][tagIndex] = tags[f"tag{tagIndex}"]

        return self.groups