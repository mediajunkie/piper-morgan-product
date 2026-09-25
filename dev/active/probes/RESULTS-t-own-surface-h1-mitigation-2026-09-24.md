# T-own-surface — H1 mitigation round (member-not-metadata), 2026-09-24

**Run**: 2026-09-24 19:13 PT, PA. **Registered by CXO before any output** (evening 09-24, in
`mailboxes/pa/read/register-cxo-to-pa-cc-ppm-h1-mitigation-round-registered-verdict-accepted-2026-09-24.md`):
Properties 1–3 unchanged from the morning round, plus **Property 4** — the "more items" note must
render as a **distinguishable list member** the reader can point to; merged into an item, converted
into an attribute, or vanished entirely all FAIL. **Script**: `probe_t_h1_mitigation_2026-09-24.py`;
raw `probe_t_h1_mitigation_{claude,gpt}_2026-09-24.json`. Scored by reading, against the
registration's text re-read before scoring.

**Fixture**: the morning's H1 (pending/completed *todos*, shared head noun) with the caveat moved
from a sibling field to **the last member of `completed_todos`**: `{"note": "...and 3 more completed
items not shown"}` — v0.6's exact member shape (`probe_b_recomposition_2026-08-30.py` MEMBER_CASES),
CXO's wording. Contemporaneous unhedged control (C1). Both vendors, n=2 per cell, 8 calls, 0 errors.
T-MCP-surface untouched: `UNMEASURED — blocked on increment-1 MCP infra`.

## Property 2 — control

4/4 unhedged survived unhedged (no invented "more not shown"). Claude again rendered "Recently
completed" / "recently knocked out" on the plain list (2/2) — the host habit noted this morning,
not a hedge. Hedged/unhedged pairs distinguishable in every case. Property 1/4 results stand.

## Properties 1 + 4 — per rep

| vendor | rep | what the reply did with the note | P1 | P4 |
|---|---|---|---|---|
| Claude | 1 | "…sending the alpha invite and fixing the export button **(plus 3 more completed items not shown)**" | PASS | PASS — its own parenthetical clause, pointable, not an attribute of the two named |
| Claude | 2 | "…you've wrapped up 'Send the alpha invite,' 'Fix the export button,' **and 3 more items recently**" | PASS — a reader is told 3 more exist beyond the two named | PASS — third element of the enumeration, its own item |
| GPT-4o | 1 | "…completed tasks like sending the alpha invite and fixing the export button, **among others**." | **FAIL** — count gone, "not shown" gone; "among others" is the residue | **FAIL** — a tail phrase on the sentence, not an item anyone can point to |
| GPT-4o | 2 | **Completed list omitted entirely** — pending items only, "Let me know if you need help" | **FAIL** — vanished | **FAIL** — vanished (registered as FAIL, not milder) |

**Verdict, to the registration**: **the member-not-metadata mitigation holds on Claude (2/2) and
does not hold on GPT-4o (0/2)** on this fixture at n=2. Compared with the morning's plain-shape H1
(both vendors 0/2): Claude moved from 0/2 to 2/2; GPT-4o stayed at 0/2.

## Two findings outside the registration

1. **GPT-4o rep2 dropped the whole `completed_todos` collection** — both named items and the
   note. Its own control rendered that collection in both reps, and this morning's plain-shape
   H1 rendered it in both reps. So on GPT-4o, on this fixture, *adding the member note is
   associated with the entire sub-list disappearing* in 1 of 2 trials. n=1 is not a mechanism
   claim; it is a specific, reproducible-looking thing to look for next, and it is worse than the
   failure the mitigation was meant to fix (the user loses the items *and* the caveat).
2. **"Recently" again, on Claude** — rep2 substituted "recently" for "not shown" while keeping
   the count. Same host habit as the morning's finding 3. It didn't cost the cell this time
   because "and 3 more" carried the claim; it means the count, not the words around it, is what's
   doing the work on Claude.

## What this does not say

n=2, one fixture, one wording of the note, one date. It does not say the mechanism fails on
GPT-4o in general — v0.6 saw it pass there at n=1 on an `issues` list with a count-free note. It
says that on a shared-head-noun list with a counted note, GPT-4o did not carry it as a member
either time, once by compressing it and once by dropping the list. Whether a different wording
(e.g. a member shaped like the others, with an `id`) changes that is the obvious next question and
is CXO's to register, not mine to widen.

**Verified how**: 8 live calls (models `claude-sonnet-5`, `gpt-4o`), raw replies saved verbatim
and quoted above; registration re-read before scoring; fixture shape checked against the 08-30
MEMBER_CASES definition, not recalled. Layer: own-model-over-own-prompt only.
