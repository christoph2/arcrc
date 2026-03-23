# Examples

## Python
### Basic CRC32
```python
import arcrc as crc

data = b"123456789"
assert crc.crc32_runtime(data) == 0xCBF43926
assert crc.crc32_runtime(data) == crc.crc32_table(data)
```

### CRC16 ARC vs CCITT-FALSE
```python
payload = b"\x92\x6B\x55"
assert crc.crc16_runtime(payload) == 0x0745       # CCITT-FALSE
assert crc.crc16_arc_runtime(payload) == 0xE24E   # ARC (reflected)
```

### CRC64 ECMA over chunks
```python
buf1 = b"\x33\x22\x55\xAA"
buf2 = b"\xBB\xCC\xDD\xEE\xFF"
# single pass
one_shot = crc.crc64_runtime(buf1 + buf2)
# chunked: compute CRC on buf1, then continue with buf2 using result as seed
part1 = crc.crc64_runtime(buf1)
chunked = crc.crc64_runtime(buf2, start_value=part1)
assert one_shot == chunked
```

## C (incremental)
```c
#include "Crc.h"

void example_crc32_chunked(void) {
    const uint8 buf1[] = {0x33, 0x22, 0x55, 0xAA};
    const uint8 buf2[] = {0xBB, 0xCC, 0xDD, 0xEE, 0xFF};

    uint32 crc = Crc_CalculateCRC32(buf1, 4u, 0u, TRUE);
    crc = Crc_CalculateCRC32(buf2, 5u, crc, FALSE);
    /* crc now equals the CRC32 of buf1+buf2 with Ethernet settings */
}
```

```c
void example_crc8_single_and_multi(void) {
    uint8 data[] = {0x00, 0xFF, 0x55, 0x11};
    uint8 crc_one_shot = Crc_CalculateCRC8(data, 4u, 0u, TRUE);

    uint8 crc_chunked = Crc_CalculateCRC8(&data[0], 2u, 0u, TRUE);
    crc_chunked = Crc_CalculateCRC8(&data[2], 1u, crc_chunked, FALSE);
    crc_chunked = Crc_CalculateCRC8(&data[3], 1u, crc_chunked, FALSE);

    /* crc_one_shot and crc_chunked both equal 0xB8 */
}
```
