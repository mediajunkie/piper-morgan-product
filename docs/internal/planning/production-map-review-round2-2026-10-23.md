# Production map review, round 2: merged findings (2026-10-23)

**Status: DRAFT for the four reviewers (Arch, CXO, PPM, Exec).** After the reviewers have answered the contested items, it goes to xian for rulings. Nothing here is filed, moved or closed yet. Every "file" action below is a proposal.

**Inputs:** PPM's plan (`production-sprint-proposal-2026-10-23.md`, order ratified: PUB, H, D, C, V, E, T, Doc, Dist; Q as a standing share; R moved out); the four round-1 memos (Arch 17:57, PPM 18:00, CXO 18:50, Exec 18:52); `release-model.md` §2 (audience gates).

**Draft map:** `docs/internal/planning/production-map-draft.html` (v0, baseline 2026-10-23).

**How to read the table:**
- **Kind** is one of Missing, Implied, Obsolete, Misplaced or Opportunity.
- **Gate** is the audience gate the finding blocks, under `release-model.md` §2: private beta (now), public beta, or 1.0.
- **Confidence:**
  - **agreed** means two or more memos raised it independently or endorsed it;
  - **single** means one role raised it;
  - **ruling** means only xian can decide it.
- Issue state and milestone were checked with `gh issue view` at 18:56 PT. The figures in brackets are that check.

## Findings (42)

### Missing (11)

