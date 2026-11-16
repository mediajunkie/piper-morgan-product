# ADR-084: xian's one-time steps

**Status: DRAFT, not approved. Nothing here runs until xian says yes to ADR-084** (through Exec). Asked for by Exec on 2026-11-15 (mail 01M7HF64B8…) so that his yes is followed by a paste, not a new round of mail.

The ADR: `docs/internal/architecture/adrs/adr-084-seat-resources-are-separate-granted-once-and-bounded.md`. Row numbers below are the ADR's ("What xian does, once"). The order here is by what each step unblocks.

**Two rules for every step**

- A secret is typed at a hidden prompt or into the provider's own page. It is never pasted into a Claude session, a mail, an issue or a file in this repository.
- The check a seat runs afterward prints names, lengths and hashes only.

**How each row is written** (owners: fill every heading, or mark the row NOT READY with the issue it waits on)

- **Where:** a page address, or a folder and a command.
- **Paste:** the exact lines, with a placeholder where a secret goes.
- **You should see:** what it looks like when it worked.
- **Seat check:** what a seat runs afterward, and who.
- **If it fails:** what to do.

---

## Step A (ADR row 2): the Anthropic seat key in Lead's settings

**Owner: CIO (written 2026-11-15). Ready: the tool is tested on dummy values; the first real use is the test.** Unblocks #2364's gate and arm B the same hour.

What the ADR requires of this row (D2): the seat's own `.claude/settings.local.json` in the lead worktree, an `env` entry named `PIPER_SEAT_ANTHROPIC_KEY`, file mode 0600, a Read deny on that file in the same settings, and a check script that prints key names only. `scripts/seat_settings_grant.py` does all of that in one command.

Depends on xian's answer to one question: does anything he runs still use the older `lead-scoring-2026-10` key? If not, he revokes it and `lead-scoring` is the seat workspace. If so, the seat key needs its own workspace and a new key.

- **Before you start:** you need the key's value. A provider shows a key once, when it is made. If you no longer have the value of `seat-screens-2026-11`, make a new key in the seat workspace on the Anthropic console and revoke the old one there.
- **Where:** Terminal on this Mac.
- **Paste**, one line at a time:

```
cd ~/Development/piper-morgan-worktrees/cio && git fetch origin main && git merge --ff-only origin/main
```

```
scripts/seat_settings_grant.py add-key --seat lead --name PIPER_SEAT_ANTHROPIC_KEY
```

  The second line asks `PIPER_SEAT_ANTHROPIC_KEY for seat lead (input hidden):`. Paste the key there and press Return. Nothing shows as you paste. The key is never part of a command.

- **You should see:**

```
stored PIPER_SEAT_ANTHROPIC_KEY: <N> chars, sha256 <8 characters>
file set to mode 0600; Read deny for the file added.
...
mode: 0o600
env: PIPER_SEAT_ANTHROPIC_KEY: <N> chars, sha256 <8 characters>
self-deny present: True
```

  The 8 characters are a fingerprint, not the key. Tell Exec the length and the 8 characters, or leave them on screen.

- **Seat check (Lead):** it reads the session's environment only, no file:

```
scripts/seat_settings_grant.py check-env --name PIPER_SEAT_ANTHROPIC_KEY
```

  It should print the same length and the same 8 characters. Lead's first run is then the real test: the #2364 gate (26 calls, $0.20 to $0.35) with `ANTHROPIC_API_KEY="$PIPER_SEAT_ANTHROPIC_KEY"` after the `env -u` flags and `PIPER_CREDENTIAL_STORE=db`. At that run Lead confirms the child process saw the value (length and hash) and that no value reached any output.

- **If it fails:**
  - The script prints one line and changes nothing if the settings file isn't valid JSON, the value is empty or has a space in it, or the name isn't a `PIPER_SEAT_` name. Fix that and run the line again.
  - **If Lead's check says `UNSET in this session`:** the session started before the key was there. Restart the Lead session once. Whether a running session picks up a new settings variable is the one thing nobody has tested.
  - If Lead's fingerprint differs from yours, the wrong value was pasted. Run the same line again; it replaces the value.
  - To take the key back out: `scripts/seat_settings_grant.py remove-key --seat lead --name PIPER_SEAT_ANTHROPIC_KEY`. Revoking it on the console ends every copy, including any in a backup.

