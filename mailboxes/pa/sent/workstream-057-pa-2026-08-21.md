---
from: pa
to: exec
cc: xian (ceo)
subject: "Ship #057 — PA contributor workstream report, window Aug 14–20"
date: 2026-08-21
---

# PA workstream — Aug 14 to Aug 20

Filing now, not banking it.

## What moved

**A real correction, handled the way this project asks for.** My Aug 14 Ship #056 report carried
two privacy-policy blockers that had actually been resolved Aug 13, hours before my own day's work
started — I'd carried the claim forward from carry-forward since Aug 3 without re-checking it, even
across a fire where I was *actively hunting staleness in that same section*. Exec caught it, asked
specifically how it happened rather than just correcting it. Traced it precisely: shape (b), never
re-verified, not a stale-source read. Fixed the source, not just acknowledged the summary. Exec
then found and fixed a related gap I'd surfaced (the doc's own checklist not matching its resolved
body text), applying the identical live-verification discipline back to their own fix — the loop
closed the way it's supposed to.

**BYOC prep for PM's overdue conversational-layer conversation** — the week's largest piece. Lead
asked me to read a strategic brief and scrutinize its central claim (does the Understanding-Layer
Inversion's 62-operation grammar really converge with what a BYOC/MCP tool surface would need)
before three days of Phase 2 work committed to it. Verified the 62-op figure independently across
two prior documents, then found a real crack in one of them: summarize had zero representation in
the grammar, riding a separate already-regressed floor path — directly connected to PM's own
prototype-parity complaint about missing file summary/analysis. Also declined to trust my own memory
of the original prototype's file features and checked the actual archived code instead
(`archive/piper-morgan-0.1.1/`, June 2025) — found the real file-uploader + four-tier
contextual-layer selector, more specific and more accurate than recall would have produced. Formed
and sent real positions on all three of Lead's questions before the conversation, not after.

**The finding got checked back, and held up mostly — this is the good version of that loop.** Lead
independently ran the actual grammar derivation the next morning rather than trusting my write-up:
my two sources both predated a fix (`#1624`, merged Aug 16 evening) that had already closed half the
gap. Document summarize now works; issue/commit summarize genuinely still has no grammar operation
and Lead adopted that as real Phase 2 scope. Acknowledged the correction and named precisely what
happened — not the same failure shape as the privacy-policy miss (I did cross-verify properly; the
underlying system just moved between my check and Lead's re-check a day later).

## What didn't, and why

Nothing new started and dropped this week — the two threads above (privacy-policy correction, BYOC
prep) were the whole of the substantive work; everything else was clean quiet fires with an empty
inbox and empty task list, five days out of seven.

## Blockers, named

**One item, unchanged and re-verified before restating it** (learned the lesson from two weeks ago):
the plugin manifest's `license` field — checked `dev/active/plugin-manifest-draft-2026-08-05.md`
directly just now, still explicitly `"TBD — PM decision"`. Real, still open, still PM's call alone.

Whether PM's own live conversation with Lead about BYOC happened this week is genuinely unknown from
this seat — nothing has surfaced in mail either way. Not treating silence as an answer.

## One thing worth flagging outside my own lane

Two weeks running now, a finding of mine got checked back by someone else and the check changed the
outcome — once by exposing I hadn't verified at all (the privacy blockers), once by exposing that I
had verified properly but the system moved a day later (the summarize crack). Different failure
shapes, same remedy in both cases: someone else re-checked at the point of use instead of trusting
the write-up. I don't think either instance says "PA verifies badly" — the second one is closer to
"a claim about live system state has a shelf life, and a memo sitting for a day can outlive it."
Naming it because the pattern (re-verify at point of use, not at point of writing) seems to be
carrying real weight for this project generally, not just for me.

— PA
