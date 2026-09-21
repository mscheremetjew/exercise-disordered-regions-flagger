#!/usr/bin/env bash
#
# configure_exercise_repo.sh — one-shot repository configuration for the
# "Flagging Disordered Regions in Protein Sequences" exercise (Step 6).
#
# Run it from the root of the freshly generated cookiecutter project:
#
#     bash scripts/configure_exercise_repo.sh
#
# It applies three changes that the exercise depends on:
#
#   6a  pyproject.toml         [tool.pytest.ini_options] pythonpath = ["."]
#                              so the supplied acceptance suite can import src.idr
#   6b  .pre-commit-config.yaml  exclude: ^hidden/ on ruff-check, ruff-format
#                              and end-of-file-fixer, so graded material is not
#                              auto-reformatted
#   6c  pyproject.toml         [tool.mypy] exclude = ["^src/idr\\.py$", "^hidden/"]
#
# The script is idempotent: running it twice changes nothing the second time.
# Pass --check to verify without writing anything.

set -euo pipefail

CHECK_ONLY=0
if [[ "${1:-}" == "--check" ]]; then
  CHECK_ONLY=1
elif [[ -n "${1:-}" ]]; then
  echo "usage: $(basename "$0") [--check]" >&2
  exit 2
fi

# --- locate the project root ------------------------------------------------
# Works whether you run it from the project root or from scripts/.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "pyproject.toml" ]]; then
  ROOT="$(pwd)"
elif [[ -f "${SCRIPT_DIR}/../pyproject.toml" ]]; then
  ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
else
  echo "error: no pyproject.toml found. Run this from the project root:" >&2
  echo "       cd disordered-regions-flagger && bash scripts/configure_exercise_repo.sh" >&2
  exit 1
fi

PYPROJECT="${ROOT}/pyproject.toml"
PRECOMMIT="${ROOT}/.pre-commit-config.yaml"

# --- pick a python ----------------------------------------------------------
if command -v python3 >/dev/null 2>&1; then
  PY=(python3)
elif command -v python >/dev/null 2>&1; then
  PY=(python)
elif command -v uv >/dev/null 2>&1; then
  PY=(uv run --no-project python)
else
  echo "error: need python3 (or uv) on PATH to edit the config files." >&2
  exit 1
fi

echo "Configuring: ${ROOT}"
[[ ${CHECK_ONLY} -eq 1 ]] && echo "(--check: reporting only, nothing will be written)"

"${PY[@]}" - "${PYPROJECT}" "${PRECOMMIT}" "${CHECK_ONLY}" <<'PYEOF'
"""Apply the Step 6 configuration edits, idempotently."""

import re
import sys

pyproject_path, precommit_path, check_only_raw = sys.argv[1:4]
check_only = check_only_raw == "1"

changes: list[str] = []
already: list[str] = []
problems: list[str] = []


def read(path: str) -> str | None:
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except FileNotFoundError:
        return None


def write(path: str, text: str) -> None:
    if check_only:
        return
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def section_bounds(text: str, header: str) -> tuple[int, int] | None:
    """Return (start, end) character offsets of a TOML section's body."""
    match = re.search(rf"^\[{re.escape(header)}\]\s*$", text, flags=re.MULTILINE)
    if match is None:
        return None
    body_start = match.end()
    nxt = re.search(r"^\[", text[body_start:], flags=re.MULTILINE)
    body_end = body_start + (nxt.start() if nxt else len(text[body_start:]))
    return body_start, body_end


def has_key(body: str, key: str) -> bool:
    return re.search(rf"^\s*{re.escape(key)}\s*=", body, flags=re.MULTILINE) is not None


def add_toml_key(text: str, header: str, key: str, line: str, label: str) -> str:
    """Add `line` to the `header` section unless `key` is already set there."""
    bounds = section_bounds(text, header)
    if bounds is None:
        # Section missing entirely (unexpected, but recoverable): append it.
        addition = f"\n[{header}]\n{line}\n"
        changes.append(f"{label}: added a [{header}] section with {key}")
        return text.rstrip("\n") + "\n" + addition
    start, end = bounds
    body = text[start:end]
    if has_key(body, key):
        already.append(f"{label}: [{header}] already sets {key}")
        return text
    trimmed = body.rstrip("\n")
    new_body = f"{trimmed}\n{line}\n" + ("\n" if body.endswith("\n\n") else "")
    changes.append(f"{label}: added {key} to [{header}]")
    return text[:start] + new_body + text[end:]


