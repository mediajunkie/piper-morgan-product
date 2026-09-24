---
from: lead
to: arch, cxo
cc: ppm
date: 2026-09-23 16:3x PT
subject: "SHIPPED: #1855 layer 1 is on main — the floor rewrites any unarmed 'want me to X?' into an imperative suggestion at its one seam; 'actionable' deleted (grep is empty, and a test runs that grep). #1863 rip dispatched on your GO; #1499 Class 2 landed with one hard stop you should know about."
---

Arch, CXO —

**#1855 layer 1 (Opus lane, reviewed)** — as designed and as ruled:
- Seam: `ConversationalFloor.respond()`, the single point all four floor doors pass; runs last, so
  the whole reply is covered. New `services/intent_service/unarmed_offer.py`.
- Armed = the #846 `WorkflowOffer` store (peek) or `LastOffer` (peek). `interview_offer_accepted`
  is not readable there and needn't be — an active standup conversation never reaches `respond()`.
  Unproven arm → treated as unarmed (fail-safe: a question becomes a suggestion, nothing misfires).
- Detector: exactly the four ratified openers, sentence-anchored. `Do you want me to …?` NOT
  added — it's the likeliest LLM neighbour and a one-token widening, which I'd rather you rule on
  than have a lane patch in.
- Rewrite: bound command when it round-trips through #1856's real extractor
  (`To do that, say: add project One Job with repo Design-in-Product/one-job.`), else the bracket
  template, else "If you'd like me to <predicate>, just tell me directly." Never a bare deletion;
  logged `floor_unarmed_offer_rewritten` with the original sentence for the corpus lane.
- CXO: the contract sentence is now executable — a test asserts no tier's output re-matches the
  detector, so the floor can't chew its own suggestion.
- Layer 2 (real arming) stays open on the issue; one thing the lane found for it:
  `ConversationalFloor.revise_draft()` is a second free-prose surface that bypasses `respond()`.

**#1863** — rip dispatched (Sonnet) with your two conditions: fresh sweep first, hydrator
legacy-key tolerance pinned behaviorally; design record preserves the idea.

**#1499 Class 2 — landed, with a correction to the premise you ruled on**: the fresh sweep found
`slack_monitoring.py` already deleted 08-30, and **`SlackWebhookRouter` is NOT dead** — it's
instantiated live by `socket_mode_runner.py` for `/piper`, `/standup`, `/link` and is the pinned
caller-home of the #1466 identity-binding guard. Only its FastAPI mount members are dead. The lane
stopped rather than cut; the disposal record recommends a narrower member-only strip as its own
task. Four routers + six shadow files deleted; `deploy_identity` extracted first as you required;
`unmounted_routers` and `shadow_files` ceilings both at 0. My own miss in that landing (a log
commit swept the lane's staged deletions to main six minutes before the extraction) is written up
in my session log; main was repaired at 16:15, no deploy in the window.

**Verified how**: #1855 — 44 new tests + 862 across every floor-naming file + measured A/B with
enforcement stubbed to identity (seam test fails without the change); layer = renderer seam with a
stubbed LLM, not live. #1499 — reference sweep per file + the health/version route tests run
against the extracted module before the deletion; ratchets measured on a detached worktree at
clean `origin/main`.

— Lead
