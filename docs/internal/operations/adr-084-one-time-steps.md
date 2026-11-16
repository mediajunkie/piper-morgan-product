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

**Owner: CIO (written 2026-11-15). Ready: the tool is tested on dummy values; the first real use is the test.** Unblocks arm B the same hour (its $8 stop is in code). The #2364 gate runs the same hour only if #2383 (the live-call cap) has landed; if it hasn't, Lead sends Exec the planned-calls line first (26 calls, $0.20 to $0.35), as ADR-084 D2 requires for a run with no in-code stop (Lead, 11-15 22:07).

What the ADR requires of this row (D2): the seat's own `.claude/settings.local.json` in the lead worktree, an `env` entry named `PIPER_SEAT_ANTHROPIC_KEY`, file mode 0600, a Read deny on that file in the same settings, and a check script that prints key names only. `scripts/seat_settings_grant.py` does all of that in one command.

Depends on xian's answer to one question: does anything he runs still use the older `lead-scoring-2026-10` key? If not, he revokes it and `lead-scoring` is the seat workspace. If so, the seat key needs its own workspace and a new key.

- **Before you start:** you need the key's value. A provider shows a key once, when it is made. If you no longer have the value of `seat-screens-2026-11`, make a new key in the seat workspace on the Anthropic console and revoke the old one there.
- **When:** while Lead's session is idle (not mid-fire). Claude Code writes this same file itself when a permission is saved from a prompt, and whether a running session can write it back without the new entry is untested (Arch, 11-15).
- **Where:** Terminal on this Mac, in any checkout that is at main. Your own is fine after its usual sync. The script finds the seat's settings by absolute path, so it doesn't need to run from a seat's folder, and nothing here changes a seat's folder.
- **Paste**, one line at a time:

```
cd ~/Development/piper-morgan-product && ls scripts/seat_settings_grant.py
```

  This should print `scripts/seat_settings_grant.py`. If it says "No such file or directory", that checkout is behind main: stop and tell Exec. A seat brings it up to date with `scripts/sync-pm-local.sh`, which never touches your uncommitted edits.

```
scripts/seat_settings_grant.py prepare --seat lead
```

  This puts the Read deny and the file mode in place with **no key in the file**. It prints `no key was added`. **Then wait for Lead's word** (Lead's order, 11-15): Lead tries to open that settings file with its Read tool and should be refused. If Lead's Read succeeds, stop here; nothing real was in the file, and CIO fixes the deny before any key goes in. If Lead's session needs a restart to pick up the deny, this is where it happens.

```
scripts/seat_settings_grant.py add-key --seat lead --name PIPER_SEAT_ANTHROPIC_KEY
```

  This third line asks `PIPER_SEAT_ANTHROPIC_KEY for seat lead (input hidden):`. Paste the key there and press Return. Nothing shows as you paste. The key is never part of a command.

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

  It should print the same length and the same 8 characters. Lead's first run is then the real test (arm B, or the #2364 gate on the condition above), with `ANTHROPIC_API_KEY="$PIPER_SEAT_ANTHROPIC_KEY"` after the `env -u` flags and `PIPER_CREDENTIAL_STORE=db`. At that run Lead confirms the child process saw the value (length and hash) and that no value reached any output.

- **If it fails:**
  - The script prints one line and changes nothing if the settings file isn't valid JSON, the value is empty or has a space in it, or the name isn't a `PIPER_SEAT_` name. Fix that and run the line again.
  - **If Lead's check says `UNSET in this session`:** the session started before the key was there. Restart the Lead session once. Whether a running session picks up a new settings variable is the one thing nobody has tested.
  - **After any restart of the Lead session, check the entry survived:** `scripts/seat_settings_grant.py show --seat lead` should still list `env: PIPER_SEAT_ANTHROPIC_KEY` with the same fingerprint, mode `0o600` and `self-deny present: True`. If the entry is gone, run the `add-key` line again and tell Exec, because that means the session rewrote the file.
  - If Lead's fingerprint differs from yours, the wrong value was pasted. Run the same line again; it replaces the value.
  - To take the key back out: `scripts/seat_settings_grant.py remove-key --seat lead --name PIPER_SEAT_ANTHROPIC_KEY`. Revoking it on the console ends every copy, including any in a backup.

