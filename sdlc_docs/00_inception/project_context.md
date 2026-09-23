# Project Context

## 1. Document Control

- **Project name:** disordered regions flagger
- **Source request:** `clarified_project_request.md` (Closed, Ready, approved 2026-09-21)
- **Prepared by:** AI-assisted draft in the SDLC session, for Maxim Scheremetjew
- **Version:** 1.0
- **Last updated:** 2026-09-21
- **Document state:** Closed

## 2. Project Summary

Scientists planning condensate assays need to shortlist protein constructs by their intrinsically disordered regions, and they do not write code. The first version is a command-line tool that they run themselves over many protein sequences in one run and that prints, for each sequence, a table of flagged disordered regions they can quickly eyeball. Regions are found with a simple sliding-window composition heuristic, explicitly not a disorder predictor. The dominant confirmed limit is time: the first version is due at the end of the workshop, roughly 50 minutes from 2026-09-21.

## 3. Evidence and Classification Register

| Statement | Classification | Evidence or basis | Confirmation path if unconfirmed |
|---|---|---|---|
| Disordered regions in protein sequences must be flagged so constructs can be shortlisted for condensate assay planning. | Confirmed fact | Approved request, Initial Understanding; source ticket IDR-101 | — |
| Regions are found by sliding a window, scoring each residue by the fraction of disorder-promoting residues in its window, treating residues above the threshold as disordered, joining consecutive disordered residues into regions reported by start and end position, and ignoring regions below a minimum length. | Confirmed fact | Approved request, Initial Understanding; source ticket IDR-101 | — |
| The twenty standard amino acids are partitioned into disorder-promoting `P E S Q K A G R D T` and order-promoting `W C F I Y V L M N H`. | Confirmed fact | Approved request, Initial Understanding; source ticket IDR-101 | — |
| The defaults are window 5, threshold 0.6, and minimum region length 5. | Confirmed fact | Approved request, Initial Understanding; source ticket IDR-101 | — |
| The result is a deliberately simplified compositional heuristic and must not be presented as real disorder prediction. | Confirmed fact | Approved request, Initial Understanding; source ticket IDR-101 | — |
| The first version is delivered as a command-line tool. | Approved decision | Approved request, Question 1 | — |
| One run accepts many sequences and reports regions for each. | Approved decision | Approved request, Question 2 | — |
| Window, threshold, and minimum region length are user-tunable, keeping the stated values as defaults. | Approved decision | Approved request, Question 3 | — |
| The users are scientists who run the tool themselves and do not write code. | Approved decision | Approved request, Question 4 | — |
| A useful first version produces a per-sequence table of flagged regions that can be quickly eyeballed. | Approved decision | Approved request, Question 5 | — |
| Accepted residues are the twenty standard amino acids plus the ambiguous codes X, B, Z, and U; the ambiguous codes occupy their slot in the window denominator and are never disorder-promoting. Gap characters are rejected with an error. | Approved decision | Approved request, Question 6 | — |
| Lowercase marks a soft-masked position. Soft-masked residues are accepted and occupy their slot in the denominator, never count as disorder-promoting, and can never appear in a reported region. The sequence must not be uppercased to avoid this. | Approved decision | Approved request, Questions 6 and 9 | — |
| The first version is due at the end of the workshop, roughly 50 minutes from 2026-09-21, and this is the dominant constraint. | Approved decision | Approved request, Question 7 | — |
| Maxim Scheremetjew owns the work as requester and is the authorized approver for the inception artifacts. | Approved decision | Approved request, Question 8 and Readiness Approval | — |
| The time limit requires holding the first-version scope to the smallest tool that produces the readable per-sequence region table. | Derived interpretation | Derived from the confirmed deadline above; the approved request records the same consequence | — |
| Because the users do not write code, readable output and clear error messages are project-level expectations rather than refinements. | Derived interpretation | Derived from the confirmed decisions on users and on the per-sequence table | — |
| Exclusion from reported regions is stated for soft-masked positions but was not stated for the ambiguous codes X, B, Z, and U, so whether an ambiguous code may sit inside a reported region is undetermined. | Open question | Matters because it changes which regions are reported for real sequence data | Requester, during Product Requirements Management |
| How the many sequences are supplied to one run. | Open question | Determines the shape of the tool's input | Requester, during Product Requirements Management |

