# Product Requirements

## 1. Document Control

- **Project:** disordered regions flagger
- **Mode:** Initial release
- **Source project context or increment issue:** `sdlc_docs/00_inception/project_context.md` (Closed, Ready for Product Requirements, 2026-09-21)
- **Last updated:** 2026-09-21
- **Active scope state:** Approved

## 2. Requirements Overview

| Requirement | Requirement status | Stories | Story status | Source | Repository issues |
|---|---|---|---|---|---|
| REQ-0001 — Flag disordered regions across a FASTA file from the command line | Approved | US-0001, US-0002, US-0003, US-0004 | Approved | Project Context section 12; acceptance criteria agreed with the requester (IDR-101), recorded 2026-09-21 | Not created |
| REQ-0002 — Adjustable analysis parameters | Approved | US-0005, US-0006 | Approved | Project Context section 12; acceptance criteria agreed with the requester (IDR-101), recorded 2026-09-21 | Not created |
| REQ-0003 — Predictable sequence input rules | Approved | US-0007 | Approved | Project Context section 12; acceptance criteria agreed with the requester (IDR-101), recorded 2026-09-21 | Not created |
| REQ-0004 — Heuristic notice | Approved | US-0008 | Approved | Project Context section 12; acceptance criteria agreed with the requester (IDR-101), recorded 2026-09-21 | Not created |

### Source Statement Coverage Register

| Source ID | Source scope statement | Source location | Statement role | Decomposed into CAP IDs | Rationale |
|---|---|---|---|---|---|
| SRC-001 | Run as a single command from a terminal. | Project Context section 12, Included High-Level Capabilities | Atomic | CAP-001 | One independently observable outcome: the user starts the tool from a terminal. |
| SRC-002 | Accept many protein sequences in one run. | Project Context section 12, Included High-Level Capabilities | Atomic | CAP-002 | One independently observable outcome: every sequence in the supplied FASTA file is processed in a single run. |
| SRC-003 | Flag disordered regions using the stated sliding-window composition heuristic. | Project Context section 12, Included High-Level Capabilities | Atomic | CAP-003 | One independently observable outcome: the flagged regions produced by the heuristic. |
| SRC-004 | Report flagged regions per sequence, by start and end position, in a readable table. | Project Context section 12, Included High-Level Capabilities | Atomic | CAP-004 | One independently observable outcome: the table the user reads. |
| SRC-005 | Accept overrides for window, threshold, and minimum region length. | Project Context section 12, Included High-Level Capabilities | Compound | CAP-005, CAP-006, CAP-007, CAP-008 | Three separately observable overrides plus the separately observable rejection of invalid values. |
| SRC-006 | Apply the stated rules for accepted residues, ambiguous codes, gap rejection, and soft-masked positions. | Project Context section 12, Included High-Level Capabilities | Compound | CAP-009, CAP-010, CAP-011, CAP-012 | Four separately observable input behaviours stated in one sentence. |
| SRC-007 | Make clear that the result is a heuristic and not a disorder prediction. | Project Context section 12, Included High-Level Capabilities | Atomic | CAP-013 | One independently observable outcome: the notice the user sees. |

### Source Scope Coverage Matrix

