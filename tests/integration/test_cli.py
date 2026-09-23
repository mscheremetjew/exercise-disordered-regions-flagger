"""Integration tests for the identify-disordered-regions command.

The command is driven as a real subprocess so that the console-script name,
the printed table, and the error contract are all exercised as a user sees them.
"""

import subprocess
import sys
from pathlib import Path

import pytest

CLI = Path(sys.executable).parent / "identify-disordered-regions"

# Whole sequence disordered -> one region spanning 1..10.
FLAGGED = "PESQKAGRDT"
# Whole sequence order-promoting -> no region at all.
UNFLAGGED = "WCFIYVLMWCFIYVLMWCFI"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(CLI), *args], capture_output=True, text=True)


@pytest.fixture
def fasta(tmp_path: Path) -> Path:
    path = tmp_path / "constructs.fasta"
    path.write_text(f">seqA\n{FLAGGED}\n>seqB\n{UNFLAGGED}\n")
    return path


def test_command_is_available_under_its_approved_name() -> None:
    assert run("--help").returncode == 0


def test_every_record_is_reported_under_its_fasta_identifier(fasta: Path) -> None:
    result = run(str(fasta))
    assert result.returncode == 0
    assert "seqA" in result.stdout
    assert "seqB" in result.stdout


def test_a_sequence_without_regions_is_still_reported(fasta: Path) -> None:
    result = run(str(fasta))
    assert "no flagged regions" in result.stdout.lower()


def test_a_wrapped_record_is_joined_before_scoring(tmp_path: Path) -> None:
    path = tmp_path / "wrapped.fasta"
    path.write_text(">seqC\nPESQK\nAGRDT\n")
    result = run(str(path))
    columns = [line.split() for line in result.stdout.splitlines() if line.startswith("seqC")]
    assert columns and columns[0][1:4] == ["1", "10", "10"]


def test_the_table_carries_the_approved_columns(fasta: Path) -> None:
    header = next(line for line in run(str(fasta)).stdout.splitlines() if "start" in line.lower())
    assert header.split() == ["sequence", "ID", "start", "end", "length", "residues"]


def test_the_heuristic_notice_is_printed_once_below_the_table(fasta: Path) -> None:
    lines = run(str(fasta)).stdout.splitlines()
    notices = [index for index, line in enumerate(lines) if "heuristic" in line.lower()]
    assert len(notices) == 1
    assert notices[0] > max(index for index, line in enumerate(lines) if "seqB" in line)


def test_default_parameters_are_the_approved_values(tmp_path: Path) -> None:
    path = tmp_path / "defaults.fasta"
    path.write_text(">seqD\nWCFIYPESQKWCFIY\n")
    row = next(line for line in run(str(path)).stdout.splitlines() if line.startswith("seqD"))
    assert row.split()[1:4] == ["6", "10", "5"]


def test_a_supplied_threshold_takes_effect(tmp_path: Path) -> None:
    path = tmp_path / "strict.fasta"
    path.write_text(">seqD\nWCFIYPESQKWCFIY\n")
    result = run(str(path), "--threshold", "1.0")
    assert "no flagged regions" in result.stdout.lower()


@pytest.mark.parametrize(
    ("flag", "value"), [("--window", "4"), ("--threshold", "1.5"), ("--min-length", "0")]
)
def test_an_invalid_parameter_is_refused_without_a_traceback(
    fasta: Path, flag: str, value: str
) -> None:
    result = run(str(fasta), flag, value)
    assert result.returncode == 1
    assert result.stderr.strip()
    assert "Traceback" not in result.stderr


def test_a_missing_file_is_refused_without_a_traceback(tmp_path: Path) -> None:
    result = run(str(tmp_path / "absent.fasta"))
    assert result.returncode == 1
    assert result.stderr.strip()
    assert "Traceback" not in result.stderr
