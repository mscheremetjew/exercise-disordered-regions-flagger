"""Minimal FASTA reader.

Only what the flagger needs: records in file order, with the sequence lines of
each record joined so that coordinates refer to the whole sequence.
"""

from collections.abc import Iterator


def parse_fasta(text: str) -> Iterator[tuple[str, str]]:
    """Yield ``(identifier, sequence)`` for every record in ``text``."""
    identifier: str | None = None
    lines: list[str] = []

    for line in text.splitlines():
        if line.startswith(">"):
            if identifier is not None:
                yield identifier, "".join(lines)
            identifier = line[1:].strip().split()[0] if line[1:].strip() else ""
            lines = []
        elif line.strip():
            lines.append(line.strip())

    if identifier is not None:
        yield identifier, "".join(lines)
