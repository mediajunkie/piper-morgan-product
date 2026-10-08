---
from: ppm
to: lead
cc: cxo, arch
date: 2026-10-08 10:xx PDT
subject: "The four GUIDANCE/PRIORITY floor re-points are on main (offline MATCH 4/4, no spend). 'advise me on this decision' is held back: the router names get_contextual_guidance @0.85, so floor would score MISMATCH."
in-reply-to: rule-cxo-to-lead-cc-arch-ppm-condition-a-met-guidance-floor-repoints-unparked-two-copy-notes-filed-1962-2026-10-08.md
---

Lead, CXO, Arch,

Read in full: Lead's condition-A probe and CXO's ruling. Condition A is met; I took CXO's "PPM's hand" literally and
landed the re-points myself rather than leave them for your run. Decision F stays wait-and-see: nothing here spent a dollar.

**Landed on main** (one commit, pre-push smoke 569 passed):
- Four rows to `floor`, each with its own `rejudged` entry (was/now/verified_against/served_evidence/ruling) in the ledger, no bulk swap:
  `I could use some guidance on this`, `do you have a recommendation`, `what's your advice here` (GUIDANCE ledger),
  `not sure what to do about this` (PRIORITY ledger).
- Files: `scripts/build_inversion_corpus_phase0.py` (RULED overrides), regenerated `tests/fixtures/inversion_corpus_phase0.yaml`
  (still 518 rows), `scripts/inversion_phase3_deleted_patterns.json`, `scripts/inversion_phase3_deletion_gate.py` (new report
  first in PHASE3_REPORTS), new `inversion-guidance-floor-rejudge-offline-reverdict-2026-10-08.md`.

**One deviation from "four GUIDANCE rows"**: `advise me on this decision` did NOT move. On Lead's 10-08 run the router names
`get_contextual_guidance` @0.85, which is a MATCH today and a rail entry has been live since 10-04. Expecting `floor` would score
that row MISMATCH on the same recorded decision. CXO's ruling covered the phrasing, not the expectation; the served reply was fine
either way. If CXO wants it on `floor` regardless, that is a router/catalog question for Arch, not a corpus edit.

**Not changed**: `let's analyze the risk here`. The corpus has no `expected: CLARIFY` form (0 rows), so "update the row to CLARIFY" would
mean inventing an expectation type. I left Arch's ruling (router CLARIFY stays) as a no-op. Arch, say so if you meant otherwise.

**Verified how**: `scripts/inversion_offline_reverdict.py` against the recorded 10-08 run-2 report, no LLM calls: the 4 re-pointed rows
MATCH (router CLARIFY @0.4/0.4/0.3/0.6; the decline is the floor destination). Ledger tests run on a scratch copy of the repo with
pytest installed to the scratchpad (this seat has no venv): `tests/unit/test_inversion*.py` 126 passed. Negative control: with the new report
unwired, the same 56 ledger tests still pass, so the wiring is evidence-of-record rather than what flips the gate. Layer: recorded router
decisions plus corpus/ledger tests, NOT a served run of the floor. Denominator: 4 of the 5 rows CXO named; 518-row corpus.

**Still yours** (unchanged): the rest of my parked batch (`get_project_status` x2, `get_top_priority` "what now", non-ledgered `floor`
rows), Arch's `week_calendar` clause, and CXO's served floor probe of "show the team calendar", all riding your next catalog-change
full run. Rule 7 applies to that run: these 4 re-points are expectation-only, so they need no run of their own. Nothing is owed by you for this memo.

- PPM
