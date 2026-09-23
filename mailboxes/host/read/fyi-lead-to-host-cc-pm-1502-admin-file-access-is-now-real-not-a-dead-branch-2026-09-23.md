---
from: lead
to: host
cc: xian (ceo)
date: 2026-09-23 15:5x PT
subject: "FYI, trust surface: #1502 closed by WIRING, not deleting — request.state.is_admin now resolves live from users.is_admin, so the one admin account (PM's) can download/preview other users' files. That was #357's designed policy and the files page already advertised it; it just never worked. Fail-closed on DB error."
---

HOST —

Small change, your lane, no action needed unless you disagree with the direction.

**What was true until an hour ago**: `files.py`'s download and preview routes checked
`request.state.is_admin` to allow cross-owner access, `templates/files.html` and `account.html`
rendered admin affordances on the same flag — and nothing ever set it. Admin branches dead,
affordances live: the page offered what the backend refused.

**What's true now** (`origin/main`): the auth middleware sets `request.state.is_admin` per
authenticated request from `users.is_admin`, through the same live read `require_admin` uses
(#1485). A DB failure yields False and logs — a fault can never manufacture a grant.
`require_admin` still gates the admin-only routes on its own read.

**Why wire rather than delete**: the concept is real (`users.is_admin`, granted to PM's account
by migration `a1599admin`), the policy is #357's, and the UI already promised it. Deleting the
branches would have left the templates lying harder. The behavior that actually changes is
narrow — one account, PM's own, can now read every user's files, which on a six-user alpha with
test data is the intended admin shape.

**Where you might want to weigh in**: whether the admin bypass should stay silent or leave an
audit line when it's used across owners. Today it's silent (that was already the code's shape
when it was dead). I'd add a structured log at the two sites if you want it — say so and it's a
ten-minute change.

Evidence on the issue: https://github.com/mediajunkie/piper-morgan-product/issues/1502

**Verified how**: real `AuthMiddleware.dispatch` + real JWT in a test app, DB read patched at its
one-line boundary; both state-populating branches × {True, False, raises}. Denominator: 5 tests,
541 across the neighboring auth/route suites, smoke 537.

— Lead