| Scope ID | Atomic capability | Source IDs | Source scope statement | Source location | Disposition | Requirement / Stories | Rationale or approval evidence |
|---|---|---|---|---|---|---|---|
| CAP-001 | Run the flagger as one terminal command named identify-disordered-regions | SRC-001 | Run as a single command from a terminal. | Project Context section 12 | Covered | REQ-0001 / US-0001 | Single independently observable outcome |
| CAP-002 | Process every sequence of a supplied FASTA file in one run | SRC-002 | Accept many protein sequences in one run. | Project Context section 12 | Covered | REQ-0001 / US-0002 | Single independently observable outcome |
| CAP-003 | Flag disordered regions with the sliding-window composition heuristic | SRC-003 | Flag disordered regions using the stated sliding-window composition heuristic. | Project Context section 12 | Covered | REQ-0001 / US-0003 | Single independently observable outcome |
| CAP-004 | Read a per-sequence table of flagged regions | SRC-004 | Report flagged regions per sequence, by start and end position, in a readable table. | Project Context section 12 | Covered | REQ-0001 / US-0004 | Single independently observable outcome |
| CAP-005 | Override the window width | SRC-005 | Accept overrides for window, threshold, and minimum region length. | Project Context section 12 | Grouped | REQ-0002 / US-0005 | Approved grouping — the requester approved combining the three parameter overrides into one story on 2026-09-21 during Product Requirements Management |
| CAP-006 | Override the disorder threshold | SRC-005 | Accept overrides for window, threshold, and minimum region length. | Project Context section 12 | Grouped | REQ-0002 / US-0005 | Approved grouping — the requester approved combining the three parameter overrides into one story on 2026-09-21 during Product Requirements Management |
| CAP-007 | Override the minimum region length | SRC-005 | Accept overrides for window, threshold, and minimum region length. | Project Context section 12 | Grouped | REQ-0002 / US-0005 | Approved grouping — the requester approved combining the three parameter overrides into one story on 2026-09-21 during Product Requirements Management |
| CAP-008 | Reject invalid parameter values with an error | SRC-005 | Accept overrides for window, threshold, and minimum region length. | Project Context section 12 | Covered | REQ-0002 / US-0006 | Single independently observable outcome |
| CAP-009 | Accept the twenty standard amino acids plus the ambiguous codes X, B, Z, U | SRC-006 | Apply the stated rules for accepted residues, ambiguous codes, gap rejection, and soft-masked positions. | Project Context section 12 | Grouped | REQ-0003 / US-0007 | Approved grouping — the requester approved combining the four sequence input rules into one story on 2026-09-21 during Product Requirements Management |
| CAP-010 | Exclude soft-masked lowercase positions from reported regions | SRC-006 | Apply the stated rules for accepted residues, ambiguous codes, gap rejection, and soft-masked positions. | Project Context section 12 | Grouped | REQ-0003 / US-0007 | Approved grouping — the requester approved combining the four sequence input rules into one story on 2026-09-21 during Product Requirements Management |
| CAP-011 | Reject gap characters or any unrecognised character | SRC-006 | Apply the stated rules for accepted residues, ambiguous codes, gap rejection, and soft-masked positions. | Project Context section 12 | Grouped | REQ-0003 / US-0007 | Approved grouping — the requester approved combining the four sequence input rules into one story on 2026-09-21 during Product Requirements Management |
| CAP-012 | Strip whitespace from the input sequence silently | SRC-006 | Apply the stated rules for accepted residues, ambiguous codes, gap rejection, and soft-masked positions. | Project Context section 12 | Grouped | REQ-0003 / US-0007 | Approved grouping — the requester approved combining the four sequence input rules into one story on 2026-09-21 during Product Requirements Management |
| CAP-013 | Print the heuristic notice once below the table | SRC-007 | Make clear that the result is a heuristic and not a disorder prediction. | Project Context section 12 | Covered | REQ-0004 / US-0008 | Single independently observable outcome |

## 3. Requirements

## REQ-0001 — Flag disordered regions across a FASTA file from the command line

- **Status:** Approved
- **Source:** Project Context section 12, Included High-Level Capabilities SRC-001 to SRC-004
- **Evidence or basis:** Approved Project Context 2026-09-21; acceptance criteria agreed with the requester for IDR-101, recorded 2026-09-21
- **Imported classification:** Not applicable
- **Repository representation:** Not created
- **Repository issue:** Not created
- **Description:** A scientist runs one terminal command against a FASTA file and receives, for each sequence in that file, the disordered regions found by the sliding-window composition heuristic, presented as a readable table.
- **Approved by:** Maxim Scheremetjew
- **Reviewer role or responsibility:** Requester and owner of the work
- **Approval date:** 2026-09-21
- **Blocking Issues or Feedback:** None

