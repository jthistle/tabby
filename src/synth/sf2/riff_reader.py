
import struct

from .exceptions import RiffReadException

class DataReader:
    pos = 0

    def __init__(self, data):
        self.data = data
        self.maximum = len(data)

    def read_bytes(self, n):
        if self.pos + n > self.maximum:
            raise EOFError()
        data = self.data[self.pos:self.pos+n]
        self.pos += n
        return data


class Chunk:
    specific_ident = None

    def __init__(self, ident, length, data):
        self.ident = ident
        self.length = length
        self.data = data
        self.children = []

        if self.ident in ("RIFF", "LIST"):
            self.read_children()

    def read_children(self):
        child_data = DataReader(self.data)

        # 4 BYTES - specific identifier for this LIST or RIFF
        specific_ident = child_data.read_bytes(4)
        try:
            self.specific_ident = str(specific_ident, encoding="ascii")
        except:
            raise RiffReadException("Specific ident for {} does not have ASCII encoding ".format(self.chunk_name))

        while True:
            # 4 BYTES - chunk identifier, ascii string
            try:
                ident = child_data.read_bytes(4)
            except EOFError:
                break

            try:
                ident = str(ident, encoding="ascii")
            except:
                raise RiffReadException("Chunk ident does not have ASCII encoding, child of {}".format(self.chunk_name))

            # 4 BYTES - length, LE unsigned 32-bit int
            length = child_data.read_bytes(4)
            length = struct.unpack("<I", length)[0]

            # length BYTES - chunk data
            try:
                new_data = child_data.read_bytes(length)
            except EOFError:
                raise RiffReadException("Incorrect length for chunk {}, child of {}".format(ident, self.chunk_name))

            self.children.append(Chunk(ident, length, new_data))

    def child(self, ident):
        for child in self.children:
            if child.specific_ident == ident:
                return child
            elif child.ident == ident:
                return child
        return None

    @property
    def chunk_name(self):
        if self.specific_ident is not None:
            return "{} ({})".format(self.specific_ident, self.ident)
        else:
            return self.ident

    def get_str(self, i):
        desc = self.chunk_name

        if len(self.children) == 0:
            return "Chunk {}, length {} bytes".format(desc, self.length)

        child_str = None
        if i > 10:
            child_str = "..."
        else:
            child_arr = [""]
            for y in [x.get_str(i + 1) for x in self.children]:
                child_arr += y.split("\n")
            child_str = "\n- ".join(child_arr)

        return "Chunk {}, length {}, {} children: {}".format(desc, self.length, len(self.children), child_str)

    def __str__(self):
        return self.get_str(0)


class RiffReader:
    def __init__(self, file):
        self.filename = file
        self.file = None

    def read(self):
        with open(self.filename, "rb") as self.file:
            return self.read_master_chunk()

    def read_master_chunk(self):
        # 4 BYTES - chunk identifier, ascii string
        ident = self.read_bytes(4)
        try:
            ident = str(ident, encoding="ascii")
        except:
            raise RiffReadException("Ident for master chunk is not ASCII")

        # 4 BYTES - length, LE unsigned 32-bit int
        length = self.read_bytes(4)
        length = struct.unpack("<I", length)[0]

        # length BYTES - chunk data
        try:
            data = self.read_bytes(length)
        except EOFError:
            raise RiffReadException("Incorrect length for master chunk")

        return Chunk(ident, length, data)

    def read_bytes(self, n):
        data = self.file.read(n)
        return data