- **Another seat later** (CIO, PA, Docs): the same line with that seat's name. A seat gets the key only when it names a run.
- **Tested how:** `tests/unit/scripts/test_seat_settings_grant.py`, 16 cases on a dummy value: the value never appears in any output, the file ends at mode 0600, existing rules are kept, a deny is never removed, a broken file is left alone, `check-env` and `add-allow` refuse anything but seat keys and exact `Bash(...)` rules. **Not tested:** a real key and a live session.
- **What the Read deny does and doesn't cover** (CIO's probe, 11-15 22:38, dummy files only):
  - A deny of the form `Read(**/name)` **is honoured inside the seat's own worktree.** With the fleet's existing `Read(**/.env)`, my Read of a dummy `.env` in my worktree was refused ("File is in a directory that is denied by your permission settings").
  - The same deny **did not stop a Read of a dummy `.env` outside the worktree.** So the deny this step adds keeps Lead's Read tool out of Lead's own settings file. It does not stop another seat's Read tool from opening that file by its full path. For that case the limits are the classifier and the key's cap, unless HOST and Arch want a second deny that names the path from the home folder, added to every seat (open question, mailed 11-15).

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

- **Where:** Terminal, in a checkout at main, as in Step A.
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

- **Provider half (HOST, written 2026-11-15 from OpenAI's spend-limits guide at developers.openai.com/api/docs/guides/spend-limits and a search result; I could not open OpenAI's help pages, so every menu name below is unverified until xian sees it):**
  1. On platform.openai.com make a **new project** just for seats, named for the seat budget (for example `seat-screens`). Do not reuse a project anything of yours runs on: the limit must be the seat budget and nothing else may spend in it.
  2. In that project's **Limits** (spend) settings set the **monthly spend limit to the seat budget** and **turn on "Enforce a hard limit"**. The guide says a spend *alert* only notifies and traffic continues, while a *hard limit* makes requests return `429`. **Look at the page and confirm the hard-limit switch exists and is on.** Community posts say project limits were once notification-only. If you cannot find the hard-limit switch, stop and tell Exec: then the cap is not a bound. The fallback bound is the account's **prepaid credit balance with auto-recharge off**, funded only to the seat budget (check your billing page shows prepaid credits).
  3. In the project's **API keys**, create one key. If the dialog offers **Restricted** permissions, restrict it to what the screens call (chat/responses and batch endpoints); if you cannot tell which, leave the default, since the project limit is the bound, not the key's scope.
  4. The key is shown **once**. Copy it only into the hidden prompt in the next step (never into a chat, mail, note or file).
  - **You should see:** the project's Limits page showing the monthly figure and the hard-limit setting on; the API keys list showing one key in that project.
  - **Custody row records** (no value): provider, project name, monthly limit and whether enforced, date created, seats holding it, review date a month out.
  - **If you cannot find the hard-limit switch, or the project cannot be capped:** do not create the key. Tell Exec; the OpenAI half of #2364 waits.
- **Where (settings half):** Terminal, in a checkout at main, as in Step A, and while Lead's session is idle.
- **Paste:**

```
scripts/seat_settings_grant.py add-key --seat lead --name PIPER_SEAT_OPENAI_KEY
```

  The key goes in at the hidden prompt, as in Step A.

- **You should see:** the same lines as Step A, with this name.
- **Seat check (Lead):** `scripts/seat_settings_grant.py check-env --name PIPER_SEAT_OPENAI_KEY`. A run names it as `OPENAI_API_KEY="$PIPER_SEAT_OPENAI_KEY"`.
- **If it fails:** as Step A.

## Step F0 (before Step F's connect): create the second seat account on beta

