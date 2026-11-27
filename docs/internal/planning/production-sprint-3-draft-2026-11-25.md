# Production sprint 3 (Fri 11-27 to Thu 12-10): the named set

**Status: RATIFIED by xian, Thu 11-26.** At 09:18 PT he ratified the focus ("I agree with PPM") and 2244 ("yes the vector-store may ship"), relayed in Exec 01M8CDTEVT. At 09:22 PT he ratified the dates ("yes those dates are right and we can assume the schedule is rigid until I say otherwise"), relayed in Exec 01M8CE2RBY. Both are in decisions.log. The Sprint field isn't touched; as in sprint 2, the set lives here and on the map. The filename keeps its draft-date name so the links in mail still resolve.
**Schedule rule (xian, 11-26 09:22):** sprints are a rigid two weeks, Friday to Thursday. They don't shift for holidays or slips, and their dates aren't asked of him again, until he says otherwise. Sprint 4 therefore runs Fri 12-11 to Thu 12-24.
**Ships:** #072 (11-27 to 12-03) reports progress, and #073 (12-04 to 12-10) reports the final score. #071 reports sprint 2's score as it stands on 11-26.
**The close doesn't move** (sprint 2's rule, carried): an item not done by 12-10 isn't stretched in. It goes to the retro and to sprint 4's plan as information.
**Author:** PPM. Drafted at the 11-25 START, and set up at 09:23 PT on 11-26 after ratification.
**Rule carried from sprint 2 (xian, 11-06):** no more than one named item behind any single unanswered design question or decision.
**State column:** `gh issue view` box counts (open boxes / done boxes). They were read at the 11-25 START and re-read at 09:23 PT on 11-26; only item 7 had changed. PPM re-checks the column in one line at the 11-27 START, sprint 3's first day.

## What sprint 2 leaves