### US-0001 — Run the flagger from the terminal

- **Status:** Approved
- **Source or evidence basis:** Project Context SRC-001; acceptance criteria 15 and 17 agreed with the requester
- **Covered scope IDs:** CAP-001
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a scientist planning condensate assays  
I want to start the flagger from my terminal  
so that I can use it without writing code.

#### Acceptance Criteria

**Scenario: Command name (criterion 15)**

Given the tool is installed  
When the scientist types `identify-disordered-regions`  
Then that command is the entry point of the tool.

**Scenario: Errors are reported without a traceback (criterion 17)**

Given an input or parameter that the tool rejects  
When the command runs  
Then the error message is written to standard error, the exit code is 1, and no traceback is shown.

### US-0002 — Flag every sequence of a FASTA file in one run

- **Status:** Approved
- **Source or evidence basis:** Project Context SRC-002; requester answer of 2026-09-21 selecting a FASTA file path
- **Covered scope IDs:** CAP-002
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a scientist shortlisting constructs  
I want to point the command at a FASTA file  
so that every sequence in it is processed in one run.

#### Acceptance Criteria

**Scenario: Every record is processed**

Given a FASTA file containing three sequence records  
When the scientist runs the command with the path to that file  
Then all three sequences are analysed in the single run.

**Scenario: Records are identified by their FASTA header**

Given a FASTA file whose records carry identifiers  
When the results are reported  
Then each result row carries the sequence identifier taken from that record's FASTA header.

### US-0003 — Flag disordered regions with the sliding-window heuristic

- **Status:** Approved
- **Source or evidence basis:** Project Context SRC-003; acceptance criteria 1 to 7 and 13 agreed with the requester
- **Covered scope IDs:** CAP-003
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a scientist planning condensate assays  
I want each residue scored by the composition of its surrounding window  
so that likely disordered stretches are flagged.

#### Acceptance Criteria

**Scenario: Residue score (criterion 1)**

Given a residue and a window width  
When the residue is scored  
Then the score is the fraction of residues in its window that are disorder-promoting, where the window is centred on that residue and is `window` residues wide.

**Scenario: Truncated window at the termini (criterion 2)**

Given a residue near the start or end of the sequence where a full centred window does not fit  
When the residue is scored  
Then the window is truncated to the residues that exist, every residue still receives a score, and the denominator is the number of residues actually present in the truncated window.

**Scenario: Threshold comparison (criterion 3)**

Given a scored residue  
When the score is compared with the threshold  
Then the residue counts as disordered when its score is greater than or equal to the threshold.

**Scenario: Regions are maximal runs (criterion 4)**

Given a sequence with two stretches of disordered residues separated by one residue below the threshold  
When regions are formed  
Then two separate regions are reported and they are not merged across that residue.

**Scenario: Coordinates are 1-based and inclusive (criterion 5)**

Given a sequence of ten residues that is disordered along its whole length  
When the region is reported  
Then its start is 1 and its end is 10.

**Scenario: Short regions are discarded (criterion 6)**

Given a run of disordered residues whose inclusive length is below the minimum region length  
When regions are reported  
Then that run is discarded entirely and is not merged into a neighbouring region.

**Scenario: Regions are ordered (criterion 7)**

Given a sequence containing several reported regions  
When the regions are returned  
Then they are sorted by start position.

**Scenario: Empty sequence (criterion 13)**

Given an empty sequence  
When it is analysed  
Then no regions are reported and no error is raised.

### US-0004 — Read the flagged regions as a table

- **Status:** Approved
- **Source or evidence basis:** Project Context SRC-004; acceptance criterion 14 agreed with the requester
- **Covered scope IDs:** CAP-004
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a scientist shortlisting constructs  
I want the flagged regions laid out as an aligned table  
so that I can scan them quickly.

