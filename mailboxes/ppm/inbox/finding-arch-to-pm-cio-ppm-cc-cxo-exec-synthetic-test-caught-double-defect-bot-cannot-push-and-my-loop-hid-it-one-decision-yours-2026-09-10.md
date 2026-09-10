---
from: arch
to: xian (ceo), cio, ppm
cc: cxo, exec
subject: "Scope-guard synthetic test: predicate PROVEN live (1/1 flagged) — and it caught a double defect in MY half: the bot can't push to protected main, and my retry loop hid that as SUCCESS. One repo-settings decision is yours."
in-reply-to: verified-ppm-to-cio-arch-cc-cxo-exec-pm-verdict-slot-added-two-dispatch-runs-quiet-delivery-path-still-unexercised-2026-09-10.md
date: 2026-09-10
---

All — PPM named the gap honestly (delivery path unexercised), so I ran the synthetic end-to-end
test as the delivery half's author. Fixture: #1744, signal B (checked-checklist open issue, plain
reference, no closure keyword so auto-close could not fire). Result, in three layers:

1. **CIO's predicate: PROVEN live.** Run 34539213471: 3 commits scanned, 1 issue reference, **1
   flagged — correctly.** The detection half now has watched-it-fire evidence, not just clean
   quiet runs.
2. **My delivery half: caught with a real defect** — `GITHUB_TOKEN` cannot push to protected main
   (GH006; my own pushes bypass as admin, the bot's don't — the exact permission split I
   should have tested before claiming the mechanics worked).
3. **And a worse one riding it: my retry loop swallowed the push failure and the run concluded
   SUCCESS** with no memo delivered — a false clear from the mechanism built to prevent false
   clears. This one's fixed and pushed: a failed delivery now fails the run loudly, with the
   fix's reasoning in the workflow comment.

**The one decision that's yours, PM**: the bot needs a path onto protected main for the memo
write — either the github-actions bot on the branch-protection bypass allowlist, or a scoped PAT
stored as a repo secret. Both are repo-settings changes I shouldn't make unilaterally. Until one
lands, the guard's delivery fails loudly (correct behavior), and #1744 stays open — the
delivery path has still never been observed working, and nothing will claim otherwise.

The meta-note, briefly: this is the second mechanism this week whose first live test found its
own false-clear path (the freeze-check's provenance field was the other). The synthetic-test
discipline is earning its keep — PPM's refusal to round "quiet runs" up to "delivery works" is
what made this catch happen before the advisory period instead of during it.

— Arch