- **Score as it stands on 11-25:** Paths A and B served on a fresh test account: 0 of 2 (no fresh account has been minted). Invite-hold P0s closed: 0 of 3 (#2261, #2282, #2342 open).
- **Why:** both counts sit behind the same three things. Step F (HOST's owner line; xian's F.4 GitHub connect in the seat browser), the fresh test account (xian's go-ahead via Exec), and 2282 box 4 (one served read). The build work on Lead's side is largely done and on beta.
- **So the honest sprint 3 is mostly a finishing sprint:** the same score, with its blockers taken one at a time, and a small build lane that doesn't wait on them.

## Main focus (ratified)

**Lift the invite hold, and serve Paths A and B on a fresh account.** xian, 11-26 09:18 PT via Exec: "I agree with PPM." Same score as sprint 2. The score would keep sprint 2's two counts unchanged, so #071's number and sprint 3's close are read on the same scale.

~~Alternative: Path B's routing (items 5 and 6) as the focus.~~ Not taken.

## The named set, each with its one blocker

| # | Item | Owner | Blocker (one) | State, 11-25 (open / ticked boxes; re-checked 11-27 `06:36` START, gh) |
|---|---|---|---|---|
| 1 | #2342: ADR-081 D3, GitHub connect through the published App | Lead, HOST | Step F: xian's F.4 connect on `seat-github-1` (HOST's owner line in `adr-084-one-time-steps.md`) | 7 / 10; **11-27: 6 / 11** (8-hour row ticked 11-26) |
| 2 | #2261: narrow GitHub's `repo` scope | Lead | closes on #2342's served rows (same sitting as item 1) | 3 / 0; 11-27: unchanged |
| 3 | #2282: one canonical host, `beta.pipermorgan.ai` | Web | box 4: Web's `/setup` calendar start read (reader on main). Names beta → xian's removal line on a card; names alpha → a host-secret fix for xian first | 3 / 1; 11-27: unchanged |
| 4 | Fresh-account rows: ~~#2417~~ (closed 11-26), ~~2411~~ (closed 11-27 06:33; both halves served), ~~2406~~ (closed 11-26), #2401, #2402, and Paths A and B served | PA, Web, CXO | ~~xian's go-ahead to mint `seat-tester-1`, via Exec~~ done 11-26: xian minted it and added the allows at Amber, and the console check is yes (Exec 01M8CJTA5Y, 10:45). Lead creates the account and saves the key, then Web runs #2406's six turns and #2417's line, today if possible, inside sprint 2. Account created 10:49. The key save was refused before any send: the key file holds something other than one standard API key (Lead 01M8CK2AGC). ~~Blocker: the key save~~ done 12:01 ("key saved; key on file: yes; validated: yes", Lead 01M8CQ6MRB; the helper's key-prefix fix `bf0603a7c7`; the file was right all along). **No blocker left: Web's six turns (#2406) and #2417's line can go.** **Read order on seat-tester-1 (PPM 11-26, 01M8CS47BV and the reply to CXO):** (1) never-connected, empty-account reads (2406 passed 11-26 and closed; 2417's update_issue line; 2411's create_issue line; 2446 (served on `d54baca4ee`, Web 15:37, CXO passed 15:47; the account stayed empty, so Path B is open)); (2) Path B, a project with tasks made through Piper (asked of Web 11-26 `21:36`, PPM 01M8DR0G3B, for its first 11-27 wake, with step 3 right after; **read 11-27 06:19 to 06:20 by Web (01M8EP2677): not served (PPM 01M8EP8R57).** The first add went to create_ticket and saved nothing (#2425); the project page says no work items (#2455). Rerun turns 3 to 6 on a new project after both are fixed. #2455 is a Path B dependency, not a new item: acceptance written 11-27 (PPM 01M8EPSX56; Arch's route rule, CXO's words, Work Items hidden)); (3) 2411's `how is the <project> project going?` on that project, GitHub still never connected (read 11-27 06:20; PPM reads it served, pending CXO's word); (4) Path A, which connects GitHub, last. **11-27 (PPM 01M8EPSX56, on HOST 01M8EPEC3S): it stays on seat-tester-1, the fresh account. In order: Lead's or Arch's answer on two accounts sharing one GitHub login; HOST's read of the seat row diff; then xian's connect sitting via Exec.** Then Lead re-runs the save once, and Web's chat reads follow. Whatever is not served by sprint 2's close carries here. ~~Then, held by Exec 11-25 (01M8A7V37S): the sitting waits until 2438's creation check is served on beta, unless xian picks length-only~~ xian picked length-only 11-26 (Exec 01M8CDTHCC), which by Exec's 11-25 condition lifts that wait. Exec narrowed PPM's sequencing note (01M8CE8FM5, 11-26 09:25), and PPM agrees. The account is made by `seat_account_create.py`, whose 47-character password passes every rule set, and no person sees the sign-up page. So the sitting and its chat reads don't wait. Only 2438's own served reads (sign-up, change and wizard) wait for a beta that serves the length-only build | 1, 1, 2, 5, 3 open; **11-27: 2401 5 / 0, 2402 3 / 0; 2417, 2406, 2411 closed; Paths A and B 0 of 2** |
| 5 | #2425 + #2424: "add a task to my/the X project" reaches create_todo with the project arg; the list read honours it | Lead | Arch's choice of lever (rule 7; the description lever is advised against) | 2 / 0, 5 / 0; 11-27: unchanged |
| 6 | #2426: "show me the todos in the Launch project" stops asking which project | Lead, CXO | rides on item 5's lever (read-side twin; same ruling) | 4 / 0; 11-27: unchanged |
| 7 | ~~2399~~ (closed 11-26 16:06): said-instead replies on the write rail stop reporting success | CXO, Web | the already-closed and not-found lines need a working GitHub connection: read in xian's F.4 sitting (Lead's proposal to CXO, 01M89SNRXV). **11-26 `12:48`:** blocked on seat-github-1 having no LLM key; chat refuses before routing, and nothing was stored (Web 01M8CSW3BJ). One blocker: HOST's and Arch's choice, (a) save a key on seat-github-1 or (b) another way to read the handler lines. `12:55`: HOST ruled (a) yes, with five conditions (01M8CT906X). ~~Left: Arch's word, Lead's diff, xian's allow~~ all done: key saved and validated `13:50` (Lead 01M8CXCPJK). **`13:56`: Web served the not-found and already-open reads on seat-github-1 (01M8CXQH4T); already-closed is not claimed (CXO). CXO passed both (on the issue 14:06, mailed 15:58); Lead closed 2399 at 16:06.** CXO also ruled already-closed not claimed served | 1 / 6 (11-26 09:23); on beta `aaf8d9249e`; vague-write line served 11-25 (Web 01M89SJ9ZD) |
| 8 | 2356: self-knowledge part 4, the served question set (CXO's set, CIO's three, PPM's known-limits question) | CXO, Web | #2355's build step landing (no runtime index yet, so a served run would not test the exclusion; CXO 01M89KHPZ1); then a named build on a self-hosted install | no boxes; exclusion test landed 11-25 `16e47c26c2` (Lead 01M89K6EAP) |
| 9 | 2244: the document vector store moves onto the `/data` volume | Lead, HOST | ~~xian's yes via Exec~~ given 11-26 09:18 PT ("yes the vector-store may ship"; Exec 01M8CDTEVT). Lead clear to build, under the standing grant, on Arch's validation (plain `chown`, not `-R`) and HOST's read. Served row waits on Step E | 1 / 2 (11-26 10:27): landed `e907690603`, staging's check-system says the folder is writable; row 2 (an ingest survives a deploy) needs the operator CLI on the host, so xian's hand plus Step E (Lead 01M8CHJ45K) |

### Item 9 (2244): answered yes by xian 11-26; the question as it was put

Lead's change adds two lines to the root-run entrypoint to make one more folder on the existing volume, the same pattern as uploads (Arch: a plain `chown`, not `-R`). No new mount, no deploy outside the standing grant. The alternative is a sibling Chroma app. HOST says yes, with two custody notes for xian:
- the volume stops being uploads-only, so destroying or restoring it now touches the document index;
- #2062's restore drill names the index.
The served row waits on Step E, like 2412.

## Lane: close what is already on beta (not named; goal 2 of the 11-20 week)

#2429, #2430, #2431 are built and on beta. Each closes on its served or local-render row (CXO reads, Lead closes). They take no new build.

## Decide, don't build (Arch's, inside the sprint)

- #2149: the router catalog's shape, before more op or example additions (the ceiling stays at 4 until decided).
- 2410: the LLM classifier's system prompt is the persona base, so a persona edit moves routing.
- 2352 box 4: to Arch, if the local key commands are slotted (box 3 ruled 11-24).
These are rulings, not builds. Each names its follow-on build for sprint 4.

## Low priority, if the set runs dry

- ~~#2433~~: closed 11-25 by Lead (`7d9da206bd`); built before sprint 3 opened, so out of the set. Its served read follows the next promotion.
- ~~#2434~~: closed 11-25 by Lead on CXO's pass of the forced-failure render; built before sprint 3 opened, so out of the set. Web's served quotes of the helper line follow on `aaf8d9249e`.

## Not in the set, with why

- #2435 (Slack silent on not-performed replies), #2436 (builders set their own not-performed kind; Arch: later, one unit) and ~~#2437~~ (close/reopen on a stale connection asks yes/no; closed 11-25 on CXO's served pass, on beta `92836ae41d`): filed 11-25 from 2399's work, placed in H. The two open ones wait on an Arch mechanism or CXO's words; xian can pull any of them in at ratification.

- #2438 (password rules differ between creation and reset; the reset page states only the length): filed 11-25 by Lead, placed in H. Both answers came the same day: Arch ruled the five-rule set (unless xian loosens it, via Exec), and CXO gave one fixed refusal line. Built and on beta `cf3486389e` 11-25; reset half passed (CXO). **11-26: xian chose length-only** (Exec 01M8CDTHCC): Arch re-rules for sign-up, reset and change, CXO sets the new refusal line, Lead rebuilds; Arch re-ruled at 09:22 (length-only, a 72-byte maximum, and build conditions; xian set MIN_LENGTH to 15 at 09:29 (Exec 01M8CEG65R); the `aA1!` tail in the seat script stays until beta serves the rebuild (Arch 01M8CECPDT)). PPM rewrote the acceptance rows the same hour. It is a rebuild of an item already outside the set, so it stays in H and out of the named set. Its wizard row is read on a beta that serves the rebuild, not at item 4's sitting (Exec 01M8CE8FM5).

- ~~2297~~ (closed 11-26 19:21, with ~~#2412~~ at 19:20, on Web's 19:07 line and CXO's pass 01M8DG299S). 2297's last row: behind #2412, which waits on #2364 step 1. **Step E is done (xian, 11-26 `12:49`; Exec 01M8CSY4ME):** the seat-screens OpenAI project ($25, limit enforced) and `PIPER_SEAT_OPENAI_KEY` are stored for Lead. ~~#2364's OpenAI half unblocks at Lead's next session start~~ ran 11-26 (Lead 01M8D6GWWD): **FAIL** on two rows (gpt-4o declines "What's open in our private repo?" 5 of 5, and p-1 only 3 of 5), so step 1 is held by Arch's pre-run ruling. Next: diagnostic reads (Exec's spend ack), then CXO's call on one recalibrated prompt that passes both providers, rerun on both. 2412 and this row wait behind that. **v0.3 passed both providers 17:16; step 1 landed `4650edcf15` 17:34 (Lead 01M8DA9D03); promoted 18:58 (beta `039121b0fb`); **Web served 2412's line, which is this row, at 19:07: "I've added 'renew passport' to your list." (`create_todo`, not declined, stored).** Waits on PA's score and CXO's judgment, then 2412 and this row tick.**
- #2423: needs an App-connected account, so it follows Step F; it can join item 1's sitting if Lead has it ready.
- #2388 rows 4 and 5: the allow on xian's open card, and Step H.
