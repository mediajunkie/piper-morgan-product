# Spec verification notes (Spec's own checks on workstream claims)

## V-A1 — A finding #1 "unauthenticated setup routes overwrite any user's keys" → **WEAKENED (conditional)**
- `POST /setup/complete` (setup.py:956), `/setup/projects` (:798) and `/setup/slack-credentials` (:1166) all carry
  `dependencies=[Depends(require_setup_incomplete)]` (setup.py:294, #1504, added after an 2026-08-07 audit). That guard
  refuses with 403 once **any** user has `setup_complete = true` (`_completed_setup_exists`, setup.py:279), and fails closed on DB error.
- So the exposure is real **only on an instance where no user has completed setup** (fresh deploy, or one whose users
  were all created via the invite path without the wizard's final step). Locally: 0 of 53 users have setup_complete →
  guard open; probe of /setup/complete with a nonexistent user_id → HTTP 500 (generic message), not 403.
- **Unverified for production (Fly)**: one SQL check (`SELECT count(*) FROM users WHERE setup_complete`) by Lead/PM
  settles it. Not probed by Spec — out of bounds for a read-only review.
- Residual design concerns that still stand: lockout is instance-wide not per-user; `/setup/use-keychain` and
  `/setup/check-system` are unguarded (not yet assessed); the whole prefix is auth-exempt.
- Verified how: read setup.py:279-317, 798-801, 956-959, 1166-1169; local psql count; local curl probe · static + ran-server (local only) · 3 of 3 write routes named by A.

## V-A2 — Gemini API key in public history → **stands; action item independent of the evaluation**
- Per A: present in `dev/2025/10/16/server-startup.log` from 2025-10 until masked at tip 2026-09-24. CLAUDE.md's own rule:
  a credential that ever landed in git history is burned — rotate it. Rotation status unknown → surfaced to PM immediately.

## V-G1 — invite token in a public commit SUBJECT on main → **new finding (Spec, incidental)**
- Commit `7941ae4b97` (2026-07-09, `host(roster): …`) carries a tester's name and a full alpha invite token (masked `QGQP…KJGP`) in its subject line — public in git history. The bearer lint gates files, not commit messages, so this class is unguarded.
- D0's `metrics/commits.csv` copied the subject; masked in place before further pushes (the earlier branch push contained it, adding no new exposure beyond main's own history).
- Action for PM: if that token is still live, revoke/reissue; consider extending the bearer check to commit messages (the autoclose-guard hook already inspects messages).
