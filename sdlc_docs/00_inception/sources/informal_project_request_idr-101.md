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