#### Acceptance Criteria

**Scenario: Table columns (criterion 14)**

Given a run that flagged at least one region  
When the results are printed  
Then a plain whitespace-aligned table is shown with the columns sequence ID, start, end, length, residues.

**Scenario: A sequence with no flagged regions (criterion 14)**

Given a sequence in which no region passes the threshold and minimum length  
When the results are printed  
Then that sequence appears as a row stating that there are no flagged regions.

### Requirement Validation

- **Source evidence recorded:** Yes
- **Approved content changed:** No
- **Source scope statements omitted:** 0
- **Atomic capabilities without disposition:** 0
- **Compound stories without approved grouping:** 0
- **Coverage matrix/story mapping conflicts:** 0
- **Unsupported product behavior:** 0
- **Unresolved blocking questions:** 0
- **Duplicate repository story references:** 0
- **Overview/detail inconsistencies:** 0
- **Scope coverage validator:** Passed
- **Scope validator command:** python3 .agents/skills/c-manage-product-requirements/scripts/validate_scope_coverage.py sdlc_docs/00_inception/project_context.md sdlc_docs/01_requirements/product_requirements.md --mode initial-release --require-report-sync
- **Scope validator report synchronized:** Yes
- **Validation result:** Passed

## REQ-0002 — Adjustable analysis parameters

- **Status:** Approved
- **Source:** Project Context section 12, Included High-Level Capabilities SRC-005
- **Evidence or basis:** Approved Project Context 2026-09-21; acceptance criteria 12 and 16 agreed with the requester
- **Imported classification:** Not applicable
- **Repository representation:** Not created
- **Repository issue:** Not created
- **Description:** A scientist can vary the stringency of the analysis by supplying their own window width, threshold, and minimum region length, and is told plainly when a supplied value is not usable.
- **Approved by:** Maxim Scheremetjew
- **Reviewer role or responsibility:** Requester and owner of the work
- **Approval date:** 2026-09-21
- **Blocking Issues or Feedback:** None

### US-0005 — Adjust the analysis parameters

- **Status:** Approved
- **Source or evidence basis:** Project Context SRC-005; acceptance criterion 16 agreed with the requester; requester grouping approval of 2026-09-21
- **Covered scope IDs:** CAP-005, CAP-006, CAP-007
- **Atomicity:** Approved grouping — the requester approved combining the three parameter overrides into one story on 2026-09-21 during Product Requirements Management, because they are supplied the same way and are varied together when tuning stringency
- **Repository issue:** Not created

As a scientist shortlisting constructs  
I want to vary the window width, the threshold, and the minimum region length  
so that I can tune how strict the flagging is.

#### Acceptance Criteria

**Scenario: Parameter flags (criterion 16)**

Given the command is run  
When the scientist supplies parameters  
Then the flags `--window`, `--threshold`, and `--min-length` are the way to supply them.

**Scenario: Defaults when no flag is given**

Given no parameter flags are supplied  
When the command runs  
Then the window is 5, the threshold is 0.6, and the minimum region length is 5.

**Scenario: A supplied value takes effect**

Given a sequence that yields a region under the default threshold  
When the scientist raises the threshold so that no residue passes it  
Then no region is reported for that sequence.

### US-0006 — Reject invalid parameter values

- **Status:** Approved
- **Source or evidence basis:** Project Context SRC-005; acceptance criterion 12 agreed with the requester
- **Covered scope IDs:** CAP-008
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a scientist who does not write code  
I want an unusable parameter value refused with a clear message  
so that I do not act on a result produced by a setting I mistyped.

#### Acceptance Criteria

**Scenario: Window must be odd and positive (criterion 12)**

Given a window value that is even, zero, or negative  
When the command runs  
Then the value is refused with an error rather than analysed.

