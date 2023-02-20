import struct
from io import BufferedWriter

class WriteStream:

    data: BufferedWriter = None

    def __init__(self, data: BufferedWriter = None, byteOrder: str = 'little'):
        self.data = data
        self.byteOrder = byteOrder

    def write_bytes(self, data: bytes, length: int = 0):
        """Writes a number of bytes to the stream."""
        if length == 0:
            self.data.write(data)
        else:
            if len(data) < length:
                self.data.write(data + b'\x00' * (length - len(data)))
            elif len(data) > length:
                self.data.write(data[:length])
            else:
                self.data.write(data)
    
    def write_string(self, string: str, lengthBytes: int = 0):
        """Writes a string to the stream."""
        if lengthBytes > 0:
            stringBytes = string.encode('utf-8')
            if len(stringBytes) < lengthBytes:
                self.data.write(stringBytes + b'\x00' * (lengthBytes - len(stringBytes)))
            elif len(stringBytes) > lengthBytes:
                self.data.write(stringBytes[:lengthBytes])
        else:
            self.data.write(string.encode('utf-8'))
    
    def write_string_nt(self, string: str):
        """Writes a null-terminated string to the stream."""
        self.data.write(string.encode('utf-8') + b'\x00')
    
    def write_int8(self, value: int):
        """Writes a signed 8-bit integer to the stream."""
        self.data.write(struct.pack(f'<b', value))
    
    def write_uint8(self, value: int):
        """Writes an unsigned 8-bit integer to the stream."""
        self.data.write(struct.pack(f'<B', value))
    
    def write_int16(self, value: int):
        """Writes a signed 16-bit integer to the stream."""
        self.data.write(struct.pack(f'<h', value))
    
    def write_uint16(self, value: int):
        """Writes an unsigned 16-bit integer to the stream."""
        self.data.write(struct.pack(f'<H', value))
    
    def write_int32(self, value: int):
        """Writes a signed 32-bit integer to the stream."""
        self.data.write(struct.pack(f'<i', value))
    
    def write_uint32(self, value: int):
        """Writes an unsigned 32-bit integer to the stream."""
        self.data.write(struct.pack(f'<I', value))
    
    def write_int64(self, value: int):
        """Writes a signed 64-bit integer to the stream."""
        self.data.write(struct.pack(f'<q', value))
    
    def write_uint64(self, value: int):
        """Writes an unsigned 64-bit integer to the stream."""
        self.data.write(struct.pack(f'<Q', value))
    
    def write_float(self, value: float):
        """Writes a 32-bit float to the stream."""
        self.data.write(struct.pack(f'<f', value))

    def write_double(self, value: float):
        """Writes a 64-bit float to the stream."""
        self.data.write(struct.pack(f'<d', value))
    
    def write_vector2(self, value: tuple):
        """Writes a 2D vector to the stream."""
        self.write_float(value[0])
        self.write_float(value[1])
    
    def write_vector3(self, value: tuple):
        """Writes a 3D vector to the stream."""
        self.write_float(value[0])
        self.write_float(value[1])
        self.write_float(value[2])
    
    def write_color_rgba8(self, value: tuple):
        """Writes an RGBA8 color to the stream."""
        self.write_uint8(value[0])
        self.write_uint8(value[1])
        self.write_uint8(value[2])
        self.write_uint8(value[3])
    
    def write_color_rgb8(self, value: tuple):
        """Writes an RGB8 color to the stream."""
        self.write_uint8(value[0])
        self.write_uint8(value[1])
        self.write_uint8(value[2])
    
    def write_color_rgba32(self, value: tuple):
        """Writes an RGBA32 color to the stream."""
        self.write_float(value[0])
        self.write_float(value[1])
        self.write_float(value[2])
        self.write_float(value[3])
    
    def write_color_rgb32(self, value: tuple):
        """Writes an RGB32 color to the stream."""
        self.write_float(value[0])
        self.write_float(value[1])
        self.write_float(value[2])
    
    def write_uv_coord_set(self, value: tuple):
        """Writes a UV coordinate set to the stream (8 16-bit floats that make up the top left, top right, bottom left, and bottom right UVs)."""
        self.write_float(value[0][0])
        self.write_float(value[0][1])
        self.write_float(value[1][0])
        self.write_float(value[1][1])
        self.write_float(value[2][0])
        self.write_float(value[2][1])
        self.write_float(value[3][0])
        self.write_float(value[3][1])
    
    def seek(self, offset: int, whence: int = 0):
        """Seeks to a position in the stream."""
        self.data.seek(offset, whence)
    
    def tell(self):
        """Returns the current position in the stream."""
        return self.data.tell()