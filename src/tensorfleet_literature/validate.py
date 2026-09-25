"""Validate a JSONL literature matrix from the command line.

Usage:
    python -m tensorfleet_literature.validate path/to/matrix.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .models import EvidenceRecord, LiteratureMatrix


def load_jsonl(path: Path) -> LiteratureMatrix:
    records: list[EvidenceRecord] = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            try:
                payload = json.loads(line)
                records.append(EvidenceRecord(**payload))
            except (TypeError, json.JSONDecodeError) as exc:
                raise ValueError(f"line {line_number}: {exc}") from exc
    return LiteratureMatrix.from_records(records)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a TensorFleet literature matrix")
    parser.add_argument("matrix", type=Path, help="JSONL matrix file")
    parser.add_argument("--minimum", type=int, default=12)
    parser.add_argument("--maximum", type=int, default=15)
    args = parser.parse_args(argv)

    try:
        matrix = load_jsonl(args.matrix)
        errors = matrix.validate(minimum=args.minimum, maximum=args.maximum)
    except (OSError, ValueError) as exc:
        print(f"invalid: {exc}", file=sys.stderr)
        return 2

    if errors:
        print("invalid:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"valid: {len(matrix.records)} literature records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
