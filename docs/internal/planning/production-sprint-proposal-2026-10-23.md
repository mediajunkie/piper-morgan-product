# Production milestone: proposed sprints (PPM, 2026-10-23)

**Status: ORDER RATIFIED** (xian, 2026-10-23 17:54, via Exec: "I approve all 4 questions for me"; decisions.log). No dates; PPM proposes none.
- **Order:** PUB, then H, D, C, then V, E, T, Doc, Dist.
- **Q** is a standing share of every sprint. Its size is open until the CI ruling.
- **The 9 "Beta Blockers - Hard Gates Only" issues are re-labelled** per item (`assign-sprint-safely`; the Sprint option list is unchanged at 57):
  - #1522 and #1698 → PROD-TECHDEBT;
  - #1625, #1828 and #1907 → PROD-DESIGN;
  - #1735 → PROD-TRUST;
  - #1817 → PROD-INFRA (the nearest existing option to D);
  - #1632 and #1891 (V) → unset, because no V option exists.
- **R is out of Production** (PPM's placement, 10-23): #371 and #1061 → Enterprise; #557 and #1209 → Dot Releases. On Arch's 17:57 points, #1219 followed #1209, and #482 came back into D: managed key custody depends on what #2062's Terms commit to. #1474, dead code, reads as Q, not V.
- **Round 2, C5 and F29 (Arch, 21:33; CXO raised F34 and F35), applied 21:36:** #1487, #2103, and the timezone slice (#1828 parent, #1550, #1535, #1915) move E → H. H's acceptance for the timezone slice is "no false time statement". #2103's code fix has landed and it closes on Web's served toast row. #1550 needs a served check before anyone builds. #1011 moves E → V to be decided with the catalog seam (#2149, #1891, #2145). F28 (#1242, #1244, #1245 superseded) waits on PA's answer on live POC installs.
- **xian's Production-map rulings (10-24 17:28, decisions.log; Exec's relay), applied 17:36:**
  - **1.0 = every 1.0 promise has a closed issue and main is green** (ruling 2). xian is "the final arbiter of whether a given bug blocks production launch". Non-promise rows move to Ongoing after a body read (in progress; see the PPM log).
  - **Main green** = the 12 workflows now, and the full suite by the end of H. **Q's share is about 1 in 5 issues per sprint** until then (ruling 8). Q stays a standing share, sized at that ratio when each sprint is built.
  - **Order:** H → D's isolation slice → PUB (go-ahead).
  - **Ruling 2 applied 17:42:** 48 Q and Dist rows read in full (a Sonnet subagent, with PPM checking the low-confidence ones).
    - 27 moved to Ongoing with their Sprint cleared. 6 of them are close candidates for their owners: #1356, #1365, #1469, #2058, #2102, #1300.
    - 3 closed as superseded by PDR-006: #830, #831, #832.
    - #1282 stays, narrowed to listing the hosted plugin.
    - 18 stay: 14 for main green (#1224, #1349, #1357, #1367, #1371, #1372, #1385, #1437, #1439, #1451, #1452, #1479, #1506, #1528), plus #1494 and #1549 (possible honesty shapes, unruled), #966 (plugin identity) and #1282.
    - #1242, #1244 and #1245 wait on F28.
  - **Readiness lane** (ruling 7, Exec owns it): HOST's send-morning checks are its standing check. Its Terms-backed items are #2062's children and gate public beta: #2157 backups and the restore drill, #2158 deletion (#651 and #336 are its children), #2159 export, #2160 support intake, #2161 incident notice. #2162 (staging, ruling 1) sits in the lane without gating. All six are listed under D.
  - **Filed with them:** #2163 (GitHub identity ADR, C, a seam ahead of H, C and D); #2164 (waitlist) and #2165 (abuse limits) in PUB (ruling 6: waitlist first, after the inner-circle invitations). #2156 (Send feedback findability, CXO) is in E.
  - **Rulings 3 to 5** (ESSENCE 6 rewrite, PRD/spec after 1.0, PDR-001 wording) are Arch's and CXO's to record. F28 waits on xian.
- **Not yet on the board:** H, D and V have no Sprint options, so their issues read unset or under the nearest PROD-* bucket. Adding an option is a field-definition change, which is xian's to make in the web UI, never an API full replace. The map review (Exec, 17:54) decides whether the board should carry these sprint names at all.

**The ask** (xian, 10-23 16:57, via Exec): "start looking at the issues in the Production milestone and organizing them into potential sprints. We know we will discover more along the way and we already have a proposed first sprint during the private beta that we use a gate for public beta but the rest is still wide open."

**The population:** 230 open Production issues, read from the project board at 17:2x. 116 carry no Sprint value. 9 still carry the retired "Beta Blockers - Hard Gates Only" value. The rest sit in eight PROD-* or PUB buckets from the July sweep. Three open Production issues were missing from the board (#1918, #2107, #2138); PPM added them today.

## The shape

Production's own close is 1.0 / GA (`release-model.md` §2). Named front-loaded subsets gate earlier audiences. PUB, the MCP path, already gates public beta. This proposal keeps that and orders the rest by **what the next audience would hit first**:

| # | Sprint (proposed) | Why this place in the order | Open |
|---|---|---|---|
| 1 | **PUB: Public Beta gate** (unchanged) | xian's ratified gate (ESSENCE v1.0, 08-30). It runs through the private beta. | 24 |
| 2 | **H: Honesty sweep** (no false "none", "0", "not connected", "I can't see it") | xian approved the systematic sweep at 16:57: Arch scopes it, and Lead builds it after #2132. Design partners will hit these first, and each one is a Class 3 shape. Arch scoped it at 17:04 as **#2151** (placed Production by PPM), not #1423, because this week's served instances had no broad `except` for #1423's scanner to find. The list below is input to #2151's inventory, not a substitute for it. | 27 |
| 3 | **D: Data boundaries and terms** (ownership, isolation, keys, Terms, legal) | xian, 10-16: the Terms and legal review come before any outside user beyond the design partners. The owner-id and isolation work is the same promise in code. | 31 |
| 4 | **C: Connectors complete** (GitHub, Calendar, Notion on the #1232 contract, published OAuth apps) | v18.7(kk): the core connectors must finish to close Production. #2087 (Google verification) is submitted. | 24 |
| 5 | **V: Conversation reliability** (multi-intent, armed offers, routing, catalog cost) | Correctness of the chat path beyond the honesty class. #2145 and #2149 (catalog cost and size) sit here, with #1011 (slash-command precedence) decided alongside them. | 32 |
| 6 | **E: Experience polish** (layout, dialog copy, nav) | CXO-led. These are visible and irritating, but not false. | 28 |
| 7 | **T: Trust and learning** | #2135 (trust never progresses) makes the PDR-002 gradient inert today. The rest follows it. | 15 |
| 8 | **Doc: Documents** | Follows #2132's family table. | 8 |
| 9 | **Dist: Distribution** (marketplace, MCPB, plugin, onboarding skills) | Most of it waits on PUB's MCP path. | 5 |
| — | **Q: Health lane** (CI, tests, mypy, dead code), proposed as a standing share of every sprint, not a sprint of its own | Main is red today and the CI target isn't ruled (Exec 16:57, "not ruled"). A share keeps it moving without parking product work. | 16 |
| — | **R: Re-triage, done 10-23 (moved out)** (#371 time-series DB, #482 KMS, #557 WebSockets, #1061 multi-OAuth infra, #1209 mutating auto-exec) | Speculative infrastructure, likely Enterprise or Dot Releases. Placement is PPM's call, but I'll hold it until xian reads this. | 0 (moved out: #371, #1061 Enterprise; #557, #1209, #1219 Dot Releases; #482 back in D) |

Total: 210 open (#2155 added to V 10-24; 12 filed or moved in, then 27 moved to Ongoing and 3 closed on ruling 2, 10-24) (refreshed 19:11 10-23 from the board, then #2137 closed and the round-2 C5/F29 moves at 21:36; 230 at 17:2x before R, #957, #958, #366, #2132's #2138 and #2152 left, and #2151 joined).

## Choices xian may want to make

1. **The order of 2 to 4.** PPM's lean is H, then D, then C. The partners' first harm is a false answer. D's Terms row must close before outside users beyond the partners. C is the longest pole to 1.0.
2. **The health lane as a share, or its own sprint?** If it's a share, what share? PPM has no basis to pick a number before the CI ruling.
3. **The 9 issues carrying "Beta Blockers - Hard Gates Only"**: re-label them to the proposed sprints when the board is touched.
4. **Re-triage R** out of Production (PPM's placement), yes or no.

Sizes are counts, not effort. Nothing here is estimated. We'll discover more along the way, as xian says, so this is a starting order, not a plan of record.


## Every open issue, by proposed sprint

"was" is the board's Sprint value at the 19:11 refresh ("—" for none).

### PUB: Public Beta gate (24)

| # | Title | was |
|---|---|---|
| #1378 | Auth security polish (from #441 Phase 4): CSRF [PUBLIC-BETA GATE per PM 7/7] + lockout, timeout warnings, U… | PUB |
| #1379 | Config hygiene follow-ups from #1324 audit (post-beta) | PUB |
| #1462 | EPIC: Hosted MCP endpoint + plugin distribution (PDR-006 implementation) | PUB |
| #1537 | FTUX-COMPOSER: chat input doesn't grow — you cannot read your own message before sending, and it gates the … | PUB |
| #1538 | FTUX-ELICITATION: progressive elicitation — one thing at a time, reflect between steps, goal-driven not har… | PUB |
| #1539 | FTUX-PURPOSE: 'what uncertainty is it reducing for me' — the only lens item with no twin, and the closest t… | PUB |
| #1540 | FTUX-NAV: primary navigation hidden in the avatar/settings pill — findability, not taste (CXO re-ruling) | PUB |
| #1551 | EPIC: Per-user isolation — Production scope (split from #1419 per PM ruling 2026-08-09) | PUB |
| #1553 | Status-truth F6-F10: remaining surfaces after IntegrationStatusService landed (#1547 slice 2) | PUB |
| #1591 | Standup two-modes: Production/PUB half — first-run interactive fallback + preference capture on #1510's dec… | PUB |
| #1612 | Multi-LLM-provider support before public beta — OpenAI/Gemini genuinely reachable, not just code-complete | PUB |
| #1624 | Chat document-summarize: finish #1187's deferred branch — the capability PM remembers has not worked in cha… | PUB |
| #1658 | PROTOTYPE PARITY: chat-side file upload (UI element + drag-drop), file→project connection, and contextual l… | PUB |
| #1673 | AUDIT: held-state parity — equip Piper (the agent) with the operating discipline the cohort has proven on i… | PUB |
| #1701 | MCP-path increment 2: create a GitHub issue from natural language (host LLM drafts, tool files) | PUB |
| #1702 | MCP-path increment 3: todos and reminders (first Piper-native persistence) | PUB |
| #1703 | MCP-path increment 4: morning standup (north star; honesty-under-recomposition probe must run inside this i… | PUB |
| #1704 | MCP-path increment 5: document knowledge base (upload → chunk → embed → cited answers) | PUB |
| #1705 | MCP-path increment 6: "same Piper" cross-session memory (preferences/working-mode, resource not tool) | PUB |
| #1706 | MCP-path increment 7: calendar tool exposure on the plugin surface (depends on #1441's connector port) | PUB |
| #1707 | MCP-path increment 8: trust-gated proactivity — PLACEHOLDER, do not build until the plugin-surface trust-gr… | PUB |
| #2164 | Waitlist sign-up with batch admission (after the inner-circle invitations) (10-24) | — |
| #2165 | Per-account rate and abuse limits, with a user-facing line when a limit is hit (10-24) | — |
| #2168 | Plugin surface rubric: ratify CXO's v0.1 and run it per increment as the precondition for #1701-#1707 (10-24) | PUB |

### H: Honesty sweep (27)

| # | Title | was |
|---|---|---|
| #1427 | /api/v1/todos REST surface is mocked end-to-end: fabricated responses, nothing persists, hardcoded default-… | — |
| #1525 | Todo handlers' string-return contract cannot carry failure — call sites wrap ALL returns in success=True (r… | — |
| #1552 | Insight repo: three sibling one-bad-row kill-all reads (get_for_object / get_unsurfaced / get_for_context) | — |
| #1554 | Created issues use raw command text as description (f-string fallback ships the user's sentence as the body) | — |
| #1961 | [HONESTY] 'show my todos' reply renders an OPEN overdue todo with strikethrough (~~revise the pr~~) — LLM-c… | — |
| #1963 | [HONESTY] Populated Radar with a failed source shows no disclosure (partial render reads as complete) — fol… | — |
| #1995 | [HONESTY] GitHub token missing a permission reads as an empty result (e.g. no Pull requests: Read -> 'my pu… | — |
| #2010 | [HONESTY] list_projects renderer offers things nothing is armed to do (empty state and closing question) | — |
| #2011 | Unarmed-ask census (#1766) scans 2 packages; 67 holder sites elsewhere in services/ escape it (34 in consci… | — |
| #2022 | MCP github-issues payload doesn't say what it searched (assignee:@me across all repos), so Claude attribute… | — |
| #2042 | Floor LLM narrates actions or data that code never produced (class tracking; #2033, #2040) | — |
| #2074 | Revoked Calendar/Slack tokens still read 'connected' on the four #2072 surfaces: extend needs-reconnecting … | — |
| #2093 | "Is my calendar connected?" answers with the integrations setup boilerplate: lists all four as Connected, t… | — |
| #2107 | Chat says 'usually a brief outage — try again in a moment' when the cause is the Anthropic workspace usage … | — |
| #2125 | Setup wizard reports the server's encryption misconfiguration as a key 'Validation error' (staging: 'master… | — |
| #2134 | Semantic boundary detector: a failed check is cached as clear and recorded as a pass (48/63 turns off, unse… | — |
| #2147 | "show all events" answers with today's meeting time only and omits the week's other events, without saying … | — |
| #2150 | Calendar: a later revoke of calendar access in the user's Google account leaves Settings saying connected u… | — |
| #2151 | Sweep: every reply that reads user data says 'none / 0 / not connected / can't see it' only on a verified r… | — |
| #1487 | renderInboundStatus lives inside a Jinja template — the branch deciding what users are told is unreachable … | — |
| #2103 | Ten templates call an undefined global showToast() (121 call sites); toast.js exposes Toast.success/error, … | — |
| #1828 | TZ-PROJECT: per-user timezone / time-handling fix — parent for #1493's 6 F-slice children | PROD-DESIGN |
| #1550 | All-day calendar events render as 'at 12am' — technically the stored time, maladroit to humans | — |
| #1535 | Reminder times display in UTC — per-user timezone rendering (1521 follow-on) | — |
| #1915 | [TIMEZONE] 'set it back to pacific time' is refused — accept common zone names/abbreviations (Pacific, PT, … | — |
| #2167 | UX (class 3): the API key Remove dialog says "we destroy our copy immediately"; backups keep it up to about five days (10-24; proposed for MVP) | — |
| #2045 | Integrations card after a successful Test keeps 'Not checked yet. Press Test.' and '0 of 4 healthy' until… (added 10-24: missing from the plan, found by the map generator) | — |

### D: Data boundaries and terms (31)

| # | Title | was |
|---|---|---|
| #482 | SEC-KMS-INTEGRATION: Migrate from environment variable to AWS KMS | PROD-INFRA |
| #1203 | KeyAuditService query/report surfaces unwired — deferred to M5 reconsideration with the hosted-credential w… | PROD-INFRA |
| #1257 | [REFACTOR] P7 cutover: migrate user_id→owner_id reads + drop user_id (deferred from #1252) | PROD-INFRA |
| #1345 | Route all LLM-billing paths through one fail-closed wrapper (m-36 structural end-state for #1343's ratchet … | PROD-INFRA |
| #1499 | Route-surface audit (PM-directed, 8/7): 7 unmounted routers, 4 duplicate-purpose OAuth starts, UI calls to … | — |
| #1531 | tests/security/test_cross_user_isolation.py has NO teardown — hardcoded fixture rows persist in shared dev … | — |
| #1561 | ProjectQueryService by-id reads remain owner-unscoped + ProjectContext.resolve_project does global cross-te… | — |
| #1817 | [TASK] Invalidation trigger: consent-from-key-presence stops being safe the moment a de-authorize surface e… | PROD-INFRA |
| #1911 | MCP OAuth consent page: brand it, and show the user's name/email instead of a raw UUID | — |
| #1918 | MCP: 'Connected apps' in Settings, so users can see and revoke ChatGPT/Claude access from Piper | — |
| #2009 | owner_id is NULLABLE on 8 user-data tables that have no other owner column: count the NULLs, then NOT NULL | — |
| #2013 | knowledge_nodes/knowledge_edges owner_id: the KG write routes store rows the owner-filtered reads can never… | — |
| #2014 | items: a base item row with no list has no owner path (list_id nullable, no FK); add CHECK (item_type <> 'i… | — |
| #2016 | 10 DB-bound unit tests insert rows with random owner ids and fail on an empty migrated database (users FK):… | — |
| #2021 | Soft delete with an undo window for todos, then bulk delete may return (xian's 10-14 ruling, PPM's option C… | — |
| #2043 | OAuth redirect defaults: GitHub handler and calendar wizard fall back to localhost, not PIPER_BASE_URL (#13… | — |
| #2062 | Terms of Service published before Production, every commitment mapped to a mechanism (xian's Option 2, 10-16) | — |
| #2063 | Legal review of Terms before any outside user beyond the design partners (xian 10-16: 'a good cutoff') | — |
| #2086 | Admin grant on Fly was never applied: migration a1599 keys on username 'dinp', which does not exist in the … | — |
| #2109 | Inversion and preclaim shadows spend the requesting user's own LLM key (the task inherits the request's key… | — |
| #2123 | Activity reads (status report, analyze commits) use the deployment's GitHub token instead of the account's … | — |
| #2136 | Seat identity: GitHub App for agents so seats stop acting as the admin account (xian approved the route 10-… | — |
| #2157 | Production DB: scheduled backups and retention, one timed restore drill on a short-lived copy (five proof… (10-24) | — |
| #2158 | Account deletion in product with a real purge, and a deletion record kept outside the snapshot (re-applie… (10-24) | — |
| #651 | FUTURE-CONSCIOUSNESS: Account Deletion confirmation pattern (10-24) | Fast Follow |
| #336 |  DATA-SOFT-DELETE: Implement Soft Delete Strategy Across Domain Models (10-24) | Fast Follow |
| #2159 | Export everything Piper holds for a user, in open formats (read against the owner-id inventory) (10-24) | — |
| #2160 | Support intake and the 'tell us' loop: one queue, a named owner, a response window the Terms can state (10-24) | — |
| #2161 | Incident notice to users: an in-app banner during an outage, an after-note, and prepared words for data l… (10-24) | — |
| #2162 | Staging instance for destructive tests and promotion rehearsal: synthetic data only, never restored from … (10-24) | — |
| #2166 | Todo/list/project Share: the UI sends user_to_share_with but the API requires user_id (422); with user_id the API answers 500 (10-24; E → D 10-24, hidden on alpha meanwhile) | — |

### C: Connectors complete (24)

| # | Title | was |
|---|---|---|
| #1051 | POST-MVP: GitHub query state/prerelease filters (milestones state, releases prerelease) | PROD-RECONNECT |
| #1323 | RECONNECT tech-debt: extract BindingBackedConnector mixin (dedupe connector-protocol logic across adapters) | PROD-RECONNECT |
| #1327 | RECONNECT: GitHub target resolution — hierarchy (explicit→infer→ask→default) + default-repo mechanism | PROD-RECONNECT |
| #1336 | [placeholder] Expand/refactor canonical-query regression for connector states + trust properties | PROD-RECONNECT |
| #1352 | RECONNECT-WS4 follow-up: migrate calendar to the shared degrade(reason) contract + apply to other connector… | PROD-RECONNECT |
| #1359 | cli/commands/notion.py: self.adapter referenced 10x but never assigned (AttributeError waiting to happen) | PROD-RECONNECT |
| #1361 | Notion: repoint legacy services/integrations/mcp/notion_adapter.py callers to canonical + delete shim | PROD-RECONNECT |
| #1362 | Notion adapter: rate-limiting tests reference removed _call_notion_api/configure_notion_api (pre-SDK-migrat… | PROD-RECONNECT |
| #1363 | test_publish_creates_actual_notion_page: hardcoded fallback test-parent page ID is dead | PROD-RECONNECT |
| #1376 | Follow-up to #1279: ~23 more fresh-GitHubIntegrationRouter sites (intent_service, context_assembler, canoni… | PROD-RECONNECT |
| #1440 | EPIC: RECONNECT R2 — Production connector gate: GitHub · Google Calendar · Notion complete on the #1232 con… | — |
| #1441 | RECONNECT R2: Google Calendar — full port to the #1232 Connector contract | — |
| #1442 | RECONNECT R2: Notion — full port to the #1232 Connector contract | — |
| #1514 | Published OAuth apps for ALL FOUR core connectors (Calendar, Slack, GitHub, Notion) — kill bring-your-own-c… | — |
| #1916 | Calendar Connect: tell testers up front when the Google OAuth audience excludes them, and record started-ne… | — |
| #1917 | GitHub: 'PRs needing review' has no operation — list_prs is author-scoped, stale_prs is age-based (CXO ruli… | — |
| #1966 | GitHub has two credential resolvers (OAuth grant vs per-user PAT) that disagree; converge on one resolver i… | — |
| #1983 | Settings → GitHub: recommend fine-grained read-only PATs (not classic repo-scope) in the token hint | — |
| #2036 | GitHub Test says 'needs re-authorizing' after a deliberate Disconnect when a personal token serves | — |
| #2053 | Stale grant with a PAT serving: the Integrations card has no Reconnect button, and pressing Test prints the… | — |
| #2087 | Google OAuth consent screen is Internal user type: only Workspace accounts on PM's domain can connect Googl… | — |
| #2106 | PAT-leg GitHub create fails with McpError unknown tool "issue_write", and the reply says it "may or may not… | — |
| #2130 | Calendar asks: no weekday lookup; conflict check answers a multi-person question the user didn't ask | — |
| #2163 | GitHub identity: one app/token model and whose token serves a read (ADR plus carrying it into the six iss… (10-24) | — |

### V: Conversation reliability (32)

| # | Title | was |
|---|---|---|
| #1468 | Canonical judge calibration: STRICT bar has no ratified threshold, judge scores vary run-to-run (same respo… | — |
| #1473 | Multi-intent turns of two QUERY-category halves fail both and return the generic fallback (orchestrator has… | — |
| #1555 | Surface-1 self-inconsistency: pre_classify vs _get_github_action diverge on milestone routing — one decisio… | — |
| #1563 | Floor-prose offers dangle: 'Want me to pull up your reminders?' → 'yes' executes nothing (offer-binding cov… | — |
| #1586 | Collapse the #902 in-handler close-confirm into the #1190 rail gate (redundant two-step UX on the rail path) | — |
| #1619 | Registry: four mutations filed under the read-only QUERY category (create/close/reopen/comment issue) — saf… | — |
| #1632 | Capability-legibility catalog should state outwardness per action ('visible to others') now that the axis e… | — |
| #1841 | [TESTS] pm039 live-LLM param 'show me all project plans' consistently classified manage_portfolio by gpt-4o… | — |
| #1854 | [TESTS/LLM] Live canonical accuracy under bar — identity 92% (<95%), temporal + overall also red; newly VIS… | — |
| #1891 | [DESIGN] The floor's capability_manifest_block (137 raw action names, every turn) is what 'what can you do?… | — |
| #1931 | Completed todos can't be reopened from chat (reopen_todo exists, no chat route) | — |
| #1932 | Chat cannot edit/rename/update a project (no update capability; floor is the honest answer until built) | — |
| #1935 | Chat can't delete a project: wire delete through the #1190 destructive tier (follow-up to #1930 step 2) | — |
| #1943 | [ARCH] Todo/reminder target + clear-verb interpretation should consume the router's extracted args, not reg… | — |
| #1949 | [ROUTING] 'show me all project plans' classifies as PORTFOLIO/manage_portfolio, not a document search (live… | — |
| #1955 | Ask-and-wait dead end: "which reminder would you like to close?" leaves the next reply with nothing to land on | — |
| #1962 | Subject-less advice asks ("what's your advice here"): 'you might have sent that before it was ready' blames… | — |
| #1970 | Consent framing (imperative vs ambiguous) moves to the router as a structured arg; _EXECUTE_RE becomes a ra… | — |
| #1984 | [KNOWN MISS] Cold two-topic 'summarize my current work and I need the archived list too': router reads 'my … | — |
| #2023 | Standup interview swallows the user's own requests as answers (a question or 'do a standup' lands in the dr… | — |
| #2024 | Contextual offers (#852 offer_hint) arm only on a single yes/no question: drop directive arms, single-offer… | — |
| #2025 | Delete gate reads 'delete todo 1 and 2' as todo 1 only; the second item is silently dropped | — |
| #2030 | Multi-intent path renders canonical builders' questions unarmed: IntentOrchestrator._execute_single keeps o… | — |
| #2041 | Multi-intent path drops write offers: IntentOrchestrator._execute_single does not carry write_offer | — |
| #2057 | Surface 1 claims 'how do I archive my project Foo?' as PORTFOLIO/manage_portfolio, and the legacy branch ar… | — |
| #2133 | "Create issues from this meeting's action items" gets a single-subject prompt: #886's batch decline is stra… | — |
| #2145 | Router and classifier calls send the full ~3.3k-token catalog uncached: enable Anthropic prompt caching on … | — |
| #2149 | Router catalog size: single op or example additions move unrelated rows; decide a catalog shape before more… | — |
| #1011 | ARCH-DESIGN: Slash-command dispatch precedence — post-MVP design decision needed | PROD-DESIGN |
| #2155 | UX: "What's on my agenda?" with no calendar answers about meeting-time analysis (placed 10-24) | — |
| #2169 | Chat delete: a list-item remove ask gets a confirmation for a different object (the prior turn's to-do) (10-24; class pending Lead's pin) | — |
| #2170 | Chat: remove an item from a list (a list-item rail), with exact-match arming and an id-bound confirm (added 10-24: missing from the plan, found by the map generator) | — |

### E: Experience polish (28)

| # | Title | was |
|---|---|---|
| #1043 | En-masse copy review pass for new M2e handlers + standup prompts | PROD-DESIGN |
| #1090 | UI-1.0-PLAN: scope conversation history + settings UI surfaces for 1.0 launch | PROD-DESIGN |
| #1183 | VOICE-LINT: attention/spatial references must stay present-tense + session-scoped (no implied cross-session… | PROD-DESIGN |
| #1186 | PIPER-SELF-KNOWLEDGE: support info + help-doc pointers + RAG over own docs (so Piper can answer 'how do you… | PROD-DESIGN |
| #1249 | Design-floor primitive: inline-editable text (D2, sibling to Dialog #1170) | PROD-DESIGN |
| #1284 | [DESIGN] 'Your stuff' nav group — nomenclature (CXO + Comms) + maybe a parent hub route | PROD-DESIGN |
| #1288 | [DESIGN] Standup content curation + home morning-card (#1269 follow-on, post-beta) | PROD-DESIGN |
| #1290 | [D2][DESIGN] Nav menu structure — work/learning/insights/settings top-level + a Settings submenu? (PM quest… | PROD-DESIGN |
| #1298 | Remove dead templates/components/navigation.html + retire its dead-code tests (once nav_rail #1280 confirme… | PROD-DESIGN |
| #1347 | Conversation history viewer: full backward pagination + transcript-completeness failsafe (follow-on to #1235) | PROD-DESIGN |
| #1350 | [BUG] settings_projects.html missing tokens.css / toast.js / nav include — 3 test failures (pre-existing, u… | PROD-DESIGN |
| #1483 | TRUST-COPY follow-on: four latent 'cannot be undone' defaults remain in dialog.js — unreachable today, but … | — |
| #1495 | localStorage chat fallback never persists assistant replies — the degraded-render surface that made #1489 p… | — |
| #1515 | Conversation switching flash-rebuilds the entire screen — PM: 'a distracting, sloppy, unprofessional experi… | — |
| #1516 | Conversation delete/archive have NO reachable UI — the affordances live in home.html's superseded sidebar, … | — |
| #1519 | Insight Journal page ignores the design system — PM: 'designed randomly… breaks the nav. Really goofy looking' | — |
| #1523 | SessionTimeout.logoutUrl points at nonexistent /logout UI route — works only via the login-bounce accident | — |
| #1546 | Dialog copy voice pass: honest but awkward phrasing on delete/remove dialogs — PM: 'strangely written, soun… | — |
| #1564 | iPad Safari layout float: large empty content block, composer detached mid-page, greeting scrolls under too… | — |
| #1609 | No user-reachable surface exists for editing personal context (role/priorities) — the overlay is file-only … | — |
| #1625 | Reminder surfacing is relentless — PM design ruling: pin due reminders to the top of Radar, mention in conv… | PROD-DESIGN |
| #1907 | [RENDER] iPad (Safari) layout on alpha: portrait new-chat shows an empty full-height gray panel with the co… | PROD-DESIGN |
| #1945 | [UX] Project Config page lists the same repo under 'Linked Repositories' and 'Integrations'; no surface sho… | — |
| #1946 | [RADAR] Radar did not refresh after a reminder was completed in chat — the cleared reminder stayed pinned a… | — |
| #1957 | [WEB] Personality page: 'Reset to Defaults' reloads with a query string and leaves Warmth at its saved value | — |
| #2099 | Invites page: minting a code does not refresh the list (revoke does) on alpha e801b1a309; xian's read after… | — |
| #2116 | [UX] "What makes you different?" asked a fifth time is answered with a question about motive, no answer (se… | — |
| #2156 | UX: Send feedback is a quiet footer link, and absent from the setup wizard and error pages (10-24) | — |

### T: Trust and learning (15)

| # | Title | was |
|---|---|---|
| #558 | MUX-STANDUP-CONVERSE: LLM-based preference extraction | PROD-TRUST |
| #954 | TRUST-LITE: Trust graduation via context (lightweight implementation) | PROD-TRUST |
| #955 | PREF-INFER: User-correctable preferences (Claude memory model) | PROD-TRUST |
| #956 | LEARNING-SURFACE: Trust-graduated learning surfacing | PROD-TRUST |
| #1062 | CORE-LEARN-PHASE-3: Learning infrastructure phase 3 (broken out from #471) | PROD-TRUST |
| #1131 | CANONICAL-TODO-JUDGE-ARTIFACT: stateless judge flags honest todo responses as fabrication (canonical-test u… | PROD-TRUST |
| #1139 | Audit task: which PremonitionService methods are dead vs used? frame_insight_for_surfacing IS production-used | PROD-TRUST |
| #1174 | BEING-GOOD-PROACTIVE-PRESENCE: discovery thread — proactive relevance / notifications (when + how Piper nud… | PROD-TRUST |
| #1217 | ETHICS-FLOOR-PERSONHOOD-ASSUMPTION: floor should not assume sapient/human personhood for role-named parties… | PROD-TRUST |
| #1326 | M4: Introduce-person flow — People entity (Option A, user_confirmed provenance) | PROD-TRUST |
| #1377 | Insight provenance: add is_seed/source field to InsightDB + surface it (full fix deferred from #1216) | PROD-TRUST |
| #1735 | The personalization 'learning loop' is disconnected at every joint: auto-apply is a silent no-op, the learn… | PROD-TRUST |
| #2056 | Preference hook never fires on a cache hit or a context-free miss (reads user_id from an empty context); co… | — |
| #2135 | Trust stage never progresses: no turn path records an interaction, so every account stays at Stage 1 and st… | — |
| #1509 | TRUST-CONSENT: consent gate + capability legibility — one feature (Jake alpha FTUX; PPM's hold-a-release … (added 10-24: missing from the plan, found by the map generator) | — |

### Doc: Documents (8)

| # | Title | was |
|---|---|---|
| #302 | CONV-MCP-DOCS: Unified Document Processing via Skills | PROD-DOCS |
| #712 | MUX-DOCUMENT-VIEWER: Create Document Viewer with Lifecycle | PROD-DOCS |
| #713 | MUX-DOCUMENTS-LIFECYCLE-UI: Wire Lifecycle to Documents View | PROD-DOCS |
| #1175 | SOURCE-TYPE-SLOT-LOCATION: revisit intent.context vs intent.slots for source_type (post slot-filling unific… | PROD-DOCS |
| #1202 | FILES-FOLLOW-ON: G65 artifact persistence (export/share/versions) + tagging full release — split from #313 | PROD-DOCS |
| #1246 | ARTIFACT-EXPORT-FORMATS: pdf/docx export + save-time format picker (#1184 follow-on) | PROD-DOCS |
| #1270 | [D1] Refactor /documents · /files around the Document source-type object model (uploaded/generated/federated) | PROD-DOCS |
| #2139 | "Create a doc from this conversation" and "Synthesize these sources" on an OpenAI-only account reply with t… | — |

### Dist: Distribution (5)

| # | Title | was |
|---|---|---|
| #966 | DIST-VISUAL-IDENTITY: Visual identity for the plugin and MCP Apps surfaces (the MCPB half dropped, supersed… | PROD-DIST |
| #1242 | MEET-PIPER-GITHUB — Add GitHub connector setup step to meet-piper onboarding | PROD-ONBOARD |
| #1244 | CONSULT-ENRICH-FIX — Fix two enrichment layer bugs blocking consult-piper (Cowork/GitHub + Code/payload) | PROD-ONBOARD |
| #1245 | PIPER-SKILL-MERGE — Collapse ask-piper + consult-piper into one smart piper skill | PROD-ONBOARD |
| #1282 | BYOC-DIST — Plugin packaging and marketplace distribution | PROD-DIST |

### Q: Health lane (16)

| # | Title | was |
|---|---|---|
| #1224 | Pre-existing test failures (3 clusters: standup conversation-state, perf-indexes, error-message integration… | PROD-TECHDEBT |
| #1349 | [BUG] test_github_place_has_name asserts repo name in Place.name but Place.name is just 'GitHub' (pre-exist… | PROD-TECHDEBT |
| #1357 | test_github_api_connection.py's live 401s appear only in large combined test runs — likely GitHub rate-limi… | PROD-TECHDEBT |
| #1367 | test_execution_intent_no_placeholder fails: mocks .classify but code calls .classify_multiple | PROD-TECHDEBT |
| #1371 | Test-collection fragility: ModuleNotFoundError for real packages (services.configuration/services.cache) wh… | PROD-TECHDEBT |
| #1372 | tests/intent/contracts/: 42 pre-existing failures, ContainerNotInitializedError (ServiceContainer test frag… | PROD-TECHDEBT |
| #1385 | tests/security cross-file fixture contamination: full-suite runs leak 1111/2222 fixture rows, making isolat… | PROD-TECHDEBT |
| #1437 | Stale integration test: test_get_default_project_query pins a 422 the pipeline no longer returns (pre-exist… | — |
| #1439 | Pre-existing: two llm_config_service tests read the machine's REAL keychain (fail on any host with a stored… | — |
| #1451 | settings/projects template test fails: test_template_includes_navigation (pre-existing) | — |
| #1452 | Full Test Suite backlog: 413 failed + 71 errors (suite's first real run in weeks) — burn-down + honest inte… | — |
| #1479 | Flaky (order-dependent): test_github_query_handlers TestCommentIssueResults::test_formats_comment_confirmat… | — |
| #1494 | ADR-059 blanket skip on test_portfolio_service.py also disables pins for the LIVE archive/restore extractio… | — |
| #1506 | tests/domain/test_file_reference_detection.py classification tests fail keyless (ContainerNotInitializedErr… | — |
| #1528 | test_validate_openai_key_success hits the LIVE OpenAI API with the real keychain key — network-dependent te… | — |
| #1549 | GET /api/v1/todos/shared-with-me is shadowed by /{todo_id} route order — matches as todo_id='shared-with-me' | — |
