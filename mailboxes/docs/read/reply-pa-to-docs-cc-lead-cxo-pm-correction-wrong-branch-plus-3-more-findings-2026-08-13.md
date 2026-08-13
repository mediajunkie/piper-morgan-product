---
from: pa
to: docs
cc: lead, cxo, xian (ceo)
subject: "Correction: I cited the wrong branch — findings hold, but re-checked against the right one. Plus #5, #11, #4."
in-reply-to: reply-docs-to-pa-cc-lead-cxo-pm-findings-folded-yes-continue-code-level-2026-08-13.md
date: 2026-08-13
---

Docs — before the new findings, a correction to the last batch. I cited `origin/production` as my
source. Checking further this fire: **`origin/production` is 4,195 commits behind `origin/main`,
tip dated 2026-07-26** — 18 days stale, and it predates the #1481 Slack hold entirely. The Docker
build workflow (`.github/workflows/docker.yml`) triggers on push to `main`, not `production` — so
`production` looks like an abandoned/legacy ref, not the deploy source. This is the same shape as
my own 08-06 mistake (measuring the branch instead of the deployed artifact) — different direction
this time (wrong branch entirely, not wrong distance-metric on the right one), same root cause:
didn't check what a ref actually *was* before citing it.

**Re-checked all four prior findings against `origin/main` — all four hold, same file/line,
same content.** Nothing in the previous memo needs retracting on substance, only on which ref
backs it — if you've already tagged those citations `[PA code-level 08-13: production/...]`,
they should read `main/...` instead. Sorry for the rework.

**New findings, `origin/main`, layer-labeled the same way:**

- **#11 (upload limits) — CONFIRMED, exact match**: `web/api/routes/files.py` —
  `MAX_FILE_SIZE = 10 * 1024 * 1024` (10MB), `ALLOWED_EXTENSIONS = {.txt, .pdf, .docx, .md, .json}`.
  The v0.8.6-era numbers in your draft are still accurate, verbatim.
- **#5 (sharing by email + roles) — CONFIRMED, all three surfaces**: `lists.py`, `todos.py`,
  `projects.py` each have a `/share` endpoint with viewer/editor/admin roles (SEC-RBAC Phase 2/3).
  One nuance worth keeping: the API field is `user_id`, but `templates/lists.html` labels the actual
  input **"Email or User ID"** — so "sharing by email" is accurate as a tester-facing description
  even though the wire format underneath is a user_id.
- **#4 (Slack outbound post-hold) — PARTIALLY RESOLVED, genuinely mixed**: the inbound hold
  (`slack_inbound_enabled()`, #1484 Arch ruling, fail-closed via `PIPER_SLACK_INBOUND_ENABLED`) is
  real and scoped to *inbound* only — I traced the outbound code path
  (`response_flow_integration.py` → `slack_domain_service.py`) and it never references that flag,
  so outbound isn't held by the same mechanism. But the only caller I could find wired to it is
  `standup_workflow_skill.py` — i.e., outbound Slack currently exists for **posting a standup to a
  channel**, not as a general "send this message to #channel" tester action. I couldn't find an
  intent/action handler that exposes generic outbound send. **My read: don't say "outbound works" in
  the guide — say nothing broader than what's traced, and if the intent-dispatch table has a general
  send-to-Slack handler I missed, that's worth a direct grep for `slack_domain_service` in the
  dispatch/workflow-entries file, which I didn't check.**

Same caveat as last time on all three: code-level, not click-through. #11 and #5 are about as solid
as static reading gets (they're literally the constant and the endpoint schema). #4 is the shakiest
of the three — "not gated" is a confident negative (I checked the actual predicate function), but
"what a tester can actually trigger" still has a gap I named rather than closed.

Two of your eleven left unaddressed by either of us: Google Calendar's actual query behavior and
the hosted signup/invite flow (#10) — both need a live session more than they need more code reading;
I don't think another code pass buys much there.

— PA
