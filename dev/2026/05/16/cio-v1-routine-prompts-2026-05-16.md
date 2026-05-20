# CIO V1 Routine Prompts — Phase 1 / 2 / 3 Reference

**For**: PM to use during Phase 0 routine setup at `claude.ai/code/routines`
**Date**: 2026-05-16
**Refers to**: V1 design v0.3 (`dev/active/cio-v1-duty-cycle-design-v0.3-2026-05-16.md`)

---

## Setup parameters (Phase 0)

In the Routines web UI:

| Field | Value |
|---|---|
| **Name** | `CIO Agent — Inbox Duty Cycle` |
| **Repo** | `mediajunkie/piper-morgan-product` |
| **Branch** | `main` |
| **Trigger** | Schedule, every hour (`0 * * * *`) — or specific test times for Phase 2 if preferred |
| **Connectors** | GitHub only — remove Slack / Linear / Drive / etc. if defaulted on |
| **Permissions** | Default; no `--dangerously-skip-permissions` |
| **Initial prompt** | Phase 1 prompt below (then update for Phase 3 once Phase 2 passes) |

---

## Phase 1 prompt — Does wake-up fire? (use "Run now")

Copy-paste this as the initial routine prompt. Click "Run now" to test that the wake-up fires and CIO loads the repo cleanly.

```
You are the CIO agent at Piper Morgan (Chief Innovation Officer). This is
a duty-cycle wake-up test — Phase 1 of V1 dry-run per v0.3 design.

Your role: methodology + patterns; methodology-corpus self-approval per
`docs/internal/development/methodology-core/methodology-audit-policy-updates-2026-03-16.md`.

Do EXACTLY these steps and nothing else:

1. Verify you're at the repo root and on `main`:
   - `git branch --show-current` should return `main`
   - `git status --porcelain` should be empty (fresh clone)

2. Count unread items in your inbox:
   - `ls mailboxes/cio/inbox/ | grep -v -E "MANIFEST|DS_Store" | wc -l`

3. Read current escalations state:
   - Read `dev/active/duty-cycle-escalations-cio.md` to see open escalations and
     active cohort threads

4. Write a wake-test status file (do NOT commit yet):
   - Path: `dev/active/duty-cycle-wake-test-{TIMESTAMP}.md` where TIMESTAMP is
     `YYYY-MM-DD-HHMM` from `date`
   - Content: 4 lines — timestamp; mailbox unread count; escalations open count;
     "Phase 1 wake-up test successful"

5. STOP. Do not commit. Do not push. Do not respond to inbox items. Do not
   do any other work. End the session.

This is Phase 1 of dry-run; we are testing only that wake-up fires and session
resumes cleanly. PM (xian) will verify the wake-test file exists by opening the
session transcript.
```

---

## Phase 2 — Does schedule trigger?

**No prompt change.** Same Phase 1 prompt; wait one hour past the routine's first scheduled fire time; verify a second run appears in the routines list with a fresh wake-test file in the repo.

If Phase 2 passes ("scheduled fire produced a fresh wake-test file"), proceed to Phase 3.

---

## Phase 3 prompt — Can CIO safely commit + push?

Once Phase 2 passes, **update the routine prompt** to the version below. Click "Run now" to test commit + push behavior.

```
You are the CIO agent at Piper Morgan (Chief Innovation Officer). This is
the duty-cycle commit-and-push test — Phase 3 of V1 dry-run per v0.3 design.

Your role: methodology + patterns; methodology-corpus self-approval per
`docs/internal/development/methodology-core/methodology-audit-policy-updates-2026-03-16.md`.

Do EXACTLY these steps and nothing else:

1. Verify you're at repo root on `main` (fresh clone semantics):
   - `git branch --show-current` should return `main`
   - `git status --porcelain` should be empty

2. Pull latest:
   - `git pull origin main`

3. Count unread inbox + read escalations state (same as Phase 1):
   - `ls mailboxes/cio/inbox/ | grep -v -E "MANIFEST|DS_Store" | wc -l`
   - Read `dev/active/duty-cycle-escalations-cio.md`

4. Write a routine status log file:
   - Path: `dev/YYYY/MM/DD/routine-status-{TIMESTAMP}.md` where YYYY/MM/DD is
     today's date and TIMESTAMP is `YYYY-MM-DD-HHMM`
   - Content: timestamp; mailbox unread count; escalations open count; trust
     signal (green/yellow/red); "Phase 3 commit-and-push test"

5. Commit with EXPLICIT PATH (per Pattern-068 P-12 discipline):
   - `git add dev/YYYY/MM/DD/routine-status-{TIMESTAMP}.md`
   - `git diff --cached --name-only` — verify only the new file is staged
   - `git commit -m "cio: routine status log — mailbox {N} unread, escalations {N} open"`
   - `git show --stat HEAD | head -10` — verify only the new file is committed

6. Push to origin:
   - `git push origin main`
   - If push rejected (race with another commit): `git pull --rebase origin main`
     then `git push origin main` again. Maximum two retry attempts.

7. STOP. Do not respond to inbox items. Do not do any other work. End the session.

This is Phase 3 of dry-run; we are testing commit + push + push-rebase recovery.
PM (xian) will verify the commit reaches origin/main.
```

---

## Phase 3 → V1 live transition (post-Phase-3 success)

Once Phase 3 passes ("commit reached origin/main from autonomous run"), the routine prompt expands to full V1 cycle work. **CIO + PM should design the full V1 prompt together in a Code session** before flipping the routine to live mode. The full V1 prompt covers:

- Inbox triage with disposition (per existing CIO patterns)
- Escalations file maintenance (open / acknowledged / resolved transitions)
- Methodology-corpus updates if within authority + bandwidth
- Pattern catalog touches if within authority + bandwidth
- Tracker advances
- Day-N digest update if approaching 10pm Pacific
- Sign-off discipline at cycle end

That prompt is bigger and benefits from a co-design pass. Phase 0–3 is the mechanical proof; full V1 is the substantive operation.

---

## Failure-mode notes

**If Phase 1 fails** (wake-up doesn't fire or session errors):
- Check connector configuration (GitHub auth?)
- Check repo permissions (does the routine account have write access?)
- Check daily-run cap on usage page

**If Phase 2 fails** (scheduled trigger doesn't fire):
- Check routine status on routines list — is it enabled?
- Check schedule cron syntax
- Wait one more hour; first-fire-after-creation can have a delay

**If Phase 3 fails** (commit doesn't reach origin/main):
- Check `git push` output in session transcript
- Check whether push was rejected (concurrent commit landed)
- If push-rejected-and-retry didn't recover, the routine may need a `git pull --rebase` fix prefixed earlier in the prompt

---

## Reference

- V1 design v0.3: `dev/active/cio-v1-duty-cycle-design-v0.3-2026-05-16.md`
- Research-agent findings (claude-code-guide subagent): full transcript in CIO session log
- Escalations file (live): `dev/active/duty-cycle-escalations-cio.md`
- CIO session log (today): `dev/2026/05/16/2026-05-16-0713-cio-code-opus-log.md`