## 4. Background

Condensate assay planning requires choosing which protein constructs to take forward. Intrinsically disordered regions are a signal used in that choice. The approved request records the need for a helper that flags such regions so candidate constructs can be shortlisted.

## 5. Problem Statement

Scientists planning condensate assays cannot quickly see which parts of their protein sequences look disordered, so shortlisting constructs is slower and less consistent than it should be. The scientists doing this work do not write code.

## 6. Why the Project Is Needed

The shortlisting decision is being made now, for condensate assay planning, and the people making it need a result they can read and act on without programming. The approved request also fixes a short delivery window, so the need is immediate.

## 7. Desired Future Situation

A scientist can run one command over a set of protein sequences and read, per sequence, where the likely disordered stretches are, with the stringency adjustable when a first pass is too permissive or too strict. `Derived interpretation:` because the users do not write code, the output must be readable and the errors understandable without help.

## 8. Project Goal

Give scientists planning condensate assays a command they can run themselves that flags likely disordered regions across many protein sequences and reports them in a form they can quickly scan.

## 9. Expected Outcomes

- Scientists shortlist constructs from a readable per-sequence table of flagged regions.
- Stringency can be adjusted by changing window, threshold, and minimum region length.
- Real-world sequence data is handled under stated, predictable rules rather than silently cleaned.
- Users understand that the result is a heuristic and not a disorder prediction.

## 10. People Involved

### Intended Users

- Scientists planning condensate assays, who run the tool themselves and do not write code.

### Other People Affected

- Not identified in the approved source.

### Confirmed Responsibilities

- **Maxim Scheremetjew:** Requester and owner of the work, and the authorized approver for the inception artifacts. Evidence: approved request, Question 8 and Readiness Approval.

## 11. High-Level Scope

### Included

- A command-line tool run by the scientists themselves.
- Flagging of disordered regions using the stated sliding-window composition heuristic.
- Processing of many protein sequences in a single run.
- Per-sequence reporting of flagged regions by start and end position, in a readable table.
- User-adjustable window, threshold, and minimum region length, with the stated values as defaults.
- The stated input-handling rules for accepted residues, ambiguous codes, gap characters, and soft-masked positions.
- A clear statement that the result is a heuristic, not a disorder prediction.

### Excluded

- Ranking of sequences, scoring dashboards, and aggregate analytics.
- Real disorder prediction using learned models, evolutionary information, or calibrated scores.
- A graphical user interface.
- A published importable library as the user-facing deliverable. This does not constrain internal structure decisions taken at the architecture stage.

### Future Design Considerations

- Comparison against production disorder tools such as IUPred3, metapredict, flDPnn, or AlphaFold pLDDT. Classification: `Derived interpretation`, derived from the confirmed statement that those tools use learned models and calibrated scores while this project does not. This adds no capability to the current version.

## 12. MVP Boundary

### Intended User

A scientist planning condensate assays who runs the tool from a terminal and does not write code.

### Minimum Useful Outcome

The scientist runs one command over a set of protein sequences and reads, for each sequence, a table of flagged disordered regions with start and end positions.

### Included High-Level Capabilities

- Run as a single command from a terminal.
- Accept many protein sequences in one run.
- Flag disordered regions using the stated sliding-window composition heuristic.
- Report flagged regions per sequence, by start and end position, in a readable table.
- Accept overrides for window, threshold, and minimum region length.
- Apply the stated rules for accepted residues, ambiguous codes, gap rejection, and soft-masked positions.
- Make clear that the result is a heuristic and not a disorder prediction.

### Explicitly Excluded

- Ranking, scoring dashboards, and aggregate analytics.
- Learned models, evolutionary information, and calibrated scores.
- A graphical user interface.
- A published importable library as the user-facing deliverable.

