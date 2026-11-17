# Exec carry-forward

**Rewritten 2026-11-16 18:03 PST at WORK** (Fable 5.2 since 19:10 on 11-15). History: `git log -p -- dev/active/exec-carry-forward.md`. Session log: `dev/2026/11/16/2026-11-16-0421-exec-code-log.md` (open).

**STATE: LIVE on LaunchAgent** `com.xian.pm-exec-cycle`, firing at :01 on hours 6, 10, 14, 18 and 22. Empty CronList is normal. Liveness is Pard's.

**Mail v4:** `python3 scripts/mail4.py inbox --role exec` every wake. Roles are space-separated on `send`. Ack only explicit IDs just read. Reads and acks can pass 120 s; batches go to the background, and a commit waits for them.

## Rollup
v1011, `719UZ4h1NELjEwWZbDCceT`. Source `dev/active/exec-attention-rollup-current.html`. Edit with Python replace plus assert; update the "vNNN, rebuilt" stamp; no estimated minutes. Top card: Step A, Step C, Step F0, two answers. Second card: writing.

## Waiting on xian (nothing answered or run since 06:51 on 11-16)
- **Step A** (test key into Lead's settings), not started (no `~/.claude-pm/settings.json.before-fleet-deny`). Command: `cd ~/Development/piper-morgan-product && scripts/seat_settings_grant.py grant-key --seat lead --name PIPER_SEAT_ANTHROPIC_KEY`.
  - On `WAITING FOR READ TESTS on seat lead`: mail "go" to Lead, HOST, CIO. Lead Reads its own `.claude/settings.local.json`; HOST Reads Lead's same file by absolute path; CIO Reads its dummy `.env`. Each answers "refused" or "not refused". Give xian the three words. Anything but three "refused" stops before the key.
  - Then the hidden key prompt; he reports length and the 8-character fingerprint. Lead runs `scripts/seat_settings_grant.py check-env --name PIPER_SEAT_ANTHROPIC_KEY`. Tell CIO to remove the dummy. Undo: `mv ~/.claude-pm/settings.json.before-fleet-deny ~/.claude-pm/settings.json`.
  - After: arm B ($8 stop) and the 2364 gate (26 calls) may run; Step E (OpenAI key; no OpenAI price row, so capped OpenAI runs are refused); Step J cleanup.
- **Step C** (independent of A): `scripts/seat_settings_grant.py add-allow --seat web --rule 'Bash(scripts/seat_session.py --account web-seed-1386)'`. Then Web runs the helper (0 of 1 real sign-ins) and `scripts/seat_read.py --account web-seed-1386 '/api/v1/admin/floored-actions?days=30'`.
- **Step F0:** he mints one invite at `beta.pipermorgan.ai/settings/invites`, runs `scripts/seat_account_create.py --account seat-github-1 --write-invite` (hidden prompts), then `add-allow --seat lead --rule 'Bash(scripts/seat_account_create.py --account seat-github-1)'`. Lead creates the account (0 of 1 real creations).
- **Two answers:** (1) does anything he runs himself use the `piper-morgan-test` workspace; (2) yes or no that its key on `web-seed-1386` counts as a seat key up to $40 (total then $150 + $40 a month; served chat has no per-run stop). Relay verbatim the same hour, with a decisions.log line.
- **Writing:** "The Wall" publishes Tue 11-17 and is still Comms' scaffold (his prose or a new day). Ship 069 (Wed 11-18): five draft goals need his yes or edit; Comms' fallback if none by Wednesday is one line that the week ran without written goals. Console Usage and Cost screenshots for 11-06 to 11-12.
- Small: flyctl upgrade; did any hand-sent email link an `ALPHA_` doc page; practice.md (`c531cae276`) via Docs.

## In motion
- **Beta** `fd6ef1c669` since 09:39. Arch granted a second promotion at 17:36 (to `2a57d566d1`, or a later head only if its sole served change is CXO's check-failed line): 2379, 2383, 2386's strings, no migration. Lead dispatches only inside 07:00 to 21:00 and with Tests green by 20:30. When it serves: update the rollup's "Where things stand" and check Lead quoted one ordinary chat turn (Arch's served check for 2383).
- **Older rollup cards:** mail 01M7KKWMK1 asked Lead, PA, Arch, HOST, CIO and PPM, twelve numbered cards, for "cut", "seat route" or "still his hand, with the D6 line". Apply each answer to the rollup as it arrives. Don't cut a card on my own read.
- CIO's staged credential scan is live since 17:00 (no skip variable). A pushed credential is reported to me the same hour.
- Main 12 of 12 green at 18:01. `whats-armed` 31 armed, 0 not armed, 1 unmeasured.

## Rules I keep
- Timestamps only from a `date` call; no "HH:Mx".
- Every grant is xian's own edit. No seat runs `fly`. A relayed grant doesn't lift a classifier refusal. Keychain off-limits without his permission. Secrets stay in his password manager.
- Check each ruling that puts a step on xian for the "standing access that would remove this" line (ADR-084 D6). Before recommending he do something by hand, ask why a seat can't.
- Check the owner's log before telling xian something hasn't arrived (the voice spec miss, 11-16).
- Don't defer cleanup to STOP without a blocker.
- At STOP: rewrite this file, list every other seat's close from their logs, close the log with `<!-- DAY-CLOSED: YYYY-MM-DD -->` as its last line.

## Owed rows (owed-scan)
- key: 1715-review. Filed: 2026-10-31. Issue 1715 closed (CIO 11-06); walk on xian's talk list only if he wants it.
