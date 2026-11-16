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

**Owner: CIO. To write.** Unblocks #2364's gate and arm B the same hour.

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

**Owner: HOST.** **Status: PARTLY NOT READY.** The "connects it on the second seat account" part needs that beta account to exist. The ADR does not say who creates it (Lead's seed script, or Web). Arch or Lead: name the owner and tell Exec. Until then, steps 1 to 3 can be done; steps 4 to 7 wait.

**Why a machine account:** GitHub's terms (Section B.3, read 11-15) allow one free machine account beside a personal account, and forbid a second personal one. A human must create it.

1. **Create the account.** At github.com/signup, in a browser window where you are NOT signed in to your own GitHub (a private window is enough). Username: `<machine-account-name>` (your choice; it will be public, so not your name or a tester's). Use an email address you control that is not your main one. Then turn on 2FA with an authenticator app; **keep the 2FA secret in your own password manager, nowhere a seat can read.** Put in the profile bio: "Machine account for Piper Morgan test automation." *(Recommended, not something GitHub's terms require as far as I read.)*
   - **You should see:** the new account's empty dashboard.
2. **Bound it in the org.** Signed in as yourself: github.com/organizations/pipermorgan/settings/member_privileges, set **Base permissions** to **No permission**. Then github.com/orgs/pipermorgan/people, **Invite member**, enter the machine account's username, role **Member** (never Owner). Accept the invitation while signed in as the machine account. Then Teams, create a team `seat-test`, add the machine account, and give the team access to the **test repositories only** (`piper-test` and the second private test repository). Nothing else.
   - **You should see:** the account listed under People as Member, and the team's Repositories tab listing only the test repositories.
   - Also check: the account is not a collaborator on `mediajunkie/piper-morgan-product` or any repository of yours (each repository's Settings, Collaborators).
   - **One thing I have not read:** whether this account counts as a paid seat. Look at github.com/organizations/pipermorgan/settings/billing and tell Exec what the seat count line shows.
3. **Do not install the App yet.** The order matters: connect first, install second, with PA's read in between (the "installed nowhere" line can be read once only before the first install).
4. *(waits on the beta account)* **Connect.** In the dedicated seat browser (only once row 10 has loaded it; before that, any browser window you sign in and out of) sign in to beta as the **second seat account** (you type its password at beta's login page). Settings, Integrations, GitHub card, press Connect. GitHub asks you to sign in: sign in as the **machine account** (you type its password and the 2FA code). On GitHub's authorize page, read the App name and the permissions list before pressing Authorize; it should be the one Piper App (client ID `Iv23…tj64`).
   - **You should see:** beta's GitHub page saying "✓ Connected with GitHub", no token form.
   - Tell Exec "connected, not installed". **Stop here until PA's zero-install read is done.**
5. **Install, after PA says go.** On beta's GitHub repositories section press "Install on GitHub". On GitHub choose the `pipermorgan` account, **Only select repositories**, pick `piper-test` only, Install.
   - **You should see:** beta's repository list showing `piper-test` and nothing else.
6. **Sign out of GitHub** in that browser (so the profile does not keep the machine account signed in).
7. **Seat checks afterwards (names and counts only):** Web reads the repository section as the seat account; PA reads the connector (expect only `piper-test` items); HOST reads what the account holds and records it.

**If it fails or looks wrong:**
- Authorize page shows another App name, extra permissions, or asks for access to all repositories: **do not press Authorize**; tell Exec.
- Undo, in this order: beta Disconnect button on the GitHub page (clears the stored token); GitHub, the machine account's Settings, Applications, revoke the App; remove the install on the `pipermorgan` org's Installed GitHub Apps; remove the machine account from the org.
- 2FA lost: GitHub's account recovery for the machine account only; nothing else of yours depends on it.

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

**Owner: HOST.** **Status: NOT READY.** Waits on **#2384** (the job and the secret's exact name) and on **Lead stating what a Fly deploy token for this app can do beyond deploying** (HOST runs no fly; I have not verified whether such a token can run commands inside the app, which would make it production-database reach). The names below are placeholders until #2384 fixes them.

1. **Create the environment.** github.com/mediajunkie/piper-morgan-product, Settings, Environments, **New environment**, name `<environment-name from #2384>`. Under **Deployment branches and tags** choose **Selected branches and tags**, add **main**. (This is what stops a branch pushed with an edited workflow from reading the secret.)
   - **You should see:** the environment page showing the branch rule "main".
2. **Create the token and copy it without showing it.** In Terminal, any folder:
   `fly tokens create deploy -a piper-morgan-mcp -x <lifetime> | pbcopy`
   *(exact command and expiry flag: Lead confirms before this goes on the card; HOST has not run it.)* It must name the app `piper-morgan-mcp` and **no other app, never an organization-wide token.** The token goes to your clipboard and nothing prints.
3. **Store it.** On the environment page, **Add environment secret**, name `<secret-name from #2384>`, paste, save. Then clear the clipboard: `pbcopy < /dev/null`.
   - **You should see:** the secret's name listed, "Updated now". The value is never shown again.
4. **Tell Exec the date and the expiry** you chose (HOST's custody row takes both; no value).
5. **Seat check afterwards (names only):** `gh api repos/mediajunkie/piper-morgan-product/environments/<environment-name>` shows the branch policy; the same path with `/secrets` lists secret names. If the seat's access is refused, that is fine; Lead reads the first dispatch's output (sha and release only).

**If it fails or looks wrong:**
- `fly tokens create` offers or defaults to a wider scope: stop and tell Exec; do not store it.
- Undo: delete the secret and the environment on GitHub; in Terminal `fly tokens list -a piper-morgan-mcp` and revoke the token's entry (Lead gives the exact revoke line).
- Token seen anywhere in clear (a session, a log, a mail): revoke the same day and create a new one.

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
