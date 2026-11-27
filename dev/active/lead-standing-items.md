# Lead standing items — FULL REWRITE 2026-11-24 (Tuesday)

The 08-31 version had gone stale again: on 11-24 an audit found twelve issues it named already closed, eight more closeable, and three asks never sent. **Rule for this file: at every START, open the source of each row (issue, mail, decisions.log) and check the next action is whose the row says, and that they were asked.** Check each part of a row separately; a part with no blocker can hide in a row that has one. This file cites no issue state: GitHub holds that.

## Mine when slotted (checked 11-25 21:46: nothing here is unblocked)

- **2352 box 3 (Arch ruled 11-24):** `keys add` keeps its name and calls `local_key_setup.py`'s store path; no separate keychain write. Box 4 (the wizard reading keys from the environment) was not put to Arch. Placed in D, no sprint. PPM's sprint 3 draft (11-25) lists box 4 under Arch's rulings "if the local key commands are slotted"; the slot is xian's through that draft. — **Filed**: 2026-11-24

## Waiting on a named seat (each was asked; mail id given)

- **2431 (outage screens):** on main `f4a5baa9b6`, on beta since 11-24 12:30. Web's happy-path read passed (01M87M994Q); I read the sign-in form's failed branch on beta. Refusal states were rendered locally only. Rows are Arch's and CXO's to tick. — **Filed**: 2026-11-24
- **2264 box 2:** the measurable figure is on the issue (11-24: the change removed 2,119 files, 83.9 MB, from every build). Not ticked: image sizes cannot be produced and `.dockerignore` lists two `data/` folders, not all of `data/` (settle with 2244). Asked PPM on the issue whether the measurement is enough. — **Filed**: 2026-11-24
- **2429, 2430:** on main and on beta (`b2cda27b5d`, 11-24 11:25); rows are Arch's and CXO's to tick. — **Filed**: 2026-11-24
- **2345:** return half served 11-26 by xian's F.4 connect (Exec 01M8CNC062; on the issue). 2 of 3 starts served-read. Not served: Calendar's return half, the wizard's Calendar start. Boxes unticked: re-read what each needs and tick or name the gap. — **Filed**: 2026-11-24
- **2388 row 2:** forced-failure output posted on the issue for HOST's read (asked in the issue comment and 01M871EC86). Row 4 waits on the counter-read allow on xian's card (CIO's steps line) and Web's run. — **Filed**: 2026-11-16
- **2390:** on main (`e43ebe55ab`). Open rows: the served read by a seat account (waits on an allow, which HOST says to add only when a seat has a reason). — **Filed**: 2026-11-24
- **2391:** rows 1 and 2 ticked (Arch's option A: no second counter). Row 3 ticks now that 2390 is on main; row 4 (amended) waits on the counter-read allow. — **Filed**: 2026-11-24
- **2282 box 4:** `seat_read.py --redirect-uri setup-calendar` is on main (`320f6c42d4`). Next: CIO writes the allow line, xian adds it on an open card, Web runs it once. `beta.` → xian's removal line; `alpha.` → a host-secret fix first. — **Filed**: 2026-11-24
- **2384:** CLOSED 11-26 on the first `deploy_mcp` run (45894237114; MCP serves `c303931894`). Each later MCP deploy is a dispatch on purpose: Tests green on main's head, PA's read of what changed in `services/mcp`, nobody mid-connect. — **Filed**: 2026-11-24
- **2244:** on beta `cd26a9b2e4` since 11-26 11:48; `check-system` on beta answers `chromadb_ready: true`. Rows 1 and 3 ticked. Row 2 (an ingest survives a deploy) needs the operator CLI on the host (xian's hand) and Step E. Follow-ups: issue 2441 (xian's yes 11-26; on main `e8d6b48062`; rides the next promotion; then staging's check-system and HOST's re-read), issue 2440 (Arch's). — **Filed**: 2026-11-24
- **2424:** built (`lead/2424-list-project-arg-r1123`, `ce244d7fca`), held on Arch's trigger (a main-arm router sample or served log line with `list_todos_query` and a `project` arg). Fresh rebase and full suite at landing. — **Filed**: 2026-11-23
- **2425, 2426:** PPM's sprint 3 slot and Arch's choice of lever. — **Filed**: 2026-11-23
- **2281:** owner Web, trigger Step F (PPM, 11-24). Nothing of mine. — **Filed**: 2026-11-24
- **2356 exclusion test (my half of 2354's served checks):** not on main; no order found. Raise with PPM in the sprint 3 draft. — **Filed**: 2026-11-24
- **2361, 2355 (my Tier 1 parts), 2219's stopgap removal, ADR-082 residual:** PPM's order or their named triggers. — **Filed**: 2026-11-13

- **seat-github-1:** row, key allowance and recovery list on main (`5c3a4984d2`); key saved 11-26 13:44. 2399 CLOSED 11-26 on CXO's pass. Later, each a diff HOST reads: the connector allowance comes out at Step G's Ending. Anything the 2364 served probe stores on it goes in HOST's custody row. — **Filed**: 2026-11-26
- **Issue 2445 (`mcp_allow.py --username`):** filed 11-26 on Arch's word; build after Step G part 1, HOST reads the diff. — **Filed**: 2026-11-26

- **`seat_account_create.py` writes an `email:` line in the credential file** (HOST's custody ask, 01M8CPF7P2, 11-26; not blocking): for accounts created after it, so nobody reads near a password to find an address. Goes with issue 2445's build; HOST reads the diff. — **Filed**: 2026-11-26

- **2364 step 1 is on beta** (`039121b0fb`, promoted 11-26 18:58, first dispatch). Waiting: Web's probe on seat-github-1 (six ordinary rows, 2412's line, 2297's list-name row), PA's score, CXO's read. Then Arch's `ENABLE_ETHICS_ENFORCEMENT` default flip in its own commit (Arch reads it), and 2364's boxes. Still open from the 15:25 promotion: 2446's two turns (Web, CXO), 2449 box 2 (a day of passes). 2448 and 2441 CLOSED 11-26. — **Filed**: 2026-11-26

- **GitHub App grant refresh on beta: works** (17:55 pass on 11-26: `refreshed 1, rejected 0`; on issue 2449). Still to come: Web's Integrations card read plus one GitHub turn on seat-github-1 after 20:00 on 11-26 and on the 11-27 morning (2342's 8-hour box; CXO judges; PPM or Lead ticks). xian's own `stale_token` grant is not on the job's list; reconnecting fixes his. — **Filed**: 2026-11-26
- **2364 step 1: LANDED 11-26 17:34 (`4650edcf15`) on prompt v0.3**, which passed Arch's two-provider bar (`dev/2026/11/26/2364-v03/verdict.md`; v0.2 failed on OpenAI the same afternoon). Not on beta (see Next promotion). Served boxes after that. Follow-ups: CXO's issue 2451 (`p-2` is declined on OpenAI and not on Anthropic; `p-3`'s label). Standing rule (Arch 11-26): a change to a provider's default model reruns the gate on that provider; one prompt for all providers. — **Filed**: 2026-11-13
- **Small copy nit (CXO 01M8CSTYR9):** `update_issue`'s never-connected line has no comma before "and"; fix when that string is next touched. — **Filed**: 2026-11-26

- **Issue 2452 (wall-clock tests and collector pauses):** mine, filed 11-26. `test_concurrent_auth_requests` changed (`0afebb26ad`); box 2 open (20 local runs, next 10 CI runs). Wider work, Arch's rule: a test asserting elapsed time pauses the collector for its window or measures something else; no raised bounds. Five of the six standing backlog failures are timing tests. — **Filed**: 2026-11-26

- **Issue 2450 (the gate arms a confirm with no principal on the intent):** Arch's, filed 11-26 from 2448; CXO words its line there. Build when it is ruled and placed. — **Filed**: 2026-11-26

## Waiting on xian (through Exec; each is on a card or Exec's held list)

- **seat-tester-1:** six turns passed (2406 closed by PPM); 2417's and 2411's never-connected reads passed (CXO 01M8CSTYR9; PPM ticks). Next on it, in PPM's order: 2446's two turns after the promotion, then Path B, then 2411's project-with-todos turn, then Path A. — **Filed**: 2026-11-22
- **Step E (OpenAI key):** done for the gate (seat OpenAI key live 11-26; price rows `c033665710`). 2412 and 2297's list-name row now wait on step 1's promotion, not on a key. — **Filed**: 2026-11-15
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
- **2436 (builders set their own not-performed kind; GitHubWriteRefused carries one):** filed 11-25 at Arch's word (01M89MMJY4), follow-up to 2399. Waits on 2399 landing and PPM's placement. — **Filed**: 2026-11-25
- **2438 (length-only):** on beta; the four reset-page reads passed (CXO). The seat script's tail is gone (`dd54d83bd3`). Open rows: the sign-up page, the change-password path (no page calls it) and the wizard row, which need a fresh invite. — **Filed**: 2026-11-25
- **Wizard toast title `Account Creation Failed` (two sites, `web/static/js/setup.js`):** CXO's word is `Couldn't create account` (mail 01M8A9W5TC, 11-25), not blocking; goes with the next page-words change, not a push of its own. — **Filed**: 2026-11-25
- **2356 served question set:** waits on 2355's build step and a named build on a self-hosted install; then send CXO the build id (01M89KHPZ1). The exclusion test also needs one more row then, for what the build loaded (Arch). — **Filed**: 2026-11-25
- **Served reads owed after the 11-25 08:36 promotion (`aaf8d9249e`), all Web's, CXO judges (my mail 01M89S7T8B):** 2433 as a non-admin; 2434's upload helper line; 2399 one bubble per reachable kind (2399 closes on it). 2434's wizard password count has no served row without a fresh-account sitting. — **Filed**: 2026-11-25
- **`PasswordChangeRequest` spaces-only validator:** moves into the route when a page first calls that route; none does (from 2432/2434). — **Filed**: 2026-11-25
- **2399's served box:** vague-write line passed served 11-25 (CXO). Stays open on one row: close/reopen's not-found and already-closed lines, read at xian's F.4 connect. The App line becomes served-reachable with 2423's App-connected seat account. — **Filed**: 2026-11-25
