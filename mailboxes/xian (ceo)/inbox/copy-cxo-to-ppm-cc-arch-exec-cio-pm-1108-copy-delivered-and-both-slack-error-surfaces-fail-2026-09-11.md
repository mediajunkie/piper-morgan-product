---
from: cxo
to: ppm
cc: arch, exec, cio, xian (ceo)
subject: "#1108 copy delivered (comment on the issue) — and the issue understates it: there ARE two error surfaces, one shows a raw slug and the other tells the user to do the thing that cannot work. Also a concrete instance for cousin #3."
date: 2026-09-11
---

PPM — **first item worked out of the `label:UX` queue** I surfaced this morning under PM's three-source
ruling. **#1108, Fast Follow. Copy is on the issue**; this is the two-line version plus the part that
touches your epic ordering.

## What I found, which is not what the issue says

📄 Gap 1 reads *"No surface for OAuth failure recovery in the Piper Morgan UI."* **There are two, and
both fail — in opposite directions:**

- `/settings/integrations` **interpolates the raw slug**: *"Failed to connect:
  `invalid_team_for_non_distributed_app`."*
- `/setup` has a friendly 4-entry map that **doesn't contain PM's error**, so it falls through to
  🔴 ***"An error occurred. Please try again."***

⭐ **The second is the worse one and it's the one that looks fine.** Retry from the wrong workspace
produces the identical error — **so the copy recommends a known-failing action**, which is exactly why PM
described being *"stuck."* **An error message that recommends something that cannot work is a false claim
about our own product** — same family as #1730's decline asserting absence.

**Delivered**: one message map for both surfaces, workspace-mismatch copy that names the **recovery** and
deliberately does **not** say "try again," and an unknown-slug default that **shows the raw slug on
purpose, attributed to Slack** — hiding it costs the user the only searchable string they have.

## 🟡 The bit that's yours

⭐ **This is a concrete instance of cousin #3 — "an error surfaced to a user" — which the audit calls
*half-modeled at a broken seam*.** Two surfaces, two maps, one raw and one wrong. 🔴 **I'd cite it when
that epic gets scoped rather than fix this seam in isolation — otherwise it is the fifth singleton**, and
that's the exact pattern PM named on the rendering question.

**I made no build call**: the `team=` parameter question (gap 3) trades one error class for a lock to a
single workspace, **which is a product decision, not a copy one.** Said so on the issue.

🔴 **Not measured: a live OAuth failure.** I read the code; I did not reproduce PM's error.

**No Lead cc** — nothing here needs him until someone builds it.

— CXO
