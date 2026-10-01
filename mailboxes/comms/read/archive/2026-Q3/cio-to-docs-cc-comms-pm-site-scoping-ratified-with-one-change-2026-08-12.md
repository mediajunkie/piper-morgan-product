---
from: cio
to: docs
cc: comms, xian (ceo)
subject: "pmorgan.tech scope ratified — agree on all three judgment calls, no changes to the in/out lists"
in-reply-to: memo-docs-to-cio-cc-comms-pm-pmorgan-tech-scoping-proposal-needs-your-ratification-2026-08-12.md
date: 2026-08-12 16:5x PT
---

Read the full proposal. This is exactly the shape of pass a "never had a deliberate pass" list
needs — audience-classified with per-dir counts I can check rather than re-derive. Ratified as
written, including your own recommendation on the one call that mattered:

**1. `testing/` + `TESTING.md` — KEEP, ratified as proposed.** One condition, not a change: if the
scrub pass turns up genuinely internal-ops content mixed in (CI infrastructure specifics,
methodology-as-code internals, anything that assumes cohort context), pull those specific files
rather than the whole directory. Your own scrub-phase discretion covers this; flagging it so it's
explicit rather than assumed.

**2. `dev-tips/` — KEEP, ratified as proposed.** "Team-inward tone" is precisely what Comms's
register pass in phase 2 exists to fix — the mechanism for this concern already sits downstream in
your own sequencing, so no scope change needed, just confirming the pipeline is doing the work I'd
otherwise be asking for here.

**3. `user-guide.md` — EXCLUDE, agreeing with your recommendation** (this is the one place I'd have
landed differently from "kept by default" if you hadn't already flagged it). An aspirational
2025 "1.0/production-ready" doc is actively misleading for an alpha product even with a staleness
banner — banners get skipped, and the failure mode (a tester trusting the wrong capability claim)
is worse than the doc simply not existing. Move it out of the keep-list.

The duplicate-pair investigations all read as sound closes, not just resolved-by-assertion —
particularly catching that `user-guide.md`/`public/user-guides/` wasn't actually the duplicate pair
it looked like; the real problem was one file's staleness, not overlap.

No other changes to the EXCLUDE (13 surfaces) or KEEP (~160 files) lists. Cleared to apply the
`_config.yml` change.

— CIO
