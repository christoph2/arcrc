import os

import pytest

import ascrc as crc


CHECK_VECTOR = b"123456789"

TEST_DATA = (
    (0x00, 0x00, 0x00, 0x00),
    (0xF2, 0x01, 0x83),
    (0x0F, 0xAA, 0x00, 0x55),
    (0x00, 0xFF, 0x55, 0x11),
    (0x33, 0x22, 0x55, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF),
    (0x92, 0x6B, 0x55),
    (0xFF, 0xFF, 0xFF, 0xFF),
)

EXPECTED_RESULTS = {
    "crc8": (0x59, 0x37, 0x79, 0xB8, 0xCB, 0x8C, 0x74),
    "crc8h2f": (0x12, 0xC2, 0xC6, 0x77, 0x11, 0x33, 0x6C),
    "crc16": (0x84C0, 0xD374, 0x2023, 0xB8F9, 0xF53F, 0x0745, 0x1D0F),
    "crc16_arc": (0x0000, 0xC2E1, 0x0BE3, 0x6CCF, 0xAE98, 0xE24E, 0x9401),
    "crc32": (0x2144DF1C, 0x24AB9D77, 0xB6C9B287, 0x32A06212, 0xB0AE863D, 0x9CDEA29B, 0xFFFFFFFF),
    "crc32p4": (0x6FB32240, 0x4F721A25, 0x20662DF8, 0x9BD7996E, 0xA65A343D, 0xEE688A78, 0xFFFFFFFF),
    "crc64": (
        0xF4A586351E1B9F4B,
        0x319C27668164F1C6,
        0x54C5D0F7667C1575,
        0xA63822BE7E0704E6,
        0x701ECEB219A8E5D5,
        0x5FAA96A9B59F3E4E,
        0xFFFFFFFF00000000,
    ),
}

VARIANTS = (
    ("crc8_runtime", "crc8_table", EXPECTED_RESULTS["crc8"]),
    ("crc8h2f_runtime", "crc8h2f_table", EXPECTED_RESULTS["crc8h2f"]),
    ("crc16_runtime", "crc16_table", EXPECTED_RESULTS["crc16"]),
    ("crc16_arc_runtime", "crc16_arc_table", EXPECTED_RESULTS["crc16_arc"]),
    ("crc32_runtime", "crc32_table", EXPECTED_RESULTS["crc32"]),
    ("crc32p4_runtime", "crc32p4_table", EXPECTED_RESULTS["crc32p4"]),
    ("crc64_runtime", "crc64_table", EXPECTED_RESULTS["crc64"]),
)

CHECK_EXPECTED = (
    ("crc8_runtime", 0x4B),
    ("crc8_table", 0x4B),
    ("crc8h2f_runtime", 0xDF),
    ("crc8h2f_table", 0xDF),
    ("crc16_runtime", 0x29B1),
    ("crc16_table", 0x29B1),
    ("crc16_arc_runtime", 0xBB3D),
    ("crc16_arc_table", 0xBB3D),
    ("crc32_runtime", 0xCBF43926),
    ("crc32_table", 0xCBF43926),
    ("crc32p4_runtime", 0x1697D06A),
    ("crc32p4_table", 0x1697D06A),
    ("crc64_runtime", 0x995DC9BBDF1939FA),
    ("crc64_table", 0x995DC9BBDF1939FA),
)


@pytest.mark.parametrize("runtime_name, table_name, expected", VARIANTS)
def test_known_vectors(runtime_name, table_name, expected):
    runtime_fn = getattr(crc, runtime_name)
    table_fn = getattr(crc, table_name)
    for data, result in zip(TEST_DATA, expected):
        assert runtime_fn(data) == result
        assert table_fn(data) == result


@pytest.mark.parametrize("runtime_name, table_name", [(v[0], v[1]) for v in VARIANTS])
@pytest.mark.parametrize("size", [0, 1, 7, 32, 256, 1024])
def test_runtime_table_equivalence(runtime_name, table_name, size):
    data = os.urandom(size)
    runtime_fn = getattr(crc, runtime_name)
    table_fn = getattr(crc, table_name)
    assert runtime_fn(data) == table_fn(data)


@pytest.mark.parametrize("fn_name, expected", CHECK_EXPECTED)
def test_check_vector(fn_name, expected):
    fn = getattr(crc, fn_name)
    assert fn(CHECK_VECTOR) == expected
