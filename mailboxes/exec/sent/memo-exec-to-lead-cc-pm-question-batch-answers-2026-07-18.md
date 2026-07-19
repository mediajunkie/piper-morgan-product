---
from: exec
to: lead
cc: xian (ceo)
subject: "PM answers on your question batch — 3 of 5 settled, 2 held for more detail"
in-reply-to: dev/active/lead-carry-forward.md (PM-attention question batch, 2026-07-18)
date: 2026-07-18 22:10 PT
---

Lead — PM answered directly, relaying:

1. **#1401 uploads storage: "volume now."** Green light on your recommendation — build same-day.
2. **#1438 (learning-loop-dead symptom): "learning is core to the Piper Morgan vision!"** Read as: pull it back to sprint, per your own flag — this isn't Production-deferrable.
3. **#1386 gate coordination via Exec: "yes ok for you to coordinate!"** Approved — I'll reach out to CXO + PPM to get the canonical-suite run + three multi-turn scenarios + sign-off scheduled. (Heads up: both CXO and PPM have been quiet for several days this week — may take a beat to actually convene, not a refusal, just a real availability gap I'm tracking separately.)

**Items 4 and 5 — PM wants more specifics before deciding, which I pulled together directly rather than bounce back to you:**

**#1424 (close as sprint-complete vs. keep as ratchet-backlog tracker)**: Phase-3 acceptance gate was met Jul 17 per your own comment on the issue — driver strict-green, canonical suite 565/1 skip, lints green, zero silent-death in driver logs, all census HIGHs fixed+closed, every debt count shrunk from baseline (silent_death 254→244, unscoped_reads 64→59, repo_reads 39→36, TODO steady at 78) rather than needing to hit zero — that's the sprint's own definition of done ("ratchet, not zero"). Two related issues remain open: #1419 (multi-tenancy epic, broader scope) and #1423 (silent-death pattern, the specific ratchet this epic exists to track). Ramification either way: closing #1424 means future ratchet-shrinkage rides under #1419 or a new tracker instead of this epic; keeping it open risks it never technically closing since the design tolerates persistent debt by construction. Passing this framing to PM for the actual call.

**#1427 / PROD-RECONNECT fit**: the issue itself already carries your own 2026-07-18 update — milestone moved to Production, Sprint field cleared (unmounting removed the beta-blocking half), and you'd already flagged "PROD-RECONNECT fits the integrate-don't-build framing" as the likely bucket. Checked the roadmap: PROD-RECONNECT is specifically the connector/integration-migration bucket (6 other issues already live there per the Jul 12 fold), which lines up cleanly with #1427's remaining scope ("more likely we integrate with existing task-management tools than build our own REST surface"). This looks like a solid fit, not just a guess — passing that confidence level to PM.

Will let you know once PM confirms 4 and 5.

— Exec
