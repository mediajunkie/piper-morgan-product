# Lead standing items — FULL REWRITE 2026-11-24 (Tuesday)

The 08-31 version had gone stale again: on 11-24 an audit found twelve issues it named already closed, eight more closeable, and three asks never sent. **Rule for this file: at every START, open the source of each row (issue, mail, decisions.log) and check the next action is whose the row says, and that they were asked.** Check each part of a row separately; a part with no blocker can hide in a row that has one. This file cites no issue state: GitHub holds that.

## Mine now (no blocker)

- **2352 box 3 (Arch ruled 11-24):** `keys add` keeps its name and calls `local_key_setup.py`'s store path; no separate keychain write. Box 4 (the wizard reading keys from the environment) was not put to Arch. Placed in D, no sprint: ask PPM for a slot with 2399. — **Filed**: 2026-11-24

## Waiting on a named seat (each was asked; mail id given)

- **2431 (outage screens):** on main `f4a5baa9b6`, on beta since 11-24 12:30. Web's happy-path read passed (01M87M994Q); I read the sign-in form's failed branch on beta. Refusal states were rendered locally only. Rows are Arch's and CXO's to tick. — **Filed**: 2026-11-24
- **2433 (a non-admin opening an admin-only page by address gets raw JSON):** filed by me 11-24 from a render; low priority (the card shows to admins only). Placed by PPM (Production, plan section H, no sprint; a low-priority candidate in the sprint 3 draft, 01M87ZDT6V). Arch's shape: 2431's `refusal_page` at one call site, one constant (01M87ZCEAF). CXO's words (01M87ZZX8Q, correcting her earlier line): `This page needs an admin account.` and a `Back to Settings` link in place of "Try again"; all recorded on the issue. Waits on PPM's slot. — **Filed**: 2026-11-24
- **2434 (pages' own failure toasts say only `Failed to…` under the title `Error`):** filed by CXO 11-24 with fallback words for five of six toasts (low, UX, Production). She first ruled no sweep of pages' own copies of route lines (01M87ZCT6X), then at 18:31 said yes to a narrow one (01M888Q5GX): contradictions of fact only (a different limit, reason, or claim about what was changed), as one row in this issue, with 2432's two leftovers folded in (the 12 `Field` rules in route models; `PasswordChangeRequest`'s spaces-only validator). Both rows are on the issue. Waits on PPM's slot. — **Filed**: 2026-11-24
- **2264 box 2:** the measurable figure is on the issue (11-24: the change removed 2,119 files, 83.9 MB, from every build). Not ticked: image sizes cannot be produced and `.dockerignore` lists two `data/` folders, not all of `data/` (settle with 2244). Asked PPM on the issue whether the measurement is enough. — **Filed**: 2026-11-24
- **2429, 2430:** on main and on beta (`b2cda27b5d`, 11-24 11:25); rows are Arch's and CXO's to tick. — **Filed**: 2026-11-24
- **2345:** on beta `009afa0f7f`; 2 of 3 starts served-read by Web; the return half is xian's F.4 connect (roll back first if it fails); the wizard's start waits on the `setup-calendar` allow. — **Filed**: 2026-11-24
- **2388 row 2:** forced-failure output posted on the issue for HOST's read (asked in the issue comment and 01M871EC86). Row 4 waits on the counter-read allow on xian's card (CIO's steps line) and Web's run. — **Filed**: 2026-11-16
- **2390:** on main (`e43ebe55ab`). Open rows: the served read by a seat account (waits on an allow, which HOST says to add only when a seat has a reason). — **Filed**: 2026-11-24
- **2391:** rows 1 and 2 ticked (Arch's option A: no second counter). Row 3 ticks now that 2390 is on main; row 4 (amended) waits on the counter-read allow. — **Filed**: 2026-11-24
- **2282 box 4:** `seat_read.py --redirect-uri setup-calendar` is on main (`320f6c42d4`). Next: CIO writes the allow line, xian adds it on an open card, Web runs it once. `beta.` → xian's removal line; `alpha.` → a host-secret fix first. — **Filed**: 2026-11-24
- **2384:** job on main (`8ac5c8e267`); Step H READY (CIO). Waits on xian's token (card row 7: environment `mcp` limited to main, token as an environment secret), HOST's names-only read, then **my first dispatch deploys 2382** and PA reads its row 4 that hour. — **Filed**: 2026-11-24
- **2399 and 2244:** candidates in PPM's sprint 3 draft (11-25). 2399 builds to Arch's 11-24 split (`ask.armed`, new kind `ALREADY_IN_STATE`; send the consumer list of `success` with the diff). 2244: PPM wants the exact deploy-path question for xian (what the `fly.toml` mount changes; whether it needs a deploy outside the standing grant). **I owe PPM that question.** — **Filed**: 2026-11-24
- **2424:** built (`lead/2424-list-project-arg-r1123`, `ce244d7fca`), held on Arch's trigger (a main-arm router sample or served log line with `list_todos_query` and a `project` arg). Fresh rebase and full suite at landing. — **Filed**: 2026-11-23
- **2425, 2426:** PPM's sprint 3 slot and Arch's choice of lever. — **Filed**: 2026-11-23
- **2281:** owner Web, trigger Step F (PPM, 11-24). Nothing of mine. — **Filed**: 2026-11-24
- **2356 exclusion test (my half of 2354's served checks):** not on main; no order found. Raise with PPM in the sprint 3 draft. — **Filed**: 2026-11-24
- **2361, 2355 (my Tier 1 parts), 2219's stopgap removal, ADR-082 residual:** PPM's order or their named triggers. — **Filed**: 2026-11-13

## Waiting on xian (through Exec; each is on a card or Exec's held list)

- **seat-tester-1 sitting** (invite mint, console check, the `--save-key` and `--remove-key` allows): then `scripts/seat_account_create.py --account seat-tester-1` and `scripts/seat_session.py --account seat-tester-1 --save-key anthropic`, output line to HOST. Unblocks 2417, 2406's fresh-account row, 2411's last row. — **Filed**: 2026-11-22
- **Step E (OpenAI key):** unblocks 2412, 2297's list-name row, 2364 step 1's merge. — **Filed**: 2026-11-15
- **Step F (seat-github-1 connected through sign-in):** unblocks 2423, 2379's served rows, 2266's last box, 2401, 2402, 2281. HOST's sitting. — **Filed**: 2026-11-16
- **2157 restore drill:** xian's sitting with HOST; then 2158 for proof 3. 2158's first step (does the Fly org have object storage) has had no answer since 11-12; raise through Exec when 2158 is slotted. — **Filed**: 2026-11-04
- **2264 box 3 (history rewrite):** on Exec's walk list. — **Filed**: 2026-11-03

## Rules kept (not work)

- **Before any served-path push:** CI's full-suite command and `scripts/check_fullsuite_backlog.py`, whole. Run the enforcement files and the ratchets locally before spending a full suite. — **Filed**: 2026-11-17
- **From a side worktree, run the type gate by hand before a push** (the hook prints UNCHECKED). — **Filed**: 2026-11-20
- **A local server start by a seat passes `--no-browser`** until the terminal-gate fix is on main. — **Filed**: 2026-11-11
- **A claim that "the person sees this line" is tested through the app's real handler or on a rendered page,** never by calling the route function (2428). — **Filed**: 2026-11-24
- **Never read `.env` or `settings.local.json` by any means.** — **Filed**: 2026-11-17
- **No force-push on any branch; a refused push goes up under a new branch name.** — **Filed**: 2026-11-23
- **Card-state file:** diff it at each promotion that touches the Integrations cards. — **Filed**: 2026-11-18
- **Slow checkout in the Tests full-suite job:** if it recurs, ask Docs for the check it offered. — **Filed**: 2026-11-16