### Confirmed Delivery Limits

- The first version is due at the end of the workshop, roughly 50 minutes from 2026-09-21. This is the dominant constraint.

### Completion Condition

A single command run over a set of protein sequences produces, for each sequence, a readable table of flagged disordered regions with start and end positions, using the default window 5, threshold 0.6, and minimum region length 5 unless the user overrides them, and applying the stated input-handling rules.

## 13. Constraints

- The first version is due at the end of the workshop, roughly 50 minutes from 2026-09-21, and this is the dominant constraint.
- The method must be the stated compositional heuristic, not a learned or calibrated disorder predictor.
- The result must not be presented as real disorder prediction.
- The residue partition and default parameter values stated in the approved request must be used.
- Gap characters must be rejected with an error rather than ignored.
- The sequence must not be uppercased to bypass soft-masking.

## 14. Assumptions

No assumptions recorded.

## 15. Dependencies

No dependencies identified in the approved source.

## 16. Risks and Uncertainties

- **The time limit may force parts of the intended scope to be dropped:** the first version could ship without adjustable parameters or without the full input-handling rules.
  - **Classification:** Derived interpretation
  - **Evidence or basis:** Derived from the confirmed deadline of roughly 50 minutes from 2026-09-21
  - **Affected project area:** Scope and schedule
- **Users may read the output as a real disorder prediction:** constructs could be shortlisted on a confidence the method does not support.
  - **Classification:** Derived interpretation
  - **Evidence or basis:** Derived from the confirmed fact that the method is a deliberately simplified stand-in and must not be presented as prediction
  - **Affected project area:** Scope and user understanding
- **Whether an ambiguous code may appear inside a reported region is undetermined:** the reported regions for real sequence data could differ from what the requester expects.
  - **Classification:** Open question
  - **Evidence or basis:** The approved request states exclusion from regions for soft-masked positions only
  - **Affected project area:** Scope, to be resolved during Product Requirements Management
- **How the many sequences are supplied to one run is undetermined:** the input shape of the tool is not yet fixed.
  - **Classification:** Open question
  - **Evidence or basis:** Not identified in the approved source
  - **Affected project area:** Scope, to be resolved during Product Requirements Management

## 17. Success Criteria

- A scientist who does not write code can run one command over a set of protein sequences without assistance.
- The run reports, per sequence, a readable table of flagged regions with start and end positions.
- Default parameters match the approved values, and all three can be overridden.
- Sequences containing ambiguous codes and soft-masked positions are handled under the stated rules, and gap characters produce an error.
- The tool makes clear to its users that the result is a heuristic and not a disorder prediction.

## 18. Confirmed Decisions and Responsibilities

- **Person who requested the project:** Maxim Scheremetjew
- **Person who makes project-level decisions:** Maxim Scheremetjew
- **Person who confirms the software meets the agreed scope:** Not assigned in the approved source
- **Person responsible for building the software:** Not assigned in the approved source

## 19. Validation Report

- **Approved source modified:** No
- **Unsupported confirmed claims:** 0
- **Derived interpretations without basis:** 0
- **Classification conflicts across sections:** 0
- **Mixed confirmed-and-derived statements:** 0
- **Stakeholder-confirmed interpretations not promoted:** 0
- **Assumptions without confirmation path:** 0
- **Open questions presented as resolved:** 0
- **Scope contradictions:** 0
- **Premature downstream detail:** 0
- **Authorized traceability fields changed:** `Project context`: Status, Missing or blocked, Next action
- **Unauthorized traceability changes detected:** 0
- **Traceability Mutation Guard:** Passed
- **Working Questions remaining:** 0
- **Blocking validation failures:** None

## 20. Project Context Approval

### Status

- [x] Ready for Product Requirements
- [ ] Not Ready

### Reviewed by

- **Name:** Maxim Scheremetjew
- **Role or responsibility:** Requester, owner of the work, and authorized approver for the inception artifacts
- **Date:** 2026-09-21

### Blocking Issues or Feedback

None

