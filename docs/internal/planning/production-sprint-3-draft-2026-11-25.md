# Production sprint 3: draft named set

**Status: DRAFT for xian.** Nothing here is ratified. Dates, the main focus and the score are xian's. PPM proposes the set and the blockers, not dates.
**Author:** PPM, 2026-11-25 START, on the sprint 2 score as it stands. Revised at the 11-26 close if sprint 2's last day changes a row.
**Rule carried from sprint 2 (xian, 11-06):** no more than one named item behind any single unanswered design question or decision.
**State column:** `gh issue view` box counts read at the 11-25 START, written `06:35` (open boxes / done boxes).

## What sprint 2 leaves

- **Score as it stands on 11-25:** Paths A and B served on a fresh test account: 0 of 2 (no fresh account has been minted). Invite-hold P0s closed: 0 of 3 (#2261, #2282, #2342 open).
- **Why:** both counts sit behind the same three things. Step F (HOST's owner line; xian's F.4 GitHub connect in the seat browser), the fresh test account (xian's go-ahead via Exec), and 2282 box 4 (one served read). The build work on Lead's side is largely done and on beta.
- **So the honest sprint 3 is mostly a finishing sprint:** the same score, with its blockers taken one at a time, and a small build lane that doesn't wait on them.

## Proposed main focus (xian's choice)

**Lift the invite hold, and serve Paths A and B on a fresh account.** The score would keep sprint 2's two counts unchanged, so #071's number and sprint 3's close are read on the same scale.

Alternative, if xian wants a build focus instead: Path B's routing (items 5 and 6 below) as the focus, with the hold as a lane. PPM recommends the first: the hold is what keeps any tester out, and the build lane is small.

## The named set, each with its one blocker

| # | Item | Owner | Blocker (one) | State, 11-25 |
|---|---|---|---|---|
| 1 | #2342: ADR-081 D3, GitHub connect through the published App | Lead, HOST | Step F: xian's F.4 connect on `seat-github-1` (HOST's owner line in `adr-084-one-time-steps.md`) | 7 / 10 |
| 2 | #2261: narrow GitHub's `repo` scope | Lead | closes on #2342's served rows (same sitting as item 1) | 3 / 0 |
| 3 | #2282: one canonical host, `beta.pipermorgan.ai` | Web | box 4: Web's `/setup` calendar start read (reader on main). Names beta → xian's removal line on a card; names alpha → a host-secret fix for xian first | 3 / 1 |
| 4 | Fresh-account rows: #2417, 2411, 2406, #2401, #2402, and Paths A and B served | PA, Web, CXO | xian's go-ahead to mint `seat-tester-1`, via Exec (one decision, so one named item) | 1, 1, 2, 5, 3 open |
| 5 | #2425 + #2424: "add a task to my/the X project" reaches create_todo with the project arg; the list read honours it | Lead | Arch's choice of lever (rule 7; the description lever is advised against) | 2 / 0, 5 / 0 |
| 6 | #2426: "show me the todos in the Launch project" stops asking which project | Lead, CXO | rides on item 5's lever (read-side twin; same ruling) | 4 / 0 |
| 7 | 2399: said-instead replies on the write rail stop reporting success | Lead | none (Arch's 11-24 split: `ask.armed`, new kind `ALREADY_IN_STATE`) | 7 / 0 |
| 8 | 2356: self-knowledge part 4, exclusion test and the served question set | Lead | none (Lead's half of 2354's served checks) | no boxes |
| 9 | 2244: the document vector store moves onto the `/data` volume | Lead, HOST | xian's yes via Exec to two lines in the root-run `deploy/docker-entrypoint.sh` (below) | 3 / 0 |

### Item 9, the question for xian (2244)

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

- #2433: a non-admin opening an admin-only page by address sees raw JSON (card shows to admins only). The way out is a closed `way_out` choice (Arch 01M880KDHY).
- #2434: pages' own "Failed to…" toasts, plus one sweep row for page copy that contradicts the route in fact (CXO 01M888Q5GX).

## Not in the set, with why

- 2297's last row: behind #2412, which waits on #2364 step 1 (xian's OpenAI run).
- #2423: needs an App-connected account, so it follows Step F; it can join item 1's sitting if Lead has it ready.
- #2388 rows 4 and 5: the allow on xian's open card, and Step H.