**Owner: Lead.** **Status: NOT READY.** It waits on one small script, `scripts/seat_account_create.py` (not built; Lead builds it after xian's yes, HOST reads it against the list below). Written by Lead on 11-15 from the record, not from memory.

**How `web-seed-1386` was actually made (the record, 2026-10-20 omnibus, 18:44 to 18:49):** xian minted beta invite codes himself and stored them in files; Web then signed the account up through beta's own setup page in its browser, with one of those codes, and wrote the account's file under `~/.piper-shared`. No seed command and no database insert. Lead did not create it. Not verified by Lead: which command xian used to mint (the repo's `scripts/mint_prod_invite.sh` is the one written for it), and what Web's session read to do it. That path can't be repeated as it was: a seat now reads neither an invite file nor a password file, which is the rule ADR-084 keeps.

**The path for the second account, once the script exists** (the sign-up route is the same one a tester uses, `POST /api/v1/setup/create-user`: username, email, password twice, invite code):

- **Where:** Terminal, in `~/Development/piper-morgan-product`, on main.
- **Paste, two lines, one at a time.** The first mints one invite code on beta and prints it in your Terminal only:

  ```
  scripts/mint_prod_invite.sh --apply
  ```

  (Without `--apply` it is a dry run that mints nothing. With it, it mints exactly one.)

  The second creates the account. It asks for the invite code at a hidden prompt (paste the code from the line above), makes a password itself, signs the account up on beta, and writes the account's file:

  ```
  scripts/seat_account_create.py --account <second-seat-account-name>
  ```

- **You should see:** `created <second-seat-account-name> on beta`, the path of the account's file, `mode 0600`, and `password copied to the clipboard for Step F; it clears in 60 seconds`. No password, no invite code and no cookie on screen.
- **Seat check (HOST, from xian's screen or the atlas, until `seat_session.py` exists):** the account's own Account page shows no admin marking, no provider key and no connected service. Lead's check from source: the script's fixed list holds this account name and no other new one.
- **If it fails:**
  - `invite code not accepted`: the code was already spent or mistyped. Mint one more and run the second line again. Nothing was created.
  - `that username or email is taken`: nothing was created; tell Exec, and Lead picks another name in the script's list.
  - anything else: stop and tell Exec. An account that was created but whose file wasn't written is unusable by design; it gets a password reset, never a guess.

**What the script will hold (for HOST's read when it is built):** a fixed list of allowed account names and one fixed host in code; the invite code only from a hidden prompt, never an argument or the environment; the password from the operating system's random source, written only to the file and the clipboard; output limited to the lines above; a test that searches its output for the password and the code on a forced failure; it refuses to run without a terminal.

**Unverified until the script is built and run once:** that `mint_prod_invite.sh --apply` still mints and prints one code on beta as it stands today (its header says so; Lead has not run it, since it runs inside the production app), and the email address the account takes (it must be one xian controls, since password reset goes there; xian's to name).

What the row must hold, whatever the path:
- The account is created on beta by xian's hand (a sign-up with an invite code he mints, or a seed command he runs). An invite code is spent at account creation, so it is one mint for this one account.
- Its password is generated, used nowhere else, and written straight into the account's file under `~/.piper-shared` (a name the existing Read denies match, mode 0600) by the same step that creates the account. xian types it at beta's login page in Step F; no seat reads it. `seat_session.py` (Step C) reads it later.
- No admin flag, no `ops_reader`, no provider key of a real person.
- HOST reads what the account holds from its account page before first use (HOST's bound B4).

## Step F (ADR row 4): the test GitHub identity

**Owner: HOST.** **Status: PARTLY NOT READY.** The "connects it on the second seat account" part needs that beta account to exist. The ADR does not say who creates it (Lead's seed script, or Web). Arch named the owner on 11-15: Lead writes it as Step F0, above. Until that account exists, steps 1 to 3 can be done; steps 4 to 7 wait.

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
   `fly tokens create deploy -a piper-morgan-mcp -x 2160h -n seat-mcp-deploy | pbcopy`
   *(Line read against Fly's docs by Lead 11-15 22:24: `-a` app, `-x` expiry as a duration, `-n` name; the default expiry is 20 years, so keep `-x`. 2160h is 90 days and the name is a suggestion, yours to set. Not run by any seat. Fly's pages do not say whether a deploy token can run commands inside the app or set its secrets, so treat it as full control of `piper-morgan-mcp`: the workflow text on main and the `main`-only environment are the bound, not the token. If the command prints anything besides the token into the pipe, the stored value would be wrong, so after storing it look at the Actions run, not at the value.)* It must name the app `piper-morgan-mcp` and **no other app, never an organization-wide token.** The token goes to your clipboard and nothing prints.
3. **Store it.** On the environment page, **Add environment secret**, name `<secret-name from #2384>`, paste, save. Then clear the clipboard: `pbcopy < /dev/null`.
   - **You should see:** the secret's name listed, "Updated now". The value is never shown again.
4. **Tell Exec the date and the expiry** you chose (HOST's custody row takes both; no value).
5. **Seat check afterwards (names only):** `gh api repos/mediajunkie/piper-morgan-product/environments/<environment-name>` shows the branch policy; the same path with `/secrets` lists secret names. If the seat's access is refused, that is fine; Lead reads the first dispatch's output (sha and release only).

**If it fails or looks wrong:**
- `fly tokens create` offers or defaults to a wider scope: stop and tell Exec; do not store it.
- Undo: delete the secret and the environment on GitHub; in Terminal `fly tokens list -a piper-morgan-mcp` and revoke the token's entry (Lead gives the exact revoke line).
- Token seen anywhere in clear (a session, a log, a mail): revoke the same day and create a new one.

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

## Arch's read of the whole file (2026-11-15 22:22)

Read in full: Steps A to J and `scripts/seat_settings_grant.py` (193 lines). Steps F, G, H and I match ADR-084 with no change asked. The findings below are on Step A and the tool; CIO owns both.

**Two changes to the tool before it goes on xian's card (asked of CIO):**

1. **`check-env` must accept only `PIPER_SEAT_` names.** Today it takes any name, so `check-env --name ANTHROPIC_API_KEY` (or any other variable in a seat's session) prints that value's length and the first 8 characters of its hash. For a long random key that tells nobody anything. For a short or guessable value it is a way to test guesses, and it is a fingerprint of something that isn't a seat resource. `add-key` already refuses other names with `NAME_RE`; `check-env` should refuse them the same way, with a test.
2. **`add-allow` should accept only `Bash(...)` rules.** The ADR's grants are exact-command allows. Today the tool would also add an exact `Read(...)` or `Write(...)` rule. A deny would still beat an allowed Read, but a tool whose job is one kind of grant should refuse the others. Anything else stays a hand edit by xian.

**Two changes to Step A's text:**

3. **Where xian runs it.** The paste starts with `cd` into CIO's worktree and a `--ff-only` merge there. That touches a seat's working folder while its session may be running, and `--ff-only` fails if that branch has anything main doesn't. The script finds the seat's settings by absolute path, so it runs from any up-to-date checkout. Use his own checkout after its usual sync, or say what to do when the merge line refuses.
4. **Check that the entry survived.** Claude Code itself writes to `settings.local.json` (when a permission is saved from a prompt). Whether a running session can write the file back without the new entry is untested. So: add the key while the Lead session is idle, and after the session restart run `scripts/seat_settings_grant.py show --seat lead` once more. The `env` line and `self-deny present: True` should still be there.

**Read and found sound in the tool:** the value comes only from a hidden prompt and is never an argument; the write is a temp file at 0600 renamed into place, so a failure leaves the old file; nothing removes a deny; a wildcard rule is refused; a broken settings file is left alone.

**Other notes:**
- Step G part 1 and Step H use `fly` commands in xian's own Terminal. That is by design: production writes and Fly tokens stay his.
- Step F step 4 has xian type the second seat account's password at beta's login page, so Step F0 says where that password lives.
- **Still to write:** Lead's Step F0; HOST's provider half of Step E. Steps C, D and H stay NOT READY until `seat_session.py`, Pard's plist and #2384 exist.
- **Unproven until the first real install** (CIO lists them too): a real key, a live session picking up the variable, and whether Claude Code honours the Read deny as written.

## Not on this list, by design

A promotion that carries a migration, a change to the deploy path, and anything outside a bound stay decisions for xian. They are not chores this ADR removes.
