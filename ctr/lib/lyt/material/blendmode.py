from enum import IntEnum

from ....util.data_stream import DataStream

"""
Blend Mode Entry
===================
Offset |  Size  |   Type   | Description
-------+--------+----------+------------
 0x00  |  0x01  |   byte  | Blend Operation (see BlendOp enum)
 0x01  |  0x01  |   byte  | Blend Factor Source (see BlendFactor enum)
 0x02  |  0x01  |   byte  | Blend Factor Destination (see BlendFactor enum)
 0x03  |  0x01  |   byte  | Logic Operation (see LogicOp enum)
===================
"""

# Blend Factor Enum
class BlendFactor(IntEnum):
    FACTOR0 = 0
    FACTOR1 = 1
    DEST_COLOR = 2
    DEST_INV_COLOR = 3
    SRC_ALPHA = 4
    SRC_INV_ALPHA = 5
    DEST_ALPHA = 6
    DEST_INV_ALPHA = 7
    SRC_COLOR = 8
    SRC_INV_COLOR = 9

# Blend Operation Enum
class BlendOp(IntEnum):
    DISABLE = 0
    ADD = 1
    SUBTRACT = 2
    REV_SUBTRACT = 3
    SELECT_MIN = 4
    SELECT_MAX = 5

# Logic Operation Enum
class LogicOp(IntEnum):
    DISABLE = 0
    NO_OP = 1
    CLEAR = 2
    SET = 3
    COPY = 4
    COPY_INV = 5
    INV = 6
    AND = 7
    NAND = 8
    OR = 9
    NOR = 10
    XOR = 11
    EQUIV = 12
    REV_AND = 13
    INV_ADD = 14
    REV_OR = 15
    INV_OR = 16

class BlendMode:

    blendOp: BlendOp = None
    blendFactorSrc: BlendFactor = None
    blendFactorDest: BlendFactor = None
    logicOp: LogicOp = None

    def __init__(self, data: DataStream = None):
        if data is not None:
            self.read(data)
    
    def read(self, data: DataStream) -> DataStream:
        """Reads the BlendMode section from a material data stream"""

        # Read in each mode as a single byte
        self.blendOp = data.read_bytes(1)
        self.blendFactorSrc = data.read_bytes(1)
        self.blendFactorDest = data.read_bytes(1)
        self.logicOp = data.read_bytes(1)

        return data
