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
        self.seek(offset)
        return self.read_string_nt()

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

    def read_double(self) -> float:
        """Reads a 64-bit float from the stream."""
        return struct.unpack(f'<d', self.data.read(8))[0]

    def read_vector2(self) -> tuple:
        """Reads a 2D vector from the stream (32-bit floats for both the x and y values)."""
        return (self.read_float(), self.read_float())
    
    def read_vector3(self) -> tuple:
        """Reads a 3D vector from the stream (32-bit floats for the x, y and z values)."""
        return (self.read_float(), self.read_float(), self.read_float())

    def read_color_rgba8(self) -> tuple:
        """Reads a RGBA8 color from the stream."""
        return (self.read_bytes(1), self.read_bytes(1), self.read_bytes(1), self.read_bytes(1))
    
    def read_color_rgb8(self) -> tuple:
        """Reads a RGB8 color from the stream."""
        return (self.read_bytes(1), self.read_bytes(1), self.read_bytes(1))
    
    def read_color_rgba16(self) -> tuple:
        """Reads a RGBA16 color from the stream."""
        return (self.read_bytes(2), self.read_bytes(2), self.read_bytes(2), self.read_bytes(2))
    
    def read_color_rgb16(self) -> tuple:
        """Reads a RGB16 color from the stream."""
        return (self.read_bytes(2), self.read_bytes(2), self.read_bytes(2))

    def tell(self) -> int:
        """Returns the current position of the stream."""
        return self.data.tell()
    
    def seek(self, offset: int, whence: int = 0) -> int:
        """Seeks to a position in the stream."""
        return self.data.seek(offset, whence)