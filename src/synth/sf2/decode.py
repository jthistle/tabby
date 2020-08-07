
import struct

def ascii_str(val):
    res = ""
    for byte in val:
        if byte == 0:
            break
        try:
            res += chr(byte)
        except:
            raise SoundfontReadException("Invalid byte in ASCII string: {}".format(" ".join([hex(int(x)) for x in val])))

    return res


def WORD(val):
    return struct.unpack("<H", val)[0]

def DWORD(val):
    return struct.unpack("<I", val)[0]

def BYTE(val):
    return struct.unpack("<B", val)[0]

def CHAR(val):
    return struct.unpack("<b", val)[0]

def SHORT(val):
    return struct.unpack("<h", val)[0]
