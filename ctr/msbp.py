import json
import operator

from ctr.lib.lms.common.lmsHeader import lmsBinaryHeader
from ctr.lib.lms.msbp.alb1 import ALB1
from ctr.lib.lms.msbp.ali2 import ALI2
from ctr.lib.lms.msbp.ati2 import ATI2
from ctr.lib.lms.msbp.clb1 import CLB1
from ctr.lib.lms.msbp.clr1 import CLR1
from ctr.lib.lms.msbp.cti1 import CTI1
from ctr.lib.lms.msbp.slb1 import SLB1
from ctr.lib.lms.msbp.syl3 import SYL3
from ctr.lib.lms.msbp.tag2 import TAG2
from ctr.lib.lms.msbp.tgg2 import TGG2
from ctr.lib.lms.msbp.tgl2 import TGL2
from ctr.lib.lms.msbp.tgp2 import TGP2
from ctr.util.data_stream import DataStream
from ctr.util.serialize import JsonSerialize


class Msbp:
    """A class that repersents a Message Studio Binary Project file"""

    def __init__(self, filepath: str = None):
        self.filepath: str = filepath
        if filepath is not None:
            self.parse()

    def __str__(self):
        j: JsonSerialize = JsonSerialize()
        colorData: dict = {}
        attributeData: dict = {}
        tagData: dict = {}
        styleData: dict = {}
        contentInfo: list[str] = []

        # Sort each list so the items are in order
        self.clb1.entries = sorted(
            self.clb1.entries, key=operator.attrgetter("itemIndex"))
        self.alb1.entries = sorted(
            self.alb1.entries, key=operator.attrgetter("itemIndex"))
        self.slb1.entries = sorted(
            self.slb1.entries, key=operator.attrgetter("itemIndex"))

        # Colors
        for entry in self.clb1.entries:
            colorData[entry.label] = self.clr1.colors[entry.itemIndex].color

        # Attributes
        for entry in self.alb1.entries:
            attribute = self.ati2.attributes[entry.itemIndex]
            type: int = attribute.type
            listIndex: int = attribute.listIndex
            offset: int = attribute.offset
            if attribute.type == 9:
                listItems: list = self.ali2.attributeLists[listIndex].list
                attributeData[entry.label] = {
                    "type": type, "offset": offset, "listItems": listItems}
            else:
                attributeData[entry.label] = {"type": type, "offset": offset}

        # Tags
        for entry in self.tgg2.tagGroups:
            groupName: str = entry.groupName
            tagCount: int = entry.tagCount
            tagIndexes: list[int] = entry.tagIndexes

            tagData[groupName] = {"tagCount": tagCount,
                                  "tagIndexes": tagIndexes, "tags": {}}
            for index in tagIndexes:
                tagName: str = self.tag2.tags[index].name
                parameterCount: int = self.tag2.tags[index].parameterCount
                parameterIndexes: list = self.tag2.tags[index].parameterIndexes
                tagData[groupName]["tags"][tagName] = {
                    "parameterCount": parameterCount, "parameterIndexes": parameterIndexes, "parameters": {}}
                for parameterIndex in parameterIndexes:
                    parameterName: str = self.tgp2.tagParameters[parameterIndex].parameterName
                    parameterType: int = self.tgp2.tagParameters[parameterIndex].type
                    if parameterType != 9:
                        tagData[groupName]["tags"][tagName]["parameters"][parameterName] = {
                            "listItemCount": 0, "listItemIndexes": [], "listItems": {}}
                    else:
                        listItemCount: int = self.tgp2.tagParameters[parameterIndex].ListItemCount
                        listItemIndexes: int = self.tgp2.tagParameters[parameterIndex].ListItemIndexes
                        listItems: list[str] = []
                        tagData[groupName]["tags"][tagName]["parameters"][parameterName] = {
                            "listItemCount": listItemCount, "listItemIndexes": listItemIndexes, "listItems": {}}
                        for listIndex in listItemIndexes:
                            listItems.append(self.tgl2.tagList[listIndex].item)
                        tagData[groupName]["tags"][tagName]["parameters"][parameterName]["listItems"] = listItems

        # Styles
        for entry in self.slb1.entries:
            regionWidth: int = self.syl3.styles[entry.itemIndex].regionWidth
            lineNumber: int = self.syl3.styles[entry.itemIndex].lineNumber
            fontIndex: int = self.syl3.styles[entry.itemIndex].fontIndex
            baseColorIndex: tuple = self.syl3.styles[entry.itemIndex].baseColorIndex

            styleData[entry.label] = {"regionWidth": regionWidth, "lineNumber": lineNumber,
                                        "fontIndex": fontIndex, "baseColorIndex": baseColorIndex}
        # Content info
        for entry in self.cti1.contentInfo:
            contentInfo.append(entry.sourceFile)
        j.add("header", {
            "byteorderMark": self.header.byteOrderMark,
            "revision": self.header.revision,
            "messageEncoding": self.header.messageEncoding,
            "numberOfBlocks": self.header.blockCount,
            "fileSize": self.header.fileSize
        })

        j.add("colorData", colorData)
        j.add("attributeData", attributeData)
        j.add("tagData", tagData)
        j.add("styleData", styleData)
        j.add("contentInfo", contentInfo)

        return json.dumps(json.loads(j.serialize()), indent=3)

    def to_json(self, jsonFilename: str) -> None:
        """Writes a json file containing serialized MSBP data"""
        with open(jsonFilename, "w+") as j:
            j.write(json.dumps(json.loads(str(self)), indent=2))
            print(f"{jsonFilename} has been created!")

    def parse(self) -> None:
        with open(self.filepath, "rb") as d:
            data: DataStream = DataStream(d)
            self.header: lmsBinaryHeader = lmsBinaryHeader(data)
            for _ in range(self.header.blockCount):
                magic: str = data.read_string(4)
                match magic:
                    case "CLR1":
                        self.clr1: CLR1 = CLR1(data)
                    case "CLB1":
                        self.clb1: CLB1 = CLB1(data)
                    case "ATI2":
                        self.ati2: ATI2 = ATI2(data)
                    case "ALB1":
                        self.alb1: ALB1 = ALB1(data)
                    case "ALI2":
                        self.ali2: ALI2 = ALI2(data)
                    case "TGG2":
                        self.tgg2: TGG2 = TGG2(data)
                    case "TAG2":
                        self.tag2: TAG2 = TAG2(data)
                    case "TGP2":
                        self.tgp2: TGP2 = TGP2(data)
                    case "TGL2":
                        self.tgl2: TGL2 = TGL2(data)
                    case "SYL3":
                        self.syl3: SYL3 = SYL3(data)
                    case "SLB1":
                        self.slb1: SLB1 = SLB1(data)
                    case "CTI1":
                        self.cti1: CTI1 = CTI1(data)
