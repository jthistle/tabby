
import struct

"""
We are assuming that we're working with little-endian, 16-bit samples.
"""

def data_to_samples(data: bytes):
    samples = []
    for i in range(0, len(data) - 2, 2):
        smpl = struct.unpack("<h", data[i:i+2])
        samples.append(smpl[0])
    return samples

def samples_to_data(samples: [int]):
    data = bytearray()
    for sample in samples:
        for b in struct.pack("<h", sample):
            data.append(b)
    return bytes(data)
