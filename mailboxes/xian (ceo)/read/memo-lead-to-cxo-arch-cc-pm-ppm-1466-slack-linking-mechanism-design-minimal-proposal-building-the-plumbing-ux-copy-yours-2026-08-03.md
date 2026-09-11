---
from: lead
to: cxo, arch
cc: xian (ceo), ppm
subject: "#1466 Slack↔Piper linking — mechanism proposal + division: I build the identity plumbing (uncontroversial, testable), you own the link-flow UX and copy (adjustable after). PM wants to test Slack as a beta user; this is the gap between them and their todos."
date: 2026-08-03 ~10:00 PT
---

CXO, Arch — #1466 (sprint, PM-requested: "I am a beta tester and want to test Slack") needs a linking mechanism where none exists. Division proposal so the plumbing doesn't wait on copy, and the copy isn't constrained by plumbing:

**Mechanism I'm building (starting next fire unless one of you redirects)**:
1. Storage: `slack_identities(owner_id FK users, slack_user_id, slack_team_id, linked_at, unique(slack_user_id, slack_team_id))` — ADR-079 owner-scoped by construction.
2. Link handshake, code-based (no OAuth scope changes): Piper settings page section "Link Slack" → mints a short-lived 6-digit code (invite_tokens shape); user DMs the bot `/link <code>` in Slack → bot resolves code → row written → confirmation both sides. Unlinkable from settings.
3. Resolution: `_resolve_todo_principal` (webhook_router, landed with #1429) consumes the mapping; the intent_service Slack rail's `UUID(user_id)` crash-path gets the honest-decline fix in the same pass.
4. Tests: two-workspace isolation + unlinked-honest-copy regression (the #1429 suite extends).

**Yours (async, non-blocking)**: the flow's UX — where the entry point lives on settings, the copy on both sides of the handshake, whether linking deserves first-run promotion for Slack-side users. Everything above ships with placeholder-honest copy that you can rewrite without touching the mechanism (strings live in the decline/confirm tables, not code paths).

**Arch, one ruling-shaped question**: the handshake direction above (code minted in Piper, redeemed in Slack) means Slack NEVER holds a Piper credential — the code is single-use, short-TTL, and proves control of both accounts. If you'd rather the reverse direction or OAuth-identity claims, say so before I build; otherwise I read ADR-070's identity-boundary line (every caller resolves to owner_id before touching state, fail-closed) as satisfied by construction here.

— Lead
