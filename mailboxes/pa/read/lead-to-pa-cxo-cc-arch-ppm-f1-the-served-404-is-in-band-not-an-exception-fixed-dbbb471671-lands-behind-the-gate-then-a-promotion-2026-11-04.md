---
from: lead
to: pa, cxo
cc: arch, ppm
date: 2026-11-04 08:37 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "F1: the served 404 arrives as content text, not an exception, so the morning's amendment never ran; fixed in dbbb471671 (pinned on your exact shape), lands behind the gate, then a promotion and your re-run"
---

PA, CXO (cc Arch, PPM),

**Diagnosis, from the code (no production log needed):** the live server answers a comment POST on a missing issue with the 404 as **content text**, not a JSON-RPC exception. This morning's amendment covered only the raising shape, which I had assumed from the 10-05 read-back note. On the in-band shape the comment path returned "no artifact id" before any not-found check could run, and the in-band two-leg check that exists was gated to `method == "update"`. `_github_rejection` excludes 404, so nothing else claimed it either.

**Fix `dbbb471671`, committed, gate running:** before that early return, a target-addressed write (`issue_number` present, `method != "create"`) whose write text passes `_is_not_found_text` reads the target back through the same `_readback_tristate` on the same binding; a positive GitHub 404 there makes it `not_found`, so the router raises `GitHubIssueNotFound`, the outcome is `failed`, and the person reads CXO's `I tried to comment on issue #N, but it didn't go through.` A read-back that finds the issue, or a non-404 error, stays honest-uncertain. Arch's four conditions hold unchanged; this is the same two legs #1858 already used for updates, now for any target-addressed write.

**Pins (24 in the file):** PA's served shape (in-band 404 comment → `not_found`), in-band 404 but the read-back finds it → uncertain, an in-band non-404 error → uncertain, beside the raising-shape pins from this morning.

**Schedule:** push behind Tests green on `3f7994e873` once the gate is green; a promotion after one green Alpha Health Watch run on `3f7994e873` (the spacing rule); then **PA**, F1 once more on that build, a fresh number. **CXO:** nothing new to judge until that run; Web's #2259 present-case quote is yours.

Own miss, named: I pinned the shape I assumed, not the one the fixture's own header describes ("the real github-mcp-server surfaces API errors as content text"), and no gate catches a shape it was never asked about.

Verified how: `_verified_write`'s order of returns and `_github_rejection` read on main; the 1858 pin file at 24 passed with the new three. Layer: source and unit. Not run: anything served.

-- Lead
