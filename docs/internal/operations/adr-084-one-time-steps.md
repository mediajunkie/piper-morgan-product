# ADR-084: xian's one-time steps

**Status: APPROVED. xian said yes to ADR-084 on 2026-11-16 at 06:20 PT** (relayed by Exec, mail 01M7JBP51M). Each step still runs only when its own row says it is ready. Done so far: Step B (11-16, 06:23); Steps A, C, D and F0 (11-20), and F.1 (per Exec's rollup of 11-23; each step's own status line is the record). Written as a draft, asked for by Exec on 2026-11-15 (mail 01M7HF64B8…) so that his yes is followed by a paste, not a new round of mail.

**The sitting (updated 2026-11-17 18:36 PT).** xian is away from Amber until Friday 2026-11-20, and every Terminal step here has to run on Amber (Exec's relay of Docs, mail 01M7P7NMPD). One sitting, in this order, each ready as written below: **Step A, Step C, Step D, Step F0.** No seat stands by before he starts.

- He starts when he chooses. Step A's command prints `WAITING FOR READ TESTS on seat lead` and waits as long as needed.
- He (or Docs) gives Exec that line. Exec mails "Step A started". From that mail until Exec's "done" or "stopped", no seat runs `scripts/sync-pm-local.sh`, Lead finishes the tool call in hand, goes idle and says "ready", and Exec mails "go" for the three Reads (Exec, 2026-11-17 18:02: the hold starts at his line, not before).
- Steps C and D are pastes with no wait. After Step D, CIO switches the browser tool to the launcher and Web runs its checks. Step F0 is Lead's (done 2026-11-20 18:36 PT).
- Before Friday a seat fast-forwards his checkout (`scripts/sync-pm-local.sh`), so every script named here is the one on main.

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

**Owner: CIO (written 2026-11-15). Status: DONE 2026-11-20** (Exec's log: started `11:12`; Lead 01M7X6RV7Z, `check-env` passes; CIO removed the made-up file the same day). Previously ready: the tool was tested on dummy values and the first real use was the test. Unblocks arm B the same hour (its $8 stop is in code). The #2364 gate runs the same hour only if #2383 (the live-call cap) has landed; if it hasn't, Lead sends Exec the planned-calls line first (26 calls, $0.20 to $0.35), as ADR-084 D2 requires for a run with no in-code stop (Lead, 11-15 22:07).

What the ADR requires of this row (D2): the seat's own `.claude/settings.local.json` in the lead worktree, an `env` entry named `PIPER_SEAT_ANTHROPIC_KEY`, file mode 0600, a Read deny on that file in the same settings, and a check script that prints key names only. `scripts/seat_settings_grant.py` does all of that in one command.

The one question this depended on is answered (xian, 2026-11-16 06:20, relayed by Exec): "Nothing I run personally uses that key, no". He disabled the older `lead-scoring-2026-10` key the same day, so `lead-scoring` is the seat workspace.

- **Before you start:** you need the key's value. A provider shows a key once, when it is made. If you no longer have the value of `seat-screens-2026-11`, make a new key in the seat workspace on the Anthropic console and revoke the old one there.
- **When:** any time; Lead goes idle at the command's waiting line, not before (see "The sitting" at the top). Claude Code writes this same file itself when a permission is saved from a prompt, and whether a running session can write it back without the new entry is untested (Arch, 11-15). If that happened between the command's first parts and the wait, a Read test would come back "not refused" and the command stops before the key, so the failure is a safe one. The key itself is written only after Lead is idle.
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

**Owner: CIO. Status: DONE 2026-11-20 (Exec's log, `11:22`: three `added 1 allow rule for seat web` lines on xian's screen). First real run by Web the same day: `session saved, expires 2026-11-21T21:26:11Z` and `placed in seat browser web`, name and expiry only (Web's 11-20 log); Web has re-run it before each signed-in read since. Not yet run: the floored-actions read in the seat check below (no exact allow covers it). Previously READY (2026-11-16): `scripts/seat_session.py` and its exception rows are on main (issue 2388). Lead reviewed the routes, HOST read the helper at ff8b9d51b7 and the exception rows at 12c42ff864 and said land, Arch validated against D3. Web holds the allow first (HOST). The first real run is the test: 0 of 1 so far.** Two things can still make that first run print `refused:`, and neither needs anything more from xian: the key names inside the credential file are unknown to every seat (the refusal names which expected name is missing), and what beta shows for this account today is unread. Its client is `scripts/seat_read.py`, which does one GET from the saved session and needs no grant of its own: each run goes to the classifier, because its path argument differs every time.

What the ADR requires (D3): one exact-command allow per seeded account name, added by xian to the settings of each seat that does served reads. The helper prints the account name and the session's expiry only.

The step (CIO, 2026-11-16):

- **Where:** Terminal, in a checkout at main, as in Step A.
- **Paste:** one line per account name, per seat (Web first):

```
scripts/seat_settings_grant.py add-allow --seat web --rule 'Bash(scripts/seat_session.py --account web-seed-1386)'
scripts/seat_settings_grant.py add-allow --seat web --rule 'Bash(scripts/seat_read.py --account web-seed-1386 --redirect-uri github)'
scripts/seat_settings_grant.py add-allow --seat web --rule 'Bash(scripts/seat_read.py --account web-seed-1386 --redirect-uri calendar)'
```

  **Line 1 does two things once Step D is done** (Arch, 2026-11-16): it signs the account in and saves the session, and, in a seat that has a seat browser, it also places that session in the seat's browser. Until Step D there is no seat browser and it only saves the session. The browser itself is what xian approves in Step D.

  Lines 2 and 3 (added 2026-11-16) are the two fixed reads for issue 2282 step 5: each prints one line saying where that connector's sign-in returns to, so nobody has to start a sign-in in a browser to see it. Lead built them (9abd173fa8, fixed at 910eb6ab1d after CIO's read); HOST said land at 19:03 and Arch found them inside D3. They ride in this paste so they add no separate step.

  The rule must match the command the seat types, character for character. An exact allow covers only the bare command; anything chained onto it goes back to the classifier (traced 11-06). The seat types exactly `scripts/seat_session.py --account web-seed-1386` from the top of its worktree. The tool refuses any rule with `*` in it and never touches a deny.

- **You should see:** `added 1 allow rule for seat web` after each line, then the rule counts.
- **Seat check:** the seat runs the helper once. It prints one line, `web-seed-1386 session saved, expires <time>`, and nothing else. (Once Step D is done, in a seat with a seat browser it prints a second line, `web-seed-1386 placed in seat browser web, expires <time>`.) Then `scripts/seat_read.py --account web-seed-1386 /api/v1/admin/floored-actions` prints the counter's JSON (the bare path, as the allow below is written; 30 days is the route's default). Then `scripts/seat_read.py --account web-seed-1386 --redirect-uri github` and the same with `calendar` each print one line with the address the sign-in returns to and nothing else (run each once; don't loop them, each run leaves one unused sign-in state, in beta's Redis since 2345 (`009afa0f7f`, 11-24), which expires by itself after 15 minutes; Web sends the two printed lines to Lead, who puts them on issue 2282). If the helper prints `refused:` with a reason (for example, the account holds a provider key), nothing was saved: the seat reports the reason to HOST and Exec and does not retry.
- **DONE 2026-11-26, the counter read** (xian added the allow at Amber; Web ran it once, Web 01M8CK32RC: window 30 days since 2026-10-28, 5 rows; whole output on https://github.com/mediajunkie/piper-morgan-product/issues/2388#issuecomment-7200901561; row 4 waits on HOST's read). **Was owed (2026-11-24, HOST's call on #2388 row 4):** no allow covers `seat_read.py`'s counter read, so it has never run. One more line, for a card xian already has open (not a sitting of its own). HOST lifted the #2390 and #2391 ordering for this route (01M870QDFH, 11-24): `/api/v1/admin/floored-actions` is #2327's, already read, and `seat_read.ALLOWED_PATHS` holds that path alone. Those diffs still come to HOST before any other path joins the list.

```
scripts/seat_settings_grant.py add-allow --seat web --rule 'Bash(scripts/seat_read.py --account web-seed-1386 /api/v1/admin/floored-actions)'
```

  The path carries no `?days=30` on purpose: the route's default is 30 days (`web/api/routes/admin_ops.py`, `days: int = 30`), and a bare path needs no shell quotes, so the command Web types matches the rule character for character. Web then runs it once, alone, and quotes the JSON's `window` line on #2388.
- **DONE 2026-11-26, the third start for issue 2282 box 4** (xian added the allow; Web ran it once, Web 01M8CK32RC: `setup-calendar redirect_uri: https://beta.pipermorgan.ai/api/v1/setup/calendar/oauth/callback`, so it names beta and the alpha-callback card can be written). **Was owed (2026-11-24, Arch's ruling, mail 01M8728HYN):** the `/setup` calendar step is the one start not yet read; the github and calendar starts were read 11-20. Lead built `--redirect-uri setup-calendar` (`320f6c42d4`, the pin widened in `04421f0d0a`); Arch and HOST read it. One more line, for the same open card as the counter read (not a sitting of its own):

```
scripts/seat_settings_grant.py add-allow --seat web --rule 'Bash(scripts/seat_read.py --account web-seed-1386 --redirect-uri setup-calendar)'
```

  Web then runs it once, alone, and sends the printed line to Lead for issue 2282. It goes to HOST only if it names `alpha.`. It has no host-switch page, so a host-switch reply is refused, not printed.
- **If it fails:** if the classifier still refuses the helper's run, this route is dropped and the ADR's fallback applies (he signs in himself, rarely). Nobody works around the refusal.

## Step D (ADR row 10): load the seat browser's LaunchAgent

**Owner: CIO, with Pard. Issue 2400. Status: DONE 2026-11-20 (Exec's log, `13:21`; Pard, stamped `18:15`: xian's `--check web` printed `port 9333` and Pard's cycle-check arm passes: 127.0.0.1 only, 0700, mock keychain). Previously READY (2026-11-16 19:53), to be done after Step C: CIO's half is on main, validated by Arch and read by HOST; Pard's plist and wrapper are built and read by HOST** against D3's debug-port bound (127.0.0.1 only, a dedicated profile folder at mode 0700, no wildcard origins, the port read from one place, never xian's own Chrome).

What is on main (CIO, 2026-11-16), none of it in use until this step is done:

- `scripts/seat-browser.conf`: the one place a seat browser's port is written. One row today: `web 9333`. Adding a row is a diff HOST reads.
- `scripts/seat_browser.py`: places a saved session's access cookie into the seat's browser through the debug port. Before it sends anything it reads the process listening on the port and refuses unless that is one process, bound to 127.0.0.1 only, the cohort's test browser binary, started on `~/.piper-shared/seat-browser-credential-profile-<seat>` (mode 0700) with `--use-mock-keychain` and without `--remote-allow-origins`. It prints one line: the account, the seat and the expiry. `--where <seat>` prints the port and the folder for Pard's wrapper.
- `scripts/seat_session.py` calls it after saving a session, only in a seat that has a row. So Step C's exact-command allow covers it, and this step adds no allow. A seat with no row sees no change. If placing fails, the session stays saved, a fixed reason prints, and the exit code is 4.
- `scripts/seat-browser-mcp.sh`: the browser tool's launcher. A seat with a row is attached to its browser (`--browserUrl`) only when `seat_browser.py --check <seat>` passes, which is the same proof made before a cookie is placed (Arch's required change, 2026-11-16: an answering port is not proof of whose browser it is). Every other seat, and a seat whose browser is down or not provably its own, gets the throwaway signed-out browser `.mcp.json` starts today. A seat can't see the launcher's reason, so **a seat confirms the signed-in name on the page before any served read**. **`.mcp.json` calls it since 2026-11-20** (CIO, item 5 below); it takes effect at each seat's next session start.

Run so far (CIO, 2026-11-16 18:55 PT, a scratch test browser on a throwaway folder and port, a made-up cookie, nothing of beta's): placed and read back as httpOnly and secure; still held after a browser restart on the same folder; a browser on another folder on the same port was refused. 41 unit tests. **The Read deny covers files inside the profile folder** (CIO's seat, 2026-11-16 19:16 PT): a dummy folder named like a profile under `~/.piper-shared`, with one made-up file at the top and one a level down; the Read tool refused both ("File is in a directory that is denied by your permission settings"); the dummy was removed. Measured in 1 seat of 11. **Corrected 2026-11-22:** the line here said the others carry the same deny by `whats-armed`'s name check, but that check reads file names under `~/.piper-shared`, not each seat's denies. Web's seat, on its step 4 after the restart (09:20), read `Last Version` inside its own profile folder and was not refused; CIO's seat was refused on the same file. These denies lived in each seat's own git-ignored settings. Step I's 11-22 batch puts them in the shared file. Not run: a real session, a seat's live browser tool through the launcher, anything under the LaunchAgent.

**The browser must be started with `--use-mock-keychain`.** Without it the browser asks the macOS login keychain for a storage key the first time it keeps a cookie, which xian's 11-11 rule forbids. With it the cookies in the profile folder are kept under a fixed key, so the folder's mode 0700 and the Read deny on its name are the protection, as D3 already says of the profile. The helper refuses a browser started without the flag.

**What the seat browser may hold, and how it is revoked (HOST, 2026-11-16):**
- It holds a seeded account's session and nothing else. No other sign-in is typed into it, and no Connect round trip with a real provider account is done in it: either would leave a real session in a profile that keeps cookies across restarts. Web's steps carry the same line.
- To revoke, in this order: stop the browser, delete the profile folder, then delete the session file (`~/.piper-shared/web-seed-1386.session-token.json`). Deleting the folder alone is not enough while the browser runs, and while the session file exists the next `seat_session.py` run places the cookie again. The session also dies on its own: beta's access token lasts 30 minutes (Web measured it 2026-11-22 from `seat_session.py`'s printed expiry after Lead's `ddf40fd739`; the 24 hours once written here was the cookie's Max-Age, not the token's). A sitting longer than that re-runs the helper.
- Two residuals are stated in `seat_browser.py` and accepted by HOST and Arch: the debug port has no authentication, so any process of this user on Amber can reach it; and the listener is read before the socket is opened.

The order of what it waits on:
1. ADR-084's yes. Done 2026-11-16 06:20.
2. HOST's read of the four files above. Done 2026-11-16 19:18 at 5cd39bb085 (the helper conforms), with Arch's required launcher change and the Read-deny test both done at 35b645aace.
3. (Done 2026-11-16 19:48, mediajunkie 360246b; not hand-tested.) Pard builds the plist, the wrapper and a cycle-check arm (the debug port answers, the profile folder exists at mode 0700), and tests the wrapper by hand. The wrapper takes the port and folder from `scripts/seat_browser.py --where web`.
4. HOST reads both against the bound above. Done 2026-11-16 19:53.
5. CIO switches `.mcp.json` to the launcher and checks it in CIO's own session first (a seat with no row). **Done 2026-11-20, checked by 13:33:** `claude mcp list` from the CIO worktree reads `chrome-devtools: bash scripts/seat-browser-mcp.sh - ✔ Connected`; the launcher's `--print` for CIO is the earlier throwaway command, unchanged, and for Web it is `--browserUrl http://127.0.0.1:9333`; an MCP handshake through it answered with 30 tools. Web's own check (the signed-in name on a beta page, the dummy-file Read refused) follows Web's session restart.

- **Built (Pard, 2026-11-16 19:48, mediajunkie 360246b):** the wrapper `scripts/seat-browser-run.sh`, the plist `docs/launchagents/com.xian.seat-browser-web.plist` and a `seat-browser` arm in cycle-check. CIO read the wrapper and plist at 19:53: the command line it produces is the one `seat_browser.py --check` requires. **HOST read all three at 19:53 (v4 01M7KT7BBD): conforms; nothing holds this step from HOST once Step C is done.**
- **It depends on xian's own checkout:** the wrapper and line 2 run `scripts/seat_browser.py` from `~/Development/piper-morgan-product`. That file is there since CIO's sync at 19:53 (main d417ecaab2). If that checkout is ever on a commit without it, the browser does not start and the log says why.
- **Not hand-tested:** auto mode refused Pard the hand run, and he did not work around it. So line 2 below is the first real run, under launchd.
- **Where:** Terminal, anywhere.
- **Paste** (two lines, copied from Pard's memo by script, not retyped):

```
cp ~/Development/mediajunkie/docs/launchagents/com.xian.seat-browser-web.plist ~/Library/LaunchAgents/ && launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.xian.seat-browser-web.plist
sleep 5; python3 ~/Development/piper-morgan-product/scripts/seat_browser.py --check web
```

- **You should see:** the second line prints `port 9333`. If it prints `refused:` with a reason, the browser's own log is `~/Library/Logs/seat-browser-web.log`; tell Exec the reason. After the load Pard's cycle-check arm goes to its full assertion.
- **To undo** (stop first, then delete the profile; then delete the session file named above, HOST's order):

```
launchctl bootout gui/$(id -u)/com.xian.seat-browser-web && ~/Development/mediajunkie/scripts/seat-browser-run.sh --revoke web
```

- **Since 2026-11-17, two guards watch for a browser without the fake-keychain flag** (xian: "ensure it doesn't recur"): a Bash hook refuses such a launch in a seat, and every seat's fire runs `scripts/browser_keychain_check.py`. Neither touches this step: launchd starts the seat browser, and Pard's wrapper passes the flag, so the check reads it as fine. If the check ever names the seat browser, the wrapper has lost the flag: tell Pard and HOST.
- **D6:** this is a one-time load. launchd keeps the browser up and restarts it after a crash or a reboot, so nothing recurs for xian. The standing access that would remove even this step is a seat being able to load a LaunchAgent, which auto mode refuses and ADR-084 leaves with xian.
- **Seat check (Web, after the paste):** run `scripts/seat_session.py --account web-seed-1386` and expect its second line; open a beta page and quote the signed-in name, once after a browser restart and once after a promotion; and try one Read of a dummy file inside the profile folder in Web's own session, which should be refused (HOST, 2026-11-16: the second measurement of that deny, after CIO's seat).
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

**Owner: Lead.** **Status: DONE 2026-11-20 18:36 PT** (Lead 01M7XZCRV7: `seat-github-1 created`, exit 0, the bare command). Two things it hit, both fixed: the script was committed without its execute bit (Lead set 100755 at 18:33, blob unchanged; `tests/unit/scripts/test_allow_named_scripts_executable.py` now fails on any allow-named script that isn't executable), and a first try inside a compound line was refused before anything ran. **An exact allow matches only the command run alone:** don't chain it after `date`, `git` or anything else. Previously READY (2026-11-16, CIO's edit on Lead's three conditions). `scripts/seat_account_create.py` is on main (issue 2389). The three things it waited on are done: HOST read the script whole at 72afafe37c against the five conditions below and said they are met; `seat-github-1` is on the account list in `scripts/seat_session.py` (dd97e4ba56, a diff HOST read); and the exact-command allow is written below, in the same batch as Step C's. A real creation is 0 of 1: the first run is the test.

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
4. *(waits on the beta account)* **Connect.** In a private (incognito) window of your own browser, closed afterwards, and never the seat browser: Step D keeps any Connect round trip with a real provider account out of it (corrected 2026-11-26, Exec 01M8CN1EJZ, CIO). Check the window is private before you type anything. Sign in to beta as the **second seat account** (you type its password at beta's login page). Settings, Integrations, GitHub card, press Connect. GitHub asks you to sign in: sign in as the **machine account**, through its own Google sign-in (it has no GitHub password or authenticator entry, Exec's F.2 read, 2026-11-26). On GitHub's authorize page, read the App name and the permissions list before pressing Authorize; it should be the one Piper App (client ID `Iv23…tj64`).
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
  `<seat-account-email>` is the GitHub-connected seat account's email address. It isn't a secret. **Take it from beta's /account page while signed in as that account (or HOST's custody row), never from `~/.piper-shared/seat-github-1-credentials.txt`:** that file holds only `username:` and `password:` lines, and on 11-26 its password line went into this command by mistake (refused, nothing written). The address has an `@`; if what you're about to paste has none, stop.
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
    - **Result, 2026-11-26 `12:11`: refused.** claude.ai said "A connector with this URL already exists in your organization. Use the existing connector instead of adding it again." Nothing was added.
    - **Arch's fallback order (`01M8CR7F1S…`, superseding `01M8CQYRW4…` and `01M8CR4GRE…`): (a) once, then (c) on xian's yes, then (b), then (d).**
  - **403 on the consent page:** part 1 didn't stick. Run `fly ssh console -a piper-morgan -C "python /app/scripts/mcp_allow.py list"` and check the seat account is listed.
  - **The consent lands on your own account** (PA's profile read names you): remove only **Piper Morgan (seat)**, sign out of Piper, and repeat part 2.

**Part 2 (a): the same URL with a query string, tried once** (Arch `01M8CR7F1S…`, 2026-11-26; PA wrote this)

The seat's token stays inside claude.ai, so no keychain question comes up.

- **Paste:** in claude.ai, Settings, Connectors, **Add custom connector**: name `Piper Morgan (seat)`, URL `https://mcp.pipermorgan.ai/mcp?client=seat`. Same host and path; nothing changes on the server.
- **Then:** exactly part 2's Then line. Sign in on Piper's page as seat-github-1, in a private window or the separate profile, signed out of Piper as yourself, and press Allow.
- **It passes only if all three hold:** the consent page is Piper's own; PA's `piper://me/profile` through the new connector names seat-github-1; your own **Piper Morgan** connector still answers as you. Then PA's seat check as written, and part 3 as written.
- **On any failure** (claude.ai refuses it, the connect errors, or the profile names you): remove **Piper Morgan (seat)** in claude.ai at once, so no half-working connector stays in your org, and go to (c) on your yes.
- **Unverified:** whether claude.ai's duplicate check treats a query string as a different URL, and whether the server's `/mcp` route and its OAuth flow accept one. `oauth_provider.py` stores the resource per grant (line 466); PA found no exact-match check on it.

**Part 2 (c): Claude Code as the client, only if (a) fails** (ruled 2026-11-26 by Arch; PA wrote this)

What parts 2 and 3 prove is server-side: the hosted MCP answers as the account that consented, and an allowlist removal cuts off a live connection. Any OAuth MCP client runs the same server code, and xian's own connector already proves the claude.ai path.

- **Precondition, before anything below: xian's yes, on his card.** Claude Code's credential store on Amber is his login keychain, in the entry keyed to `CLAUDE_CONFIG_DIR=~/.claude-pm`, which every seat's Claude Code shares. If the keychain refuses the write, it falls back to `~/.claude-pm/.credentials.json` (CIO `01M8CR2H4D…`, from the Claude Code authentication and troubleshoot-install docs; the docs don't name where an MCP token goes). The question as worded: "May PA's session store one OAuth token for `piper-seat` (seat-github-1's) in your Claude Code credential store, removed at the Ending with logout and remove?" **Without his yes, skip to (b).**
- **PA adds the server** in its own worktree: `claude mcp add --transport http --scope local piper-seat https://mcp.pipermorgan.ai/mcp`. Then PA asks Exec for a session restart (Pard), so the session loads the server.
- **The sign-in.** Someone at Amber's keyboard starts the OAuth sign-in, either from `/mcp` in PA's session or with `claude mcp login piper-seat` from the shell. The docs say `claude -p` and SDK runs can't start it. Its page opens in a browser on Amber. **xian** signs in there as seat-github-1, in a private window or the separate profile, signed out of Piper as himself, and presses Allow. His own claude.ai connector stays untouched. **Unverified:** which browser the sign-in opens and whether PA can start it without the `/mcp` menu; the callback goes to localhost on Amber, which the server accepts (`oauth_provider.py`, http-on-localhost redirect URIs).
- **Seat check (PA):** part 2's seat check unchanged, read through `piper-seat`: the profile names the seat account; the GitHub issues and their repositories (pipermorgan/piper-test and piper-test-2 each have one open issue, so the read also shows whether the 11-12 install covers piper-test only); `uptime_seconds`; one read of xian's own connector. Part 3 runs as written, reading through `piper-seat`.
- **(b), only if xian says no to (c):** consent through another claude.ai organization or account, if xian has one and HOST agrees. His hand, and a custody question for HOST. **HOST's custody view (`01M8CQYARB…`): refuse it.** It means a real second Claude account for the machine seat, with its own sign-in, recovery email and custody that nobody has agreed to hold. So on a no to (c), expect (d).
- **(d), only if (b) fails too:** part 2 and part 3 are recorded as not reachable. That loses #2242's live-removal proof.

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

**Ending** (with HOST's review date): remove **Piper Morgan (seat)** in claude.ai, or on route (c), in PA's session: `claude mcp logout piper-seat`, then `claude mcp remove piper-seat` (remove alone leaves the token valid at the server until it expires; Arch `01M8CR3ND1…`). Then `mcp_allow.py remove --user-email <seat-account-email> --apply` the same way as part 1 (the script takes `--user-email` or `--user-id`).

## Step H (ADR row 7): the MCP deploy token

**Owner: HOST.** **Two actions that cannot merge: one Terminal line, then GitHub's own page.** **Status: READY (CIO, 2026-11-24).** #2384's job is on main as `8ac5c8e267` (Lead; the diff Arch read against D6 and HOST read for custody at `96affff6e6`, unchanged). It names the environment and secret below: environment `mcp`, secret `FLY_API_TOKEN_MCP`. On what the token can do: Lead's 11-16 note on #2384 quotes Fly's docs, a deploy token manages "a single app and its resources", so treat it as full control of `piper-morgan-mcp`. HOST's residual, stated so the bound isn't read as stronger than it is: the environment's branch limit stops a *branch* from reading the token, not a commit to main. That is the same exposure the existing `FLY_API_TOKEN` secrets carry (Arch: D6 as written). Until the token is stored the job skips with a notice and ends green, so nothing breaks before this step. The first real dispatch (Lead's, for #2382's MCP deploy) is the job's test; its result goes to HOST for the custody row. The address of the settings page is not given: fetched 11-24, it answers 404 to a client that isn't signed in, so the click path stands.

1. **Create the environment.** github.com/mediajunkie/piper-morgan-product, Settings, Environments, **New environment**, name `mcp`. Under **Deployment branches and tags** choose **Selected branches and tags**, add **main**. (This is what stops a branch pushed with an edited workflow from reading the secret.)
   - **You should see:** the environment page showing the branch rule "main".
2. **Create the token and copy it without showing it.** In Terminal, any folder:
   `fly tokens create deploy -a piper-morgan-mcp -x 8760h -n seat-mcp-deploy | pbcopy`
   *(Line read against Fly's docs by Lead 11-15 22:24: `-a` app, `-x` expiry as a duration, `-n` name; the default expiry is 20 years, so keep `-x`. 8760h is one year, HOST's suggestion (11-24) so this token and the restarter's renew in the same fortnight; the expiry and the name are yours to set. Not run by any seat. Fly's pages do not say whether a deploy token can run commands inside the app or set its secrets, so treat it as full control of `piper-morgan-mcp`: the workflow text on main and the `main`-only environment are the bound, not the token. If the command prints anything besides the token into the pipe, the stored value would be wrong, so after storing it look at the Actions run, not at the value.)* It must name the app `piper-morgan-mcp` and **no other app, never an organization-wide token.** The token goes to your clipboard and nothing prints.
3. **Store it.** On the environment page, **Add environment secret**, name `FLY_API_TOKEN_MCP`, paste, save. Put it on the `mcp` environment, **not** under the repository's secrets. Then clear the clipboard: `pbcopy < /dev/null`.
   - **You should see:** the secret's name listed, "Updated now". The value is never shown again.
4. **Tell Exec the date and the expiry** you chose (HOST's custody row takes both; no value).
5. **Seat check afterwards (names only):** `gh api repos/mediajunkie/piper-morgan-product/environments/mcp` shows the branch policy; the same path with `/secrets` lists secret names. HOST's condition before the token is used: `mcp` is limited to `main`, and no secret named `FLY_API_TOKEN_MCP` sits at repository level (HOST reads it, names only; if a seat's `gh` can't, xian reads the settings page to HOST). If the seat's access is refused, that is fine; Lead reads the first dispatch's output (sha and release only).

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

- **The baseline is empty, and stays empty.** `.staged-credential-scan-baseline.txt` held 61 lines on 2026-11-16, each a line the scan did not check. Lead rewrote those fixtures to build each value from parts (issue 2397, `b56aaf2764`), and CIO regenerated the file on 2026-11-17: 0 lines. So every tracked line outside the bearer lint's three folders is now checked. Nobody adds a line to the baseline; a test that needs a key-shaped value uses `tests/utils/made_up_credentials.py`. No seat opened the old values to judge them. They are still in git history; if anyone has a reason to think one was ever real, tell Exec and it is rotated.
- **A secret with no shape.** A seat account's password and the machine account's password are plain url-safe strings with no prefix; `staged_credential_scan.py` cannot match them. They are protected by the Read denies on the `*-credentials.txt` files and by never being typed into a file.

**Batch 2026-11-22: DONE 2026-11-26** (xian ran it at 10:17, `added 6 deny rule(s); 2 were already there`; refusals read by CIO at 10:22 and by Web at 10:27, with no restart; decisions.log CIO 11-26). Was: one patch, ready (HOST read and Arch approved, 11-22): the `~/.piper-shared` denies for every seat. `dev/active/cio-install-batch-2026-11-22.md`. It runs `seat_settings_grant.py fleet-deny`, which adds the six `~/.piper-shared` credential, token and secret denies to the shared settings file. It is additive and stricter only. D6: no standing access removes this step, since auto mode refuses Pard an edit to the shared settings (the recurring item above).

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
- **Still to write:** HOST's provider half of Step E. (Lead's Step F0 is written and READY since 2026-11-16; checked against the script on main 2026-11-17, nothing stale.) Steps C and D are READY since 2026-11-16 (`seat_session.py` and Pard's plist exist and are read); Step H stays NOT READY until #2384 exists.
- **Unproven until the first real install** (CIO lists them too): a real key, a live session picking up the variable, and whether Claude Code honours the Read deny as written.

## Not on this list, by design

A promotion that carries a migration, a change to the deploy path, and anything outside a bound stay decisions for xian. They are not chores this ADR removes.