**Scenario: Threshold must lie between 0 and 1 (criterion 12)**

Given a threshold below 0 or above 1  
When the command runs  
Then the value is refused with an error rather than analysed.

**Scenario: Minimum region length must be at least 1 (criterion 12)**

Given a minimum region length below 1  
When the command runs  
Then the value is refused with an error rather than analysed.

### Requirement Validation

- **Source evidence recorded:** Yes
- **Approved content changed:** No
- **Source scope statements omitted:** 0
- **Atomic capabilities without disposition:** 0
- **Compound stories without approved grouping:** 0
- **Coverage matrix/story mapping conflicts:** 0
- **Unsupported product behavior:** 0
- **Unresolved blocking questions:** 0
- **Duplicate repository story references:** 0
- **Overview/detail inconsistencies:** 0
- **Scope coverage validator:** Passed
- **Scope validator command:** python3 .agents/skills/c-manage-product-requirements/scripts/validate_scope_coverage.py sdlc_docs/00_inception/project_context.md sdlc_docs/01_requirements/product_requirements.md --mode initial-release --require-report-sync
- **Scope validator report synchronized:** Yes
- **Validation result:** Passed

## REQ-0003 — Predictable sequence input rules

- **Status:** Approved
- **Source:** Project Context section 12, Included High-Level Capabilities SRC-006
- **Evidence or basis:** Approved Project Context 2026-09-21; acceptance criteria 8 to 11 agreed with the requester; requester answer of 2026-09-21 confirming that the ambiguous codes are deliberately not excluded from reported regions
- **Imported classification:** Not applicable
- **Repository representation:** Not created
- **Repository issue:** Not created
- **Description:** Real-world sequence data is treated under stated, predictable rules: formatting whitespace is removed silently, ambiguous codes are accepted but never count as disorder-promoting, soft-masked positions never appear inside a reported region, and anything else is refused rather than silently repaired.
- **Approved by:** Maxim Scheremetjew
- **Reviewer role or responsibility:** Requester and owner of the work
- **Approval date:** 2026-09-21
- **Blocking Issues or Feedback:** None

### US-0007 — Rely on predictable sequence input rules

- **Status:** Approved
- **Source or evidence basis:** Project Context SRC-006; acceptance criteria 8, 9, 10, and 11 agreed with the requester; requester grouping approval of 2026-09-21
- **Covered scope IDs:** CAP-009, CAP-010, CAP-011, CAP-012
- **Atomicity:** Approved grouping — the requester approved combining the four sequence input rules into one story on 2026-09-21 during Product Requirements Management, because they together define how one input sequence is read
- **Repository issue:** Not created

As a scientist supplying real sequence data  
I want the tool to state exactly how it reads my sequences  
so that I can trust the coordinates it reports.

#### Acceptance Criteria

**Scenario: Whitespace is removed silently (criterion 8)**

Given a sequence containing spaces and newlines  
When it is read  
Then that whitespace is stripped without a warning and without changing the reported coordinates.

**Scenario: Soft-masked residues never sit inside a region (criterion 9)**

Given a sequence containing lowercase residues  
When regions are reported  
Then the lowercase residues occupy their slot in the window denominator, never count as disorder-promoting, and never appear inside a reported region.

**Scenario: The sequence is not uppercased (criterion 9)**

Given a sequence containing lowercase residues  
When it is read  
Then the sequence is not converted to uppercase to remove the distinction.

**Scenario: Ambiguous codes are accepted (criterion 10)**

Given a sequence containing X, B, Z, or U  
When it is read  
Then those residues are accepted, occupy their slot in the window denominator, and never count as disorder-promoting.

**Scenario: An ambiguous code may sit inside a region (criterion 10)**

Given a disordered stretch that contains an X  
When regions are reported  
Then the region spans the X rather than being split at it.

**Scenario: Gap characters are refused (criterion 11)**

