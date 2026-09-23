"""Unit tests for the disorder-region flagging rules.

Covers the parameter-validation contract (US-0006) and the input rules of
US-0007 that the supplied acceptance suite does not already exercise.
The core algorithm itself is covered by hidden/test_acceptance.py.
"""

import pytest

from disordered_regions_flagger.idr import find_disordered_regions as fdr

# --- Parameter validation (US-0006) -----------------------------------------


@pytest.mark.parametrize("window", [-1, 0])
def test_non_positive_window_raises(window: int) -> None:
    with pytest.raises(ValueError):
        fdr("PESQKAGRDT", window=window)


@pytest.mark.parametrize("threshold", [-0.01, 1.01])
def test_threshold_outside_unit_interval_raises(threshold: float) -> None:
    with pytest.raises(ValueError):
        fdr("PESQKAGRDT", threshold=threshold)


@pytest.mark.parametrize("min_length", [0, -1])
def test_min_length_below_one_raises(min_length: int) -> None:
    with pytest.raises(ValueError):
        fdr("PESQKAGRDT", min_length=min_length)


@pytest.mark.parametrize(
    ("name", "value"), [("threshold", 0.0), ("threshold", 1.0), ("min_length", 1)]
)
def test_boundary_parameter_values_are_accepted(name: str, value: float) -> None:
    assert isinstance(fdr("PESQKAGRDT", **{name: value}), list)


# --- Ambiguous residue codes (US-0007) --------------------------------------


def test_ambiguous_codes_are_accepted_and_never_disorder_promoting() -> None:
    # B, Z and U occupy their window slot but never count as disorder-promoting.
    assert fdr("BZUBZUBZUB") == []


def test_an_ambiguous_code_may_sit_inside_a_region() -> None:
    # Deliberate asymmetry with soft masking: an X does not split a region.
    # Position 11 scores 4/5 = 0.8, so the run spans it.
    assert fdr("PESQKAGRDTXPESQKAGRDT") == [(1, 21)]
