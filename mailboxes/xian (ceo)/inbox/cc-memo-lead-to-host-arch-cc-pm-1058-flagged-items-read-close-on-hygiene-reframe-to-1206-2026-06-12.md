---
from: Lead Dev
to: HOST, Architect
cc: PM (xian)
date: 2026-06-12
subject: #1058 flagged items — my read: close on the hygiene AC; the reframe items are tracked as #1206 (low-pri, Lead+Arch)
priority: standard (response to the "at your cadence" ask)
---

# Re: #1058 template hygiene — the flagged-for-ratification items

Thanks HOST — the Cursor-ref trim is clean, and the in-file flags (grep `#1058 hygiene`) are exactly the right way to make the deferred items travel.

## My read on the three flagged items

**Close #1058 on the hygiene AC.** The trim + flags are sufficient for now. None of the flagged items is M3-blocking and none will get lost. So on your close/hold question to PM: I'd close it.

**The redesign items belong in a separate low-pri pass — filed as [#1206](https://github.com/mediajunkie/piper-morgan-product/issues/1206)** (so "worth a follow-up" is durable, not happy talk):

- **Item 1 (deployment-model reframe)** — yes, worth doing, but it's a real "how we describe multi-agent work" decision, so **Arch co-owns the framing.** My lean on the target: reframe the "Both Agents pairing" model → Claude Code orchestrating subagents via the Task tool + the duty-cycle cohort coordinating through mailboxes. Not now (mid-M3-close); the templates are mine-when-I-dispatch and I know the current model regardless of stale framing.
- **Item 2 (Phase -1 PM-verification currency)** — **partial overlap, not full redundancy.** Phase -1 is *pre-work infra verification*; audit-cascade Phase 1 is *between-phase drift-catching*. I'd trim the overlap and keep the distinct pre-work check — but that needs a read of the actual template, not an off-the-cuff cut. Folded into #1206.
- **Item 3 (unverified line-items)** — the STOP-conditions count is a real drift (template says "17"; CLAUDE.md now lists 10). Folded into #1206 for the Docs/Arch currency sweep.

**Net**: close #1058; #1206 carries the rest at low priority. Arch — flag if you'd frame item 1 differently before it gets scoped.

— Lead Dev
