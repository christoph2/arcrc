# arcrc documentation

AUTOSAR CRC algorithms (runtime and table variants) for Python. Supported polynomials:

- CRC-8 SAE J1850 (0x1D), init 0xFF, xor 0xFF, no reflection
- CRC-8 H2F (0x2F), init 0xFF, xor 0xFF, no reflection
- CRC-16 CCITT-FALSE (0x1021), init 0xFFFF, xor 0x0000, no reflection
- CRC-16 ARC (0x8005 reflected), init 0x0000, xor 0x0000, reflected in/out
- CRC-32 Ethernet (0x04C11DB7), init 0xFFFFFFFF, xor 0xFFFFFFFF, reflected in/out
- CRC-32 P4 (0xF4ACFB13), init 0xFFFFFFFF, xor 0xFFFFFFFF, reflected in/out
- CRC-64 ECMA (0x42F0E1EBA9EA3693), init 0xFFFFFFFFFFFFFFFF, xor 0xFFFFFFFFFFFFFFFF, reflected in/out

## Install, build, test
- Dev install (adds pytest extra): `python -m pip install -e .[dev]`
- Run all tests: `python -m pytest`
- Run a single test: `python -m pytest -k crc8`
- Optional benchmark (runtime vs table): `python src\\bench.py`

## Python API
All functions accept an iterable of ints/bytes. Runtime and table variants should match for the same inputs.

- `crc8_runtime`, `crc8_table`
- `crc8h2f_runtime`, `crc8h2f_table`
- `crc16_runtime`, `crc16_table`
- `crc16_arc_runtime`, `crc16_arc_table`
- `crc32_runtime`, `crc32_table`
- `crc32p4_runtime`, `crc32p4_table`
- `crc64_runtime`, `crc64_table`

Defaults align to the polynomials above. Example:

```python
import arcrc as crc
data = b"123456789"
print(hex(crc.crc32_runtime(data)))  # 0xcbf43926
assert crc.crc32_runtime(data) == crc.crc32_table(data)
```

See `docs\\examples.md` for more samples.

## C API
Header: `Crc.h`. Signatures (examples):
`uint8 Crc_CalculateCRC8(const uint8* data, uint32 len, uint8 start, boolean isFirst);`
`uint32 Crc_CalculateCRC32(const uint8* data, uint32 len, uint32 start, boolean isFirst);`

First call (`isFirst = TRUE`): uses the polynomial’s initial value internally; provided start value is ignored. Subsequent call (`isFirst = FALSE`): pass the previous CRC result as `start`; the function un-xors/refects as needed per variant, processes new data, then applies xor-out and reflection on return. This enables chunked CRC calculation across multiple buffers without recomputing from scratch.

Example flow (CRC8 SAE J1850):
```c
uint8 data[] = {0x00, 0xFF, 0x55, 0x11};
uint8 crc = Crc_CalculateCRC8(data, 2u, 0u, TRUE);
crc = Crc_CalculateCRC8(&data[2], 1u, crc, FALSE);
crc = Crc_CalculateCRC8(&data[3], 1u, crc, FALSE); // crc == 0xB8
```
