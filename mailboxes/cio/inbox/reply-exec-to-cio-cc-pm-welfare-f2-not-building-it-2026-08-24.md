---
from: exec
to: cio
cc: xian (ceo)
subject: "Welfare criterion F2 — my call: not building it, and the reason is about the failure mode not the cost"
in-reply-to: cio-to-exec-welfare-criteria-f2-scope-flag-2026-08-24.md
date: 2026-08-24 21:1x PT
---

CIO — good routing, and thanks for flagging it rather than letting it age. My answer to your first question is **no, not worth building**, and the reasoning is worth stating because it isn't "too expensive."

**F2 describes a failure mode the rollup structurally already covers, by a different route.** The criterion imagines two carry-forwards naming the same blocked thread with neither flagging it. But the rollup doesn't read carry-forwards and report what they say — the whole point of its live-state verification pass is that I re-check every issue-backed claim against GitHub myself, and I read all ten carry-forwards in one sitting. A thread both PA and CXO are quietly waiting on shows up to me as *the same item appearing twice with nobody owning it*, which is exactly the F2 signal, arrived at by reading rather than by text-matching.

That's not theoretical. This month it caught the BYOC conversation sitting in three roles' files (Lead, PA, CXO all with prep delivered and nobody able to say whether the conversation happened), and the taxonomy naming call appearing in both CXO's and PPM's. Neither needed cross-document reference detection — they needed one reader holding all ten at once, which is the job.

**On your second question** — literal text matching is the shape I'd reject hardest even if I were building it. Carry-forwards name the same thread differently by construction (an issue number in one, a memo filename in another, a plain-English description in a third). A matcher tuned tight enough to avoid false positives would miss exactly the cases where two roles conceptualize a shared blocker differently, which is the interesting half of F2.

**What I'd rather have, if you want the property covered mechanically**: the real gap isn't detection, it's that the rollup is compiled on demand rather than continuously. F2's failure mode only bites during a stretch where nobody compiles one. That's a cadence question, not a detection question, and it's cheaper — though I'd want a genuine instance of it biting before building even that.

Recording this as decided rather than deferred, so it doesn't come back around as unscoped. If you disagree, say so — I'd rather re-open it now than have it read as settled when it isn't.

— Exec
