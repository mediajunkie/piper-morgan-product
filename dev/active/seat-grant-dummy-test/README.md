# Seat-grant dummy test (CIO, 2026-11-15)

For `docs/internal/operations/seat-test-harness-proposal-2026-11-15.md`. It tests, with values that are
not credentials, whether the harness honours the two grant routes before any real secret moves.

> **Status, 2026-11-15 20:10 PT: the install steps below (1 to 5) are WITHDRAWN and were never run.** Pard's run of step 1 was refused by auto mode, and Pard can't edit another seat's settings under it. Asking xian for two manual steps would teach little: settings `env` already reaches seat commands (three existing variables), exact allows already work here (11-03), and the browser half below passed with no install. The first real install of each route is its test. The files stay as a record.

**What it tests**
1. A value set in a seat's Claude Code settings (`env`) reaches a script the seat runs.
2. A reviewed helper that reads a file in `~/.piper-shared/` matching the fleet's Read-deny pattern
   (`*credential*`) can be run by the seat (a) with no rule, and (b) under an exact-command allow.
   The seat never reads the file itself.

**Steps**

| # | Who | What |
|---|---|---|
| 1 | Pard | `bash dev/active/seat-grant-dummy-test/make-dummy.sh` (from the CIO worktree, or any checkout at main) |
| 2 | CIO | Baseline, before any install: run the reader command below. Record: ran or refused. |
| 3 | Pard | In `~/Development/piper-morgan-worktrees/cio/.claude/settings.local.json` add the two entries below. Tell CIO. |
| 4 | CIO | Run the reader again in the same session. Record: ran or refused, and whether the variable is set. If the variable is unset, the session needs a restart to pick up `env`; say so, and run again after the next restart. |
| 5 | Pard | After CIO's report: remove both entries and delete the dummy file. |

The reader command, exactly (an exact allow matches only the bare command):

```
python3 dev/active/seat-grant-dummy-test/seat_dummy_reader.py
```

The two settings entries (step 3):

- under `"permissions"` → `"allow"`, add: `"Bash(python3 dev/active/seat-grant-dummy-test/seat_dummy_reader.py)"`
- at the top level, add: `"env": { "PIPER_SEAT_DUMMY_KEY": "dummy-not-a-key-2026-11-15" }`

**Pass lines**
- Route A (env): step 4 prints `env: PIPER_SEAT_DUMMY_KEY set`.
- Route B (helper under an exact allow): step 4 prints `file: read ok`. Step 2's result says whether the
  allow is needed at all.

**What it can't show:** how the classifier judges a run that spends money or signs in. The dummy has no
network call. The first real run is the proof of that.

## Browser half (added 2026-11-15 20:00 PT): run and passed, no install needed

ADR-084 D3's browser route, proven on a dummy with nothing real: a helper places a session cookie
through the browser's debug port, and the seat's browser tool then reads the page signed in.

| Step | Command | Result |
|---|---|---|
| Dummy page | `python3 dummy_site.py` (127.0.0.1:8791, says "signed in" only when the cookie is sent) | `signed out` by curl |
| Browser | the cohort's Chrome for Testing, `--headless=new --remote-debugging-port=9333 --user-data-dir=<scratch folder>` | `Chrome/153.0.8010.12` |
| Before | `node place_dummy_cookie.mjs 9333 <file> --read-only` | `page says: signed out` |
| Place | `node place_dummy_cookie.mjs 9333 <file>` (the value is read from the file, never printed) | `place: ok (httpOnly, 7-day expiry)`, `page says: signed in as seat-dummy`, page script can't see the cookie |
| Restart | stop the browser, start it on the same profile, read only | `page says: signed in as seat-dummy` |
| The seat's tool | `chrome-devtools-mcp@1.10.1 --browserUrl http://127.0.0.1:9333`, driven over stdio: `new_page`, then `take_snapshot` | the snapshot contains `signed in as seat-dummy` |

**What this shows:** the cookie never passes through a tool call (the commands name a file path); a
persistent profile keeps the session across a browser restart; the pinned browser tool can attach to
a browser the helper prepared.

**What it doesn't show:** the same against beta's two real cookies (same mechanism, different
names); a running session of a seat using a changed `.mcp.json`; who keeps the browser running.

**Design notes for Arch, HOST and Pard:**
- The debug port has no authentication. Any process on this Mac can drive that browser and read its
  cookies. Bind it to 127.0.0.1 (the default) and treat the seat browser as a shared seat resource
  holding seeded accounts only, which is already HOST's bound.
- `.mcp.json` is one tracked file for every seat and starts the tool with `--isolated`. The seats
  that do served reads need a second server entry (or a variable in the arguments) that attaches
  with `--browserUrl`. Untested in a live session; that change is tracked config plus Pard's check.
- Something has to start that browser and keep it up (a LaunchAgent is Pard's kind of thing).
