"""Command-line entry point for identify-disordered-regions."""

import argparse
import sys
from pathlib import Path

from disordered_regions_flagger.fasta import parse_fasta
from disordered_regions_flagger.idr import find_disordered_regions

COLUMNS = ("sequence ID", "start", "end", "length", "residues")
NO_REGIONS = "no flagged regions"
NOTICE = (
    "Note: these regions come from a compositional heuristic, "
    "not a disorder prediction."
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="identify-disordered-regions",
        description="Flag likely disordered regions in every sequence of a FASTA file.",
    )
    parser.add_argument("fasta", type=Path, help="path to the FASTA file to analyse")
    parser.add_argument("--window", type=int, default=5, help="window width (odd, default 5)")
    parser.add_argument(
        "--threshold", type=float, default=0.6, help="disorder threshold (default 0.6)"
    )
    parser.add_argument(
        "--min-length", type=int, default=5, help="minimum region length (default 5)"
    )
    return parser


def _rows(text: str, window: int, threshold: float, min_length: int) -> list[tuple[str, ...]]:
    rows: list[tuple[str, ...]] = []
    for identifier, sequence in parse_fasta(text):
        regions = find_disordered_regions(
            sequence, window=window, threshold=threshold, min_length=min_length
        )
        if not regions:
            rows.append((identifier, NO_REGIONS, "", "", ""))
            continue
        cleaned = "".join(sequence.split())
        for start, end in regions:
            rows.append(
                (identifier, str(start), str(end), str(end - start + 1), cleaned[start - 1 : end])
            )
    return rows


def _render(rows: list[tuple[str, ...]]) -> str:
    """Lay the rows out as plain whitespace-aligned columns.

    A "no flagged regions" row carries no coordinates, so it is excluded from the
    width calculation to keep the numeric columns narrow and scannable.
    """
    measured = [COLUMNS, *(row for row in rows if row[1] != NO_REGIONS)]
    widths = [max(len(row[column]) for row in measured) for column in range(len(COLUMNS))]
    lines = []
    for row in [COLUMNS, *rows]:
        if row[1] == NO_REGIONS:
            lines.append(f"{row[0].ljust(widths[0])}  {NO_REGIONS}")
        else:
            cells = (cell.ljust(width) for cell, width in zip(row, widths, strict=True))
            lines.append("  ".join(cells).rstrip())
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Run the command and return its exit code."""
    arguments = _build_parser().parse_args(argv)
    try:
        text = arguments.fasta.read_text()
        rows = _rows(text, arguments.window, arguments.threshold, arguments.min_length)
    except (OSError, ValueError) as error:
        print(f"identify-disordered-regions: {error}", file=sys.stderr)
        return 1

    print(_render(rows))
    print()
    print(NOTICE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
