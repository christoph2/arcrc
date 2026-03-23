# Copilot instructions for this repo

## Build, install, test
- Install for development (adds pytest extra): `python -m pip install -e .[dev]`
- Run full test suite: `python -m pytest`
- Run a single test (example): `python -m pytest tests/test_crc.py -k crc8`
- Optional microbenchmark comparison: `python src\\bench.py`
- No dedicated linting configured.

## Architecture (big picture)
- Src layout: `ascrc` package in `src/` exposes CRC-8/16/32 runtime and table variants via `crc_module.py` and re-exports in `__init__.py`.
- Each CRC has two implementations: bitwise runtime loops and table-driven versions using module-scope lookup tables (`CRC8_TABLE`, `CRC16_TABLE`, `CRC32_TABLE`) built at import time.
- `reflect()` handles bit reflection for CRC-32 table generation and finalization; polynomials are `POLY_8=0x1D`, `POLY_16=0x1021`, `POLY_32=0x04C11DB7`.
- Tests in `tests/test_crc.py` validate the canonical `b"123456789"` vector and assert runtime/table parity across random payload sizes; pytest adds `src` to `PYTHONPATH`.
- `src/bench.py` benchmarks runtime vs table variants across payload sizes; relies on the same public API.
- Legacy AUTOSAR C sources (`Crc.c`, `Crc.h`) live at repo root for reference; they are not built or imported by the Python package or tests.

## Key conventions and patterns
- Import style used in tests/bench: `import ascrc as crc` (pythonpath points to `src` via `pyproject.toml`).
- Inputs are iterables of ints/bytes; each byte is masked to 0xFF inside the algorithms.
- Default seeds/xor: CRC-8 uses `start_value=0xFF` and `xor_out=0xFF`; CRC-16 uses `start_value=0xFFFF`; CRC-32 uses `start_value=0xFFFFFFFF` with reflection and `xor_out=0xFFFFFFFF`. Change defaults only with updated expectations/tests.
- Table variants rely on module-scope tables created at import; avoid mutating these globals to keep runtime/table results aligned.
- When adding tests, mirror the existing pattern of checking runtime vs table equality and use `pytest -k` to narrow to specific cases when iterating.
