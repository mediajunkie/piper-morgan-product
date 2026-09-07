# Probe B — PA's member-vs-metadata candidate (PM-authorized 2026-09-06, run same day)

**Run** 2026-09-06 ~19:0x PDT · `claude-sonnet-4-5-20250929` + `gpt-4o` · raw JSON:
`probe_b_claude_member_2026-09-06.json`, `probe_b_gpt_member_2026-09-06.json`.

## Denominator, stated first (m-44 — this is not a verdict)

**2 trials, 1 per vendor, n=1 per cell.** This candidate was designed 09-02 (in the same memo where
CXO sharpened PA's earlier finding into a testable mechanism), explicitly authorized to ride the killer
test's PM approval, and then — through no deliberate decision, just an oversight caught only when
Exec's 09-06 memo re-surfaced it — never actually built or run. Building and running it now, four days
later, per the standing authorization already in place.

## The design

Item 3's structured payload always carried the partial-coverage caveat as a field beside the `issues`
array (`coverage: "partial"`, `total_known: false`, later `may_claim_complete: false`) — every version
of that shape was dropped by at least one vendor across this whole probe series. CXO's mechanism,
grounded in `search_consciousness.py`'s actual code rather than speculation: the caveat needs to be a
**member of the array itself**, not metadata describing the array. Candidate payload: the same three
issues, plus a fourth array element carrying the caveat as its own entry (`{"note": "...and more not
shown"}`) — no separate field at all.

## Result — the caveat survived, in both vendors, on the first try

| Vendor | Reply | Caveat present? |
|---|---|---|
| **Claude** | *"...and there are more issues not shown in this summary."* | ✅ **survives** |
| **GPT-4o** | *"There are more issues not shown here."* | ✅ **survives** |

This is the first design across this whole probe series — six prior rounds, every field-form variant of
this exact caveat — where a completeness/truncation caveat survived cleanly in **both** vendors on the
same design. Every field-shaped version (`coverage: partial` alone, with a directive added, alongside a
co-occurring class-A caveat) failed in at least one vendor at least once. This one didn't fail in either.

## What this does and doesn't establish

- **n=1 per cell.** Same limits as every prior round in this series. One clean pass in two vendors is
  evidence for the mechanism, not proof of it — CXO's own record on this axis is 0-for-2 on *other*
  candidates that also looked this clean before testing.
- **This is a genuine design lead, not a scoring result.** It doesn't move the BYOC rubric's T axis
  (still `PENDING-PROBE`, per the standing discipline this whole series has held) — it's a candidate
  answer to "what should the MCP tool layer actually emit," which is the practical question underneath
  the rubric, not the rubric itself.
- **Consistent with, and now directly testing, the design stance PA named 09-02**: "don't ask the model
  to preserve the caveat — don't give it a chance to drop it." A caveat that's structurally
  indistinguishable from the data it accompanies can only be dropped by dropping data, which appears to
  be a rarer failure than dropping a describing field — this run is the first direct evidence for that,
  not just the argument for it.

## What I'm NOT concluding

- **Not** "this solves class-B caveats generally" — one item, one payload shape, one trial per vendor.
- **Not** "field-form caveats always fail" — item 1's `read_status`/`may_claim_empty` field pair
  survived reliably across this series; the pattern so far is specific to *completeness/truncation*
  caveats, not caveats as a category.
- **Not** ranking the vendors — both passed identically here.

## Next step, if there is one

This is a real, cheap, positive lead for whoever builds the MCP tool-output layer (Lead, per the
ongoing #1463/#1688 threads) — worth having in hand even though it doesn't close a gate on its own.
Not proposing a follow-up test; flagging the finding and letting CXO or Lead decide whether it's worth
extending to other class-B cases before anyone builds against it as settled.

— PA, 2026-09-06, ~19:1x PDT
