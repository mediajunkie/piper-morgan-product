# Seat-grant dummy test (CIO, 2026-11-15)

For `docs/internal/operations/seat-test-harness-proposal-2026-11-15.md`. It tests, with values that are
not credentials, whether the harness honours the two grant routes before any real secret moves.

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
