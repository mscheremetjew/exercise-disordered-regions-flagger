# Flagging Disordered Regions in Protein Sequences

**A beginners exercise in AI-assisted software development**

---

## How to use this document

Work through it top to bottom. Every step tells you exactly what to type, what you
should see, and what to do if you see something else.

| Part | What happens | Time      | Who reads it |
| --- | --- |-----------| --- |
| [0. Orientation](#0-orientation) | What you build and why | 3 min     | Everyone |
| [1. Setup](#part-1--setup) | Scaffold the project, install the supplied files | 10-20 min | Everyone — **do this before the session if you can** |
| [2. Round 1](#part-2--round-1-prompt-only) | Build it with prompting alone | 10 min    | Everyone |
| [3. Checkpoint A](#part-3--checkpoint-a-meet-the-acceptance-suite) | Meet the acceptance suite | 5 min     | Everyone |
| [4. Round 2](#part-4--round-2-specification-first) | Build it again, specification first | 35 min    | Everyone |
| [5. Checkpoint B](#part-5--checkpoint-b-and-debrief) | Compare and debrief | 5 min     | Everyone |
| [6. Stretch goals](#part-6--stretch-goals) | If you finish early | —         | Everyone |
| [7. Troubleshooting](#part-7--troubleshooting) | When something breaks | —         | Everyone |
| [Appendix A](#appendix-a--worked-scoring-example) | A worked scoring example by hand | —         | Everyone |
| [Appendix B](#appendix-b--facilitator-only) | Runbook, answer key, expected outcomes | —         | **Facilitator only — do not project or distribute** |

> **Participants:** stop at the end of Appendix A. Appendix B is the answer key.

---

## 0. Orientation

### 0.1 What you will build

A small command-line helper that reads a FASTA file of protein sequences and
prints, for each sequence, the stretches that look intrinsically disordered:

```text
sequence          start     end  length  residues
demo_disordered       1      20      20  PESQKAGRDTPESQKAGRDT
demo_mixed           13      22      10  PESQKAGRDT
3 sequence(s) read, 2 region(s) flagged
```

The method is simple on purpose. Two groups of amino acids (scales.py) are given.
Each of the 20 standard amino acids is either "disorder-promoting" (P E S Q K A G R D T) or
"order-promoting" (W C F I Y V L M N H). Nothing else is used. Then slide a window along the sequence.
Score each residue by the fraction of *disorder-promoting* amino acids inside its window.
Residues scoring at or above a threshold count as disordered. Unbroken runs of
disordered residues become regions. Very short regions are discarded.

Defaults: **window 5, threshold 0.6, minimum region length 5.**

### 0.2 The point of the exercise

You will build the same function **twice**, with the same coding assistant, on
the same day.

- **Round 1** — you prompt freely. Whatever you like, however you like.
- **Round 2** — you first turn a vague ticket into an agreed specification, then
  implement against it.

The same hidden acceptance suite grades both attempts. The gap between the two
scores is the entire lesson.

> Nothing about the AI changes between the two rounds. Only the specification does.

### 0.3 Scientific honesty caveat — read this before you write any code

**What you are building is not a disorder predictor.** It is a deliberately
simplified teaching stand-in.

Real intrinsic-disorder prediction — IUPred3, metapredict, flDPnn, or AlphaFold
pLDDT used as a disorder proxy — relies on learned models, evolutionary
information, and calibrated scores. What you build here is a *compositional
heuristic*: a binary disorder-promoting / order-promoting split of the twenty
amino acids, smoothed over a window.

Never present the output of this exercise as a scientific prediction. Any real
result must come from a validated tool.

### 0.4 Schedule

| Clock | Part |
| --- | --- |
| before | Part 1 — Setup |
| 0:00 | Part 1 recap, questions |
| 0:03 | Part 2 — Round 1 (prompt only) |
| 0:13 | Part 3 — Checkpoint A |
| 0:18 | Part 4 — Round 2 (specification first) |
| 0:55 | Part 5 — Checkpoint B and debrief |

### 0.5 What you need installed

| Tool | Check it works | If missing |
| --- | --- | --- |
| `git` | `git --version` | <https://git-scm.com/downloads> |
| `uv` | `uv --version` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Python 3.14 | `uv python install 3.14` | `uv` installs it for you |
| An agentic coding assistant | see below | see below |

### 0.6 Your coding assistant

This exercise is written to be tool-agnostic. It has been prepared for
**Claude Code** and **Codex CLI**, but any agentic assistant that can read and
write files in your project will do.

| What you need to do | Claude Code | Codex CLI | Any other assistant |
| --- | --- | --- | --- |
| Start it in the project folder | `claude` | `codex` | per its own docs |
| Where it finds the SDLC skills | `.claude/skills/` | `.agents/skills/` | — |
| Launch the SDLC workflow | type `/sdlc-orchestrate-workflow` | ask in plain language (see below) | ask in plain language |

**Plain-language fallback** — this works in every tool, including Claude Code and
Codex, and is the safe option if a slash command is not recognised:

```text
Read .agents/skills/sdlc-orchestrate-workflow/SKILL.md and follow it.
Act as the SDLC workflow orchestrator for this repository and tell me the
current stage and the next action I need to take.
```

**Please note:** Throughout this document, **"your assistant"** means whichever tool you chose.
Text in `>>> quoted blocks like this` is meant to be typed at your assistant, not
in the shell.

---

## Part 1 — Setup

> Budget 10 minutes. **Do this before the session if at all possible** — it needs
> network access and a dependency install, and doing it live eats the clock.

### Step 1 — Install Cookiecutter

The project skeleton comes from a Cookiecutter template. Install it once.
Run the following command in your shell (not in your AI assistant):

```bash
uv tool install cookiecutter
```

Verify:

```bash
cookiecutter --version
```

> If `cookiecutter: command not found`, reopen your shell, or prefix every
> Cookiecutter command below with `uvx`, e.g. `uvx cookiecutter <url>`.

### Step 2 — Generate the project

Move to wherever you keep code, then run:

```bash
cookiecutter https://github.com/ecarrenolozano/ai-assisted-python-template.git
```

Cookiecutter asks a series of questions. **Answer them exactly as below** — later
steps depend on the resulting folder and package names.

| No | Prompt | Answer                                     |
|----| --- |--------------------------------------------|
| 1. | `project_name` | `disordered regions flagger`                |
| 2. | `project_slug` | accept the default (`disordered-regions-flagger`) |
| 3. | `package_name` | accept the default (`disordered_regions_flagger`) |
| 4. | `project_description` | accept the default                         |
| 5. | `author_name` | your name                                  |
| 6. | `author_email` | your email                                 |
| 7. | `python_version` | `3.14`                                     |
| 8. | `project_type` | `application`                              |
| 9. | `license` | any — `No license` is fine                 |
| 10. | `documentation_tool` | `mkdocs`                                   |
| 11. | `initialize_git` | `yes`                                      |

You now have a folder named `disordered-regions-flagger`.

### Step 3 — Install dependencies and run the initial checks

```bash
cd disordered-regions-flagger
uv sync --all-groups
uv run pre-commit install
uv run pytest
```

**Expected:** `uv sync` installs the dev and docs dependency groups, and
pre-commit reports `pre-commit installed at .git/hooks/pre-commit`.

`pytest` ends with `1 test passed` and exit code **0**.

### Step 4 — Make the SDLC skills visible to your assistant

The template ships eleven workflow skills plus an orchestrator in
`.agents/skills/`. Confirm they arrived:

```bash
ls .agents/skills
```

**Expected:** twelve entries, from `a-clarify-project-request` through
`j-prepare-release-deployment`, plus `sdlc-bootstrap-project` and
`sdlc-orchestrate-workflow`.

**Codex CLI** reads `.agents/skills/` directly — nothing more to do.

**Claude Code** looks in `.claude/skills/`. Point it at the same folder with a
symlink so there is only ever one copy:

```bash
mkdir -p .claude
ln -s ../.agents/skills .claude/skills
ls .claude/skills
```

**Expected:** the same 13 entries.

> On Windows without developer mode, `ln -s` fails. Copy instead:
> `xcopy /E /I .agents\skills .claude\skills`

### Step 5 — Add the supplied residue partition

The ticket you are about to receive names the two residue groups. They also live
in `src/scales.py`, ready to import. That file is **given material**: it is an
input to the exercise, not something you design. Create it exactly as below.

```bash
cat > src/scales.py <<'EOF'
"""Compositional partition used in this exercise.

Simplified from the disorder-promoting / order-promoting split described in the
IDP literature (Uversky- and Dunker-style compositional analyses). Provided as a
fixed input to the exercise: participants are NOT asked to derive or modify it.

This file holds the partition and nothing else. Which characters an input
sequence may contain is a requirements decision, not given material.

NOTE: this is a teaching simplification, not a validated predictor.
"""

DISORDER_PROMOTING = frozenset("PESQKAGRDT")
ORDER_PROMOTING = frozenset("WCFIYVLMNH")
EOF
```

Reading it: ten amino acids are treated as disorder-promoting and ten as
order-promoting. That is the whole file. It says nothing about which characters
a sequence is allowed to contain — that is a decision, and deciding it is part
of the exercise.

**Do not edit this file at any point in the exercise.**

### Step 6 — Configure the repository for the exercise

Three small configuration changes are needed before the graded material will
run. A script in the exercise repository makes all three. Run it from the root
of the project you just generated:

```bash
mkdir -p scripts
curl -fsSL -o scripts/configure_exercise_repo.sh \
  https://raw.githubusercontent.com/mscheremetjew/exercise-disordered-regions-flagger/main/scripts/configure_exercise_repo.sh
bash scripts/configure_exercise_repo.sh
```

**Expected:** five `changed` lines, then three `PASS` lines and `Step 6
complete.`

The script is idempotent — run it as often as you like — and
`bash scripts/configure_exercise_repo.sh --check` reports what it *would* do
without writing anything.

> No network, or the repository is not reachable? Ask your facilitator for
> `configure_exercise_repo.sh` and drop it in `scripts/`. The script is also
> readable: open it if you want to see the edits before running them.

<details>
<summary>What it changes, and why (you do not need to do this by hand)</summary>

**6a — Let pytest import from `src/`.** In `pyproject.toml`, under
`[tool.pytest.ini_options]`:

```toml
pythonpath = ["."]
```

Without it, the acceptance suite you receive later fails to import with
`ModuleNotFoundError: No module named 'src'`.

**6b — Keep quality tools off the graded material.** Later you receive a folder
called `hidden/`. It is graded material and must not be auto-reformatted. In
`.pre-commit-config.yaml`, the `ruff-check`, `ruff-format` and
`end-of-file-fixer` hooks each get:

```yaml
        exclude: ^hidden/
```

**6c — Keep mypy off it too.** In `pyproject.toml`, under `[tool.mypy]`:

```toml
exclude = ["^src/idr\\.py$", "^hidden/"]
```

</details>

Note that `testpaths = ["tests"]` means a bare `uv run pytest` runs **your** tests
only. The graded suite is run explicitly, by path.

### Step 7 — Add a demo FASTA file

You need a few sequences to run against. These three are synthetic and chosen so
the answers are obvious by eye.

```bash
mkdir -p data
cat > data/demo.fasta <<'EOF'
>demo_ordered Fully order-promoting control
WCFIYVLMWCFIYVLMWCFIYVLM
>demo_disordered Fully disorder-promoting control
PESQKAGRDTPESQKAGRDT
>demo_mixed Ordered head, disordered tail
WCFIYVLMWCFIPESQKAGRDTWCFIYVLM
EOF
```

Read them as: one sequence that should yield **no** regions, one that should be
**entirely** one region, and one that should yield a **single region in its
second half**.

### Setup checklist

Before the session starts, confirm all six:

```bash
ls .agents/skills | wc -l
ls src/scales.py
ls data/demo.fasta
bash scripts/configure_exercise_repo.sh --check
uv run pytest
git status
```

Expected output:
```bash
13
src/scales.py
data/demo.fasta
Configuring: /Users/schereme/PycharmProjects/ai-workshop-beginners-exercise-test/disordered-regions-flagger
(--check: reporting only, nothing will be written)
  ok            6a: [tool.pytest.ini_options] already sets pythonpath
  ok            6c: [tool.mypy] already sets exclude
  ok            6b: ruff-check already has an exclude
  ok            6b: ruff-format already has an exclude
  ok            6b: end-of-file-fixer already has an exclude
  nothing to do — the repository is already configured.
Verifying:
  PASS  pyproject.toml sets pythonpath
  PASS  pyproject.toml excludes hidden/ from mypy
  PASS  .pre-commit-config.yaml excludes hidden/

Step 6 complete.
1 passed in 0.01s
On branch main

No commits yet
...
```

Commit your setup so you can always get back to it:

```bash
git add -A
git commit -m "Exercise setup: template, supplied scales.py, demo data"
```

---

## Part 2 — Round 1: prompt only

> **10 minutes.** Timebox this strictly. Running out of time is part of the
> exercise, not a failure.

### Step 8 — Read the ticket

This is what you have been given. It is a realistic ticket: a colleague wrote it
quickly, and it is the only thing on your desk.

> **Ticket IDR-101: Flag disordered regions in protein sequences**
>
> For the condensate assay planning we need a helper that flags intrinsically
> disordered regions in a protein sequence, so we can shortlist constructs.
>
> Slide a window along the sequence and score each residue by the fraction of
> disorder-promoting residues in its window. Residues whose score passes the
> threshold count as disordered. Consecutive disordered residues form a region —
> report each region's start and end position. Ignore very short regions.
>
> The two residue groups:
>
> - disorder-promoting: `P E S Q K A G R D T`
> - order-promoting: `W C F I Y V L M N H`
>
> Defaults: window 5, threshold 0.6, minimum region length 5.

### Step 9 — Create the stub you must fill in

The function signature is fixed, because it is what the grading suite calls.

```bash
cat > src/idr.py <<'EOF'
def find_disordered_regions(
    sequence: str,
    window: int = 5,
    threshold: float = 0.6,
    min_length: int = 5,
) -> list[tuple[int, int]]:
    """Flag intrinsically disordered regions in a protein sequence.

    Returns a list of (start, end) region coordinates.
    """
    raise NotImplementedError
EOF
```

### Step 10 — Implement it with your assistant

Start your assistant in the project folder and get it to implement IDR-101.

**Rules for this round:**

1. Prompt however you like. Long prompts, short prompts, several turns — your
   call.
2. Work from the ticket. It is self-contained — the residue groups are in it,
   so there is no other file to hand over.
3. Do **not** read ahead in this document. Part 3 onwards is spoilers.
4. Stop when the facilitator calls time, finished or not.

A perfectly reasonable opening prompt:

```text
>>> Implement the function in src/idr.py according to this ticket:
>>>
>>> [paste the ticket from Step 8]
>>>
>>> Keep it to that one file.
```

### Step 11 — Sanity-check your own work

Try it yourself before the checkpoint:

```bash
uv run python -c "
from src.idr import find_disordered_regions as f
print(f('PESQKAGRDT'))
print(f('WCFIYVLMWCFIYVLM'))
"
```

**Expected:** the first call prints `[(1, 10)]` and the second prints `[]`.

Ask yourself, and write your answer down in one line somewhere:

> *How confident am I that this is correct? What exactly am I basing that on?*

Close your AI assistant.
```text
>>> CTRL-D
```

**Stop here until the facilitator calls the checkpoint.**

---

## Part 3 — Checkpoint A: meet the acceptance suite

> **5 minutes.** Do not read this part before the facilitator says so.

### Step 12 — Receive the acceptance suite

The requester's real expectations were written down as executable tests. Create
the file exactly as given — **do not edit it, and do not adjust it to fit your
implementation.**

```bash
mkdir -p hidden
```

Now create `hidden/test_acceptance.py` with the content your facilitator shares
(or copy it from the block below).

```bash
touch hidden/test_acceptance.py
vi hidden/test_acceptance.py
```

<details>
<summary><b>hidden/test_acceptance.py</b> — click to expand</summary>

```python
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
```

</details>

### Step 13 — Run it and record your score

```bash
uv run pytest hidden/ --no-cov -q
```

**Write your score down now — you will compare against it in an hour.**

```text
Round 1 score:  ______ passed / 19
```

If you see `ModuleNotFoundError: No module named 'src'`, you missed Step 6a. Add
`pythonpath = ["."]` to `[tool.pytest.ini_options]` and run again.

### Step 14 — Reflect (3 minutes, no code)

Read the failures. Then answer, out loud with your neighbour:

> **What did those tests know that your prompt did not tell the assistant?**

Look specifically at whether your implementation:

- treats a score of exactly `0.6` as disordered, or not;
- gives the first and last residues a score at all;
- counts positions from 0 or from 1;
- keeps a region whose length is exactly 5;
- accepts `PESQ-KAGRDT` or rejects it.

None of those five questions is answered by the ticket. Your assistant had to
guess all five. So did you.

---

## Part 4 — Round 2: specification first

> **35 minutes.** Same ticket, same assistant, same tests. The difference is that
> this time you agree what the thing should do *before* anyone writes code.

### Step 15 — Park your Round 1 implementation

Keep it — you want to be able to look at it later — but get it out of the way:

```bash
git add -A
git commit -m "Round 1: prompt-only implementation"
git tag round-1
rm src/idr.py
git add -A
git commit -m "Round 1: remove implementation to start Round 2"
```

`hidden/` stays exactly where it is. You are allowed to look at the tests now,
but **do not edit them**, and resist writing code that special-cases them.

### Step 16 — Store the ticket as project evidence

The workflow you are about to run begins from written evidence, not from
conversation. Save the ticket verbatim:

```bash
mkdir -p sdlc_docs/00_inception/sources

cat > sdlc_docs/00_inception/sources/informal_project_request_idr-101.md <<'EOF'
# Source: Ticket IDR-101 — Flag disordered regions in protein sequences

Received: 2026-08-20
Origin: Ticket IDR-101, provided by the developer in the SDLC session
Preservation: verbatim, unedited

---

Ticket IDR-101: Flag disordered regions in protein sequences

For the condensate assay planning we need a helper that flags intrinsically
disordered regions in a protein sequence, so we can shortlist constructs.

Slide a window along the sequence and score each residue by the fraction of
disorder-promoting residues in its window. Residues whose score passes the
threshold count as disordered. Consecutive disordered residues form a region —
report each region's start and end position. Ignore very short regions.

The two residue groups:

- disorder-promoting: P E S Q K A G R D T
- order-promoting: W C F I Y V L M N H

Defaults: window 5, threshold 0.6, minimum region length 5.

This is a deliberately simplified stand-in for real disorder prediction, not a
predictor. Production tools (IUPred3, metapredict, flDPnn, or AlphaFold pLDDT as
a disorder proxy) use learned models, evolutionary information, and calibrated
scores. What participants build is a compositional heuristic: a binary
disorder-promoting / order-promoting partition of the twenty amino acids,
smoothed over a window.
EOF
```

### Step 17 — Re-create the stub the agent will fill in again

The function signature is fixed, because it is what the grading suite calls.

```bash
cat > src/idr.py <<'EOF'
def find_disordered_regions(
    sequence: str,
    window: int = 5,
    threshold: float = 0.6,
    min_length: int = 5,
) -> list[tuple[int, int]]:
    """Flag intrinsically disordered regions in a protein sequence.

    Returns a list of (start, end) region coordinates.
    """
    raise NotImplementedError
EOF
```

### Step 18 — Start the workflow

Start your assistant in the project folder, then launch the orchestrator:

| Tool | What to type |
| --- | --- |
| Claude Code | `/sdlc-orchestrate-workflow` |
| Codex CLI | the plain-language prompt below |
| anything else | the plain-language prompt below |

#### Claude Code skill prompting
```text
>>> /sdlc-orchestrate-workflow
```

#### Plain-language prompt in Codex CLI or any other assistant
```text
>>> Read .agents/skills/sdlc-orchestrate-workflow/SKILL.md and follow it.
>>> Act as the SDLC workflow orchestrator for this repository.
>>> A new source request is in sdlc_docs/00_inception/sources/.
>>> Tell me the current stage and the next action I need to take.
```

**Expected:** the assistant notices there is no `sdlc_docs/trace_workflow.md`,
proposes to create the workflow structure, and asks you to approve. Approve it.
Then it moves to request clarification and starts asking you questions.

> **The approval gates are the point.** The workflow deliberately stops and asks.
> Read what it proposes before you say yes. If you approve without reading, you
> have rebuilt Round 1 with more ceremony.

### Step 19 — Answer the clarification questions

The assistant will ask project-level questions. Answer from the table below.
These are the requester's real answers; you are playing the requester.

**Answer bank — project level**

| If asked about | Answer                                                                                                 |
| --- |--------------------------------------------------------------------------------------------------------|
| Is `src/scales.py` supplied, or do we design the residue partition? | Supplied as given material. The project consumes it as a fixed input and does not define or modify it. |
| Who uses this, and how? | Scientists run it themselves. They do not write code.                                                  |
| One sequence per run, or many? | Many per run. Input is a FASTA file.                                                                   |
| What makes the first version useful? | A per-sequence table of flagged regions that can be quickly eyeballed.                                 |
| Are the defaults fixed or adjustable? | Adjustable. Window 5, threshold 0.6, minimum region length 5 apply when nothing is given.              |
| Is there a deadline? | The deadline is at the end of the workshop, about 50 minutes. This is the dominant constraint.         |
| Who approves the artifacts? | I do. I am both the developer and the approver.                                                        |
| What should the output identify? | Which sequence each region came from, plus the region's start and end.                                 |
|Limits: should the output tell users it's only a heuristic? | yes, it's only a heuristic                                                                             |

If the assistant asks something not in the table, answer it yourself — sensibly
and briefly — and note that you had to. That, too, is data.

**Expected:** an approved `clarified_project_request.md` in
`sdlc_docs/00_inception/`, with your answers recorded against each question.

### Step 20 — Approve the project context

The workflow next builds `sdlc_docs/00_inception/project_context.md` — the
problem, the users, the scope boundary, the constraints, the risks.

Read it. Check three things specifically:

1. Does the MVP boundary say "many sequences in one run"?
2. Is the "not a scientific predictor" constraint written down?
3. Is the 50-minute delivery limit recorded as a constraint?

Approve it when those are right. **Keywords** are ">>> approve, approver-name, today".

### Step 21 — Approve the requirements and acceptance criteria

This is the step that decides your score. The workflow produces
`sdlc_docs/01_requirements/product_requirements.md` with user stories and
Gherkin-style acceptance criteria.

**The stories that come out of the ticket alone will still be underspecified.**
The ticket never said whether `>=` or `>` — so neither will the stories, unless
you say so.

When the assistant asks its detail questions — or, if it does not ask, when it
presents the criteria for approval — give it the following. This is the
agreement the requester and the developer actually reached.

> ### IDR-101 — Acceptance criteria (agreed with the requester)
>
> 1. **Score.** For each residue, the score is the fraction of residues in its
>    window that are in `DISORDER_PROMOTING`. The window is centred on the
>    residue and is `window` residues wide.
> 2. **Termini.** Where a full centred window does not fit, truncate it to the
>    residues that exist. Every residue in the sequence receives a score; the
>    denominator is the number of residues actually in the (possibly truncated)
>    window.
> 3. **Threshold.** A residue is disordered when `score >= threshold`.
> 4. **Regions.** Maximal runs of consecutive disordered residues. A single
>    below-threshold residue ends a run — regions are never merged across a gap.
> 5. **Coordinates.** 1-based and inclusive at both ends, matching UniProt
>    feature conventions. A region covering the whole of a 10-residue sequence is
>    `(1, 10)`.
> 6. **Minimum length.** Keep regions whose inclusive length is `>= min_length`;
>    discard shorter ones entirely (do not merge them into neighbours).
> 7. **Order.** Regions are returned sorted by start position.
> 8. **Input — silently normalised:** whitespace and newlines are stripped.
> 9. **Input — lowercase means soft-masked.** Following the convention of BLAST
>    and the masking tools, a lowercase residue marks a low-complexity or
>    otherwise untrustworthy position. Masked residues are accepted and occupy
>    their slot in the window denominator, but never count as disorder-promoting
>    and can never appear in a reported region. Do not uppercase the sequence to
>    make the problem go away.
> 10. **Input — accepted as residues:** the 20 standard amino acids plus `X`,
>     `B`, `Z`, `U`. The ambiguous four count toward the window denominator and
>     are never disorder-promoting.
> 11. **Input — rejected with `ValueError`:** gap characters (`-`, `.`) and any
>     other character. A gap means an aligned sequence was passed in; ungapping
>     it silently would produce coordinates that refer to nothing.
> 12. **Parameters.** `window` must be odd and positive; `threshold` in `[0, 1]`;
>     `min_length >= 1`. Otherwise `ValueError`.
> 13. **Empty sequence** returns an empty list, not an error.
> 14. **Output.** Table: plain whitespace-aligned columns sequence ID, start, end, length, residues;
>     a "no flagged regions" row; the notice printed once below the table.
> 15. Command name of the command-line tool: identify-disordered-regions.
> 16. Flags: --window, --threshold, --min-length.
> 17. Errors: message to stderr, exit code 1, no traceback.

Paste it like this:

```text
>>> Here are the acceptance criteria agreed with the requester. Fold every one of
>>> these into the user stories before I approve them — I want each point
>>> traceable to a scenario.
>>>
>>> [paste the thirteen points above]
```

**Expected:** requirements with four user stories (e.g. read the input; flag
regions; read the regions per sequence; override the defaults; the table) and around 21 scenarios, each carrying
scenarios that cover the thirteen points. Approve when they do.

> **Notice what just happened.** Points 8 to 12 are not in the ticket. Points 9
> and 11 are not derivable from it by any route: both are conventions that live
> in the requester's head, and point 9 is the opposite of what any careful
> implementer would do on their own. No amount of prompting skill produces them
> in Round 1 — only asking the requester does.

### Step 22 — Skip architecture and technical foundation, on purpose

The full workflow next wants architecture design, repository issue
synchronisation, and technical-foundation setup. **You do not have time, and the
template already gave you the foundation.** Tell the orchestrator explicitly and
approve the requirements and acceptance criteria when they are right beforehand:

```text
>>> approve, approver-name, today
>>> I am consciously skipping the architecture, repository synchronisation, and
>>> technical foundation stages because of the workshop deadline. Record that
>>> decision honestly in sdlc_docs/trace_workflow.md — do not mark those stages
>>> as complete. Proceed to implementation.
```

**Expected:** the trace file records those stages as *Not Started* with the
skipped-on-developer-direction reason, and does **not** claim them as done. If
your assistant marks them complete anyway, correct it. A traceability document
that lies is worse than no document.

### Step 23 — Implement against the approved criteria

```text
>>> Implement the approved user stories. Put the flagging logic in
>>> src/disordered_regions_flagger/idr.py and import the residue sets from the
>>> supplied src/scales.py, which must not be modified.
>>> Write unit tests alongside the implementation.
```

**Expected:** an implementation in the package, plus its own unit tests under
`tests/unit/`.

### Step 24 — Close your AI assistant before you continue

```text
>>> CTRL-D
```

### Step 25 — Run the acceptance suite again

```bash
uv run pytest hidden/ --no-cov -q
```

```text
Round 2 score:  ______ passed / 19
```

Also run your own tests and the quality gates:

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```

### Falling behind? The fast lane

If the clock beats you, you can still make the point. Drop the workflow and give
the criteria straight to the assistant:

```text
>>> Implement src/idr.py to this specification exactly:
>>>
>>> [paste the thirteen acceptance criteria from Step 21]
```

Then run `uv run pytest hidden/ --no-cov -q`. You will score close to full marks.
That is the lesson in its shortest form: **the specification did the work, not
the prompt.**

---

## Part 5 — Checkpoint B and debrief

### Step 26 — Compare

```text
Round 1:  ______ / 19     (prompt only)
Round 2:  ______ / 19     (specification first)
```

### Step 27 — The three points

1. **The assistant was never the variable.** Same model, same session, same
   ticket. The score moved because the specification moved.

2. **The failures clustered in the places nobody wrote down.** `>=` versus `>`.
   Termini. 1-based versus 0-based. Whether a gap character is data or an error.
   Whether lowercase means "the same residue" or "do not trust this position".
   An assistant cannot infer a decision that was never made — it can only pick
   one and sound confident about it.

3. **The approval gates are where the value is, and they are the part that is
   tempting to skip.** Every gate you clicked through without reading is a place
   where you accepted a guess as a decision.

### Step 28 — Questions worth arguing about

- Your Round 1 code probably *ran*. It produced regions. How long would it have
  taken to notice it was wrong, without the acceptance suite?
- Point 11 rejects gap characters instead of stripping them. Stripping would be
  "more helpful". Why is rejecting the right call here?
- Which of the thirteen criteria could a scientist have supplied in thirty
  seconds, if anyone had thought to ask?

---

## Part 6 — Stretch goals

If you have time left, in rough order of value.

### 6.1 Try out the command-line interface

```bash
source .venv/bin/activate
uv run flag-disordered-regions data/demo.fasta
```

### 6.2 Implement the command-line interface if it doesn't exist yet

The requester wants scientists — who do not write code — to run this over a FASTA
file. Open your AI assistant and ask it to implement a command-line entry point that reads a FASTA
file.

```text
>>> Add a command-line entry point flag-disordered-regions that reads a FASTA
>>> file, flags every sequence in it, and prints one row per region with the
>>> sequence identifier, start, end, length, and residues. Put the summary line
>>> on stderr so stdout stays pipeable. Register it in pyproject.toml.
```

Close your AI assistant again.
```text
>>> CTRL-D
```

Then:

```bash
source .venv/bin/activate
uv run flag-disordered-regions data/demo.fasta
```

**Expected, similar to:**

```text
sequence                                          start               end  length
demo_ordered Fully order-promoting control        no flagged regions
demo_disordered Fully disorder-promoting control  1                   20   20
demo_mixed Ordered head, disordered tail          13                  22   10

Note: regions are flagged by a simple compositional heuristic, not a disorder predictor.
3 sequence(s) read, 2 region(s) flagged
```

And with different parameters:

```bash
uv run flag-disordered-regions data/demo.fasta --window 7 --threshold 0.55 --min-length 10
```

### 6.2 Run the validation stage

The workflow has a stage that turns approved acceptance criteria into Gherkin
feature files and pytest-bdd scenarios:

```text
>>> Run the user story completion validation stage for the implemented stories.
```

This is the difference between "my unit tests pass" and "the agreed criteria are
demonstrably met" — a distinction the trace file takes seriously.

### 6.3 Try a real protein

Download a genuinely disordered protein from UniProt and look at what you get:

```bash
curl -o data/cdkn1a.fasta "https://rest.uniprot.org/uniprotkb/P38936.fasta"
uv run flag-disordered-regions data/cdkn1a.fasta
```

P38936 (CDKN1A / p21) is extensively disordered, so you should see substantial
regions. **Then check yourself:** run the same sequence through
[metapredict](https://metapredict.net/) or IUPred3 and compare. The differences
are the honest measure of what a compositional heuristic can and cannot do.

### 6.4 Open a pull request

```text
>>> Run the implementation pull request stage.
```

---

## Part 7 — Troubleshooting

| Symptom | Cause | Fix                                                                                         |
| --- | --- |---------------------------------------------------------------------------------------------|
| `cookiecutter: command not found` | not on PATH | reopen the shell, or use `uvx cookiecutter <url>`                                           |
| `ModuleNotFoundError: No module named 'src'` when running `hidden/` | missing pytest path config | run `bash scripts/configure_exercise_repo.sh` (Step 6)                                      |
| `ImportError: cannot import name 'find_disordered_regions' from 'src.idr'` | implementation is in the package, bridge missing | add the bridge module (Step 24)                                                             |
| `uv run pytest` says `no tests ran`, exit code 5 | correct after setup — `testpaths = ["tests"]` and you have none yet | not an error; the graded suite is run explicitly: `uv run pytest hidden/`                   |
| Coverage warnings when running `hidden/` | `addopts` applies coverage everywhere | add `--no-cov`, as the commands here do                                                     |
| `ZeroDivisionError` on a sequence of `X` | ambiguous residues excluded from the denominator | criterion 9: they count in the denominator                                                  |
| Assistant edits `hidden/` or `src/scales.py` | it is being helpful | revert with `git checkout -- hidden src/scales.py` and tell it those files are fixed inputs |
| Assistant marks skipped stages complete | it is being agreeable | correct it explicitly; see Step 22                                                          |
| Slash command not recognised | tool differences | use the plain-language fallback in §0.6                                                     |
| Pre-commit reformats `hidden/` | missing excludes | run `bash scripts/configure_exercise_repo.sh` (Step 6)                                      |
| Round 2 is running out of time | full workflow is long | take the fast lane at the end of Part 4                                                     |

---

## Appendix A — Worked scoring example

Do this one by hand before you trust any implementation, including your own.

**Sequence:** `WCFIYPESQKWCFIY` (15 residues)
**Parameters:** window 5, threshold 0.6, minimum length 5

Disorder-promoting residues are `P E S Q K A G R D T`. In `WCFIYPESQKWCFIY` those
are positions 6–10 (`PESQK`); everything else is order-promoting.

| Pos | AA | Window | Disorder / total | Score | `>= 0.6`? |
| ---: | :-- | :-- | :-- | ---: | :-- |
| 1 | W | `WCF` | 0/3 | 0.00 | no |
| 2 | C | `WCFI` | 0/4 | 0.00 | no |
| 3 | F | `WCFIY` | 0/5 | 0.00 | no |
| 4 | I | `CFIYP` | 1/5 | 0.20 | no |
| 5 | Y | `FIYPE` | 2/5 | 0.40 | no |
| 6 | P | `IYPES` | 3/5 | **0.60** | **yes** |
| 7 | E | `YPESQ` | 4/5 | 0.80 | yes |
| 8 | S | `PESQK` | 5/5 | 1.00 | yes |
| 9 | Q | `ESQKW` | 4/5 | 0.80 | yes |
| 10 | K | `SQKWC` | 3/5 | **0.60** | **yes** |
| 11 | W | `QKWCF` | 2/5 | 0.40 | no |
| 12 | C | `KWCFI` | 1/5 | 0.20 | no |
| 13 | F | `WCFIY` | 0/5 | 0.00 | no |
| 14 | I | `CFIY` | 0/4 | 0.00 | no |
| 15 | Y | `FIY` | 0/3 | 0.00 | no |

**Result:** `[(6, 10)]`

Four of the seven judgement calls are visible in this one table:

- **Positions 1, 2, 14, 15** have truncated windows — 3 or 4 residues, not 5. The
  denominator is what actually fits (criterion 2).
- **Positions 6 and 10** score *exactly* 0.60. With `>` instead of `>=`, the
  region shrinks to `(7, 9)` — length 3 — and is then dropped for being shorter
  than the minimum. The answer becomes `[]` (criterion 3).
- **Coordinates are 1-based inclusive.** 0-based would be `(5, 9)` (criterion 5).
- **The region is exactly 5 residues**, exactly the minimum. With `> min_length`
  it disappears (criterion 6).

One fifteen-residue sequence, four ways to get a defensible but wrong answer.

---
---

# Appendix B — FACILITATOR ONLY

> ## ⛔ Do not project, distribute, or share this appendix
>
> It contains the answer key, the seeded ambiguities, and the expected scores.
> If participants read it before Checkpoint A, the exercise no longer measures
> anything. Consider distributing Parts 0–7 and Appendix A as a separate file.

---

## B.1 Design intent

The exercise is a controlled comparison with one variable. Participants build the
same function twice, with the same assistant, in the same session. Only the
specification changes.

The ticket is engineered to be **plausible and underspecified in seven specific
ways**. Each ambiguity is one an experienced developer would notice and ask
about, and one an assistant will silently resolve by guessing. The acceptance
suite tests exactly those seven points.

The failure is therefore **not** a failure of the model, and it must not be
debriefed as one. The model answered the question it was asked. The question was
incomplete.

## B.2 Runbook

| Clock | Step | What you do |
| --- | --- | --- |
| before | Setup | Send Parts 0–1 out at least a day ahead. Setup needs network and a dependency install; doing it live costs 15 minutes you do not have. |
| 0:00 | Open | Confirm everyone's setup checklist passes. Fix stragglers with the fast path in B.7. Deliver the honesty caveat (§0.3) **before** any code — it is the one non-negotiable line. |
| 0:03 | Round 1 | "Implement IDR-101 with your coding assistant. Prompt however you like. Ten minutes." Do not hint. Do not answer questions about `>=`, termini, or coordinates — say *"the ticket is what you have."* That refusal is the experiment. |
| 0:13 | Checkpoint A | Distribute `hidden/test_acceptance.py`. `uv run pytest hidden/ --no-cov -q`. **Show of hands: who is fully green?** Expect none. Collect three or four scores out loud. Then three minutes on: *what did the tests know that your prompt didn't?* |
| 0:18 | Round 2 | Hand out the clarified acceptance criteria. Launch the workflow. Circulate — the failure mode here is approving gates without reading them. Announce the fast lane at 0:45 for anyone still in requirements. |
| 0:55 | Checkpoint B | Re-run the suite. Show of hands again. Put the two score distributions side by side. |
| 1:00 | Debrief | Land the three points (§B.6), then hand over. |

## B.3 The seeded ambiguities

The third column is what current assistants actually do, measured on the
material as it stands. Several of these ambiguities now resolve *correctly* by
default — that is a property of the models, not of the ticket, and it is why
B.4's numbers are higher than they once were.

| # | Ambiguity | Typical assistant behaviour | Intended resolution | Guarded by |
| --- | --- | --- | --- | --- |
| **A1** | "passes the threshold" — `>` or `>=`? | Usually `>=`; a hurried implementation picks `>` | **`>=`** — at or above counts as disordered | `test_score_exactly_at_threshold_counts_as_disordered` |
| **A2** | Termini: the first and last `window//2` residues have no complete centred window | Usually **truncates by accident** — `seq[max(0, i-h):i+h+1]` is the idiomatic Python slice and it clamps. Weak implementations skip or pad. | **Truncate the window** to the residues that exist. Every residue gets a score. | `test_n_terminal_region_reaches_residue_one`, `test_c_terminal_region_reaches_the_last_residue` |
| **A3** | Coordinate convention | Usually 1-based for protein positions — the model knows the UniProt convention. Weak implementations return 0-based or half-open. | **1-based, inclusive both ends** (UniProt feature convention) | `test_coordinates_are_one_based_inclusive` |
| **A4** | "Ignore very short regions" — is a region of exactly `min_length` short? | Usually `>= min_length`; occasionally `> min_length`, or the check is dropped | Keep regions of length **`>= min_length`** | `test_region_of_exactly_min_length_is_reported` |
| **A5** | Non-standard input: whitespace, `X`, gap `-`, digits | Strips whitespace almost always. Whether it validates at all, and whether its alphabet includes `X`, is a live coin-flip — and it decides two or three of the nineteen. | **Deliberately non-uniform** — strip whitespace, accept `XBZU` into the denominator, reject gaps and everything else | `test_whitespace_and_newlines_are_stripped`, `test_gap_character_raises`, `test_invalid_character_raises`, `test_unknown_residue_x_...` |
| **A6** | Two qualifying regions separated by a short ordered stretch | Rarely merges unless asked — this one usually resolves correctly | **No merging.** Any below-threshold residue ends the region. | `test_regions_separated_by_a_short_gap_are_not_merged` |
| **A7** | Even `window` — where is the centre? | Often silently uses an asymmetric window. The most reliable of the *guessable* failures. | `window` must be **odd and positive**, else `ValueError` | `test_even_window_raises` |
| **A8** | Lowercase residues — the same residue, or a signal? | **Calls `.upper()` and moves on. Every implementation does, which is why this is the only criterion nothing reaches.** | **Lowercase marks a soft-masked residue** (BLAST/RepeatMasker convention): accepted, occupies its window slot, never disorder-promoting, never inside a reported region | `test_lowercase_is_soft_masked_and_never_flagged`, `test_masked_stretch_splits_a_region_and_fills_its_window_slots` |

**A5 is deliberately inconsistent**, and this is the most instructive one. Case
and whitespace are normalised silently; gap characters are a hard error. There is
no general principle a model could apply to derive both. The reason is domain
knowledge: a gap character means someone passed in an *aligned* sequence, and
silently ungapping it yields coordinates that point at the wrong residues. That
rule lives in a scientist's head, not in the ticket.

Be honest with yourself about the limit of that argument: an assistant that
validates its input *at all* rejects gaps and digits together, for generic
defensive reasons rather than domain ones, and collects both tests without
understanding either. Getting a criterion right for the wrong reason still
counts as green on the board. What the suite cannot show, and the debrief must,
is that nobody in the room could have known which of these they got right.

**A8 is the one that cannot be reached by being careful.** `.upper()` is the
first line of every sequence-handling function ever written, and here it is the
bug: it erases the masking flag that a colleague's pipeline put there on
purpose. Uppercasing turns "do not trust these residues" into "these residues
are fine", and the function then reports a region the requester would have
thrown out. No amount of prompting produces this rule, because the default is
not merely a coin-flip — it is unanimous, and it is wrong. Watch for the
participant who passes the first A8 test by accident: an implementation that
never normalises case at all flags nothing in a lowercase sequence, which is the
right answer for the wrong reason. The second A8 test is there to catch exactly
that.

## B.4 Expected outcomes — measured, not estimated

Every figure below was produced by running the acceptance suite against an
implementation written to represent that case, on the current exercise material
(re-measured 2026-09-16, after the residue whitelist was removed from the
supplied `scales.py`, the residue groups moved into the ticket, and the
soft-masking rule A8 was added).

| Implementation | Score | Fails on |
| --- | --- | --- |
| **Minimal effort** — strict `>`, incomplete windows left unscored, 0-based coordinates, `> min_length`, no normalisation, no validation | **6 / 19** | 13 tests across A1–A8 |
| **Assistant default, no input validation** — `>=`, truncated windows, 1-based inclusive, `>= min_length`, uppercases and strips whitespace | **14 / 19** | gap, invalid character, even window, both masking tests |
| …plus validation against the two supplied residue sets | **15 / 19** | `test_unknown_residue_x_…`, even window, both masking tests |
| …plus validation that also accepts `X` | **16 / 19** | even window, both masking tests |
| …plus a check that `window` is odd | **17 / 19** | both masking tests |
| **Round 2, specification in hand** | **19 / 19** | — |

**17 / 19 is a hard ceiling, and this time the word is justified.** Every row
above the last fails both A8 tests, because every one of them calls `.upper()`.
That is not a coin-flip that sometimes lands well, like `>=` or the coordinate
base — it is unanimous behaviour, and the requester's convention is its
opposite. A participant cannot prompt their way past it; they can only ask.

The rest of the band is luck. Between 14 and 17 the differences are whether the
assistant validated its input at all, whether its alphabet happened to include
`X`, and whether it happened to think about even windows. Nothing in the ticket
distinguishes those cases, and nothing in the participant's experience of the
session distinguishes them either.

Two things to carry into the debrief:

- **"Nearly all green" is not "nearly right".** The surviving failures are the
  expensive ones. A 15/19 implementation crashes on any real UniProt entry
  containing `X`. A 16/19 one silently shifts every coordinate it reports when
  someone passes an even window. A 17/19 one reports masked, low-complexity
  junk as a construct worth shortlisting — and reports it with full confidence.
- **Watch for accidental correctness.** The minimal implementation passes
  `test_lowercase_is_soft_masked_and_never_flagged` without knowing the rule
  exists: it never normalises case, so a lowercase sequence matches nothing and
  it flags nothing. `test_masked_stretch_splits_a_region_and_fills_its_window_slots`
  is what separates knowing from guessing, and it fails that one.

If you want the gap wider still, the remaining lever of this kind is A2:
require positions without a complete centred window to be left *unscored*, which
several real predictors do. It defeats `seq[max(0, i-h):i+h+1]`, the idiomatic
clamped slice every assistant writes, and is worth two more tests. Re-measure
this table if you adopt it.

## B.5 Materials to prepare

| Item | When | How                                                                                                                                                                          |
| --- | --- |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Parts 0–7 + Appendix A | day before | Send as a file or link. **Not this appendix.**                                                                                                                               |
| `hidden/test_acceptance.py` | at 0:13 | Paste in chat, share a gist, or have participants expand the collapsed block in Part 3. Whichever you choose, say it out loud — the honour system holds fine if you name it. |
| The thirteen acceptance criteria | at 0:18 | They are in Step 21. Also worth a slide.                                                                                                                                     |
| `scripts/configure_exercise_repo.sh` | before | Participants fetch it with the `curl` in Step 6. Confirm that URL resolves from a fresh machine; keep a copy to hand out if the network or the repository is not reachable.  |
| A working reference repo | before | Have one on your own machine, fully green, so you can demonstrate rather than debug live.                                                                                    |

## B.6 Debrief — the three points

Deliver in this order. The order matters: point 1 removes the defensiveness
before points 2 and 3 land.

**1. Nothing about the AI changed between the two rounds. Only the
specification did.**
Say this sentence verbatim at the start. Participants arrive at Checkpoint A
assuming they prompted badly, or that the model is weak. Both readings are wrong
and both block the actual lesson.

**2. The failures clustered exactly where nobody had made a decision.**
Walk the A1–A8 table on a slide. Every failure is a place where the ticket left a
question open, so the model answered it — confidently, plausibly, and without
flagging that it had done so. That last part is the risk: there was no signal.

**3. The approval gates carry the value, and they are the first thing people
skip.**
Ask who read the requirements document before approving it. Ask who noticed the
criteria did not mention `>=` until they pasted the thirteen points in. In Round 2
the workflow forced the questions to surface; the participants still had to
actually answer them.

**Closing line:** *You will not always have an acceptance suite. You will always
have the option of writing the specification down first.*

## B.7 Facilitation notes and failure modes

| Situation | Handling |
| --- | --- |
| **Setup fails live** | Fast path: `git clone` a prepared repo at the end-of-setup state, or pair the participant with a neighbour. Do not debug `uv` in front of the room. |
| **A participant asks "should it be `>=` or `>`?" during Round 1** | *"The ticket is what you have."* Never resolve it. This is the measurement. |
| **Someone scores 15+ in Round 1** | Congratulate them, then show them B.4 row 2. Ask which of the three remaining tests they could have guessed. The answer is none. |
| **Someone hard-codes the test inputs in Round 2** | Call it out warmly — it is a real and common failure. Ask what the function does for a sequence not in the suite. |
| **The assistant edits `hidden/` or `src/scales.py`** | `git checkout -- hidden src/scales.py`. Worth pointing out to the room: an assistant asked to make tests pass may make the tests pass. |
| **The assistant marks skipped stages complete** | Correct it publicly. A traceability document that overstates completion is worse than none, and this is a live example of exactly that. |
| **Round 2 overruns** | Announce the fast lane at 0:45. The comparison survives without the full workflow; the workflow is the vehicle, the specification is the cargo. |
| **The room drifts into arguing about disorder prediction** | Redirect: the biology is a vehicle. Re-state §0.3 and move on. If interest is genuine, park it for 6.3. |

## B.8 Reference implementation

The fully worked repository — implementation, unit tests, CLI, and the complete
SDLC document trail — is the `disordered-regions-flagger` project this guide
ships with. The core function:

```python
def find_disordered_regions(
    sequence: str,
    window: int = 5,
    threshold: float = 0.6,
    min_length: int = 5,
) -> list[tuple[int, int]]:
    if window <= 0 or window % 2 == 0:
        raise ValueError(f"window must be odd and positive, got {window}")

    residues = "".join(sequence.split()).upper()
    unexpected = sorted(set(residues) - _ACCEPTED_RESIDUES)
    if unexpected:
        raise ValueError(
            "sequence contains characters that are not residue codes: "
            + ", ".join(repr(character) for character in unexpected)
        )

    half = window // 2
    length = len(residues)
    disordered: list[bool] = []
    for position in range(length):
        start = max(0, position - half)
        end = min(length, position + half + 1)
        frame = residues[start:end]
        promoting = sum(1 for residue in frame if residue in DISORDER_PROMOTING)
        disordered.append(promoting / len(frame) >= threshold)

    regions: list[tuple[int, int]] = []
    run_start: int | None = None
    for position, is_disordered in enumerate(disordered):
        if is_disordered and run_start is None:
            run_start = position
        elif not is_disordered and run_start is not None:
            if position - run_start >= min_length:
                regions.append((run_start + 1, position))
            run_start = None
    if run_start is not None and length - run_start >= min_length:
        regions.append((run_start + 1, length))
    return regions
```

Note for the debrief: this is **thirty lines**. The difficulty was never the
code. Every one of the seven ambiguities is settled in a single character or a
single clause — `>=` rather than `>`, `max(0, ...)` rather than a skip, `+ 1` on
the coordinate. The specification was the hard part, and it is the part the
ticket left out.

## B.9 Dry-run checklist

Run this yourself once, end to end, before facilitating:

- [ ] Cookiecutter generates cleanly with the answers in Step 2
- [ ] `uv sync --all-groups` completes on your network
- [ ] `.claude/skills` symlink resolves (or the copy step works on Windows)
- [ ] The Step 6 `curl` downloads `configure_exercise_repo.sh` and the script reports `Step 6 complete.`
- [ ] `uv run pytest hidden/ --no-cov -q` errors with `ModuleNotFoundError` **before** Step 6 and runs **after** it
- [ ] The orchestrator launches in the tools your participants will actually use
- [ ] The workflow reaches approved requirements in under 25 minutes at your typing speed
- [ ] The fast lane reaches 19/19
- [ ] `uv run flag-disordered-regions data/demo.fasta` reproduces the output in §6.1 exactly
