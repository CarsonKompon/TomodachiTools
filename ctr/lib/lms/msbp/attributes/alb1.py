from ctr.util.data_stream import DataStream
from ctr.util.blockutil import labelBlock

from ctr.lib.lms.msbp.attributes.ati2 import ATI2
from ctr.lib.lms.msbp.attributes.ali2 import ALI2

class ALB1:
    "A class representing the attribute labels block in a MSBP file"

    def __init__(self, data: DataStream = None) -> None:
        self.entries = {}
        self.data: DataStream = data
        self.alb1Block: labelBlock = labelBlock(self.entries, data)

    def readLabelData(self, entries, index):
        labelLength = self.data.read_uint8()
        try:
            label = self.data.read_string(labelLength)
        except:
            return
        index = self.data.read_uint32()
        entries[index] = {"Label": label}

    def read(self):
        """Reads the ALB1 section from a data stream"""
        self.entries = self.alb1Block.read(self.readLabelData)
        return self.data

    def combine(self, ati2Data: ATI2, ali2Data: ALI2):
        attributeData = ati2Data.attributes
        for attributeIndex in attributeData:
            if attributeData[attributeIndex]["type"] == 9:
                attributeData[attributeIndex]["attributeList"] = ali2Data.attributeLists[attributeData[attributeIndex]["listIndex"]]
        
        # Attributes need to be sorted, as a lot of unused ones create gaps between the indexes
        # this might appear as a bug to the user
        sortedIndexes = []
        for attributeIndex in self.entries:
            sortedIndexes.append(attributeIndex)

        for attributeIndex in sorted(sortedIndexes):
            try:
                self.entries[attributeIndex]["attributeData"] = attributeData[attributeIndex]
            except KeyError:
                # Sometimes an item will be present but no offset will point to it
                self.entries[attributeIndex]["attributeData"] = "NO OFFSET ENTRY FOUND"
                
        return self.entries