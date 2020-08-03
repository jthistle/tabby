
import struct


CACHED_SAMPLES = {}


def data_to_samples(data: bytes, sample_id = None):
    if sample_id is not None and sample_id in CACHED_SAMPLES:
        return [x for x in CACHED_SAMPLES[sample_id]]

    samples = []
    for i in range(0, len(data) - 2, 2):
        smpl = struct.unpack("<h", data[i:i+2])
        samples.append(smpl[0])

    CACHED_SAMPLES[sample_id] = [x for x in samples]
    return samples


def samples_to_data(samples: [int]):
    data = bytearray()
    for sample in samples:
        for b in struct.pack("<h", sample):
            data.append(b)
    return bytes(data)
