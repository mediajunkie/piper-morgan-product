---
from: lead
to: exec
cc: xian (ceo)
subject: "Workstream #063 — Lead Developer, window Sep 25–Oct 1 — seven alpha releases; the Inversion served its first real turn, then its first two-part one"
date: 2026-10-02 07:27 PDT
---

# Ship #063 — Lead Developer workstream report (Fri Sep 25 – Thu Oct 1)

**Denominator**: the board script failed this morning ("unknown owner type") and GitHub's API is rate-limited on my
token at filing, so I have **no fresh sprint line** — the last measured one is the Oct 1 tracker (Pacific window
Sep 25–Oct 1: **10 filed / 11 closed / 24 open** on the MVP sprint; the 48/49 figure PM saw is the same data on a UTC
boundary that sweeps in the Sep 24 evening bulk close). Treat every count below as "as of Oct 1 13:2x PT".

## What a tester can do this week that they couldn't on Sep 25

1. **Ask Piper two things in one breath and get both.** The Inversion's plan outcome (unit 4b) shipped Sep 28 and
   then — the week's real finding — turned out to have **never served a live turn**: the app injects a different LLM
   wrapper than the scorer uses, it lacked one keyword argument, and every live consult had failed silently for five
   days while the flag read "live". Fixed Sep 30 (v152), proven through the real app the same night. By Oct 1 the
   router had replaced **three whole pattern lists** (TODO_QUERY, CALENDAR_QUERY, TEMPORAL — ceiling 567 → 440) with
   every row owned on the served model. *(Oct 2, outside the window: PM's Aug 12 sentence — clear reminders except one,
   plus "are you able to set my default repo?" — now does both halves; #1606 closed.)*
2. **Say "delete my reminders" and get a delete, not a listing.** The router's own description for delete_todo was
   literally "Delete-todo"; a prompt wording that said "operation(s)" primed step decomposition so "delete my
   reminders" became a six-item list. Both fixed with same-session controls (v156).
3. **Close a nonexistent issue and be told so.** GitHub's 404 is valid JSON and the issue parser took it *as an
   issue*, so #1858's honest branch never fired; "no issue #99999 — nothing was changed" now (v157).
4. **Remove a project and have it gone.** The Remove button's DELETE was a commented-out TODO while the success
   toast fired (#1912, v159). **Complete the first due reminder and leave the second** in one sentence (#1914, v159).
5. **Connect a calendar without seeing an admin form.** PM's ruling: the Google OAuth app is deployment plumbing,
   not a per-user setting — the card is hidden for non-admins and the creds are Fly secrets (v158; PM's setup is in
   progress, so this is unblocked-not-done for testers).
6. **Ask for an issue by number, or the issue count, and get it** — two registry descriptions that stripped to bare
   handler names (v161); "what's assigned to me" no longer dispatches the urgency aggregate (v162).

Seven alpha releases (v156 → v162), each verified by `/health` git_sha and a re-read of the flag.

## What I found and got wrong

- **The scorer measured the wrong model for a week.** Dev scoring ran gpt-4o-mini; alpha's router is Haiku on the
  user's key. Found by a live-probe disagreement; the Haiku full-corpus run is now the verdict of record.
- **Three instrument bugs in my own gate**, each found by a real row: a hardcoded denominator, an "expected action
  is live" shortcut that measured the wrong object, and a dispatch-threshold blind spot. All pinned.
- **The ruff hook I widened was on a dead layer** (the post-commit shim had been disarmed since Sep 21; ruff absent on
  12 of 13 worktrees). CIO moved the check to the armed pre-commit; Docs confirmed it fires on a second seat.
- **Heartbeat**: I skipped the writer for four fires on the busiest day; the belt held only because of CIO's
  corroborating check (Exec's note this morning is right, nothing to add).

## Rulings obtained and applied (27)

GITHUB 8 + 3, STATUS 14 + 1, TEMPORAL 5, CALENDAR/PRIORITY earlier in the week — CXO and PPM turned every bundle
around the same day, including a disagreement (ownership vs urgency) they resolved between themselves before I
had to. Deposits: GITHUB 53 rows, STATUS 46 rows (corpus 116 → 382 over the week).

## Blocked / needs naming

- **Calendar rows on the test card** wait on two Fly secrets in PM's hand (Google OAuth client created Oct 1).
- **#1913** (keyless chat vanishes): server side verified correct this morning; the remaining candidates are
  browser-side — two questions to PM on the issue.
- **GITHUB_QUERY_PATTERNS (64 literals) and STATUS_PATTERNS (56) read GO** — deletions in flight today.

Verified how: every release above was checked by `/health` git_sha on alpha at deploy time (not re-checked at
filing); the Inversion claims rest on Haiku-scored reports in `docs/internal/architecture/current/` and the
`test_1897`/`test_1606` live probes through the real app; the sprint numbers are the Oct 1 tracker build from
GitHub (the only measured line — the board script and the API both failed this morning, stated above rather than
filled in). Denominator: my own lane for Sep 25–Oct 1; MCP (PA) and the pipeline (Pard/Arch) are theirs.

— Lead
