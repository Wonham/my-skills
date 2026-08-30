#!/usr/bin/env python3
"""Read verified Lumerical LDF v1.0 MODE/FDE D-card files."""

from __future__ import annotations

import argparse
import json
import math
import struct
from pathlib import Path
from typing import Any

import numpy as np


HEADER_PREFIX = "Lumerical data file 1, version "
SUPPORTED_VERSION = "1.0"
FORMAT_MARKER = b"\x03\x04\x08\x00"


class LDFError(ValueError):
    """Raised when an LDF file is unsupported, malformed, or truncated."""


class DCard:
    def __init__(
        self,
        name: str,
        metadata: dict[str, Any],
        records: dict[str, np.ndarray],
    ) -> None:
        self.name = name
        self.metadata = metadata
        self.records = records

    def __getitem__(self, name: str) -> np.ndarray:
        return self.records[name]

    def scalar(self, name: str) -> complex | float:
        value = self.records[name]
        if value.size != 1:
            raise ValueError(f"{name!r} is not a scalar; shape={value.shape}")
        return value.item()


class LDFDocument:
    def __init__(self, version: str, cards: list[DCard]) -> None:
        self.version = version
        self.cards = cards


class _BinaryReader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.offset = 0

    @property
    def remaining(self) -> int:
        return len(self.data) - self.offset

    def read_bytes(self, size: int) -> bytes:
        if size < 0 or self.remaining < size:
            raise LDFError(
                f"Truncated LDF at byte {self.offset}: "
                f"need {size} bytes, have {self.remaining}"
            )
        start = self.offset
        self.offset += size
        return self.data[start : start + size]

    def read_u32(self) -> int:
        return struct.unpack("<I", self.read_bytes(4))[0]

    def read_string(self) -> str:
        size = self.read_u32()
        raw = self.read_bytes(size)
        if not raw.endswith(b"\x00"):
            raise LDFError(f"String at byte {self.offset - size} is not NUL-terminated")
        try:
            return raw[:-1].decode("utf-8")
        except UnicodeDecodeError as exc:
            raise LDFError(f"Invalid UTF-8 string at byte {self.offset - size}") from exc

    def read_f64_array(self, count: int) -> np.ndarray:
        raw = self.read_bytes(8 * count)
        return np.frombuffer(raw, dtype="<f8", count=count).copy()


def _read_header(reader: _BinaryReader) -> str:
    end = reader.data.find(b"\x00", 0, 128)
    if end < 0:
        raise LDFError("Missing LDF header terminator")
    try:
        header = reader.read_bytes(end + 1)[:-1].decode("ascii")
    except UnicodeDecodeError as exc:
        raise LDFError("LDF header is not ASCII") from exc
    if not header.startswith(HEADER_PREFIX):
        raise LDFError(f"Unsupported LDF header: {header!r}")
    version = header[len(HEADER_PREFIX) :]
    if version != SUPPORTED_VERSION:
        raise LDFError(
            f"Unsupported LDF version {version!r}; only {SUPPORTED_VERSION!r} is verified"
        )
    marker = reader.read_bytes(4)
    if marker != FORMAT_MARKER:
        raise LDFError(f"Unsupported LDF format marker: {marker.hex()}")
    return version


def _read_metadata_value(reader: _BinaryReader) -> str | list[int]:
    value_type = reader.read_u32()
    if value_type == 0:
        return reader.read_string()
    if value_type == 2:
        count = reader.read_u32()
        return [reader.read_u32() for _ in range(count)]
    raise LDFError(f"Unsupported metadata type {value_type} at byte {reader.offset - 4}")


def _read_record(reader: _BinaryReader) -> tuple[str, np.ndarray]:
    name = reader.read_string()
    value_count = reader.read_u32()
    dimension_count = reader.read_u32()
    if dimension_count == 0 or dimension_count > 8:
        raise LDFError(f"Invalid dimension count {dimension_count} for record {name!r}")
    shape = tuple(reader.read_u32() for _ in range(dimension_count))
    expected_count = math.prod(shape)
    if value_count != expected_count:
        raise LDFError(
            f"Record {name!r} count mismatch: header={value_count}, shape={shape}"
        )

    real_flag = reader.read_u32()
    record_marker = reader.read_u32()
    if real_flag not in (0, 1):
        raise LDFError(f"Invalid real/complex flag {real_flag} for record {name!r}")
    if record_marker != 1:
        raise LDFError(f"Unsupported record marker {record_marker} for record {name!r}")

    real = reader.read_f64_array(value_count)
    if real_flag == 1:
        flat = real
    else:
        imaginary = reader.read_f64_array(value_count)
        flat = np.empty(value_count, dtype=np.complex128)
        flat.real = real
        flat.imag = imaginary
    return name, flat.reshape(shape, order="F")


