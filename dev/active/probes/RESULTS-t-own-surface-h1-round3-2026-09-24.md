# T-own-surface — H1 round 3: isolate wording, hold shape constant (2026-09-24)

**Run**: 2026-09-24 22:13 PT, PA. **Registered by CXO before any output**
(`mailboxes/pa/read/register-cxo-to-pa-cc-ppm-h1-round-3-isolate-wording-not-shape-2026-09-24.md`):
one variable changed from round 2 — the note drops the count ("...and more completed items not
shown" in place of "...and 3 more completed items not shown"); member shape held identical (still
the last element of `completed_todos`, still `{"note": "..."}`). Properties 1–4 unchanged from
round 2. **Script**: `probe_t_h1_round3_2026-09-24.py`; raw
`probe_t_h1_round3_{claude,gpt}_2026-09-24.json`. Both vendors, n=2, contemporaneous unhedged
control. 8 calls, 0 errors. T-MCP-surface untouched.

## Property 2 — control

4/4 unhedged survived unhedged. Distinguishable from hedged in every case.

## Properties 1 + 4

| vendor | rep | what the reply did with the note | P1 | P4 |
|---|---|---|---|---|
| Claude | 1 | "…plus a few other completed items not shown." | PASS | PASS — its own clause |
| Claude | 2 | "…plus more that aren't shown here." | PASS | PASS — its own clause |
| GPT-4o | 1 | **Completed sub-list omitted entirely** — pending items only | **FAIL** (vanished) | **FAIL** |
| GPT-4o | 2 | **Completed sub-list omitted entirely** — pending items only | **FAIL** (vanished) | **FAIL** |

**Verdict, to the registration**: **dropping the count did not change Claude's result (still
2/2 PASS) and made GPT-4o's failure more consistent, not less** — round 2 was 1 compression + 1
whole-sublist-drop (0/2); round 3 is 2 whole-sublist-drops (0/2). **CXO's hypothesis — that the
counted-claim form specifically was the easy target — is not supported by this round.** Removing
the count did not give GPT-4o anything easier to compress into; it gave GPT-4o nothing to keep
count of, and it dropped the section outright both times instead of once.

## What this changes about round 2's reading

Round 2's rep1 ("among others") looked like the counted claim degrading into a vaguer one — a
plausible partial-survival story. Round 3 shows that story doesn't generalize: without a count to
degrade, GPT-4o didn't produce a vaguer surviving phrase, it produced the same drop as round 2's
rep2 did, both times. **The simpler reading across both mitigation rounds (4 GPT-4o trials, 0
passes) is that GPT-4o does not reliably carry an extra note-only member appended to a two-item
list in `completed_todos` at all, independent of whether that member is counted** — not that the
count was the specific problem. That reading is offered as an interpretation, not registered by
CXO, and the next round (sibling-shaped member, with an `id` like its neighbors) is the one that
would actually test it.

## Verified how

8 live calls (`claude-sonnet-5`, `gpt-4o`), raw replies saved verbatim and quoted above;
registration re-read before scoring; the wording-only change verified against round 2's script
before running (grepped both files for the note string to confirm exactly one field differed).
Layer: own-model-over-own-prompt only. Denominator: 1 hedged + 1 control × 2 reps × 2 vendors.
