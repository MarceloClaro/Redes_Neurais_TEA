"""Compressor MS-OVBA 2.4.1 (somente literal/copy tokens), para auditoria local."""
import math
import struct


def _bit_count(difference):
    if difference <= 1:
        return 4
    return max(int(math.ceil(math.log(difference, 2))), 4)


def _find_longest(data, i, max_offset, max_length):
    best_len = 0
    best_off = 0
    lo = max(0, i - max_offset)
    for j in range(lo, i):
        n = 0
        while (n < max_length and i + n < len(data) and data[j + n] == data[i + n]):
            n += 1
        if n > best_len:
            best_len = n
            best_off = i - j
            if n == max_length:
                break
    return best_len, best_off


def _compress_chunk(data):
    tokens = []  # (is_copy, payload)
    i = 0
    while i < len(data):
        bc = _bit_count(i)
        length_mask = 0xFFFF >> bc
        max_length = length_mask + 3
        max_offset = (1 << bc) - 1
        length, offset = _find_longest(data, i, max_offset, max_length)
        if length >= 3:
            token = ((offset - 1) << (16 - bc)) | (length - 3)
            tokens.append((True, token))
            i += length
        else:
            tokens.append((False, data[i]))
            i += 1

    out = bytearray()
    for start in range(0, len(tokens), 8):
        group = tokens[start:start + 8]
        flag = 0
        for k, (is_copy, _) in enumerate(group):
            if is_copy:
                flag |= 1 << k
        out.append(flag)
        for is_copy, payload in group:
            if is_copy:
                out.extend(struct.pack('<H', payload))
            else:
                out.append(payload)
    return bytes(out)


def compress_stream(source):
    """Retorna CompressedContainer MS-OVBA para bytes de entrada."""
    out = bytearray(b'\x01')
    for start in range(0, len(source), 4096):
        chunk = source[start:start + 4096]
        compressed = _compress_chunk(chunk)
        if 2 + len(compressed) <= 4098:
            chunk_size = 2 + len(compressed)
            header = ((chunk_size - 3) & 0x0FFF) | (0b011 << 12) | (1 << 15)
            out.extend(struct.pack('<H', header))
            out.extend(compressed)
        else:
            raw = bytes(chunk) + b'\x00' * (4096 - len(chunk))
            header = ((4098 - 3) & 0x0FFF) | (0b011 << 12)
            out.extend(struct.pack('<H', header))
            out.extend(raw)
    return bytes(out)