def read_ldf(path: str | Path) -> LDFDocument:
    """Read a verified LDF v1.0 file without requiring Lumerical."""
    source = Path(path)
    reader = _BinaryReader(source.read_bytes())
    version = _read_header(reader)

    card_count = reader.read_u32()
    cards: list[DCard] = []
    for card_index in range(card_count):
        metadata_count = reader.read_u32()
        metadata: dict[str, Any] = {}
        for _ in range(metadata_count):
            key = reader.read_string()
            metadata[key] = _read_metadata_value(reader)

        record_count = reader.read_u32()
        records: dict[str, np.ndarray] = {}
        for _ in range(record_count):
            name, value = _read_record(reader)
            if name in records:
                raise LDFError(f"Duplicate record name {name!r}")
            records[name] = value

        card_name = metadata.get("name", f"card{card_index + 1}")
        if not isinstance(card_name, str):
            raise LDFError("D-card metadata field 'name' is not a string")
        cards.append(DCard(card_name, metadata, records))

    if reader.remaining == 4 and reader.read_u32() == 0:
        pass
    elif reader.remaining != 0:
        raise LDFError(f"Unexpected {reader.remaining} trailing bytes")
    return LDFDocument(version, cards)


def _json_number(value: float) -> float | str:
    number = float(value)
    if math.isfinite(number):
        return number
    if math.isnan(number):
        return "NaN"
    return "Infinity" if number > 0 else "-Infinity"


def _json_scalar(
    value: complex | float,
) -> float | str | dict[str, float | str]:
    if isinstance(value, complex):
        return {"real": _json_number(value.real), "imag": _json_number(value.imag)}
    return _json_number(value)


def document_summary(document: LDFDocument) -> dict[str, Any]:
    cards = []
    for card in document.cards:
        records = {}
        for name, value in card.records.items():
            entry: dict[str, Any] = {
                "shape": list(value.shape),
                "dtype": str(value.dtype),
            }
            if value.size == 1:
                entry["value"] = _json_scalar(value.item())
            records[name] = entry
        cards.append({"name": card.name, "metadata": card.metadata, "records": records})
    return {"version": document.version, "cards": cards}


def export_npz(card: DCard, path: str | Path) -> Path:
    """Export one D-card's native arrays to a compressed NumPy archive."""
    destination = Path(path)
    if destination.suffix.lower() != ".npz":
        raise ValueError("NPZ export path must end in .npz")
    np.savez_compressed(destination, **card.records)
    return destination


def export_mat(card: DCard, path: str | Path) -> Path:
    """Export one D-card's native arrays to a MATLAB v5 file."""
    try:
        from scipy.io import savemat
    except ModuleNotFoundError as exc:
        raise RuntimeError("MAT export requires scipy; install it or use .npz") from exc
    destination = Path(path)
    if destination.suffix.lower() != ".mat":
        raise ValueError("MAT export path must end in .mat")
    savemat(destination, card.records, do_compression=True, oned_as="column")
    return destination


def export_card(card: DCard, path: str | Path) -> Path:
    destination = Path(path)
    if destination.suffix.lower() == ".npz":
        return export_npz(card, destination)
    if destination.suffix.lower() == ".mat":
        return export_mat(card, destination)
    raise ValueError("Export path must end in .npz or .mat")


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Lumerical .ldf file")
    parser.add_argument("--json", action="store_true", help="print a JSON summary")
    parser.add_argument("--export", type=Path, help="export the first D-card to .npz or .mat")
    args = parser.parse_args(argv)

    document = read_ldf(args.file)
    summary = document_summary(document)
    if args.export is not None:
        if not document.cards:
            raise LDFError("The LDF file contains no D-cards")
        export_card(document.cards[0], args.export)
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False))
    else:
        print(f"Lumerical LDF version {summary['version']}")
        for card in summary["cards"]:
            print(f"D-card: {card['name']}")
            for name, record in card["records"].items():
                print(f"  {name}: shape={tuple(record['shape'])}, dtype={record['dtype']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
