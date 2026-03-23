
from typing import Iterable

POLY_8 = 0x1D
POLY_8H2F = 0x2F
POLY_16 = 0x1021
POLY_16_ARC = 0x8005
POLY_32 = 0x04C11DB7
POLY_32P4 = 0xF4ACFB13
POLY_64 = 0x42F0E1EBA9EA3693


def reflect(value: int, bits: int) -> int:
    result = 0
    for _ in range(bits):
        result = (result << 1) | (value & 1)
        value >>= 1
    return result

POLY_16_ARC_REFLECTED = 0xA001
POLY_32_REFLECTED = reflect(POLY_32, 32)
POLY_32P4_REFLECTED = reflect(POLY_32P4, 32)
POLY_64_REFLECTED = reflect(POLY_64, 64)


# === CRC-8 ===================================================================

def crc8_runtime(data: Iterable[int], start_value: int = 0xFF, xor_out: int = 0xFF) -> int:
    crc = start_value & 0xFF
    for c in data:
        c &= 0xFF
        for mask in (0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01):
            bit = (crc & 0x80) != 0
            if c & mask:
                bit = not bit
            crc = (crc << 1) & 0xFF
            if bit:
                crc ^= POLY_8
    return (crc ^ xor_out) & 0xFF


def _make_crc8_table() -> list[int]:
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ POLY_8) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
        table.append(crc)
    return table


CRC8_TABLE = _make_crc8_table()


def crc8_table(data: Iterable[int], start_value: int = 0xFF, xor_out: int = 0xFF) -> int:
    crc = start_value & 0xFF
    for c in data:
        crc = CRC8_TABLE[(crc ^ c) & 0xFF]
    return (crc ^ xor_out) & 0xFF


# === CRC-8 H2F ===============================================================

def _make_crc8h2f_table() -> list[int]:
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ POLY_8H2F) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
        table.append(crc)
    return table


CRC8H2F_TABLE = _make_crc8h2f_table()


def crc8h2f_runtime(data: Iterable[int], start_value: int = 0xFF, xor_out: int = 0xFF) -> int:
    crc = start_value & 0xFF
    for c in data:
        c &= 0xFF
        for mask in (0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01):
            bit = (crc & 0x80) != 0
            if c & mask:
                bit = not bit
            crc = (crc << 1) & 0xFF
            if bit:
                crc ^= POLY_8H2F
    return (crc ^ xor_out) & 0xFF


def crc8h2f_table(data: Iterable[int], start_value: int = 0xFF, xor_out: int = 0xFF) -> int:
    crc = start_value & 0xFF
    for c in data:
        crc = CRC8H2F_TABLE[(crc ^ c) & 0xFF]
    return (crc ^ xor_out) & 0xFF


# === CRC-16 ==================================================================

def crc16_runtime(data: Iterable[int], start_value: int = 0xFFFF) -> int:
    crc = start_value & 0xFFFF
    for c in data:
        c &= 0xFF
        for mask in (0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01):
            bit = (crc & 0x8000) != 0
            if c & mask:
                bit = not bit
            crc = (crc << 1) & 0xFFFF
            if bit:
                crc ^= POLY_16
    return crc


def _make_crc16_table() -> list[int]:
    table = []
    for i in range(256):
        crc = i << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ POLY_16) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
        table.append(crc)
    return table


CRC16_TABLE = _make_crc16_table()


def crc16_table(data: Iterable[int], start_value: int = 0xFFFF) -> int:
    crc = start_value & 0xFFFF
    for c in data:
        idx = ((crc >> 8) ^ c) & 0xFF
        crc = ((crc << 8) ^ CRC16_TABLE[idx]) & 0xFFFF
    return crc


# === CRC-16 ARC ==============================================================

def _make_crc16_arc_table() -> list[int]:
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ POLY_16_ARC_REFLECTED
            else:
                crc >>= 1
        table.append(crc & 0xFFFF)
    return table


CRC16_ARC_TABLE = _make_crc16_arc_table()


def crc16_arc_runtime(data: Iterable[int], start_value: int = 0x0000) -> int:
    crc = start_value & 0xFFFF
    for c in data:
        crc ^= c & 0xFF
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ POLY_16_ARC_REFLECTED
            else:
                crc >>= 1
            crc &= 0xFFFF
    return crc


