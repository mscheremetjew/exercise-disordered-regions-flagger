"""Flag intrinsically disordered regions in a protein sequence.

The method is a compositional heuristic, not a disorder predictor: each residue
is scored by the fraction of disorder-promoting residues in the window centred
on it, and runs of residues at or above the threshold become regions.

Input rules are deliberately not uniform:

* whitespace is stripped silently;
* lowercase marks a soft-masked position, which fills its window slot but never
  counts as disorder-promoting and never appears inside a reported region;
* the ambiguous codes X, B, Z and U fill their window slot and never count as
  disorder-promoting, but may sit inside a region;
* gap characters and any other character are rejected.
"""

from scales import DISORDER_PROMOTING, ORDER_PROMOTING

AMBIGUOUS = frozenset("XBZU")
ACCEPTED = DISORDER_PROMOTING | ORDER_PROMOTING | AMBIGUOUS


def _validate_parameters(window: int, threshold: float, min_length: int) -> None:
    if window <= 0 or window % 2 == 0:
        raise ValueError(f"window must be odd and positive, got {window}")
    if not 0.0 <= threshold <= 1.0:
        raise ValueError(f"threshold must lie between 0 and 1, got {threshold}")
    if min_length < 1:
        raise ValueError(f"min_length must be at least 1, got {min_length}")


def _clean(sequence: str) -> str:
    """Strip formatting whitespace and reject anything that is not a residue."""
    cleaned = "".join(sequence.split())
    for character in cleaned:
        if character.upper() not in ACCEPTED:
            raise ValueError(f"sequence contains an unsupported character: {character!r}")
    return cleaned


def _is_disorder_promoting(residue: str) -> bool:
    """Masked (lowercase) residues never count, so the test is case-sensitive."""
    return residue in DISORDER_PROMOTING


def find_disordered_regions(
    sequence: str,
    window: int = 5,
    threshold: float = 0.6,
    min_length: int = 5,
) -> list[tuple[int, int]]:
    """Return the flagged regions as 1-based inclusive (start, end) pairs."""
    _validate_parameters(window, threshold, min_length)
    residues = _clean(sequence)

    half = window // 2
    regions: list[tuple[int, int]] = []
    run_start: int | None = None

    for index, residue in enumerate(residues):
        low = max(0, index - half)
        high = min(len(residues), index + half + 1)
        frame = residues[low:high]
        score = sum(_is_disorder_promoting(other) for other in frame) / len(frame)
        # A masked residue can never be reported, so it ends any open run.
        disordered = score >= threshold and not residue.islower()

        if disordered and run_start is None:
            run_start = index
        elif not disordered and run_start is not None:
            if index - run_start >= min_length:
                regions.append((run_start + 1, index))
            run_start = None

    if run_start is not None and len(residues) - run_start >= min_length:
        regions.append((run_start + 1, len(residues)))

    return regions