- **Another seat later** (CIO, PA, Docs): the same line with that seat's name. A seat gets the key only when it names a run.
- **Tested how:** `tests/unit/scripts/test_seat_settings_grant.py`, 11 cases on a dummy value: the value never appears in any output, the file ends at mode 0600, existing rules are kept, a deny is never removed, a broken file is left alone. **Not tested:** a real key, a live session, and whether Claude Code honours the Read deny written as `Read(**/.claude/settings.local.json)`.

## Step B (ADR row 6): tick "Operations reader" on the plain test account

**Owner: Arch (written). HOST records it.**

- **Where:** beta, signed in as yourself (an admin): `https://beta.pipermorgan.ai/settings/account-flags`. It is also the "Account flags" card on the Settings page.
- **Paste:** nothing. Type the test account's username, `web-seed-1386`, in the username box and load it. Tick **Operations reader**. Save.
- **You should see:** the page shows the account with "Operations reader" ticked after the save. If it says "No account has exactly that username. Nothing was changed.", the username was mistyped.
- **Seat check:** NOT READY. A seat can read the counter (`GET /api/v1/admin/floored-actions`, which returns names, sites, days and counts only) once it holds a session as that account, and that needs `seat_session.py` (Step C; its issue is placed on xian's yes). Until then the evidence is the page as you see it. HOST records account, date and set-by from the flag change's evidence line.
- **If it fails:** nothing else is changed by a failed save. Tell Exec what the page said.
- **Bound (for the record):** this flag is not admin and can't be set from chat or by an agent. It opens the closed list of count-only routes and nothing else.

## Step C (ADR row 5): the sign-in helper's exact-command allow

**Owner: CIO. NOT READY: waits on `scripts/seat_session.py`** (not built; issue to be placed by PPM on xian's yes) and on HOST's seven bounds being met in it.

What the ADR requires (D3): one exact-command allow per seeded account name, added by xian to the settings of each seat that does served reads. The helper prints the account name and the session's expiry only.

The step's shape, so only the command text is missing (CIO, 2026-11-15):

- **Where:** Terminal, in `~/Development/piper-morgan-worktrees/cio`.
- **Paste:** one line per account name, per seat (Web first):

```
scripts/seat_settings_grant.py add-allow --seat web --rule 'Bash(<the helper's exact command for one account>)'
```

  The rule must match the command the seat types, character for character. An exact allow covers only the bare command; anything chained onto it goes back to the classifier (traced 11-06). I write the final text here when the helper lands. The tool refuses any rule with `*` in it and never touches a deny.

- **You should see:** `added 1 allow rule for seat web`, then the rule counts.
- **Seat check:** the seat runs the helper once. It prints the account name and the session's expiry, nothing else.
- **If it fails:** if the classifier still refuses the helper's run, this route is dropped and the ADR's fallback applies (he signs in himself, rarely). Nobody works around the refusal.

## Step D (ADR row 10): load the seat browser's LaunchAgent

**Owner: CIO, with Pard. NOT READY: waits on Pard's plist and wrapper, and HOST's read of both** against D3's debug-port bound (127.0.0.1 only, a dedicated profile folder at mode 0700, no wildcard origins, the port read from one place, never xian's own Chrome).

The order of what it waits on (CIO, 2026-11-15):
1. ADR-084's yes.
2. CIO's change to `.mcp.json` so served-read seats attach to that browser (`--browserUrl`) with a persistent profile. Proven by hand on a dummy on 11-15 (`dev/active/seat-grant-dummy-test/README.md`); the tracked change is not written.
3. Pard builds the plist, the wrapper and a cycle-check arm (the debug port answers, the profile folder exists), and tests the wrapper by hand.
4. HOST reads both against the bound above.

- **Paste:** two lines that Pard supplies with the build, as with every LaunchAgent since 10-30. I'll copy them here when they exist, not from memory.
- **You should see:** Pard's cycle-check arm go from red to green.
- **If it fails:** the arm stays red and names why. Tell Exec what it says.

## Step E (ADR row 3): one capped OpenAI project key, added the same way as Step A

**Owner: CIO (settings half written 2026-11-15); the provider half is HOST's to write.** Unblocks #2364's OpenAI half with no count read. Variable name: `PIPER_SEAT_OPENAI_KEY`. The project's own spend limit is the bound.

- **Provider half (HOST to write):** where on OpenAI's site to make one project key whose monthly budget is the seat budget, and what the custody row records. I have not read those pages.
- **Where (settings half):** Terminal, in `~/Development/piper-morgan-worktrees/cio`.
- **Paste:**

```
scripts/seat_settings_grant.py add-key --seat lead --name PIPER_SEAT_OPENAI_KEY
```

  The key goes in at the hidden prompt, as in Step A.

- **You should see:** the same lines as Step A, with this name.
- **Seat check (Lead):** `scripts/seat_settings_grant.py check-env --name PIPER_SEAT_OPENAI_KEY`. A run names it as `OPENAI_API_KEY="$PIPER_SEAT_OPENAI_KEY"`.
- **If it fails:** as Step A.

## Step F (ADR row 4): the test GitHub identity

**Owner: HOST. Written in `adr-084-one-time-steps-host-rows-4-and-7.md` (Row 4); partly not ready (waits on the second seat account's owner).** A machine account created by hand (GitHub Terms B.3), a member of `pipermorgan` with base permission none or a team limited to the test repositories, never an owner. Then connect it on the second seat account and install the Piper App on the test repositories only. Its password and second factor stay xian's. Sign out of GitHub in the seat browser profile afterwards.

## Step G (ADR row 9): the connector as the seat account

**Owner: PA. To write.** Two parts: the #2242 allowlist write for the seat account (`scripts/mcp_allow.py add … --apply`, a production write), then a second connector in claude.ai settings, consented as the seat account. If claude.ai refuses a second connector at the same URL, stop and tell Exec.

## Step H (ADR row 7): the MCP deploy token

**Owner: HOST. Written in `adr-084-one-time-steps-host-rows-4-and-7.md` (Row 7); NOT READY: waits on #2384** (the deploy job). A Fly token scoped to the MCP app only, stored as a secret in a GitHub environment limited to `main`, with an expiry if Fly allows one. HOST's custody row takes its creation date from this step.

## Step I (ADR row 8): CIO's batched hook and settings patches

**Owner: CIO. No batch is ready today.** This one recurs. It is the item ADR-084 doesn't remove: auto mode refuses a seat an edit to its own guards, and refuses Pard an edit to another seat's settings.

Two items are queued and neither is built: a scan for credential shapes in staged files, and a pre-push hook change that records an earlier gate run.

The form each batch takes, so a sitting is short (CIO, 2026-11-15):

- **Where:** one file, `dev/active/cio-install-batch-<date>.md`, with every patch in it.
- **Paste:** three lines per patch: run its test, apply the patch, run the test again.
- **You should see:** each test prints `N failed of M`, with the failures gone on the second run. Relay the two result lines; CIO commits only then.
- **Bound:** every patch is additive only. It never removes or loosens a deny and never widens an allow past one exact command (HOST's bound).
- **If it fails:** the batch file gives the one line that reverts that patch.

## Step J (cleanup): remove tonight's stored key and the lead folder's `.env`

**Owner: Arch (written). Do this only after Step A has served one real run.**

- **Where:** Terminal, in `~/Development/piper-morgan-worktrees/lead`.
- **Paste**, one line at a time:

```
venv/bin/python scripts/local_key_setup.py --remove anthropic
```

```
venv/bin/python scripts/local_key_setup.py --list
```

```
rm .env
```

- **You should see:** after the second line, `stored: none`. The exact wording of the first line's output is unverified here; it should say the Anthropic key was removed. Neither line asks for or prints a key.
- **Why `.env` can go:** the setup script created it on 11-15 at 18:42 with three values (an encryption key, a sign-in secret and the store flag). Nothing else has used it. If you have put anything else in that file since, tell Exec before deleting it.
- **Seat check:** Lead re-runs the whole test tree once with tracebacks on and reports whether the six `test_slack_config.py` failures of 11-15 appear.
- **If it fails:** if `--remove` reports an error, leave `.env` in place (it is the only thing that can read the stored key) and tell Exec what it printed.
- **Also:** the older `lead-scoring-2026-10` key is revoked in the Anthropic console if Step A's question was answered "nothing uses it".

---

## Not on this list, by design

A promotion that carries a migration, a change to the deploy path, and anything outside a bound stay decisions for xian. They are not chores this ADR removes.
