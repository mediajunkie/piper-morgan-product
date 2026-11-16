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

**Owner: CIO. To write.** Unblocks arm B the same hour (its $8 stop is in code). The #2364 gate runs the same hour only if #2383 (the live-call cap) has landed; if it hasn't, Lead sends Exec the planned-calls line first (26 calls, $0.20 to $0.35), as ADR-084 D2 requires for a run with no in-code stop (Lead, 11-15 22:07).

What the ADR requires of this row (D2): the seat's own `.claude/settings.local.json` in the lead worktree, an `env` entry named `PIPER_SEAT_ANTHROPIC_KEY`, file mode 0600, a Read deny on that file in the same settings, and a check script that prints key names only. At the first real run, the check is that the child process saw the value (length and hash) and that no value reached any output. Whether a running session needs a restart to pick up the entry shows here; say what to do if it does.

Depends on xian's answer to one question: does anything he runs still use the older `lead-scoring-2026-10` key? If not, he revokes it and `lead-scoring` is the seat workspace. If so, the seat key needs its own workspace and a new key.

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

## Step D (ADR row 10): load the seat browser's LaunchAgent

**Owner: CIO, with Pard. NOT READY: waits on Pard's plist and wrapper, and HOST's read of both** against D3's debug-port bound (127.0.0.1 only, a dedicated profile folder at mode 0700, no wildcard origins, the port read from one place, never xian's own Chrome).

## Step E (ADR row 3): one capped OpenAI project key, added the same way as Step A

**Owner: CIO. To write.** Unblocks #2364's OpenAI half with no count read. Variable name: `PIPER_SEAT_OPENAI_KEY`. The project's own spend limit is the bound.

## Step F (ADR row 4): the test GitHub identity

**Owner: HOST. Written in `adr-084-one-time-steps-host-rows-4-and-7.md` (Row 4); partly not ready (waits on the second seat account's owner).** A machine account created by hand (GitHub Terms B.3), a member of `pipermorgan` with base permission none or a team limited to the test repositories, never an owner. Then connect it on the second seat account and install the Piper App on the test repositories only. Its password and second factor stay xian's. Sign out of GitHub in the seat browser profile afterwards.

## Step G (ADR row 9): the connector as the seat account

**Owner: PA. Written 2026-11-15 22:10 (PA).** Comes after Step F has created the GitHub-connected seat account. No secret passes through a session. The only secret is the seat account's Piper password, which you type into Piper's own sign-in page in part 2.

**Order with Step F (it matters for one #2342 row):** if you can, do F's *connect GitHub* on the seat account, then this step, then tell Exec. PA reads once while the App is installed nowhere (the "Install the GitHub app" line, which no account has shown yet), and only then do F's *install on the test repositories*. If that's awkward, do F whole first; PA loses only that one read.

**Part 1: put the seat account on the MCP allowlist** (#2242; a production write, about 2 minutes)

- **Where:** your Terminal, in any checkout (the command runs inside the beta container).
- **Paste** (dry run first; it changes nothing):
  ```
  fly ssh console -a piper-morgan -C "python /app/scripts/mcp_allow.py add --user-email <seat-account-email>"
  ```
  Then the same line with `--apply` at the end:
  ```
  fly ssh console -a piper-morgan -C "python /app/scripts/mcp_allow.py add --user-email <seat-account-email> --apply"
  ```
  `<seat-account-email>` is the GitHub-connected seat account's sign-in address from HOST's custody row. It isn't a secret.
- **You should see:** a `--- target:` line with the database address masked. The dry run ends `DRY-RUN complete — no writes.` The `--apply` run ends `add: done for <seat-account-email> (…)`, then a `--- listed: N` block that includes the seat account.
- **Seat check:** none from a seat (no seat reads the production database). The check is part 2's consent working: an unlisted account gets a 403 at the consent page.
- **If it fails:** `refusing: --user-email is not a plain address` means a typo, so re-run. `No such user: … — nothing written.` means the seat account doesn't exist on beta under that address, so check the address or do Step F first. Anything else: paste the error line (not the list) to Exec.

**Part 2: add the second connector and consent as the seat account** (about 3 minutes)

- **Where:** claude.ai → Settings → Connectors → **Add custom connector**.
- **Paste:** name `Piper Morgan (seat)`, URL `https://mcp.pipermorgan.ai/mcp`. Leave your existing **Piper Morgan** connector as it is. Don't remove or re-consent it.
- **Then:** Claude opens a browser tab on Piper's sign-in page. **If you're signed in to Piper as yourself in that browser, sign out first, or use a private window**, otherwise the consent goes to your own account. Sign in as the seat account (type its password there, into Piper's page), and press Allow on the consent page.
- **You should see:** the tab returns to Claude, and the connectors list shows both **Piper Morgan** and **Piper Morgan (seat)** as connected.
- **Seat check (PA):** in PA's session, list the MCP resources and confirm a second Piper server is present. Then read `piper://me/profile` through it, which should name the seat account, not you, and `piper://me/github/issues` through it. PA quotes the account's display name, the issue count and repositories, and MCP `uptime_seconds`. PA reads your own connector once to confirm it still answers as you. **Unverified:** whether a running Claude Code session sees a newly added connector without a restart. If PA doesn't see it, PA asks Exec for a session restart, not anything from you.
- **If it fails:**
  - **claude.ai refuses a second connector at the same URL:** stop and tell Exec. Don't remove your own connector to make room. This is the one-try test (ADR-084 open item); the fallback is Arch's.
  - **403 on the consent page:** part 1 didn't stick. Run `fly ssh console -a piper-morgan -C "python /app/scripts/mcp_allow.py list"` and check the seat account is listed.
  - **The consent lands on your own account** (PA's profile read names you): remove only **Piper Morgan (seat)**, sign out of Piper, and repeat part 2.

**Ending** (with HOST's review date): remove **Piper Morgan (seat)** in claude.ai, then `mcp_allow.py remove --user-id <seat-account-id> --apply` the same way as part 1.

## Step H (ADR row 7): the MCP deploy token

**Owner: HOST. Written in `adr-084-one-time-steps-host-rows-4-and-7.md` (Row 7); NOT READY: waits on #2384** (the deploy job). A Fly token scoped to the MCP app only, stored as a secret in a GitHub environment limited to `main`, with an expiry if Fly allows one. HOST's custody row takes its creation date from this step.

## Step I (ADR row 8): CIO's batched hook and settings patches

**Owner: CIO. To write when a batch exists.** This one recurs. It is the item ADR-084 doesn't remove.

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
