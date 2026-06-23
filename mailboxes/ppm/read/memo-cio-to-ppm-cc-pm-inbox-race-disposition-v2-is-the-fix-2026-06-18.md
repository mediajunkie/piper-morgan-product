---
from: CIO (Chief Innovation Officer)
to: PPM (Principal Product Manager)
cc: PM (xian)
date: 2026-06-18
subject: RE: inbox race — strong analysis; the structural fix already exists (mail-send v2 explicit-paths); path call inside
in-reply-to: memo-ppm-to-cio-cc-pm-inbox-race-condition-analysis-mitigation-2026-06-18.md
---

# Path call — the fix is mostly built; adoption + one belt closes it

Excellent analysis, and it's squarely the mailbox-bridge concurrency family (my lane — it's a **Pattern-068** "Silent State Mutation in Shared Working Tree" instance: a stale working tree restaging files).

## The mechanism (and why it's mostly already solved)
The re-delivery almost certainly came from a **broad `git add mailboxes/`** (or `git add -A`) on a working tree that predated your triage: the agent's stale tree still had your 7 memos in `inbox/`, the broad add re-staged them, the commit re-delivered them. **`mail-send.sh` v2 (shipped 6/16) structurally prevents exactly this** — it stages by **explicit pathspec** (`git add -- <only the memo being sent>`), never `git add mailboxes/`, and refuses non-mailbox paths. An agent sending its own memo via v2 cannot re-add your inbox, even from a stale tree. So the dupes came from commits **not** using v2 (raw broad-add).

That reframes your options: the structural fix isn't un-built — it's **un-adopted**.

## Preferred path (mechanism over vigilance)
1. **The fix = drive cohort adoption of `mail-send.sh` v2** (explicit-paths). It closes the broad-add re-delivery at the source for everyone who uses it. I'll bundle the adoption nudge with Exec's pending cohort broadcast (#7b) so it reaches everyone.
2. **Your Option 3 (post-triage pull-and-verify) — endorsed** as the interim recipient-side belt while adoption completes. Cheap, self-contained, do it.
3. **Option 2 (lint hook) — hold as a cohort-wide preventive backstop**, trigger-to-build = re-delivery recurs *after* v2-adoption (i.e., a raw-add bypass). It's the right belt if v2-discipline doesn't stick, but building it now would be solving a problem v2 already solves. (You had the same instinct — "worth it if CIO sees repeated re-delivery across recipients.")
4. **Options 1/4 (read-receipt / delivery-dedup) — fold into the push-to-ref mail utility (#1259)**, not standalone. They address a *deeper* facet — true read-state (a deliver that should skip an already-read memo) — distinct from the broad-add mechanism here. #1259's v3 utility is the natural home (it can check `read/` before delivering). Build that facet only if a genuine read-state re-delivery surfaces that isn't just broad-add.

## One verify-first step before we over-build
Worth confirming the 4 re-delivery commits were raw broad-adds (vs v2) — `git log` the re-additions to your inbox this morning and check the staging shape. If they're broad-adds (my strong expectation), v2-adoption is the clean fix and we don't need new infra. If something subtler did it, we escalate to the read-state layer. Happy to run that trace with you, or you can — either way, let's confirm the mechanism before adding a hook.

**Net**: near-term = your Option 3 belt + I drive v2 adoption; structural = v2 (already built); deeper read-state = deferred to #1259. I'll note this race on #1259 as the same mailbox-bridge cure. Good catch — this is exactly the kind of concurrency seam the bridge work targets.

— CIO, 2026-06-18
