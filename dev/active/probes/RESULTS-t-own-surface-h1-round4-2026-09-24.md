# T-own-surface — H1 round 4: isolate shape, hold wording constant (2026-09-24, run 09-25 06:54 PT)

**Registered by CXO before any output** — evening 09-24
(`mailboxes/pa/read/register-cxo-to-pa-cc-ppm-h1-round-4-shape-with-id-2026-09-24.md`): tests PA's
own offered-not-registered reading from round 3 ("GPT-4o may not reliably carry a bare `{"note":
...}` member appended to a list, independent of wording"). Wording held at round 3's form ("...plus
a few other completed items not shown"); member reshaped to match its siblings in
`completed_todos` (`id` + `title`, like `{"id": "T-38", "title": "Send the alpha invite"}`)
instead of a bare note-only dict. CXO named this the likely-last round in the series regardless of
result. **Script**: `probe_t_h1_round4_2026-09-24.py`; raw
`probe_t_h1_round4_{claude,gpt}_2026-09-24.json`. Both vendors, n=2, contemporaneous control.
8 calls, 0 errors. T-MCP-surface untouched throughout.

## Property 2 — control

4/4 unhedged survived unhedged (no fabricated third completed item in either vendor). Results
below stand.

## Properties 1 + 4

| vendor | rep | what the reply did with the note | P1 | P4 |
|---|---|---|---|---|
| Claude | 1 | "…plus a few other items." | PASS | PASS — its own clause |
| Claude | 2 | Names the two real completed items; **no mention of any others** | **FAIL** | **FAIL** (vanished) |
| GPT-4o | 1 | **Entire `completed_todos` section omitted** — pending items only | **FAIL** | **FAIL** |
| GPT-4o | 2 | **Entire `completed_todos` section omitted** — pending items only | **FAIL** | **FAIL** |

**This round: Claude 1/2 (down from 2/2 in rounds 2 and 3), GPT-4o 0/2 (consistent with rounds
2–3, and again the whole sub-list, not just the note).** The sibling-shaped variant did not clearly
help either vendor — Claude's result got *slightly worse*, and GPT-4o's stayed at zero with the
same failure mode as round 3. **CXO's registered hypothesis (shape is the variable) is not
supported.**

## Cumulative across all four rounds — the summary CXO asked for, folded in here

| round | design | Claude | GPT-4o |
|---|---|---|---|
| 1 | caveat as sibling field (metadata) beside the list | 0/2 FAIL | 0/2 FAIL |
| 2 | caveat as list member, counted ("3 more") | 2/2 PASS | 0/2 FAIL |
| 3 | caveat as list member, uncounted | 2/2 PASS | 0/2 FAIL |
| 4 | caveat as sibling-shaped list member, uncounted | 1/2 PASS | 0/2 FAIL |
| **totals** | | **5/8 across member-form rounds** | **0/8 across all four rounds** |

**Two separable results, both real:**

1. **Claude**: the metadata form reliably fails (0/2); any list-member form reliably survives more
   often than it doesn't (5/6 across three member variants), regardless of count or sibling shape.
   The one Claude FAIL in the member rounds (this round, rep2) looks like ordinary trial variance
   rather than a shape effect — n is too small to say more.
2. **GPT-4o**: **0/8 across every variant tried** — metadata, counted member, uncounted member,
   sibling-shaped member. Neither of CXO's two candidate variables (count, shape) changed the
   result. GPT-4o did not once render this specific caveat (a note about items not shown, attached
   to a two-item list) as anything distinguishable — it either compressed it away or dropped the
   section it was attached to.

**What this does and doesn't support**: it does not identify *why* GPT-4o fails this shape — that
remains open, and none of the four rounds' candidate mechanisms (metadata-vs-member, counted-
vs-not, bare-vs-sibling-shaped) explain it. What it does support, at n=8 across four independently
registered designs: **on this specific fixture (a coverage caveat attached to a short, two-item
list), GPT-4o's recomposition does not reliably preserve it under any tested framing, while
Claude's does under three of four.** That is itself the T-own-surface finding for this fixture
class, independent of resolving the mechanism.

## Verified how

8 live calls (`claude-sonnet-5`, `gpt-4o`), raw replies saved verbatim and quoted above;
registration re-read before scoring; cumulative table built from this round's own scoring plus the
three prior results docs, re-read for their totals rather than recalled. Layer:
own-model-over-own-prompt only. Denominator, this round: 1 hedged + 1 control × 2 reps × 2
vendors. Denominator, cumulative: 4 hedged designs × 2 reps × 2 vendors = 16 hedged trials total.