# --- 6a and 6c: pyproject.toml ---------------------------------------------
pyproject = read(pyproject_path)
if pyproject is None:
    problems.append(f"missing file: {pyproject_path}")
else:
    original = pyproject
    pyproject = add_toml_key(
        pyproject,
        "tool.pytest.ini_options",
        "pythonpath",
        '# The supplied acceptance tests in hidden/ import the src.idr bridge, so the\n'
        '# repository root must be importable (hidden/ is not a package).\n'
        'pythonpath = ["."]',
        "6a",
    )
    pyproject = add_toml_key(
        pyproject,
        "tool.mypy",
        "exclude",
        '# hidden/ holds the supplied acceptance tests; src/idr.py is the bridge they\n'
        '# import through, which mypy would otherwise see as both "idr" and "src.idr".\n'
        'exclude = ["^src/idr\\\\.py$", "^hidden/"]',
        "6c",
    )
    if pyproject != original:
        write(pyproject_path, pyproject)


# --- 6b: .pre-commit-config.yaml -------------------------------------------
HOOKS = ("ruff-check", "ruff-format", "end-of-file-fixer")

precommit = read(precommit_path)
if precommit is None:
    problems.append(f"missing file: {precommit_path}")
else:
    lines = precommit.splitlines()
    out: list[str] = []
    index = 0
    changed = False
    while index < len(lines):
        line = lines[index]
        out.append(line)
        match = re.match(r"^(\s*)-\s+id:\s*([A-Za-z0-9._-]+)\s*$", line)
        index += 1
        if match is None or match.group(2) not in HOOKS:
            continue

        hook_id = match.group(2)
        item_indent = match.group(1)
        key_indent = item_indent + "  "

        # Collect the rest of this hook's mapping (keys indented past the "- ").
        block: list[str] = []
        while index < len(lines):
            nxt = lines[index]
            if nxt.strip() == "" or nxt.startswith(key_indent) and not nxt.lstrip().startswith("- "):
                block.append(nxt)
                index += 1
                continue
            break

        if any(re.match(r"^\s*exclude\s*:", entry) for entry in block):
            already.append(f"6b: {hook_id} already has an exclude")
            out.extend(block)
            continue

        # Insert after the hook's own keys, before any trailing blank lines.
        tail = len(block)
        while tail > 0 and block[tail - 1].strip() == "":
            tail -= 1
        block.insert(tail, f"{key_indent}exclude: ^hidden/")
        out.extend(block)
        changes.append(f"6b: added exclude: ^hidden/ to {hook_id}")
        changed = True

    if changed:
        trailing = "\n" if precommit.endswith("\n") else ""
        write(precommit_path, "\n".join(out) + trailing)

    missing = [
        hook
        for hook in HOOKS
        if not re.search(rf"^\s*-\s+id:\s*{re.escape(hook)}\s*$", precommit, flags=re.MULTILINE)
    ]
    for hook in missing:
        problems.append(f"6b: hook '{hook}' not found in {precommit_path} — add exclude: ^hidden/ by hand")


# --- report -----------------------------------------------------------------
for entry in changes:
    print(f"  {'would change' if check_only else 'changed'}  {entry}")
for entry in already:
    print(f"  ok            {entry}")
for entry in problems:
    print(f"  PROBLEM       {entry}")

if not changes and not problems:
    print("  nothing to do — the repository is already configured.")

sys.exit(1 if problems else 0)
PYEOF

# --- verify -----------------------------------------------------------------
echo
echo "Verifying:"
status=0
check() {
  if eval "$2" >/dev/null 2>&1; then
    echo "  PASS  $1"
  else
    echo "  FAIL  $1"
    status=1
  fi
}
check 'pyproject.toml sets pythonpath'            "grep -q 'pythonpath' '${PYPROJECT}'"
check 'pyproject.toml excludes hidden/ from mypy' "grep -q 'hidden/' '${PYPROJECT}'"
check '.pre-commit-config.yaml excludes hidden/'  "test \$(grep -c 'exclude: \\^hidden/' '${PRECOMMIT}') -ge 3"

echo
if [[ ${status} -eq 0 ]]; then
  echo "Step 6 complete."
else
  echo "Step 6 incomplete — see the failures above." >&2
fi
exit ${status}
