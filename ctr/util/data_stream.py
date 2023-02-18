import struct
from io import BufferedReader

class DataStream:

    data = None

    def __init__(self, data: BufferedReader = None, byteOrder: str = 'little'):
        self.data = data
        self.byteOrder = byteOrder

    def read_bytes(self, length: int) -> bytes:
        """Reads a number of bytes from the stream."""
        return self.data.read(length)

    def read_string(self, length: int = None, lengthBytes: int = 4) -> str:
        """Reads a string from the stream. If length is None, it will read the length from the stream first
        (Based on the provided lengthBytes which defaults to 4 for a 32-bit int)."""
        if length is None:
            length = struct.unpack(f'<{lengthBytes}B', self.data.read(lengthBytes))[0]
        return self.data.read(length).decode('utf-8')
    
    def read_string_from(self, offset: int, length: int = None, lengthBytes: int = 4) -> str:
        """Reads a string from the stream at the specified offset. If length is None, it will read the length from the stream first
        (Based on the provided lengthBytes which defaults to 4 for a 32-bit int)."""
        curPos = self.tell()
        self.seek(offset)
        string = self.read_string(length, lengthBytes)
        self.seek(curPos)
        return string

    def read_string_nt(self) -> str:
        """Reads a null-terminated string from the stream."""
        string = b''
        while True:
            char = self.data.read(1)
            if char == b'\x00':
                break
            string += char
        return string.decode('utf-8')

    def read_string_nt_from(self, offset: int) -> str:
        """Reads a null-terminated string from the stream at the specified offset."""
        curPos = self.tell()
        self.seek(offset)
        string = self.read_string_nt()
        self.seek(curPos)
        return string

    def read_int8(self) -> int:
        """Reads a signed 8-bit integer from the stream."""
        return struct.unpack(f'<b', self.data.read(1))[0]
    
    def read_uint8(self) -> int:
        """Reads an unsigned 8-bit integer from the stream."""
        return struct.unpack(f'<B', self.data.read(1))[0]
    
    def read_int16(self) -> int:
        """Reads a signed 16-bit integer from the stream."""
        return struct.unpack(f'<h', self.data.read(2))[0]
    
    def read_uint16(self) -> int:
        """Reads an unsigned 16-bit integer from the stream."""
        return struct.unpack(f'<H', self.data.read(2))[0]
    
    def read_int32(self) -> int:
        """Reads a signed 32-bit integer from the stream."""
        return struct.unpack(f'<i', self.data.read(4))[0]
    
    def read_int32_from(self, offset: int) -> int:
        """Reads a signed 32-bit integer from the stream at the specified offset."""
        curPos = self.tell()
        self.seek(offset)
        value = self.read_int32()
        self.seek(curPos)
        return value
    
    def read_uint32(self) -> int:
        """Reads an unsigned 32-bit integer from the stream."""
        return struct.unpack(f'<I', self.data.read(4))[0]
    
    def read_int64(self) -> int:
        """Reads a signed 64-bit integer from the stream."""
        return struct.unpack(f'<q', self.data.read(8))[0]
    
    def read_uint64(self) -> int:
        """Reads an unsigned 64-bit integer from the stream."""
        return struct.unpack(f'<Q', self.data.read(8))[0]
    
    def read_float(self) -> float:
        """Reads a 32-bit float from the stream."""
        return struct.unpack(f'<f', self.data.read(4))[0]
    
    def read_float_from(self, offset: int) -> float:
        """Reads a 32-bit float from the stream at the specified offset."""
        curPos = self.tell()
        self.seek(offset)
        value = self.read_float()
        self.seek(curPos)
        return value

    def read_double(self) -> float:
        """Reads a 64-bit float from the stream."""
        return struct.unpack(f'<d', self.data.read(8))[0]

    def read_vector2(self) -> tuple:
        """Reads a 2D vector from the stream (32-bit floats for both the x and y values)."""
        return (self.read_float(), self.read_float())
    
    def read_vector3(self) -> tuple:
        """Reads a 3D vector from the stream (32-bit floats for the x, y and z values)."""
        return (self.read_float(), self.read_float(), self.read_float())

    def read_color_rgba8(self, asHex=False) -> tuple or str:
        """Reads a RGBA8 color from the stream."""
        return struct.unpack('BBBB', self.read_bytes(4)) if not asHex else self.read_bytes(4).hex()
    
    def read_color_rgb8(self, asHex=False) -> tuple or str:
        """Reads a RGB8 color from the stream."""
        return struct.unpack('BBB', self.read_bytes(3)) if not asHex else self.read_bytes(3).hex()

    def read_color_rgba16(self, asHex=False) -> tuple or str:
        """Reads a RGBA16 color from the stream."""
        return struct.unpack('BBBBBBBB', self.read_bytes(8)) if not asHex else self.read_bytes(8).hex()

    def read_color_rgb16(self, asHex=False) -> tuple or str:
        """Reads a RGB16 color from the stream."""
        return struct.unpack('BBBBBB', self.read_bytes(6)) if not asHex else self.read_bytes(6).hex()

    def tell(self) -> int:
        """Returns the current position of the stream."""
        return self.data.tell()
    
    def seek(self, offset: int, whence: int = 0) -> int:
        """Seeks to a position in the stream."""
        return self.data.seek(offset, whence)
