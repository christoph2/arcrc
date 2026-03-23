
import os
import time
import arcrc


def bench(fn, data, loops=200):
    t0 = time.perf_counter()
    for _ in range(loops):
        fn(data)
    t1 = time.perf_counter()
    return (t1 - t0) / loops


def main():
    sizes = [16, 64, 256, 1024, 4096]
    print("Benchmark: Runtime vs Table\n")

    for size in sizes:
        data = os.urandom(size)
        print(f"--- {size} bytes ---")

        print("CRC-8 ",
              f"runtime={bench(crc.crc8_runtime, data)*1e6:8.2f} µs",
              f"table={bench(crc.crc8_table, data)*1e6:8.2f} µs")

        print("CRC-16",
              f"runtime={bench(crc.crc16_runtime, data)*1e6:8.2f} µs",
              f"table={bench(crc.crc16_table, data)*1e6:8.2f} µs")

        print("CRC-32",
              f"runtime={bench(crc.crc32_runtime, data)*1e6:8.2f} µs",
              f"table={bench(crc.crc32_table, data)*1e6:8.2f} µs")

        print()


if __name__ == "__main__":
    main()
