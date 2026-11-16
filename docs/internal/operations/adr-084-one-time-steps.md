# ADR-084: xian's one-time steps, written out

**Status: NOT APPROVED. Nothing here runs until xian says yes to ADR-084** (Exec's card). This file exists so his yes is followed by a paste and not by another round of mail (Exec 01M7HF64B8, 2026-11-15).

- Row numbers are the ADR's ("What xian does, once"). The order below is Exec's: the rows that unblock the most come first.
- **A secret is only ever typed at a hidden prompt or into the provider's own page.** It is never pasted into a Claude session, a mail, or a command line.
- Each row says who wrote it. A row marked **NOT READY** waits on a build and names it.
- Owners: CIO rows 2, 3, 5, 8, 10. HOST rows 4, 7. PA row 9. Arch reads the whole file.

| Order | Row | What | Ready? |
|---|---|---|---|
| 1st | 2 | Anthropic seat key into Lead's settings | Ready (tool tested on dummies; first real use is the test) |
| 2nd | 6 | Tick "Operations reader" on the plain test account | Owner to write (the control is served since 11-15) |
| 3rd | 5 | The sign-in helper's exact allow | NOT READY: waits on `seat_session.py` |
| | 3 | OpenAI seat key, same way | Settings half ready; provider half is HOST's to write |
| | 4 | Test GitHub identity (machine account) | HOST to write |
| | 7 | MCP deploy token in a GitHub environment | HOST to write; job is #2384 |
| | 9 | Allowlist write, second connector, one sign-in | PA to write |
| | 10 | Load the seat browser's LaunchAgent | NOT READY: Pard builds it, HOST reads it |
| | 8 | Install CIO's batched hook and settings patches | Recurs; no batch is ready today |
| last | cleanup | Remove tonight's stored key and the lead folder's `.env` | Lead to confirm the commands |

---

## Row 2. The Anthropic seat key, into Lead's settings (CIO)

**What it does.** Puts the capped seat key into the Lead seat's own git-ignored settings file as the variable `PIPER_SEAT_ANTHROPIC_KEY`. Lead's paid runs then name it on the command line. No keychain, no `.env`, no file read by a seat.

**Before you start.** You need the key's value. A provider shows a key once, when it is made. If you no longer have the value of `seat-screens-2026-11`, make a new key in the seat workspace on the Anthropic console and revoke the old one there. Which workspace is Arch's question on the card (does anything of yours still use `lead-scoring-2026-10`?).

**Where.** Terminal on this Mac.

**Paste these two lines, one at a time:**

```
cd ~/Development/piper-morgan-worktrees/cio && git fetch origin main && git merge --ff-only origin/main
```

```
scripts/seat_settings_grant.py add-key --seat lead --name PIPER_SEAT_ANTHROPIC_KEY
```

The second line asks: `PIPER_SEAT_ANTHROPIC_KEY for seat lead (input hidden):`. Paste the key there and press Return. Nothing shows as you paste.

**What you should see.**

```
stored PIPER_SEAT_ANTHROPIC_KEY: <N> chars, sha256 <8 characters>
file set to mode 0600; Read deny for the file added.
...
mode: 0o600
env: PIPER_SEAT_ANTHROPIC_KEY: <N> chars, sha256 <8 characters>
self-deny present: True
```

The 8 characters are a fingerprint, not the key. Tell Exec the length and the 8 characters, or just leave them on screen.

**The check a seat runs afterward (Lead).** It reads the session's environment only, no file:

```
scripts/seat_settings_grant.py check-env --name PIPER_SEAT_ANTHROPIC_KEY
```

It should print the same length and the same 8 characters. Then Lead's first run is the real test: the #2364 gate (26 calls, $0.20 to $0.35), with `ANTHROPIC_API_KEY="$PIPER_SEAT_ANTHROPIC_KEY"` after the `env -u` flags and `PIPER_CREDENTIAL_STORE=db`.

**If it fails.**
- The script prints one line and changes nothing if: the settings file isn't valid JSON, the value is empty or has a space in it, or the name isn't a `PIPER_SEAT_` name. Fix that and run it again.
- **If Lead's check says `UNSET in this session`:** the session started before the key was there. Restart the Lead session once. Whether a running session picks up a new settings variable is the one thing nobody has tested.
- If Lead's fingerprint differs from yours, the wrong value was pasted. Run the same line again; it replaces the value.
- To take the key back out: `scripts/seat_settings_grant.py remove-key --seat lead --name PIPER_SEAT_ANTHROPIC_KEY`. Revoking it on the console ends every copy, including any in a backup.

**For another seat later** (CIO, PA, Docs), the same line with that seat's name. Give a seat the key only when it names a run.

**Tested how.** `tests/unit/scripts/test_seat_settings_grant.py`, 11 cases, with a dummy value: the value never appears in any output; the file ends at mode 0600; existing rules are kept; a deny is never removed; a broken file is left alone. Not tested: a real key, a live session, and whether Claude Code honours the Read deny written as `Read(**/.claude/settings.local.json)`.

---

## Row 6. Tick "Operations reader" on the plain test account (owner to write)

Exec's order puts this second. It is not one of CIO's rows, and I have not seen the served page, so I won't guess its clicks. Lead described it on 11-15 as: Settings, Account flags; type the test account's username; tick Operations reader; Save. HOST records it. Lead or HOST: please replace this paragraph with the exact page address, what he sees after Save, and the seat's check.

---

## Row 5. The sign-in helper's exact allow (CIO). NOT READY

**Waits on:** `scripts/seat_session.py`, the helper in ADR-084 D3 with HOST's seven bounds. It is not built, and I don't know its issue number; PPM or Lead, please add it here.

**What the step will be**, once the helper is on main and HOST has read it. One line per account name, per seat that does served reads (Web first):

```
scripts/seat_settings_grant.py add-allow --seat web --rule 'Bash(<the helper's exact command for one account>)'
```

- The rule has to match the command the seat will type, character for character. An exact allow covers only the bare command; anything chained onto it goes back to the classifier (traced 11-06). So the final command text is fixed when the helper lands, and I will write it here then.
- The tool refuses any rule with `*` in it and never touches a deny.
- **What he'll see:** `added 1 allow rule for seat web`, then the rule counts.
- **The seat's check:** it runs the helper once. The helper prints the account name and the session's expiry, nothing else.
- **If it fails:** if the classifier still refuses the helper's run, that route is dropped and the fallback in the ADR applies (he signs in himself, rarely). No one works around the refusal.

---

## Row 3. The OpenAI seat key (CIO for the settings half)

**Settings half, ready.** Same as row 2 with the other name:

```
scripts/seat_settings_grant.py add-key --seat lead --name PIPER_SEAT_OPENAI_KEY
```

Lead's check: `scripts/seat_settings_grant.py check-env --name PIPER_SEAT_OPENAI_KEY`. A run names it as `OPENAI_API_KEY="$PIPER_SEAT_OPENAI_KEY"`.

**Provider half, HOST's to write:** where on OpenAI's site to make one project key with a monthly budget equal to the seat budget, and what the custody row records. I have not read those pages.

---

## Row 10. Load the seat browser's LaunchAgent (CIO). NOT READY

**Waits on, in order:**
1. ADR-084's yes.
2. My change to `.mcp.json` so served-read seats attach to that browser (`--browserUrl`) with a persistent profile. Proven by hand on a dummy on 11-15 (`dev/active/seat-grant-dummy-test/README.md`); the tracked change is not written.
3. Pard builds the plist, the wrapper and a cycle-check arm (debug port answers, profile folder exists), and tests the wrapper by hand.
4. HOST reads the plist and wrapper against D3's bound: 127.0.0.1 only, a dedicated profile folder at mode 700, no wildcard origins, the port read from one place, never xian's own Chrome.

**What the step will be:** a two-line paste that Pard supplies with the build, as with every LaunchAgent since 10-30. **What he'll see:** Pard's cycle-check arm goes from red to green. **If it fails:** the arm stays red and names why. I'll copy Pard's two lines here when they exist. I'm not writing them from memory.

---

## Row 8. Install CIO's batched hook and settings patches (CIO). Recurs

This is the one row the ADR doesn't remove. Auto mode refuses a seat an edit to its own guards, and refuses Pard an edit to another seat's settings, so these stay xian's.

**No batch is ready today.** Two items are queued and neither is built: a scan for credential shapes in staged files, and a pre-push hook change that records an earlier gate run.

**The form each batch will take**, so a sitting is short:
- one file, `dev/active/cio-install-batch-<date>.md`, with every patch in it;
- each patch has a test that prints `N failed of M`, to run before and after;
- each patch is additive only: it never removes or loosens a deny, and never widens an allow past one exact command (HOST's bound);
- the paste for each is three lines: run the test, apply the patch, run the test again. He relays the two result lines, and I commit only then.

**If a patch's test fails after applying:** the batch file gives the one line that reverts that patch.

---

## Rows 4, 7 and 9 (HOST, HOST, PA)

Not mine to write. HOST: row 4 (the machine account, its bounds in the org, the connect and install clicks) and row 7 (the MCP-app-scoped deploy token, stored in a GitHub environment limited to `main`; job #2384). PA: row 9 (the #2242 allowlist write, the second connector at the MCP address with its fallback if claude.ai refuses a second one, the one consent sign-in).

---

## Cleanup, after the settings route has served one run (Lead to confirm)

Exec asked for this row. I can state its purpose but not its commands, so they are for Lead to confirm before he sees them:

- **Remove the key stored on 11-15 at 18:42** through `local_key_setup.py`. Lead named the command as `local_key_setup.py --remove anthropic`, run from the lead folder. Unverified by me: whether that command needs the folder's `.env` to run, and who can run it (Lead's seat is refused any touch of that file).
- **Delete the lead folder's `.env`**, which is xian's file. It was created that evening and also holds a database encryption key and a sign-in secret for that folder. Lead: confirm nothing in your local runs depends on those once the stored key is gone.
- Then Lead re-runs the whole test tree once with tracebacks on (Lead's offer, 11-15 21:26) to see whether the six Slack config failures ever return.
