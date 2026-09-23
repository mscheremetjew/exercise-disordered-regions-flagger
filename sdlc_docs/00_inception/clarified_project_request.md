# Clarified Project Request

## Document Control

- **Document state:** Closed
- **Created:** 2026-09-21
- **Last updated:** 2026-09-21

## Source Metadata

| Source | Type | Date | Provided by | Notes |
|---|---|---|---|---|
| `sources/informal_project_request_idr-101.md` | Informal request (ticket) | 2026-08-20 | Developer in the SDLC session, originating from ticket IDR-101 | Original source preserved unchanged |

## Initial Understanding

Scientists planning condensate assays need to shortlist protein constructs by their intrinsically disordered regions. The first release delivers a command-line tool that these scientists run themselves; they do not write code. One run accepts many sequences and produces, for each sequence, a table of flagged regions that a person can quickly eyeball. Readable output and clear errors are therefore a project-level expectation, not a refinement.

The method is a compositional heuristic, not a disorder predictor. A window slides along the sequence and each residue is scored by the fraction of disorder-promoting residues in its window. Residues whose score passes the threshold count as disordered, consecutive disordered residues form a region, each region is reported by its start and end position, and regions shorter than a minimum length are ignored. The source partitions the twenty standard amino acids into disorder-promoting `P E S Q K A G R D T` and order-promoting `W C F I Y V L M N H`. Window 5, threshold 0.6, and minimum region length 5 are the defaults, and all three are user-tunable so planners can vary stringency.

The tool must tolerate real-world sequence data rather than assume clean input. The accepted alphabet is the twenty standard amino acids plus the ambiguous codes X, B, Z, and U; the ambiguous codes occupy their slot in the window denominator and are never disorder-promoting. Gap characters are rejected with an error. Lowercase marks a soft-masked, low-complexity or otherwise untrustworthy position, following the BLAST and masking-tool convention: soft-masked residues are accepted and occupy their slot in the denominator, never count as disorder-promoting, and can never appear in a reported region. The sequence must not be uppercased to sidestep this. The exclusion-from-regions rule applies to soft-masked positions specifically, and was not stated for the ambiguous codes.

The source is explicit that this is a deliberately simplified stand-in. Production tools such as IUPred3, metapredict, flDPnn, or AlphaFold pLDDT use learned models, evolutionary information, and calibrated scores. The project must not present its output as a real disorder prediction.

The dominant constraint is time: the first release is due at the end of the workshop, roughly 50 minutes from 2026-09-21. Scope must be held to a runnable command-line tool producing a readable per-sequence region table over multiple sequences with tunable parameters and the stated input-handling rules. Ranking, scoring dashboards, aggregate analytics, and anything else not essential to that outcome are outside the first release.

Maxim Scheremetjew owns the work as requester and is the authorized approver for the inception artifacts.

## Critical Questions

### Question 1

- **Status:** Answered
- **Question:** What must the first release deliver so the team can actually use it: an importable helper function, a command-line tool, or both?
- **Answer:** A command-line tool.
- **Answered by:** Developer (requester), recorded in the SDLC session
- **Impact:** Confirms the user-facing deliverable of the first release is a command users run in a terminal. Excludes an importable library API as the release deliverable, without forbidding internal structure decisions at architecture stage.

### Question 2

- **Status:** Answered
- **Question:** Does the first release handle one sequence at a time, or must it process many sequences in a single run when shortlisting constructs?
- **Answer:** Many sequences per run.
- **Answered by:** Developer (requester), recorded in the SDLC session
- **Impact:** Confirms the tool must accept a set of sequences and report regions for each, so a construct shortlist comes out of a single run. Broadens the boundary beyond the single-sequence helper implied by the source ticket.

### Question 3

- **Status:** Answered
- **Question:** Must users be able to override the stated defaults (window 5, threshold 0.6, minimum region length 5), or are those defaults fixed for the first release?
- **Answer:** Yes, overridable. The ticket values (window 5, threshold 0.6, minimum region length 5) remain the defaults.
- **Answered by:** Developer (requester), recorded in the SDLC session
- **Impact:** Confirms all three parameters are user-tunable, which matters because assay planners need to vary stringency when shortlisting.

