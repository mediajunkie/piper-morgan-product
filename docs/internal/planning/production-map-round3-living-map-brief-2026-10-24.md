# Production map, round 3: the living-map brief

**Status:** Exec's brief, Sat 2026-10-24, written after xian's Production map rulings (decisions.log 17:28). It's for Arch, CXO and PPM to answer, then PPM builds. It replaces the hand-kept draft (`production-map-draft.html`, v0) with a map that is generated from the board and diffs itself each week.
**Inputs:** the round-2 record (`production-map-review-round2-2026-10-23.md`, "Map design, converged" and the round-2 answers), the rulings page, and xian's 17:28 rulings.

## What the map is for

It answers four questions at a glance, each from its owner's point of view:
1. **How close is 1.0?** (ruling 2: every 1.0 promise has a closed issue, and main is green). PPM's lens.
2. **What closes next, and what is waiting on what?** This uses the closing order, and backward edges show. Arch's lens.
3. **Can a person do each step, on each surface?** This is the journey grid. CXO's lens.
4. **Can strangers arrive?** These are the Readiness lane and the gates. Exec's lens.

A gap is always shown as an **empty, red cell**, never as a missing row.

## Settled (no need to reopen)

- **Generated, not hand-kept.** Sprint membership comes from the board's Sprint field. Hand-kept data covers only slow-changing layers (promise IDs, journey tags), and it lives in labels plus one small file.
- **Front view:** rows are sprints **in closing order**: H (honesty) → D's isolation slice → PUB → D (rest) → C → V → E → Readiness → Q (health). Columns are the three gates: private beta, public beta and 1.0. A row that must close before a row above it draws a backward edge.
- **Side views, all generated:**
  - **Promise view (PPM):** rows are promises, cells are the issues that back them, and a promise with no issue is red. Its headline is "N of M 1.0 promises have a closed issue", with main's state beside it. This is ruling 2's measure.
  - **Journey grid (CXO):** rows are journey moments, columns are surfaces (web, chat, **plugin** as its own column, MCP), and cells are sprints. A cell with no sprint is red.
  - **Dependency view (Arch):** seams as nodes (credential resolver, catalog shape, GitHub identity (#2163), DB durability (#2157), green CI (#1452/#1457)), and "must close before" as edges. An empty seam is red.
  - **Readiness view (Exec):** the five Terms-backed items (#2157 to #2161) plus staging (#2162), each with its issue state. An item with no issue is red. HOST's send-morning checks are the lane's standing check.
- **"Since last" diff:** weekly, on Friday, inside Exec's weekly synthesis pass. It lists issues added, removed, moved or closed per sprint, promises amended, and edges added or removed.

## To decide in this round (each has a recommendation)

1. **Where promise and journey tags live.** *Recommendation:* labels, `promise:<id>` and `journey:<moment>`, plus one ratified file, `docs/internal/product/promises.yaml`, that PPM keeps. The file holds each promise's ID, wording, ESSENCE or Terms source, and gate. A label is visible on the issue and cheap to query. The file is the place where a promise's wording is ratified. Neither label exists yet (checked 19:10: `gh label list` finds none).
2. **Where edges live.** *Recommendation:* GitHub's native "blocked by" relation, which is Arch's proposal. It sits on the issue and both ends see it. A YAML file of edges would drift.
3. **Where the snapshot lives.** *Recommendation:* reuse `scripts/snapshot-project-board.sh`. It already writes `dev/snapshots/project-board-YYYY-MM-DD.tsv` (issue, state, milestone, Sprint, title) to git. Extend it with labels and the blocked-by edges, and the Friday diff is two TSVs compared.
4. **Where the map is published.** *Recommendation:* one HTML page generated into `docs/internal/planning/production-map.html` and republished as a single artifact link that xian keeps. Each Friday's version carries its "since last" section at the top.
5. **Who builds the generator.** *Recommendation:* **PPM owns it** (data, promise file, script), with a Sonnet subagent for the script. Arch reviews the edge view, and CXO reviews the journey grid. Exec runs the Friday diff and puts its bottom line on xian's rollup.

## Blocked on xian (one minute, already on his rollup)

The three new Sprint options (`PROD-HONESTY - Failed Reads Say So`, `PROD-DATA - Data Boundaries, Privacy & Terms`, `PROD-CONVO - Conversation Reliability`) must exist before the front view can be generated. Only xian can add them, in the GitHub web UI. Until he does, PPM can build everything else against today's options and the plan's sprint letters.

## Acceptance (what "built" means)

- The map is regenerated from a fresh snapshot by one command, and nothing in it is typed by hand except the promise file.
- Every red cell in each view is real, checked by hand on the first run against the board.
- The first Friday diff (10-30) lists the week's moves and matches the board.
- The headline "N of M 1.0 promises" reconciles with `gh issue list` for the promise labels.

## Answers wanted

Arch, CXO, PPM: reply to Exec on items 1 to 5. "Agree" is a complete answer. Name anything your lens needs that this leaves out.

Verified how: the round-2 record's map-design and round-2-answer sections were read this turn; `scripts/snapshot-project-board.sh` header read; `gh label list --search promise` and `--search journey` returned nothing. Layer: repo and GitHub. Not checked: whether GitHub's blocked-by relation is queryable from `gh` on this account (Arch's item).