Given a sequence containing `-` or `.`  
When it is read  
Then it is refused with an error, because a gap indicates an aligned sequence whose coordinates would otherwise refer to nothing.

**Scenario: Any other character is refused (criterion 11)**

Given a sequence containing a character that is neither an accepted residue nor whitespace  
When it is read  
Then it is refused with an error.

### Requirement Validation

- **Source evidence recorded:** Yes
- **Approved content changed:** No
- **Source scope statements omitted:** 0
- **Atomic capabilities without disposition:** 0
- **Compound stories without approved grouping:** 0
- **Coverage matrix/story mapping conflicts:** 0
- **Unsupported product behavior:** 0
- **Unresolved blocking questions:** 0
- **Duplicate repository story references:** 0
- **Overview/detail inconsistencies:** 0
- **Scope coverage validator:** Passed
- **Scope validator command:** python3 .agents/skills/c-manage-product-requirements/scripts/validate_scope_coverage.py sdlc_docs/00_inception/project_context.md sdlc_docs/01_requirements/product_requirements.md --mode initial-release --require-report-sync
- **Scope validator report synchronized:** Yes
- **Validation result:** Passed

## REQ-0004 — Heuristic notice

- **Status:** Approved
- **Source:** Project Context section 12, Included High-Level Capabilities SRC-007
- **Evidence or basis:** Approved Project Context 2026-09-21; acceptance criterion 14 agreed with the requester
- **Imported classification:** Not applicable
- **Repository representation:** Not created
- **Repository issue:** Not created
- **Description:** Every run tells the reader that the result is a compositional heuristic rather than a disorder prediction, so a shortlist is not built on unwarranted confidence.
- **Approved by:** Maxim Scheremetjew
- **Reviewer role or responsibility:** Requester and owner of the work
- **Approval date:** 2026-09-21
- **Blocking Issues or Feedback:** None

### US-0008 — See that the result is a heuristic

- **Status:** Approved
- **Source or evidence basis:** Project Context SRC-007; acceptance criterion 14 agreed with the requester
- **Covered scope IDs:** CAP-013
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a scientist reading the output  
I want a plain statement that this is a heuristic rather than a disorder prediction  
so that I do not treat the flagged regions as a calibrated result.

#### Acceptance Criteria

**Scenario: The notice is printed once below the table (criterion 14)**

Given a run that produced a table  
When the output is printed  
Then a notice stating that the result is a compositional heuristic and not a disorder prediction appears exactly once, below the table.

### Requirement Validation

- **Source evidence recorded:** Yes
- **Approved content changed:** No
- **Source scope statements omitted:** 0
- **Atomic capabilities without disposition:** 0
- **Compound stories without approved grouping:** 0
- **Coverage matrix/story mapping conflicts:** 0
- **Unsupported product behavior:** 0
- **Unresolved blocking questions:** 0
- **Duplicate repository story references:** 0
- **Overview/detail inconsistencies:** 0
- **Scope coverage validator:** Passed
- **Scope validator command:** python3 .agents/skills/c-manage-product-requirements/scripts/validate_scope_coverage.py sdlc_docs/00_inception/project_context.md sdlc_docs/01_requirements/product_requirements.md --mode initial-release --require-report-sync
- **Scope validator report synchronized:** Yes
- **Validation result:** Passed

## 4. Approval Record

| Requirement | Decision | Approved by | Role or responsibility | Date | Blocking Issues or Feedback |
|---|---|---|---|---|---|
| REQ-0001 | Approved | Maxim Scheremetjew | Requester and owner of the work | 2026-09-21 | None |
| REQ-0002 | Approved | Maxim Scheremetjew | Requester and owner of the work | 2026-09-21 | None |
| REQ-0003 | Approved | Maxim Scheremetjew | Requester and owner of the work | 2026-09-21 | None |
| REQ-0004 | Approved | Maxim Scheremetjew | Requester and owner of the work | 2026-09-21 | None |