### Question 4

- **Status:** Answered
- **Question:** Who are the intended users, and do they work with Python directly or do they need an interface that requires no programming?
- **Answer:** Scientists run it themselves. They do not write code.
- **Answered by:** Developer (requester), recorded in the SDLC session
- **Impact:** Confirms the primary users are non-programmers, which reinforces the command-line deliverable and makes clear, self-explanatory output and error messages a project-level expectation rather than a nicety.

### Question 5

- **Status:** Answered
- **Question:** What outcome would make the first release useful in practice, that is, what does a usable shortlist of constructs look like to the people planning the assay?
- **Answer:** A per-sequence table of flagged regions that can be quickly eyeballed.
- **Answered by:** Developer (requester), recorded in the SDLC session
- **Impact:** Defines project-level success for the first release: readable tabular output per sequence, scannable by a person. Excludes ranking, scoring dashboards, or aggregate analytics from the first release.

### Question 6

- **Status:** Answered
- **Question:** Must the first release tolerate real-world sequence data that contains characters outside the twenty standard amino acids, or is clean input guaranteed by the people supplying sequences?
- **Answer:** Accepted as residues: the twenty standard amino acids plus X, B, Z, and U. The four ambiguous codes count toward the window denominator and are never disorder-promoting. Gap characters are rejected with an error. Lowercase means soft-masked, following the BLAST and masking-tool convention in which a lowercase residue marks a low-complexity or otherwise untrustworthy position.
- **Answered by:** Developer (requester), recorded in the SDLC session
- **Impact:** Confirms the tool must tolerate real-world sequence data rather than assume clean input, and fixes the accepted alphabet, the denominator treatment of ambiguous codes, and rejection of gaps. Introduces soft-masking as a concept the project must account for; how soft-masked positions are treated is tracked as Question 9.

### Question 7

- **Status:** Answered
- **Question:** Is there a deadline, assay milestone, or planning date that the first release must meet?
- **Answer:** The deadline is the end of the workshop, roughly 50 minutes from 2026-09-21. This is the dominant constraint.
- **Answered by:** Developer (requester), recorded in the SDLC session
- **Impact:** Establishes time as the governing constraint on the first release. Scope must be held to what is deliverable in that window, and anything not essential to a runnable command-line tool producing a readable region table is out of scope for the first release.

### Question 8

- **Status:** Answered
- **Question:** Who owns this work, and who is the authorized approver for the inception artifacts?
- **Answer:** Maxim Scheremetjew owns the work as requester and is the authorized approver for the inception artifacts.
- **Answered by:** Maxim Scheremetjew, requester
- **Impact:** Establishes the authorized approver for this project's inception artifacts and confirms requester ownership of the first release.

### Question 9

- **Status:** Answered
- **Question:** Following from Question 6, how must soft-masked (lowercase) positions be treated when regions are flagged: excluded from disorder scoring, scored like any other residue, or reported but marked as untrustworthy?
- **Answer:** Lowercase means soft-masked, following the BLAST and masking-tool convention in which a lowercase residue marks a low-complexity or otherwise untrustworthy position. Masked residues are accepted and occupy their slot in the window denominator, but never count as disorder-promoting and can never appear in a reported region. The sequence must not be uppercased to avoid the problem.
- **Answered by:** Developer (requester), recorded in the SDLC session
- **Impact:** Fixes the treatment of soft-masked positions and makes masking a first-class behaviour of the tool rather than an input-cleaning step. Note this is stricter than the rule for the ambiguous codes X, B, Z, and U: those also count in the denominator and are never disorder-promoting, but were not excluded from reported regions.

## Contradictions

None identified. The two residue groups stated in the source form a complete, non-overlapping partition of the twenty standard amino acids.

## Readiness Approval

- [x] Ready
- [ ] Not Ready
- **Approver:** Maxim Scheremetjew
- **Role:** Requester
- **Approval date:** 2026-09-21
- **Blocking Issues:** None
