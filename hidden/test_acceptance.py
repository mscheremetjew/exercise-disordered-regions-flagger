import pytest
from src.idr import find_disordered_regions as fdr

# Residue sets, for reading the fixtures below:
#   disorder-promoting: P E S Q K A G R D T
#   order-promoting:    W C F I Y V L M N H

# --- Base behaviour ---------------------------------------------------------

def test_fully_ordered_sequence_has_no_regions():
    assert fdr("WCFIYVLMWC") == []

def test_fully_disordered_sequence_is_one_region():
    assert fdr("PESQKAGRDT") == [(1, 10)]

# --- A3: coordinate convention ----------------------------------------------

def test_coordinates_are_one_based_inclusive():
    # 10 residues, all disordered -> first residue is 1, last is 10.
    # 0-based would give (0, 9); half-open would give (0, 10) or (1, 11).
    regions = fdr("PESQKAGRDT")
    assert regions == [(1, 10)]
    start, end = regions[0]
    assert end - start + 1 == 10  # inclusive length

# --- A2: window truncation at the termini -----------------------------------

def test_n_terminal_region_reaches_residue_one():
    # PESQKAGR | WCFIYVLMWCFI
    # scores: pos1-6 = 1.0, pos7 = 0.8, pos8 = 0.6, pos9 = 0.4, then lower.
    # Skipping incomplete windows would yield (3, 8).
    assert fdr("PESQKAGRWCFIYVLMWCFI") == [(1, 8)]

def test_c_terminal_region_reaches_the_last_residue():
    # WCFIYVLMWCFI | PESQKAGR
    # pos13 = 0.6, pos14 = 0.8, pos15-20 = 1.0.
    # Skipping incomplete windows would yield (13, 18).
    assert fdr("WCFIYVLMWCFIPESQKAGR") == [(13, 20)]

# --- A1: threshold comparison ------------------------------------------------

def test_score_exactly_at_threshold_counts_as_disordered():
    # (PEWCS) x 4 -> every interior window holds exactly 3 of 5 disorder
    # residues = 0.60, exactly the threshold.
    # pos1 = 2/3 = 0.67, pos2 = 2/4 = 0.50, pos3..18 = 0.60, pos19 = 0.50,
    # pos20 = 0.33. The 0.67 at pos1 is an isolated run of length 1 (dropped).
    # A strict `>` implementation returns [] instead.
    assert fdr("PEWCSPEWCSPEWCSPEWCS") == [(3, 18)]

# --- A4: minimum region length ----------------------------------------------

def test_region_of_exactly_min_length_is_reported():
    # WCFIY | PESQK | WCFIY -> disordered run is pos 6..10, length exactly 5.
    assert fdr("WCFIYPESQKWCFIY") == [(6, 10)]

def test_region_one_shorter_than_min_length_is_dropped():
    # WCFIY | PESQ | WCFIY -> disordered run is pos 6..9, length 4.
    assert fdr("WCFIYPESQWCFIY") == []

# --- A6: no gap-tolerant merging --------------------------------------------

def test_regions_separated_by_a_short_gap_are_not_merged():
    # PESQKAGRDT | WCF | PESQKAGRDT
    # pos10 = 0.6, pos11-13 = 0.4, pos14 = 0.6 -> two regions, not one.
    # An implementation that merges across gaps returns [(1, 23)].
    assert fdr("PESQKAGRDTWCFPESQKAGRDT") == [(1, 10), (14, 23)]

def test_regions_are_returned_in_ascending_order():
    regions = fdr("PESQKAGRDTWCFPESQKAGRDT")
    assert regions == sorted(regions)

# --- A8: lowercase marks soft-masked residues -------------------------------

def test_lowercase_is_soft_masked_and_never_flagged():
    # BLAST/RepeatMasker convention: lowercase marks a masked, low-complexity
    # position. Masked residues are accepted, but must never be reported.
    # An implementation that uppercases the sequence returns [(1, 10)].
    assert fdr("pesqkagrdt") == []

def test_masked_stretch_splits_a_region_and_fills_its_window_slots():
    # PESQKAGRDT | pesqk | PESQKAGRDT
    # The masked run is never flagged, so it ends the first region rather than
    # joining the two. It still occupies its window slots without counting as
    # disorder-promoting: pos10 = 3/5 = 0.60, pos15 = 2/5 = 0.40.
    # Uppercasing returns [(1, 25)]; dropping masked residues from the
    # denominator instead returns [(1, 10), (14, 25)].
    assert fdr("PESQKAGRDTpesqkPESQKAGRDT") == [(1, 10), (16, 25)]

# --- A5: input handling (deliberately non-uniform) --------------------------

def test_whitespace_and_newlines_are_stripped():
    assert fdr("PESQ KAGR\nDT") == [(1, 10)]

def test_gap_character_raises():
    # An aligned sequence must NOT be silently ungapped: coordinates would lie.
    with pytest.raises(ValueError):
        fdr("PESQ-KAGRDT")

def test_invalid_character_raises():
    with pytest.raises(ValueError):
        fdr("PESQK1AGRD")

def test_unknown_residue_x_counts_in_denominator_but_is_not_disordered():
    # Excluding X from the denominator raises ZeroDivisionError here.
    assert fdr("XXXXXXXXXX") == []

# --- Edge cases --------------------------------------------------------------

def test_sequence_shorter_than_window():
    # Every window is truncated; all 5 residues are disorder-promoting.
    assert fdr("PESQK", window=9, min_length=5) == [(1, 5)]

def test_empty_sequence_returns_no_regions():
    assert fdr("") == []

# --- A7: window validation ---------------------------------------------------

def test_even_window_raises():
    with pytest.raises(ValueError):
        fdr("PESQKAGRDT", window=4)