def crc16_arc_table(data: Iterable[int], start_value: int = 0x0000) -> int:
    crc = start_value & 0xFFFF
    for c in data:
        idx = (crc ^ c) & 0xFF
        crc = (CRC16_ARC_TABLE[idx] ^ (crc >> 8)) & 0xFFFF
    return crc


# === CRC-32 ==================================================================

def crc32_runtime(data: Iterable[int], start_value: int = 0xFFFFFFFF, xor_out: int = 0xFFFFFFFF) -> int:
    crc = start_value & 0xFFFFFFFF
    for c in data:
        c &= 0xFF
        for bit in range(8):
            bit_flag = (crc & 0x80000000) != 0
            if c & (1 << bit):
                bit_flag = not bit_flag
            crc = (crc << 1) & 0xFFFFFFFF
            if bit_flag:
                crc ^= POLY_32
    crc = reflect(crc, 32)
    return (crc ^ xor_out) & 0xFFFFFFFF


def _make_crc32_table() -> list[int]:
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ POLY_32_REFLECTED
            else:
                crc >>= 1
        table.append(crc & 0xFFFFFFFF)
    return table


CRC32_TABLE = _make_crc32_table()


def crc32_table(data: Iterable[int], start_value: int = 0xFFFFFFFF, xor_out: int = 0xFFFFFFFF) -> int:
    crc = start_value & 0xFFFFFFFF
    for c in data:
        idx = (crc ^ c) & 0xFF
        crc = (CRC32_TABLE[idx] ^ (crc >> 8)) & 0xFFFFFFFF
    return (crc ^ xor_out) & 0xFFFFFFFF


# === CRC-32 P4 ==============================================================

def _make_crc32p4_table() -> list[int]:
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ POLY_32P4_REFLECTED
            else:
                crc >>= 1
        table.append(crc & 0xFFFFFFFF)
    return table


CRC32P4_TABLE = _make_crc32p4_table()


def crc32p4_runtime(data: Iterable[int], start_value: int = 0xFFFFFFFF, xor_out: int = 0xFFFFFFFF) -> int:
    crc = start_value & 0xFFFFFFFF
    for c in data:
        crc ^= c & 0xFF
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ POLY_32P4_REFLECTED
            else:
                crc >>= 1
            crc &= 0xFFFFFFFF
    return (crc ^ xor_out) & 0xFFFFFFFF


def crc32p4_table(data: Iterable[int], start_value: int = 0xFFFFFFFF, xor_out: int = 0xFFFFFFFF) -> int:
    crc = start_value & 0xFFFFFFFF
    for c in data:
        idx = (crc ^ c) & 0xFF
        crc = (CRC32P4_TABLE[idx] ^ (crc >> 8)) & 0xFFFFFFFF
    return (crc ^ xor_out) & 0xFFFFFFFF


# === CRC-64 ECMA =============================================================

def _make_crc64_table() -> list[int]:
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ POLY_64_REFLECTED
            else:
                crc >>= 1
        table.append(crc & 0xFFFFFFFFFFFFFFFF)
    return table


CRC64_TABLE = _make_crc64_table()


def crc64_runtime(data: Iterable[int], start_value: int = 0xFFFFFFFFFFFFFFFF, xor_out: int = 0xFFFFFFFFFFFFFFFF) -> int:
    crc = start_value & 0xFFFFFFFFFFFFFFFF
    for c in data:
        crc ^= c & 0xFF
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ POLY_64_REFLECTED
            else:
                crc >>= 1
            crc &= 0xFFFFFFFFFFFFFFFF
    return (crc ^ xor_out) & 0xFFFFFFFFFFFFFFFF


def crc64_table(data: Iterable[int], start_value: int = 0xFFFFFFFFFFFFFFFF, xor_out: int = 0xFFFFFFFFFFFFFFFF) -> int:
    crc = start_value & 0xFFFFFFFFFFFFFFFF
    for c in data:
        idx = (crc ^ c) & 0xFF
        crc = (CRC64_TABLE[idx] ^ (crc >> 8)) & 0xFFFFFFFFFFFFFFFF
    return (crc ^ xor_out) & 0xFFFFFFFFFFFFFFFF