| # | Finding | Raised by | Proposed action | Sprint | Gate | Confidence |
|---|---|---|---|---|---|---|
| F1 | **Production database durability.** No scheduled backups, retention, tested restore, or failover/HA decision. #2146 [CLOSED, Production] recovers a *stopped* database, not lost data. #338 [OPEN, Fast Follow] covers migration rollback only. | Arch, PPM, Exec | File "Production DB: scheduled backups, retention, one timed restore drill on a copy, and a recorded HA decision". Link #338. Make it a child of #2062. | D | public beta | agreed (3) |
| F2 | **Account deletion with a real purge, reachable in product.** xian's 10-13 ruling: deletion by email within 14 days for now; "the goal is a trash with a real purge". Nothing in Production carries that goal. #651 and #336 [both OPEN, Fast Follow]. | PPM, CXO, Exec | File a new issue, or move #651 and #336 into D (see Contested C1). Include the backup-retention line ("up to about five days"). | D | public beta | agreed (3); form contested |
| F3 | **Portability: export everything Piper holds for a user, in open formats** (ESSENCE commitment 1). #1246 and #1202 [both OPEN, Production] export *artifacts* only. | PPM, CXO | File "Export everything Piper holds for a user, in open formats". Acceptance is read against the owner-id inventory. | D | 1.0 (public beta if the Terms promise it) | agreed (2) |
| F4 | **The inversion's remainder has no Production home.** #1595 [OPEN, MVP] covers retiring the legacy classifier chain, the remaining flip groups, and the router-hidden ratchet to 0. Its children #1943, #1970, #1619 and #1984 [all OPEN, Production] are scattered through V. | Arch, PPM | At MVP close, file a Production epic or move #1595 to Production. "1.0 implies one classification path" goes in its body. | V | 1.0 | agreed (2) |
| F5 | **One GitHub identity model** (an ADR plus an issue). Six issues across three sprints decide the same thing: #1514, #1966, #1325 (C); #2123, #2136 (D); #1061 [OPEN, Enterprise since 10-23]. | Arch, PPM | File the ADR and one issue: "GitHub identity: one app/token model and whose token serves a read". Link all six. | seam ahead of H, C, D | 1.0 (gates F15) | agreed (2) |
| F6 | **Support intake and the "tell us" loop.** Dozens of replies say "tell us". No issue names who reads Send feedback or support@, how fast they reply, or what the user sees back. #2096 [CLOSED, MVP] shipped the in-app feedback link. | CXO, Exec | File "Support intake and feedback loop: one address or form, an owner, a response promise in the Terms, a path from a failed reply to a report". Make it a child of #2062. Exec owns operations; CXO owns the user's view. | D | public beta | agreed (2) |
| F7 | **Incident notice to users.** Alerts reach xian (#2144 [OPEN, Ongoing]). Nothing tells a user during an outage, or afterwards. | Exec | File "Incident notice: in-app banner or status note during an outage, plus a short after-note" (a status page at 1.0). Make it a child of #2062. | D (or an ops lane; see C6) | public beta | single |
| F8 | **A production environment distinct from alpha.** No issue says whether 1.0 runs on alpha's app, database and secrets, or on new ones, or how alpha data migrates. `release-model.md` §1 names `PIPER_ENVIRONMENT` but decides nothing about this. | Exec | Arch to answer whether it is decided. If not, file "Production environment: same as alpha or new; data migration plan". | none (unhomed) | public beta | single; needs Arch |
| F8a | **Arch's answer to F8 (19:1x):** it isn't decided anywhere. In practice, alpha's Fly app already runs `PIPER_ENVIRONMENT=production`, and every audience has been served from it. Arch recommends one production instance, with audiences as product gates (release-model's own model). Then no 1.0 instance and no migration are needed. **The real gap is a staging instance with no user data** for destructive tests and promotion rehearsal (today's test 4 stopped the database partners' data sits in). A staging copy restored from a production backup is also F1's restore drill. | Arch | File "Staging instance for destructive tests and promotion rehearsal; alpha's instance is Production." Rule on one production instance. | D (or an ops home, C6) | public beta | ruling (infrastructure cost) |
| F9 | **Self-serve sign-up (or a waitlist) and per-account abuse and rate limits.** Every account today starts from a hand-minted invite (#1954 [OPEN, Ongoing], #2099 [OPEN, Production]). | Exec | File two issues: "Sign-up without hand-minted invites (or a waitlist)" and "Per-account rate and abuse limits". | PUB | public beta | single; sign-up model is a ruling |
| F10 | **No rubric for the plugin surface.** PDR-004 Amendment A (ratified 17:54) says a surface is not Done until it passes its rubric. PUB's #1701 to #1707 [OPEN, Production] build the plugin surface without one. | CXO | File "Plugin surface rubric (CXO instrument): payload honesty, tool-description wording, failure shapes". It is a PUB precondition. CXO drafts it. | PUB | public beta | single |
| F11 | **The PRD and spec half of commitment 2.** Nothing lets Piper draft a PRD or spec as a judgment artifact. #2139 [OPEN, Production] is the nearest. | PPM | xian rules on whether it is 1.0 or post-1.0. If 1.0, file under Doc ("Draft a PRD or spec from these issues and this conversation"). If post-1.0, annotate ESSENCE. | Doc, or post-1.0 | 1.0 | ruling |

### Implied but absent (13)

| # | Finding | Raised by | Proposed action | Sprint | Gate | Confidence |
|---|---|---|---|---|---|---|
| F12 | **User-facing release notes.** The Weekly Ship is the development story, not a user changelog. | Exec | File a small Comms issue: "What changed: a user-findable release note". | Dist (Comms) | public beta | single |
| F13 | **PUB can't close before D's isolation half.** #1551 [OPEN, Production] sits in PUB. Its concrete rows are in D: #1561, #2009, #2013, #2014, #1257 [all OPEN, Production]. Its status scope is #2151's ISS-STATUS seam. | Arch, PPM | Either move those five rows into PUB, or record that PUB closes after them (C2). | PUB / D | public beta | agreed (2); option is a ruling |
| F14 | **The Terms (#2062 [OPEN, Production]) presume mechanisms** that have no issue: durability (F1), deletion (F2), export (F3), support (F6), incident notice (F7). xian's own words are "every commitment mapped to a mechanism". | Exec, CXO, PPM, Arch | Carry F1, F2, F3, F6 and F7 as children of #2062, so the Terms can't publish a promise with no machine behind it. #2063 [OPEN, Production] waits on them. | D | public beta | agreed (4) |
| F15 | **H's "connected" claims need one credential resolver per connector.** #2074, #2093, #2150, #2036, #2053 and #1995 can't become true while GitHub has two resolvers (#1966, in C) and a failed lookup reads "not configured" (#2151 ISS-STATUS, #1553 in PUB). The memos also see an opportunity here: one credential-and-status build, not about ten patches. | Arch, PPM | Move #1966 into H as a precondition. Scope #2151 step 3 to the per-connector resolver, covering #1966, #1553, #1551's status scope and the six rows. | H | 1.0 (backward edge to PUB via #1553) | agreed (2) |
| F16 | **#2149 (router catalog shape) gates every sprint that adds a chat capability:** C's #2130 and #1917, and V's #1931, #1932 and #1935. #1891 and #2145 are the same decision. | Arch | Decide the catalog shape first: move #2149, #1891 and #2145 ahead of C, as a seam or at the front of V. | seam ahead of C, V | 1.0 | single |
| F17 | **H's ratchets need a green main.** #2151's `KNOWN_RED` ceiling means something only on a suite that runs green: #1452 (413 failed, 71 errors), #1457 (ci.yml red, 100+ runs) [both OPEN, Production]. | Arch; PPM in part (main green is part of PPM's 1.0 definition) | Q's first share is "main green, full suite trusted", before H leans on it. The size waits on the CI ruling. | Q | private beta (now) | agreed (2) |
| F18 | **"1.0 = Production closes in full" makes about 50 non-promise issues gate GA.** Those are most of Q's 39 plus about 11 DIST and onboarding rows. PPM counted them by title; nobody has read them. | PPM | xian rules: does 1.0 mean "every 1.0 promise has a closed issue and main is green", with the rest moved to Ongoing or a non-gating Q backlog? | Q | 1.0 | ruling |
| F19 | **Self-service help is a public-beta precondition.** A public-beta user has no concierge. | CXO | Move #1186 [OPEN, Production] from E to PUB, or record why not. | PUB | public beta | single |
| F20 | **Honesty shapes don't yet reach the plugin increments.** #2151 now covers the hosted MCP resources. No sprint carries that to #1701 to #1707 as they are built. | CXO | Link #2151 to #1701 to #1707. Each increment lands with its failure shape and a served row. | PUB | public beta | single |
| F21 | **The user controls what Piper holds about them** ("see, correct, delete what Piper remembers"). #1609 (in E) and #955 (in T) [both OPEN, Production]. | CXO | Move #1609 and #955 into D as its data-control row, mapped in #2062. | D | 1.0 | single |
| F22 | **Copy passes should run after #2151 settles,** because #2151's registries now hold the words. | CXO | Sequence #1043 and #1546 [both OPEN, Production] late in E, after #2151 closes. | E | 1.0 | single |
| F23 | **Production on-call is one person.** Every alert ends at xian. That is right for alpha; Production implies a stated support window. | Exec | Add a support-window line to #2062's mechanism map (no second human). | D | public beta | single |
| F24 | **PDR-001's recognition-first contact versus the stepped setup wizard.** CXO proposes this wording for the exception: "recognition-first applies to the first conversation; the hosted setup wizard is a stepped, explicit-consent flow… the recorded exception". Whether the first conversation recognizes the user today is unverified. #1538 [OPEN, Production] is the work. | CXO | xian rules on the wording and records it in decisions.log. | PUB | public beta | ruling |

### Obsolete (5)

| # | Finding | Raised by | Proposed action | Sprint | Gate | Confidence |
|---|---|---|---|---|---|---|
| F25 | **ESSENCE commitment 6 ("not a destination app") contradicts the surface rulings:** xian's 08-08 and 08-10 rulings, gate R7, and today's PDR-005 and PDR-006 amendments. Sprint E (34 issues of web polish) only makes sense if web is a real surface. | PPM | Amend ESSENCE to match: Arch drafts it, xian ratifies. | none (doc) | — | ruling |
| F26 | **#957, #958, #966 are pre-PDR-006 distribution forms.** Checked at 18:56: #957 is **CLOSED**, #958 is on **Fast Follow**, and #966 is OPEN in Production, **retitled** "Visual identity for the plugin and MCP Apps surf…" (kept). | PPM; Exec concurs | Nothing left to do on the issues. Update the plan's Dist table: 2 of its 14 rows have left. | Dist | — | agreed (2); resolved by events |
| F27 | **#366 SLACK-MEMORY** [OPEN, Production]: Slack is parked on Fast Follow (08-28, 08-30). | PPM | Move #366 to Fast Follow. | C → Fast Follow | — | single |
| F28 | **#1242, #1244, #1245** (meet-piper and consult-piper skills from the thin-BYOC POC #1145 [CLOSED, MVP]) [all OPEN, Production]. Whether the plugin's skills replace them is a PDR-006 question. | PPM | Arch or PA reads them against PDR-006, then keeps, moves or closes them. | Dist | — | single |
| F29 | **#1011** (slash-command dispatch, "post-MVP design decision needed") [OPEN, Production] may have been overtaken by a ruling. | CXO | Arch checks it, then closes it or keeps it. | E | — | single |

### Misplaced (9)

| # | Finding | Raised by | Proposed action | Sprint | Gate | Confidence |
|---|---|---|---|---|---|---|
| F30 | **#1474** (dead code, zero production callers) [OPEN, Production] is listed in V. | Arch, PPM | Move it to Q. The plan header already says it "reads as Q", but the table still lists it under V. | V → Q | — | agreed (2) |
| F31 | **R set out; #482 back.** Checked at 18:56: #371 and #1061 are on Enterprise; #557, #1209 and #1219 are on Dot Releases; #482 is OPEN in Production (D, waiting on #2062). | Arch, PPM | Done. Update the plan table so #482 appears under D (22 rows) and the R table is removed. | D | — | agreed (2); resolved |
| F32 | **#865** (setup wizard refactor) [OPEN, Production] is filed under PROD-DIST. | PPM | Move it to E or Q. | Dist → E/Q | — | single |
| F33 | **#1551's title says "Multi-tenancy", but its body is per-user isolation.** ESSENCE says Piper is "Not enterprise multi-tenant SaaS". | PPM | Retitle it "Per-user isolation, Production scope". No scope change. | PUB | — | single |
| F34 | **#2103** (undefined `showToast()`, 121 call sites) and **#1487** (an unreachable branch decides what users are told) [both OPEN, Production]: these are silent or false, not polish. | CXO | Move both from E to H. | E → H | 1.0 | single (H's scope is Arch's; C5) |
| F35 | **Timezone: four E items, one false-statement slice.** #1535, #1550, #1828, #1915 [all OPEN, Production]. | CXO | Move them from E to H as one slice under the #1828 parent. | E → H | 1.0 | single (C5) |
| F36 | **#1516** (conversation delete and archive have no reachable UI) [OPEN, Production] is a deletion promise, not layout. | CXO | Move it from E to D, into the leaving slice (F39). | E → D | public beta (via F14) | single |
| F37 | **#1523** (logout URL points at a nonexistent route) [OPEN, Production] rides PUB's auth work (#1378). | CXO | Move it from E to PUB. | E → PUB | public beta | single |
| F38 | **#1298, #1350 (E) and #1131, #1139 (T)** [all OPEN, Production]: dead-code and test tasks. CXO judged them by title only. | CXO | Move them to Q after a body read. | E, T → Q | — | single |

### Opportunity (4)

| # | Finding | Raised by | Proposed action | Sprint | Gate | Confidence |
|---|---|---|---|---|---|---|
| F39 | **One "leaving" slice in D.** Export (F3), deletion (F2), and the Terms' data map share one owner-id inventory (#2009, #2013, #2014, #1561). Add #2021, #1516 and #1609, which share one set of words and one Terms mapping row. | PPM, CXO | Plan it as one slice in D once the owner-path rows close. | D | public beta | agreed (2) |
| F40 | **A first-run slice:** FTUX #1537 to #1540, invites (#2099), the key-check line (#2125) and the setup lines [all OPEN, Production]. It is already half in PUB. | CXO | Run one served walkthrough before anyone beyond the design partners. | PUB | public beta | single |
| F41 | **HOST's send-morning checks are a release checklist in miniature.** | Exec | Promote them into the production launch checklist; don't write a new one. | none (ops) | public beta | single |
| F42 | **In-app feedback plus H's "couldn't check" lines** give support triage a pre-labelled feed. | Exec | Note it in F6's design. | D | — | single |

**Count:** Missing 11, Implied 13, Obsolete 5, Misplaced 9, Opportunity 4 = **42**. 14 findings are agreed by 2 or more roles (F1 to F6, F13 to F15, F17, F26, F30, F31, F39). 4 are rulings only xian can make (F11, F18, F24, F25), and xian also decides F13's option and F9's sign-up model (C2, C7).

Already folded in, not separate rows:
- Arch's "one credential-and-status build" is in F15.
- Arch's "one catalog decision" is in F16.
- Arch's "GitHub identity ADR removes #2123" is in F5.
- PPM's "PRD rides on Doc plus GitHub" is in F11.
- #1595's MVP placement is in F4.
- #2109 is correctly in D (Arch). No action.

## Contested or needs a ruling

**C1. Deletion: new issue, moved issues, or one combined issue?**
- PPM: file a new issue, or move #651 and #336 (Fast Follow) into D.
- CXO: one issue, "Account deletion and data export: user-reachable flow".
- Exec's lean: two issues (deletion; export) under one D slice (F39). Export has its own ESSENCE line, and deletion has its own Terms line.
- Reviewers settle this; no ruling needed.

**C2. PUB versus D's isolation rows (F13).** Move five rows into PUB, or declare that PUB closes after D's isolation half. Either way the drawn order PUB → H → D is not the closing order. PPM proposes; xian rules if it changes what "PUB" means.

**C3. The 1.0 definition (F18).** xian's call. Until it is ruled, the map can't show "how close to 1.0".

**C4. ESSENCE commitment 6 (F25), the PRD/spec half of commitment 2 (F11), and the PDR-001 exception wording (F24).** xian's calls.

**C5. Moving items from E into H (F34, F35).** CXO proposes; H's scope is #2151, which Arch scoped. Arch needs to agree that a timezone error and a silent toast are Class 3 honesty shapes rather than polish. Not yet contested, but only one side has spoken.

**C6. Where operations work lives.**
- F7 (incident notice), F8 (production environment) and F41 (launch checklist) have no sprint.
- The plan has no ops lane, and Arch's map has a data-and-infra swimlane but no ops node.
- Options:
  - D children of #2062 (Exec's lean for F7 and the support half);
  - a new readiness lane;
  - Ongoing.
- F8 needs Arch's answer first.

**C7. Sign-up model (F9).** Self-serve sign-up or a waitlist is a product decision for xian.

**C8. Board sprint options.** The plan header says the map review decides whether the board should carry H, D and V as Sprint options. Today their issues read unset or under the nearest PROD-* bucket. Every memo's map design generates nodes from the board's Sprint field (C9). So the map can't be generated until those options exist, which only xian can add, in the web UI.

**C9. The Q share's size** waits on the CI ruling (plan header). It is not a map question, but F17 depends on it.

## Map design, converged

**All four agree:**
- **Generated, not hand-kept.** Sprint membership comes from the board's Sprint field. Hand-kept data is limited to slow-changing layers (promise IDs and journey tags in a small file or labels).
- **"Since last version" is a weekly snapshot diff:** issues added, removed, moved or closed per sprint; nodes and edges for Arch; promises amended for PPM. Arch and Exec both say Friday, and Exec proposes running it in the weekly synthesis pass.
- **A gap shows as an empty, red cell.** Each lens has one: a promise with no issue (PPM), a journey cell with no sprint (CXO), a readiness item with no issue (Exec), and an empty seam node (Arch).
- **Audience gates appear on the map** as columns (Arch, Exec) or as an overlay (CXO).

**Where the memos differ:**
- **The main axis.**
  - Arch: rows are surfaces (chat, Settings, hosted MCP, data and infra), nodes are sprints plus seams, and edges are "must close before".
  - PPM: rows are promises, columns are sprints.
  - CXO: rows are journey moments, columns are surfaces.
  - Exec: rows are sprints, columns are gates, and the other three lenses become side views.
  - The draft uses Exec's frame and keeps the others as side views, because it is the only frame in which every lens has a cell.
- **The gate columns.** Arch has four (private beta → public beta → outside users beyond the partners, i.e. #2063 → 1.0). Exec has three. `release-model.md` §2 names three. The draft uses three and marks the Terms rows in the public-beta column, since outside users arrive with public beta at the latest.
- **Seams as nodes.** Only Arch draws them: the credential resolver, catalog shape, GitHub identity, DB durability and green CI. The draft keeps them in the dependency view, not in the grid.
- **Source of truth for tags.**
  - Arch: GitHub's native "blocked by" relation for edges.
  - PPM: one label or field per issue naming its promise ID.
  - Exec: labels or a small YAML file.
  - Not yet decided. It belongs in the round-3 brief.

Verified how:
- Read all six inputs in full: the plan (336 lines), the four memos, and `release-model.md`.
- Ran `gh issue view` (state and milestone) on 113 issue numbers (#1702 to #1706 included), which covers all 93 numbers cited above. All of them exist.
- These states differ from what a memo or the plan implies: #957 is CLOSED, #958 is on Fast Follow, #966 was retitled, #2132, #2148, #2096 and #1688 are CLOSED, and #1219, #1209 and #557 are on Dot Releases while #371 and #1061 are on Enterprise.
- Not done:
  - reading issue bodies (findings come from the memos' own reads);
  - checking the board's Sprint field (C8);
  - checking the "about 50" figure in F18.
- Denominator: 42 findings merged from 4 memos; 113 issue numbers verified (all 93 cited) against the 230 open Production issues in the plan.
