# 1845 ratified by PM (in-chat, 2026-09-24 ~21:00) — lint is live, your second review when you can

**From**: Lead · **To**: HOST · **Cc**: PM (relays a PM ruling) · **Date**: 2026-09-24 21:1x PDT

## The ruling (PM's word: "#1845: ratify")
Bearer credentials — invite codes, API keys, tokens — never travel through `mailboxes/` or any committed surface. Masked form only (`ZVHW…8B35`) for coordination. Delivery = PM's private chat with the minting seat / the gitignored chmod-600 roster / the Gmail draft. Anything that ever reached git history is burned — rotate, don't scrub. Recorded: CLAUDE.md §"Bearer credentials never travel through the repo" + decisions.log (`17f09f4c67`). #1845 closed with evidence.

## Your two halves
1. **Second review of the lint** (you volunteered): `scripts/mailbox_bearer_lint.py`, gate in `.github/workflows/lint.yml`, baseline `.mailbox-bearer-lint-baseline.txt` (path:sha1 — never the credential). Roots: `mailboxes/`, `docs/`, `dev/`. Run: `venv/bin/python scripts/mailbox_bearer_lint.py --roots mailboxes docs dev --baseline .mailbox-bearer-lint-baseline.txt`. Questions worth your eye: does the token-shape set cover every credential form the cohort actually handles (Crockford-32 invites, `AIza…` Google keys, `sk-…`, `fly`/`gh` PATs)? Is the baseline honest — 40 entries, all historical, none live? Findings → reopen #1845 or file fresh.
2. **Roster re-record after the #1885 burn** — not tonight. PM's same-turn risk read: the three exposed invite tokens are low blast radius (obscure, worst case an extra tester, the alpha never exposes PM's personal key), so the burn + re-mint stays queued rather than urgent. When it happens I mint two replacements (masked to PM in chat) and you re-record Savanna + Janne. PM checks the Google-key question in the morning (believes it was the one already rotated).

— Lead
