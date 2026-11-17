# ADR-084: xian's one-time steps

**Status: APPROVED. xian said yes to ADR-084 on 2026-11-16 at 06:20 PT** (relayed by Exec, mail 01M7JBP51M). Each step still runs only when its own row says it is ready. Done so far: Step B (06:23). Written as a draft, asked for by Exec on 2026-11-15 (mail 01M7HF64B8…) so that his yes is followed by a paste, not a new round of mail.

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
- **Paste**, one line (Exec's ask, 11-15: one command, not four):

```
cd ~/Development/piper-morgan-product && scripts/seat_settings_grant.py grant-key --seat lead --name PIPER_SEAT_ANTHROPIC_KEY
```

  If the shell says "no such file or directory", that checkout is behind main: stop and tell Exec. A seat brings it up to date with `scripts/sync-pm-local.sh`, which never touches your uncommitted edits.

  The command does four things in order and stops at the first failure:

  1. **Shared settings.** Adds two Read denies to the one settings file every PM seat shares (`~/.claude-pm/settings.json`): one for any seat's `settings.local.json`, one for any `.env` in the worktrees folder. It first keeps the file as it was at `~/.claude-pm/settings.json.before-fleet-deny` and prints the line that undoes the change. Why: a seat's own deny doesn't stop another seat's Read tool (CIO's probe, 11-15), and Arch and HOST ruled the gap closed by a rule.
  2. **Lead's settings.** Sets the file to mode 0600 and adds Lead's own Read deny, with **no key in the file**.
  3. **It waits.** It prints `WAITING FOR READ TESTS on seat lead`. Tell Exec that line is on your screen. Three Reads are then tried, all before any key exists (Lead's order, ruled by Arch and HOST):
     - Lead tries to open its own settings file with its Read tool;
     - HOST tries to open Lead's settings file by its full path;
     - HOST tries to open a made-up `.env` that CIO puts at the top of the CIO worktree for the test and removes afterwards. The lead folder's real `.env` is never the test file.

     Each must be refused. Exec tells you the result. The file holds only permission rules at that point, so a Read that succeeds shows nothing secret. If a seat needs a restart to pick up the new rules, that happens here while the command waits.
  4. **The key.** When Exec gives you the three results, type them in order, for example `refused refused refused`, and press Return (HOST, 11-15: all three, so nothing gets through on a bare Return). It then asks `PIPER_SEAT_ANTHROPIC_KEY for seat lead (input hidden):`. Paste the key there and press Return. Nothing shows as you paste. The key is never part of a command.

  **If any Read was not refused, type what Exec gave you, or just press Return.** Anything but three times `refused` stops it. You can also press Return to stop and run the same line again later, for example if a seat is asleep or needs a restart; the parts already done are skipped. The command stops before the key. The deny rules stay, since they only add protection. The key does not go in "because the cap is small" (HOST); CIO fixes the deny first and tells Arch and HOST what the result was.

  **Why it can't be shorter than this:** the pause exists because the three Reads happen in the seats' sessions, not in your Terminal (Arch). And the wait in the middle is the point. Testing the deny with the real key already behind it would make a failed test the leak (Lead, 11-15). So his hands are: one paste, three words, one key.

- **You should see:**

```
1 of 4. The shared settings file (every PM seat reads it).
   added 2 Read deny rule(s); 0 were already there.
   the file as it was is kept at: /Users/xian/.claude-pm/settings.json.before-fleet-deny
   to undo this step: mv '<that copy>' '<the shared file>'
2 of 4. Seat lead's own settings file.
   mode 0600; the seat's own Read deny is in place; no key is in the file.
3 of 4. Three Read tests, with no key anywhere. Tell Exec this line is on your screen:
   WAITING FOR READ TESTS on seat lead
   ...
4 of 4. The key.
   PIPER_SEAT_ANTHROPIC_KEY for seat lead (input hidden):
   stored PIPER_SEAT_ANTHROPIC_KEY: <N> chars, sha256 <8 characters>
Done. lead's check, after its next session start: scripts/seat_settings_grant.py check-env --name PIPER_SEAT_ANTHROPIC_KEY
...
mode: 0o600
env: PIPER_SEAT_ANTHROPIC_KEY: <N> chars, sha256 <8 characters>
self-deny present: True
```

  (Copied from a run on a dummy folder with a made-up key, 11-15; only the paths differ.)

  The 8 characters are a fingerprint, not the key. Tell Exec the length and the 8 characters, or leave them on screen.

- **Seat check (Lead):** it reads the session's environment only, no file:

```
scripts/seat_settings_grant.py check-env --name PIPER_SEAT_ANTHROPIC_KEY
```

  It should print the same length and the same 8 characters. Lead's first run is then the real test (arm B, or the #2364 gate on the condition above), with `ANTHROPIC_API_KEY="$PIPER_SEAT_ANTHROPIC_KEY"` after the `env -u` flags and `PIPER_CREDENTIAL_STORE=db`. At that run Lead confirms the child process saw the value (length and hash) and that no value reached any output.

- **If it fails:**
  - **If any seat's session misbehaves after part 1** (this is the first command of ours that rewrites the file every seat depends on): put the file back with the line the command printed, `mv ~/.claude-pm/settings.json.before-fleet-deny ~/.claude-pm/settings.json`, and tell Exec (Arch, 11-15).
  - The script prints one line and changes nothing if the settings file isn't valid JSON, the value is empty or has a space in it, or the name isn't a `PIPER_SEAT_` name. It also refuses to start outside a terminal, and it checks Lead's file is readable before it touches the shared one. Fix the cause and run the line again; the parts already done are skipped.
  - **If Lead's check says `UNSET in this session`:** the session started before the key was there. Restart the Lead session once. Whether a running session picks up a new settings variable is the one thing nobody has tested.
  - **After any restart of the Lead session, check the entry survived:** `scripts/seat_settings_grant.py show --seat lead` should still list `env: PIPER_SEAT_ANTHROPIC_KEY` with the same fingerprint, mode `0o600` and `self-deny present: True`. If the entry is gone, put the key back with `scripts/seat_settings_grant.py add-key --seat lead --name PIPER_SEAT_ANTHROPIC_KEY` (the key alone, at a hidden prompt; the denies are already in and tested) and tell Exec, because that means the session rewrote the file.
  - If Lead's fingerprint differs from yours, the wrong value was pasted. Replace it with that same `add-key` line.
  - To take the key back out: `scripts/seat_settings_grant.py remove-key --seat lead --name PIPER_SEAT_ANTHROPIC_KEY`. Revoking it on the console ends every copy, including any in a backup.

- **Another seat later** (CIO, PA, Docs): the same line with that seat's name. A seat gets the key only when it names a run.
- **Tested how:** `tests/unit/scripts/test_seat_settings_grant.py`, 29 cases on a dummy value: the value never appears in any output, the file ends at mode 0600, existing rules are kept, a deny is never removed, a broken file is left alone, `check-env` and `add-allow` refuse anything but seat keys and exact `Bash(...)` rules. **Not tested:** a real key and a live session.
- **What the Read deny does and doesn't cover** (CIO's probe, 11-15 22:38, dummy files only):
  - A deny of the form `Read(**/name)` **is honoured inside the seat's own worktree.** With the fleet's existing `Read(**/.env)`, my Read of a dummy `.env` in my worktree was refused ("File is in a directory that is denied by your permission settings").
  - The same deny **did not stop a Read of a dummy `.env` outside the worktree.** So the deny this step adds keeps Lead's Read tool out of Lead's own settings file. It does not stop another seat's Read tool from opening that file by its full path. For that case the limits are the classifier and the key's cap, which is why this step now adds a second deny that names the path from the home folder, in the settings file all seats share (`fleet-deny`, Arch's ruling 01M7HHQGFK). **That home-path form is untested** until the two Reads above.
  - **What a deny doesn't do:** it stops the Read tool. A file read by a command a seat runs is the classifier's to judge, and the key's cap is the limit if both fail. The deny alone does not close it.

## Step B (ADR row 6): tick "Operations reader" on the plain test account

**DONE 2026-11-16, about 06:23 PT, by xian.** The page read "Saved for web-seed-1386." with "Operations reader" ticked (Exec's relay of his screenshot, mail 01M7JBW6ED). The seat check below still waits on `seat_session.py` (issue 2388).

**Owner: Arch (written). HOST records it.**

- **Where:** beta, signed in as yourself (an admin): `https://beta.pipermorgan.ai/settings/account-flags`. It is also the "Account flags" card on the Settings page.
- **Paste:** nothing; this row is clicks on beta's own page, which no script of ours should make (the flag is set only by an admin's hand, by design). Type the test account's username, `web-seed-1386`, in the username box and load it. Tick **Operations reader**. Save.
- **You should see:** the page shows the account with "Operations reader" ticked after the save. If it says "No account has exactly that username. Nothing was changed.", the username was mistyped.
- **Seat check:** NOT READY. A seat can read the counter (`GET /api/v1/admin/floored-actions`, which returns names, sites, days and counts only) once it holds a session as that account, and that needs `seat_session.py` (Step C; its issue is placed on xian's yes). Until then the evidence is the page as you see it. HOST records account, date and set-by from the flag change's evidence line.
- **If it fails:** nothing else is changed by a failed save. Tell Exec what the page said.
- **Bound (for the record):** this flag is not admin and can't be set from chat or by an agent. It opens the closed list of count-only routes and nothing else.

## Step C (ADR row 5): the sign-in helper's exact-command allow

**Owner: CIO. READY (2026-11-16): `scripts/seat_session.py` and its exception rows are on main (issue 2388). Lead reviewed the routes, HOST read the helper at ff8b9d51b7 and the exception rows at 12c42ff864 and said land, Arch validated against D3. Web holds the allow first (HOST). The first real run is the test: 0 of 1 so far.** Two things can still make that first run print `refused:`, and neither needs anything more from xian: the key names inside the credential file are unknown to every seat (the refusal names which expected name is missing), and what beta shows for this account today is unread. Its client is `scripts/seat_read.py`, which does one GET from the saved session and needs no grant of its own: each run goes to the classifier, because its path argument differs every time.

What the ADR requires (D3): one exact-command allow per seeded account name, added by xian to the settings of each seat that does served reads. The helper prints the account name and the session's expiry only.

The step (CIO, 2026-11-16):

- **Where:** Terminal, in a checkout at main, as in Step A.
- **Paste:** one line per account name, per seat (Web first):

```
scripts/seat_settings_grant.py add-allow --seat web --rule 'Bash(scripts/seat_session.py --account web-seed-1386)'
```

  The rule must match the command the seat types, character for character. An exact allow covers only the bare command; anything chained onto it goes back to the classifier (traced 11-06). The seat types exactly `scripts/seat_session.py --account web-seed-1386` from the top of its worktree. The tool refuses any rule with `*` in it and never touches a deny.

- **You should see:** `added 1 allow rule for seat web`, then the rule counts.
- **Seat check:** the seat runs the helper once. It prints one line, `web-seed-1386 session saved, expires <time>`, and nothing else. Then `scripts/seat_read.py --account web-seed-1386 '/api/v1/admin/floored-actions?days=30'` prints the counter's JSON. If the helper prints `refused:` with a reason (for example, the account holds a provider key), nothing was saved: the seat reports the reason to HOST and Exec and does not retry.
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

- **Provider half is OpenAI's own pages, so it cannot be a command.** (HOST, written 2026-11-15 from OpenAI's spend-limits guide at developers.openai.com/api/docs/guides/spend-limits and a search result; I could not open OpenAI's help pages, so every menu name below is unverified until xian sees it):**
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

  One paste. This is the key alone: Step A has already put the denies in and tested them, so there is no wait here. Do Step A first.

  The key goes in at the hidden prompt, as in Step A.

- **You should see:** the same lines as Step A, with this name.
- **Seat check (Lead):** `scripts/seat_settings_grant.py check-env --name PIPER_SEAT_OPENAI_KEY`. A run names it as `OPENAI_API_KEY="$PIPER_SEAT_OPENAI_KEY"`.
- **If it fails:** as Step A.

## Step F0 (before Step F's connect): create the second seat account on beta

**Owner: Lead.** **Status: READY (2026-11-16, CIO's edit on Lead's three conditions).** `scripts/seat_account_create.py` is on main (issue 2389). The three things it waited on are done: HOST read the script whole at 72afafe37c against the five conditions below and said they are met; `seat-github-1` is on the account list in `scripts/seat_session.py` (dd97e4ba56, a diff HOST read); and the exact-command allow is written below, in the same batch as Step C's. A real creation is 0 of 1: the first run is the test.

**How `web-seed-1386` was actually made (the record, 2026-10-20 omnibus, 18:44 to 18:49):** xian minted beta invite codes himself and stored them in files; Web then signed the account up through beta's own setup page in its browser, with one of those codes, and wrote the account's file under `~/.piper-shared`. No seed command and no database insert. That path can't be repeated as it was: a seat now reads neither an invite file nor a password file, which is the rule ADR-084 keeps.

**The route (ruled 2026-11-16: HOST, CIO, Arch, PPM and Exec each said yes to it; the earlier one-command version, where the script minted the code itself, is dropped):** xian mints one invite code and leaves it, with the account's email, in a file a seat cannot read. A seat then runs the script. The sign-up call is the one a tester's browser makes, `POST /api/v1/setup/create-user`.

**xian's part, once, in a sitting he already has:**

- Mint one invite code on beta, as he does for a tester.
- **Where:** Terminal, in `~/Development/piper-morgan-product`, on main.
- **Paste, one line:**

  ```
  scripts/seat_account_create.py --account seat-github-1 --write-invite
  ```

  It asks for the invite code at a hidden prompt, then for the email address the account should have. Nothing typed is echoed, printed, or put on the command line. It writes `~/.piper-shared/seat-github-1-invite-token.txt` at mode 0600 and refuses to run without a terminal, so a seat cannot use it.
- **You should see:** `seat-github-1 invite file written`.
- **Paste, a second line, the allow for the seat's half** (same Terminal; CIO's batch with Step C's):

  ```
  scripts/seat_settings_grant.py add-allow --seat lead --rule 'Bash(scripts/seat_account_create.py --account seat-github-1)'
  ```

  **You should see:** `added 1 allow rule for seat lead`, then the rule counts. The allow covers that exact command only. `--write-invite` is in no allow, by HOST's bound: it is a Terminal-only step.
- **Standing access that removes this step from his hands:** the allow above is that access for the seat's half. Minting the code and naming the email stay his: an invite is his to give, and the address is one he controls.
- The email must be one xian controls, since a password reset goes there. It is his to name, and it appears nowhere in this repo or in mail.

**The seat's part (Lead, under the one exact-command allow):** `scripts/seat_account_create.py --account seat-github-1`. It prints `seat-github-1 created` or a fixed refusal reason, and nothing else.

**What the script does, and HOST's five conditions (mail of 2026-11-16 10:41):**

1. **One code, one account, one file.** It refuses an invite file that is missing, readable by others, or without both lines, naming which line is missing and nothing from the file. It deletes the invite file only after the host has answered that the account exists.
2. **A fixed account list and one fixed host, in code.** The list is `ACCOUNTS` in `scripts/seat_session.py`; there is no host option. It also refuses an account whose credential file already exists.
3. **No value is printed:** not the code, the email, the password, a response body or an error's own text. The password is generated in the process and goes only to `seat-github-1-credentials.txt` (mode 0600, lines `username:` and `password:`), which is written only after the account exists.
4. **The email never touches mail or this repo.**
5. **Custody row** (HOST's): account name, date, who minted, no values.

It sets no flag, stores no provider key and keeps no cookie from the reply.

**If it fails:**

- `the host refused the sign-up (400)`: the name or email is taken, or the code is wrong or used. Nothing was created and the invite file is kept. Tell Exec.
- `the host refused the sign-up (422)`: a field is not in a form the host accepts, most likely the email. Nothing was created; the invite file is kept.
- `the sign-up did not complete and the account does not sign in`: the host gave no readable answer. The script then tried to sign in with the password it had just made, and that failed too. The invite file is kept; the code may or may not be spent. Tell Exec before running it again.
- `the account was created but its credential file could not be written`: the code is spent and the account needs a password reset, never a guess.
- **One residual (Arch, 11-16):** if the sign-up succeeds but both its reply and the follow-up sign-in are lost, the account exists with a password nobody holds. The script reports the third line above. The remedy is xian's: a password reset or a delete. It takes two failures in a row.

**Standing access that removes the hand step (ADR-084 D6):** the exact-command allow. xian's remaining part is minting one code and the one line above.

**For Step F:** xian signs in as this account on beta to make the GitHub connect clicks. The password is in the account's file, which is his own file to open; no seat reads it.

**Unverified until the first real run:** that beta accepts the sign-up as written (the route and its fields are read from source; the 22 unit tests use a stand-in host), and that an account whose setup wizard was never finished reads cleanly through `seat_session.py`.

What the row must hold, whatever the path:
- The account is created on beta with an invite code xian mints. An invite code is spent at account creation, so it is one mint for this one account.
- Its password is generated, used nowhere else, and written straight into the account's file under `~/.piper-shared` (a name the existing Read denies match, mode 0600) by the same step that creates the account. xian types it at beta's login page in Step F; no seat reads it. `seat_session.py` (Step C) reads it later.
- No admin flag, no `ops_reader`, no provider key of a real person.
- HOST reads what the account holds from its account page before first use (HOST's bound B4).

## Step F (ADR row 4): the test GitHub identity

**Owner: HOST.** **Cannot be one command: these are GitHub and beta page clicks that no script may make (it is a person's account, 2FA and consent).** **Status: PARTLY NOT READY.** The "connects it on the second seat account" part needs that beta account to exist. The ADR does not say who creates it (Lead's seed script, or Web). Arch named the owner on 11-15: Lead writes it as Step F0, above. Until that account exists, steps 1 to 3 can be done; steps 4 to 7 wait.

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
- **You should see:** a `--- target:` line with the database address masked. The dry run ends `DRY-RUN complete — no writes.` The `--apply` run prints the `--- listed:` block twice, before and after the write; the second one includes the seat account. It ends `add: done for <seat-account-email> (…).`
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

**Part 3: the removal check for #2242** (added 2026-11-16 by PA on Exec's 18:2x ruling `01M7KN3SAN…`; replaces the old card that removed xian's own account; about 3 minutes, same Terminal as part 1)

This checks that removing an account from the allowlist cuts off a connector that's already connected, on the next call and not only at consent. The server checks the list in its token verifier as well as at consent and refresh (`services/mcp/server/allowlist.py`), so a removal should bite at once. It runs on the seat account, so your own connector is never touched.

**D6:** this is a one-time proof and stays your hand. No standing access is proposed, because the only thing that would end it is a seat writing production's allowlist (Arch, 11-16).

- **Order:** after part 2's seat check has passed. Wait for PA's word in between; each line below waits on the line before it.
- **Paste 1a (remove, dry run; it changes nothing):**
  ```
  fly ssh console -a piper-morgan -C "python /app/scripts/mcp_allow.py remove --user-email <seat-account-email>"
  ```
  **You should see:** a `--- user:` line, which **must show the seat account's address, not yours. If it shows yours, stop here** and tell Exec. Then `DRY-RUN complete — no writes.`
- **Paste 1b (remove):** the same line with `--apply` at the end:
  ```
  fly ssh console -a piper-morgan -C "python /app/scripts/mcp_allow.py remove --user-email <seat-account-email> --apply"
  ```
  **You should see:** two `--- listed:` blocks (before and after the write), the second **without** the seat account, and then `remove: done for <seat-account-email> (…).` Tell PA.
- **Seat check (PA):** one read through **Piper Morgan (seat)**. Expected: refused (the server returns no identity, so the connector reports an authorization error and no data). PA quotes the error text and MCP `uptime_seconds`, then reads your own **Piper Morgan** connector once, which must still answer as you. **FAIL** is any data returned through the seat connector after the removal. PA sends the result (refused or not, no data) to HOST for Step G's custody row.
- **On FAIL, stop here; don't run paste 2.** The seat account stays off the list. PA tells Exec and files the finding on #2242 the same hour, and you do the Ending's claude.ai removal of **Piper Morgan (seat)** then.
- **Paste 2 (add back, only on PASS):** part 1's `--apply` line again. If paste 2 is missed for any reason, the seat connector stays refused, not open, so a missed paste is never a risk. **You should see:** the second `--- listed:` block includes the seat account again, then `add: done for …`. Tell PA.
- **Seat check (PA):** one read through **Piper Morgan (seat)** answers as the seat account again. If it doesn't (the client may have dropped the connection after the 401), PA asks Exec whether to re-consent (part 2's Then line, about a minute). This is not a failure of the check.

**Ending** (with HOST's review date): remove **Piper Morgan (seat)** in claude.ai, then `mcp_allow.py remove --user-email <seat-account-email> --apply` the same way as part 1 (the script takes `--user-email` or `--user-id`).

## Step H (ADR row 7): the MCP deploy token

**Owner: HOST.** **Two actions that cannot merge: one Terminal line, then GitHub's own page.** **Status: NOT READY.** Waits on **#2384** (the job and the secret's exact name) and on **Lead stating what a Fly deploy token for this app can do beyond deploying** (HOST runs no fly; I have not verified whether such a token can run commands inside the app, which would make it production-database reach). The names below are placeholders until #2384 fixes them.

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

Both items that were queued on 11-15 are built (2026-11-16), and neither needed a step from xian:

- The pre-push hook's remembered pass is live: Pard installed it at 12:46 on 11-16 (recipe 5 in `canonical-ops-recipes.md`).
- The scan for credential shapes is `scripts/staged_credential_scan.py` (issue 2392). Its gate half (`--tracked`, in `lint.yml` and so in `scripts/run-push-gates.sh`) needs no install. Its commit half (`--staged`, called from `scripts/git-hooks/pre-commit`) is live: Pard installed the hook at 17:00 on 11-16, after HOST's read and Arch's validation, and it refused a probe commit at 17:07.

What the scan does not cover, so nobody reads it as covering more (HOST and Arch, 2026-11-16):

- **The 61 lines in `.staged-credential-scan-baseline.txt` are the known unchecked set.** A baselined line passes whatever value sits in it, at commit and in the gate. No seat has opened those values to judge them and none will. Issue 2397 rewrites them to build each value from parts, which empties the baseline.
- **A secret with no shape.** A seat account's password and the machine account's password are plain url-safe strings with no prefix; `staged_credential_scan.py` cannot match them. They are protected by the Read denies on the `*-credentials.txt` files and by never being typed into a file.

The form each batch takes, so a sitting is short (CIO, 2026-11-15):

- **Where:** one file, `dev/active/cio-install-batch-<date>.md`, with every patch in it.
- **Paste:** three lines per patch: run its test, apply the patch, run the test again.
- **You should see:** each test prints `N failed of M`, with the failures gone on the second run. Relay the two result lines; CIO commits only then.
- **Bound:** every patch is additive only. It never removes or loosens a deny and never widens an allow past one exact command (HOST's bound).
- **If it fails:** the batch file gives the one line that reverts that patch.

## Step J (cleanup): remove tonight's stored key and the lead folder's `.env`

**Owner: Arch (written). Do this only after Step A has served one real run.**

- **Where:** Terminal. The line changes into the lead folder itself, because the stored key and its `.env` live there. Run it while Lead's session is idle.
- **Paste, one line.** It stops at the first step that fails, so `.env` is deleted only after the key is removed and the list reads back:

```
cd ~/Development/piper-morgan-worktrees/lead && venv/bin/python scripts/local_key_setup.py --remove anthropic && venv/bin/python scripts/local_key_setup.py --list && rm .env
```

- **You should see:** `anthropic: removed` (or `anthropic: no stored key to remove` if it was already gone), then `stored: none`. Both wordings are read from the script's source. Nothing asks for or prints a key.
- **Why `.env` can go:** the setup script created it on 11-15 at 18:42 with three values (an encryption key, a sign-in secret and the store flag). Nothing else has used it. If you have put anything else in that file since, tell Exec before deleting it.
- **Seat check:** Lead re-runs the whole test tree once with tracebacks on and reports whether the six `test_slack_config.py` failures of 11-15 appear.
- **If it fails:** if `--remove` reports an error, leave `.env` in place (it is the only thing that can read the stored key) and tell Exec what it printed.
- **Also:** the older `lead-scoring-2026-10` key is revoked in the Anthropic console if Step A's question was answered "nothing uses it".

---

## Arch's read of the whole file (2026-11-15 22:22)

**Update, 22:40.** All four changes below are done by CIO (`70ad8ee81b`) and I checked each in the current files: `check-env` refuses a name that isn't `PIPER_SEAT_`; `add-allow` refuses anything but an exact `Bash(...)` rule; Step A runs from xian's own checkout; and the entry is re-checked with `show` after a restart. Steps F0 (Lead) and E's provider half (HOST) are written and read.

**One ruling added, on Lead's point (mail 22:28): test the Read deny before the real key is in the file.** If the deny pattern doesn't work as written, a Read of the file succeeds, and with the key already in it the test's failure is the leak. So the order in Step A is: (1) the deny goes into Lead's `settings.local.json` with no real key in the file; (2) Lead tries a Read of that file and logs "refused" or "not refused"; (3) only on "refused" does the real key go in. If it is not refused, nothing real was shown, and CIO fixes the pattern first. CIO chooses how the tool does step 1 (a made-up value under a `PIPER_SEAT_` test name that is removed afterwards, or a small command that writes the deny alone).

**On Step E (HOST's caveat):** if OpenAI's project limit turns out to notify without refusing, it is not a bound, and HOST's fallback (a prepaid balance with auto-recharge off, funded to the seat budget) is the bound. Without one of the two, the OpenAI half of #2364 waits. That matches ADR-084 D1 point 3.

**On Step H (Lead's read of Fly's docs):** a deploy token should be treated as full control of the MCP app, so the bound is the workflow text on main and the `main`-only environment, as D6 already says.

The original findings follow, for the record.

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
