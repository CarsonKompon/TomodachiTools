import json
from ctr.util.serialize import JsonSerialize
from ctr.util.data_stream import DataStream

from ctr.lib.lms.msbp.attributes.alb1 import ALB1
from ctr.lib.lms.msbp.attributes.ali2 import ALI2
from ctr.lib.lms.msbp.attributes.ati2 import ATI2
from ctr.lib.lms.msbp.colors.clb1 import CLB1
from ctr.lib.lms.msbp.colors.clr1 import CLR1
from ctr.lib.lms.msbp.styles.slb1 import SLB1
from ctr.lib.lms.msbp.styles.syl3 import SYL3
from ctr.lib.lms.msbp.tags.tag2 import TAG2
from ctr.lib.lms.msbp.tags.tgg2 import TGG2
from ctr.lib.lms.msbp.tags.tgl2 import TGL2
from ctr.lib.lms.msbp.tags.tgp2 import TGP2
from ctr.lib.lms.msbp.project.cti1 import CTI1


class Msbp:
    "A class to repersent a Message Studio Binary Project file"

    def __init__(self, filepath: str = None):
        self.filepath = filepath
        if filepath is not None:
            self.parse()

    def __str__(self):
        j = JsonSerialize()
        compiled_data = {}
        compiled_data["header"] = {
            "byteorderMark": self.byteOrderMark,
            "revision": self.version,
            "messageEncoding": self.messageEncoding,
            "numberOfBlocks": self.numberOfBlocks,
            "fileSize": self.fileSize
        }
        compiled_data["colorData"] = self.clb1.combine(self.clr1)
        compiled_data["attributeData"] = self.alb1.combine(
            self.ati2, self.ali2)
        compiled_data["styleData"] = self.slb1.combine(self.syl3)
        compiled_data["tagGroups"] = self.tgg2.combine(
            self.tag2, self.tgp2, self.tgl2)
        compiled_data["projectInfo"] = self.cti1.info
        j.add(self.filepath, compiled_data)
        return j.serialize()

    def to_json(self, jsonFilename: str) -> None:
        with open(jsonFilename, "w+") as j:
            j.write(json.dumps(json.loads(str(self)), indent=2))
            print(f"Done!")

    def parse(self) -> None:
        with open(self.filepath, "rb") as d:
            # Parsing the header
            data = DataStream(d)

            # Magic
            self.magic = data.read_string(8)

            if self.magic != "MsgPrjBn":
                raise ValueError(
                    f'Input file specified has an invalid signature! (Expected "MsgPrjBn", got "{str(self.magic)})'
                )

            # BOM
            self.byteOrderMark = "little" if data.read_bytes(
                2) == b"\xFF\xFE" else "big"

            # Skip some zeros
            data.read_bytes(2)

            # Possible mesasge encoding types
            encodings = {0: "UTF-8", 1: "UTF-16", 2: "UTF-32"}

            # Get the message encoding
            self.messageEncoding = encodings[data.read_int8()]

            if self.messageEncoding != "UTF-8":
                raise ValueError(
                    f"Message Encoding is invalid, expected UTF-8, got {self.messageEncoding}")

            # Version
            self.version = data.read_uint8()

            if self.version != 3:
                raise ValueError(
                    f"Version number is unsupported! Expected 3, got {self.version}")

            self.numberOfBlocks = data.read_uint32()

            # Skip zeros

            # Filesize
            self.fileSize = data.read_uint32()

            # Skip to the start of the MSBP data
            data.read_bytes(10)
            for _ in range(self.numberOfBlocks):
                # TODO (across all block parsing): implement the following hash algorithm instead of using an index counter
                # https://github.com/kinnay/Nintendo-File-Formats/wiki/LMS-File-Format#hash-tables
                magic = data.read_string(4)
                match magic:
                    case "CLR1":
                        self.clr1 = CLR1(data)
                        data = self.clr1.read()
                    case "CLB1":
                        self.clb1 = CLB1(data)
                        data = self.clb1.read()
                    case "ATI2":
                        self.ati2 = ATI2(data)
                        data = self.ati2.read()
                    case "ALB1":
                        self.alb1 = ALB1(data)
                        data = self.alb1.read()
                    case "ALI2":
                        self.ali2 = ALI2(data)
                        data = self.ali2.read()
                    case "TGG2":
                        self.tgg2 = TGG2(data)
                        data = self.tgg2.read()
                    case "TAG2":
                        self.tag2 = TAG2(data)
                        data = self.tag2.read()
                    case "TGP2":
                        self.tgp2 = TGP2(data)
                        data = self.tgp2.read()
                    case "TGL2":
                        self.tgl2 = TGL2(data)
                        data = self.tgl2.read()
                    case "SYL3":
                        self.syl3 = SYL3(data)
                        data = self.syl3.read()
                    case "SLB1":
                        self.slb1 = SLB1(data)
                        data = self.slb1.read()
                    case "CTI1":
                        self.cti1 = CTI1(data)
                        data = self.cti1.read()
