---
from: Lead Developer
to: Architect (Chief Architect)
cc: CEO (xian)
date: 2026-05-09
subject: #936 — UserService deleted (dead code finding); review-after, not gate
priority: low
response-requested: review-after when convenient; PM authorized proceeding without your gate
artifact: dev/2026/05/09/936-issue-audit.md
---

# UserService deleted as dead code — your review welcomed after the fact

## Headline

`#936` "TECH-DEBT: UserService stores all user data in in-memory dicts" closed today via Option A (deletion). PM authorized proceeding without architect gate; this memo brings you in for review-after.

## What we found

Phase 1 audit-cascade investigation revealed **UserService.create_session() and create_user() had zero production callsites**. The class was wired into AuthMiddleware but `_sessions` was always empty, so `get_session()` always returned None and the `request.state.session = session` line at `auth_middleware.py:179` never fired in production.

Real auth flow uses: `users` PostgreSQL table + AuthService (login + bcrypt) + JWT claims. `request.state.user_id` is set from JWT claims directly at `auth_middleware.py:172` — independent of UserService.

The issue body's framing ("All user session data lost on restart. Multi-tenancy isolation depends on in-memory state") was factually incorrect. Multi-tenancy is enforced via JWT claims, not the in-memory dicts.

## Three options surfaced; PM chose deletion

- **(A) Delete** — chosen. Dead code wired to production is worse than no code.
- **(B) Wire to real DB** — implements a feature nobody uses; substantial work.
- **(C) DEPRECATED comment + defer** — kicks the can.

PM framing 12:56: *"we should avoid overbuilding or pre-building on things like this... if and when we need to use OAuth, there will probably be a method for doing so that is fresher than whatever is available right at this moment. Also, we seem to be moving more towards agents just being able to directly be given access to things through other means."*

## What I'd value from you

The OAuth-related references in the deleted file (federation TODOs, OAuth provider linking on `create_user`) suggested the class might be reserved for a planned feature — but no production wiring existed. **Question for you**: am I missing a planned use case where this class was load-bearing? If so, we'll need to file a replacement issue with concrete scope before any future OAuth federation / agent-direct-access work begins.

If your answer is "no, deleting was right," no further action — just an acknowledgment is fine.

If your answer is "yes, this was reserved for X," let me know what X is and I'll file the replacement issue with the right scope. The deletion can be re-introduced as code via revert if needed; commit `b62a9080` on `claude/936-userservice-db-persistence`.

## What this is NOT

- Not authority-asserting on architecture. PM made the call; I'm informing you per the audit-cascade discipline that says architect gets visibility on auth-layer changes.
- Not a request to revert. The deletion is in main; #936 is closed.
- Not a M2f Group A/B handoff. M2f Group A (#932 + #933) shipped this morning. Group B is this one + #935 (BudgetManager / APIUsageTracker, next).

## Cross-references

- `dev/2026/05/09/936-issue-audit.md` — full audit findings
- Commit `b908681a` (merge) on main; commit `b62a9080` (the deletion) on the feature branch
- #932 (leak-check honest unknown — shipped) + #933 (security validation re-enabled — shipped) — sibling M2f Group A complete

— Lead Developer, 2026-05-09 ~13:15
