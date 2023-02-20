
def extract_bits(value, num_bits, start_bit):
    """Extracts a number of bits from a value, starting at a given bit position."""
    mask = 0
    for i in range(start_bit, start_bit + num_bits):
        mask |= (0x80000000 >> i)
    return (value & mask) >> (32 - (start_bit + num_bits))

def insert_bits(value, start_bit, bits, num_bits):
    """Inserts a number of bits into a value, starting at a given bit position."""
    mask = 0
    for i in range(start_bit, start_bit + num_bits):
        mask |= (0x80000000 >> i)
    return (value & ~mask) | ((bits << (32 - (start_bit + num_bits))) & mask)