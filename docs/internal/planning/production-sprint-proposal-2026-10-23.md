# Production milestone: proposed sprints (PPM, 2026-10-23)

**Status: ORDER RATIFIED** (xian, 2026-10-23 17:54, via Exec: "I approve all 4 questions for me"; decisions.log). No dates; PPM proposes none.
- **Order:** PUB, then H, D, C, then V, E, T, Doc, Dist.
- **Q** is a standing share of every sprint. Its size is open until the CI ruling.
- **H, D and V carry their own Sprint options (10-25):** xian added `PROD-HONESTY - Failed Reads Say So` (xian renamed it to title case at 14:04, same option id), `PROD-DATA - Data Boundaries, Privacy & Terms` and `PROD-CONVO - Conversation Reliability` at 12:40 (60 options). PPM set every H, D and V row per item, closed rows included: H 29, D 31, V 32, 92 of 92 read back. This moved #1828 and #1011 off PROD-DESIGN, and D's five PROD-INFRA rows (#482, #1203, #1257, #1345, #1817) to PROD-DATA. The other sprints keep today's options.
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
    - #1242, #1244 and #1245 wait on F28. **Settled 10-25 14:09:** xian has no need for the skunkworks PoC plugin; all three closed not planned, and #1242's GitHub-connect intent is an acceptance line on #1462.
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
| 1 | **PUB: Public Beta gate** (unchanged) | xian's ratified gate (ESSENCE v1.0, 08-30). It runs through the private beta. 10-28: the confabulation diagnosis (#2042) and its kin (#2183, #2185, #2186) moved in on xian's word. | 28 |
| 2 | **H: Honesty sweep** (no false "none", "0", "not connected", "I can't see it") | xian approved the systematic sweep at 16:57: Arch scopes it, and Lead builds it after #2132. Design partners will hit these first, and each one is a Class 3 shape. Arch scoped it at 17:04 as **#2151** (placed Production by PPM), not #1423, because this week's served instances had no broad `except` for #1423's scanner to find. The list below is input to #2151's inventory, not a substitute for it. | 26 |
| 3 | **D: Data boundaries and terms** (ownership, isolation, keys, Terms, legal) | xian, 10-16: the Terms and legal review come before any outside user beyond the design partners. The owner-id and isolation work is the same promise in code. | 31 |
| 4 | **C: Connectors complete** (GitHub, Calendar, Notion on the #1232 contract, published OAuth apps) | v18.7(kk): the core connectors must finish to close Production. #2087 (Google verification) is submitted. | 24 |
| 5 | **V: Conversation reliability** (multi-intent, armed offers, routing, catalog cost) | Correctness of the chat path beyond the honesty class. #2145 and #2149 (catalog cost and size) sit here, with #1011 (slash-command precedence) decided alongside them. | 31 |
| 6 | **E: Experience polish** (layout, dialog copy, nav) | CXO-led. These are visible and irritating, but not false. | 28 |
| 7 | **T: Trust and learning** | #2135 (trust never progresses) makes the PDR-002 gradient inert today. The rest follows it. | 15 |
| 8 | **Doc: Documents** | Follows #2132's family table. | 8 |
| 9 | **Dist: Distribution** (marketplace, MCPB, plugin, onboarding skills) | Most of it waits on PUB's MCP path. | 5 |
| — | **Q: Health lane** (CI, tests, mypy, dead code), proposed as a standing share of every sprint, not a sprint of its own | Main is red today and the CI target isn't ruled (Exec 16:57, "not ruled"). A share keeps it moving without parking product work. | 16 |
| — | **R: Re-triage, done 10-23 (moved out)** (#371 time-series DB, #482 KMS, #557 WebSockets, #1061 multi-OAuth infra, #1209 mutating auto-exec) | Speculative infrastructure, likely Enterprise or Dot Releases. Placement is PPM's call, but I'll hold it until xian reads this. | 0 (moved out: #371, #1061 Enterprise; #557, #1209, #1219 Dot Releases; #482 back in D) |

Total: 243 open (recounted 10-31 06:54 from `gh issue list --milestone Production`; #2242 added to PUB beside #2175 10-31, the hosted MCP access decision; #2241 added to H beside #2022 10-31, PA's MCP payload size; #2240 closed in D 10-30 22:04, PA, guard fixed and dry-run verified; the 10-30 21:57 line read 241 where the board held 242, and the sections summed to 242; #1509 closed in T 10-30 20:00; #2240 added to D beside #2207, 10-30, PA's MCP deploy guard; #2239 added to PUB beside #2237, 10-30, Lead's #2237 edge; #2238 added to C beside #1442, 10-30, Arch's Notion N1/C1; #2237 added to PUB beside #2229, 10-30, Lead's #2236 follow-up; #2235 added to C beside #1327 and #2236 to H beside #2231, 10-30, Arch's and CXO's; #2234 closed in Q 10-30, superseded by #2232; #2233 added to V beside #2219 and #2234 to Q beside #2232, 10-30, both CXO's; #2232 added to Q beside #2211, 10-30, Lead's local fault-run harness for #2231; #2231 added to H beside #2224, 10-30, Lead's pins-only tracker; #2229 added to PUB and #2230 to V beside #2225, 10-30, both from xian's tracking test; #2225 closed in V 10-30, fix not served; #2228 added to H beside #1828, 10-30, row 2's Q9; #2227 placed Ongoing (router re-baseline, not counted); #2225 added to V 10-30, PA's re-check side finding; #2226 added to Doc and #2223 closed in D, 10-30; #2224 added to H beside #2215 and #2223 to D beside #2222, 10-30, both Arch's; #2215 (H), #2222 (D) and #2210 (Q) closed 10-30; #2222 added to D 10-30 beside #2207, Arch's landing-3 residual; the generator reports 0 unplanned; #2219 and #2220 added to V 10-30, CXO from row 2, and #2221 beside them on xian's word via PA; #2212-#2214 closed 10-29 as duplicates of Arch's #2218, #2216, #2217, which replace them in H; #2215 and those three added to H beside #2151 10-29, its residuals from the status-gather lane; #2210 and #2211 added to Q 10-29, Lead lanes and Arch from #2209; #2200 closed in E 10-29 16:58, served, Sprint set to PROD-DESIGN; #2199 closed in PUB 10-29 16:31, served; #2209 added to PUB beside #2197 and #2208 to H, 10-29; #2207 added to D 10-29, Arch's #2205 read; #2206 added to E 10-29; #2205 filed and admitted MVP, not counted here; #2042 moved to the top of PUB on xian's 13:2x diagnosis ask; #2202 to Q, #2203 to E, #2204 beside #2130, 10-29 from row 3; #2201 filed and admitted MVP 10-29, not counted here; #2184 moved MVP -> PUB 10-29 on xian's known-issue ruling, top of triage with #2195; #2199 added to PUB and #2200 to E 10-29, from row 0; #2197 added to PUB 10-29, #2184's boundary follow-up (#2198 closed as its duplicate); #2195 added to PUB 10-29, #1595's split, Sprint PUB on xian's word; #2194 admitted MVP 10-29, not counted here; #2191, #2192 and #2193 added to H 10-29, #2189 census rows 8, 10, 19; #2190 added to H 10-28, CXO from the #2189 census; #2187, #2188 and #2189 added to H 10-28, from #2018's served run and xian's 15:2x word; #2042 moved H to PUB, #2183 moved V to PUB, #2185 and #2186 added to PUB, 10-28 on xian's word, PA relay 10:22; #2184 admitted MVP, not counted here; #2183 added to V 10-28; #2182 closed in H 10-27 21:33, pins only; #2182 added to H 10-27, #2151's show_standup row; #2177 closed in Q 10-27 07:12; its follow-up #2181 placed Ongoing; #2109 closed in D and #2125, #2172, #2176 in H, 10-26 morning; #2171 closed in H 10-26, served; #2176 to H, #2178 to C and #2177 to Q, 10-25 evening; #2175 added to PUB 10-25, CXO's invited x MCP; #2174 added to C 10-25, Arch's D3 check node; #2173 closed in H 10-25 15:35; #1242, #1244 and #1245 closed as superseded in Dist 10-25; #2173 added to H after the 10-25 snapshot, which matched the board at 206; #2123 closed in D, #2169 in V, #2045 in H and #2156 in E, found 10-25; #1966 closed in C 10-25; #2172 added to H 10-25; #2155 added to V 10-24; 12 filed or moved in, then 27 moved to Ongoing and 3 closed on ruling 2, 10-24) (refreshed 19:11 10-23 from the board, then #2137 closed and the round-2 C5/F29 moves at 21:36; 230 at 17:2x before R, #957, #958, #366, #2132's #2138 and #2152 left, and #2151 joined).

## Choices xian may want to make

1. **The order of 2 to 4.** PPM's lean is H, then D, then C. The partners' first harm is a false answer. D's Terms row must close before outside users beyond the partners. C is the longest pole to 1.0.
2. **The health lane as a share, or its own sprint?** If it's a share, what share? PPM has no basis to pick a number before the CI ruling.
3. **The 9 issues carrying "Beta Blockers - Hard Gates Only"**: re-label them to the proposed sprints when the board is touched.
4. **Re-triage R** out of Production (PPM's placement), yes or no.

Sizes are counts, not effort. Nothing here is estimated. We'll discover more along the way, as xian says, so this is a starting order, not a plan of record.


## Every open issue, by proposed sprint

"was" is the board's Sprint value at the 19:11 refresh ("—" for none).

### PUB: Public Beta gate (37)

| # | Title | was |
|---|---|---|
| #2184 | Chat listed the wrong issues as the MVP milestone's (two-step milestone ask). **Top of PUB triage** (xian 10-29 13:02: "anything like this moved out of MVP … at the top of the triage for the first sprint of the Production milestone"); left MVP as a known issue; Sprint PUB set | MVP |
| #2042 | Floor LLM narrates actions or data that code never produced. **Top of PUB triage: xian 10-29 13:2x asked Arch for a DIAGNOSIS, not a patch, of the floor's unread record claims and its unasked "Also…" asides**; Sprint PUB set | H |
| #2195 | Inversion Phase 3 remainder: 61 surface-1 literals in 18 lists, deleted list by list under the gate (**top of PUB triage**, xian 10-29 13:02; 10-29, split from #1595 on xian's ruling; Sprint PUB set on his word) | — |
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
| #2175 | UX: a person arriving through the plugin or MCP endpoint has no clear path to an invite and an account (10-25, CXO; journey grid invited x MCP) | — |
| #2242 | Hosted MCP: decide who may connect during the beta (no allowlist today; any signed-in account can) (10-31, PPM from PA's MCP ordering; xian's decision via Exec, PPM recommends an allowlist) | — |
| #2183 | Chat ignores a count in "show my last two new issues" and lists every open issue (10-28; moved from V 10-28 with its kin on xian's word) | V |
| #2185 | "You have 261 open issues" counts assigned-to-me across all repos and "most recent" isn't sorted (10-28, split from #2183) | — |
| #2186 | GitHub list reads drop qualifiers (count, milestone, label, state): consume the router's args on the search rail (10-28, Arch; the class fix for #2183/#2184) | — |
| #2197 | A progress ask about a named milestone is answered with the list of every milestone and ignores the one named (10-29, CXO; #2184's boundary follow-up; PPM's #2198 closed as its duplicate) | — |
| #2209 | Naming a milestone the account doesn't have gets another milestone's issues, with no word that it isn't there (10-29, CXO from PA's served read on 48df90eb72; the armed pick's no-match branch, a small fix, not #2042 rung 3; not a gate row) | — |
| #2229 | Public site still invites visitors to the alpha and a beta waitlist after the private beta started (/try, /try/alpha, /get-involved) (10-30, Comms for xian's tracking test; xian decides the visitor path, then Comms, CXO, Web) | — |
| #2237 | Integrations page offers Slack and Notion Connect cards to beta accounts. Move its hard-coded lists onto the one OFFERED_CONNECTORS set (GitHub, Google Calendar) that the capability answer reads (10-30, Lead from #2236. PPM scope position: beta accounts are offered only the letter's two connectors; CXO words the page after seeing it served) | — |
| #2239 | A stale or crafted OAuth callback for a connector outside the offered set returns a JSON 409 body, not a friendly page (10-30, Lead; #2237 edge, UX, which CXO accepted for now) | — |

### H: Honesty sweep (39)

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
| #2241 | MCP what_piper_knows_about_me returns 431k characters: the github section ships 50 raw GitHub API issue objects (10-31, PA's first authenticated live call; one unit with #2022, same function and pins) | — |
| #2074 | Revoked Calendar/Slack tokens still read 'connected' on the four #2072 surfaces: extend needs-reconnecting … | — |
| #2093 | "Is my calendar connected?" answers with the integrations setup boilerplate: lists all four as Connected, t… | — |
| #2107 | Chat says 'usually a brief outage — try again in a moment' when the cause is the Anthropic workspace usage … | — |
| #2125 | Setup wizard reports the server's encryption misconfiguration as a key 'Validation error' (staging: 'master… (closed 10-26, pins only) | — |
| #2134 | Semantic boundary detector: a failed check is cached as clear and recorded as a pass (48/63 turns off, unse… | — |
| #2147 | "show all events" answers with today's meeting time only and omits the week's other events, without saying … | — |
| #2150 | Calendar: a later revoke of calendar access in the user's Google account leaves Settings saying connected u… | — |
| #2151 | Sweep: every reply that reads user data says 'none / 0 / not connected / can't see it' only on a verified r… | — |
| #2218 | #2151 residual, first of three: the hosted MCP profile serves PIPER.md fallback projects over a failed projects read (10-29, Arch; replaces Lead's duplicate #2212) | — |
| #2216 | #2151 residual: the status floor says 'not configured' when the #1590 repo auto-pick could not run; CXO's words "I couldn't check which repository to use just now." (10-29, Arch; replaces #2213) | — |
| #2217 | #2151 residual: GitHub sub-reads skipped under a DB failure render nothing instead of 'could not check' (10-29, Arch; replaces #2214) | — |
| #2215 | #2151 inventory follow-up: get_memory's stale FORCE label; check_completion_status tagged FLOOR-ABSENT but never performed (10-29, Arch's ask); closed 10-30 11:42, Arch validated, red reported as 9 KNOWN_RED + 1 NOT_PERFORMED, its product gap is #2224 | — |
| #2224 | check_completion_status answers completion questions from a gather that never reads completed todos or closed issues (10-30, Arch from #2215's NOT_PERFORMED row; #2042's class) | — |
| #2231 | Tracking: eleven `close:pins-only` closes whose failure path was never served on alpha, with what would serve each (10-30, Lead for xian's tracking test; asks CXO or Arch to rule on the three that can't be forced on alpha) | — |
| #2236 | 'What can you help me with?' is written fresh by the model: it promises learning and proactivity, calls itself honest, and contradicts the setup line (10-30, CXO from xian's first beta reply, Misleading; fix: code renders the ledger's capability lines, and the notice line lands alone first) | — |
| #1487 | renderInboundStatus lives inside a Jinja template — the branch deciding what users are told is unreachable … | — |
| #2103 | Ten templates call an undefined global showToast() (121 call sites); toast.js exposes Toast.success/error, … | — |
| #1828 | TZ-PROJECT: per-user timezone / time-handling fix — parent for #1493's 6 F-slice children | PROD-DESIGN |
| #2228 | False relative time on the STATUS floor: #35, created 15:04 PT today, described as 'updated yesterday evening' (10-30, PA from row 2's Q9 on `ac5b69f865`, child of #1828; CXO: Misleading, predates the build) | — |
| #1550 | All-day calendar events render as 'at 12am' — technically the stored time, maladroit to humans | — |
| #1535 | Reminder times display in UTC — per-user timezone rendering (1521 follow-on) | — |
| #1915 | [TIMEZONE] 'set it back to pacific time' is refused — accept common zone names/abbreviations (Pacific, PT, … | — |
| #2167 | UX (class 3): the API key Remove dialog says "we destroy our copy immediately"; backups keep it up to about five days (10-24; closed 10-24 20:24, `close:served`, never admitted to MVP) | — |
| #2171 | UX (class 3): Lists page card shows "Items: 0" for a list that holds items (10-24, CXO from Web's catch; closed 10-26 04:26, served) | — |
| #2172 | GitHub Disconnect reports success when a credential copy failed to clear (each clear's failure is swallowed) (10-25, Arch) (closed 10-26, pins only) | — |
| #2173 | Standup and Radar show every open GitHub issue as the person's own work when no GitHub username is saved; default to the signed-in login (10-25, Lead; built 7bcef2bd07; closed 10-25 15:35, served row 1 of 2) | — |
| #2176 | Setup wizard step 2 shows Slack and Google Calendar app-credential forms to a new tester (10-25, CXO; class 3; built 2d0c56082a, not served) (closed 10-26, pins only) | — |
| #2182 | Standup shows a failed calendar or source read as a free day or 'no activity' (10-27, #2151's `show_standup` row split out on Arch's advice; #1703 is blocked by it; closed 10-27 21:33, pins only, 1 of 4 rows served on alpha a1f46faafc) | — |
| #2045 | Integrations card after a successful Test keeps 'Not checked yet. Press Test.' and '0 of 4 healthy' until… (added 10-24: missing from the plan, found by the map generator; closed 10-25) | — |
| #2187 | Integrations GitHub card: an unchecked or freshly reconnected grant shows stale or unearned state (10-28, CXO from #2018's served run; E4) | — |
| #2188 | Chat's dead-grant reply gives no next step and renders in the success bubble (10-28, CXO from #2018's served run) | — |
| #2189 | Integrations 'Last checked' lives only in process memory, so every deploy resets it; plus a sweep for other memory-only user-facing state (10-28, PA; xian: not MVP, should be addressed) | — |
| #2190 | A failed OAuth connect is silent for GitHub and shows a raw key for Slack and Calendar (10-28, CXO from the #2189 census rows 17-18) | — |
| #2191 | Half-filled meeting setup (slot-filling session) is lost on a restart (10-29, #2189 row 8, Harmful) | — |
| #2192 | Pending preference hint is lost on a restart, and its confirm route never hydrates the conversation (10-29, #2189 row 10) | — |
| #2193 | Slack's IntentService has no ConversationManager, so Slack offers neither hydrate nor persist across a restart (10-29, #2189 row 19) | — |
| #2208 | Learned-pattern execute route reports a failed action as success and raises the pattern's confidence (10-29, found in #2205's lane) | — |

### D: Data boundaries and terms (30)

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
| #2109 | Inversion and preclaim shadows spend the requesting user's own LLM key (the task inherits the request's key… (closed 10-26) | — |
| #2123 | Activity reads (status report, analyze commits) use the deployment's GitHub token instead of the account's … (closed) | — |
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
| #2207 | repo_clarification resolves a bare repo name under the offer's stored principal when the turn has none (10-29, Arch's #2205 source read; read only, persist guarded) | — |
| #2240 | deploy-mcp.sh's stray-file guard skips gitignored files, so a local config/PIPER.user.md could ship in an image (10-30, PA from #2218; backstop landed on main at 738c2e5f77: .dockerignore and a deploy guard; the deployed MCP v14 is unchanged until xian's ls); closed 10-30 22:04, PA (de1d1bd714 fixed the guard under pipefail; Lead's behavioural pin fcac831ae6; Arch validated 10-31) | — |
| #2222 | Repo question: an owner/name or default answer on a turn with no principal still binds under the offer's stored user (10-30, Arch's landing-3 read; #2207's residual, queued by Lead after the six); closed 10-30 11:00, Arch validated on main | — |
| #2223 | Generic offer accept runs a stored request under the arming user when the turn has no principal; one check at the pop seam (10-30, Arch while validating #2222; on main 4e9d370d06, Arch validated 12:20; closed 10-30 12:55, Lead, with the arm-site inventory; on alpha from the promotion to ac5b69f865) | — |

### C: Connectors complete (28)

| # | Title | was |
|---|---|---|
| #1051 | POST-MVP: GitHub query state/prerelease filters (milestones state, releases prerelease) | PROD-RECONNECT |
| #1323 | RECONNECT tech-debt: extract BindingBackedConnector mixin (dedupe connector-protocol logic across adapters) | PROD-RECONNECT |
| #1327 | RECONNECT: GitHub target resolution — hierarchy (explicit→infer→ask→default) + default-repo mechanism | PROD-RECONNECT |
| #2235 | The repo validator reads only the account PAT, so OAuth-only accounts are never validated: a second credential path beside resolve_credential (10-30, Arch from the #2230 setter unit; partner-visible, because OAuth is the likely beta path; the flip doesn't wait on it) | — |
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
| #2238 | Notion on hosted: a global env key beats the user's own, and a keyless user falls back to it (N1/C1); a saved key can miss the chat read (10-30, Arch from xian's Slack/Notion ask; must close before Notion joins the beta set) | — |
| #1514 | Published OAuth apps for ALL FOUR core connectors (Calendar, Slack, GitHub, Notion) — kill bring-your-own-c… | — |
| #1916 | Calendar Connect: tell testers up front when the Google OAuth audience excludes them, and record started-ne… | — |
| #1917 | GitHub: 'PRs needing review' has no operation — list_prs is author-scoped, stale_prs is age-based (CXO ruli… | — |
| #1966 | GitHub has two credential resolvers (OAuth grant vs per-user PAT) that disagree; converge on one resolver i… (closed 10-25 10:37 on Web's rows; the resolver seam's issue) | — |
| #1983 | Settings → GitHub: recommend fine-grained read-only PATs (not classic repo-scope) in the token hint | — |
| #2036 | GitHub Test says 'needs re-authorizing' after a deliberate Disconnect when a personal token serves | — |
| #2053 | Stale grant with a PAT serving: the Integrations card has no Reconnect button, and pressing Test prints the… | — |
| #2087 | Google OAuth consent screen is Internal user type: only Workspace accounts on PM's domain can connect Googl… | — |
| #2106 | PAT-leg GitHub create fails with McpError unknown tool "issue_write", and the reply says it "may or may not… | — |
| #2130 | Calendar asks: no weekday lookup; conflict check answers a multi-person question the user didn't ask | — |
| #2204 | "This week" calendar read starts at now, so earlier-today meetings drop out; window from local midnight today (10-29, PPM's window call from #1386 row 3 K3) | — |
| #2163 | GitHub identity: one app/token model and whose token serves a read (ADR plus carrying it into the six iss… (10-24) | — |
| #2174 | ADR-081 D3 check: do github-mcp-server and our REST reads accept a GitHub App user access token? (10-25, Arch; blocks #2163 and #1514's GitHub part) | — |
| #2178 | GitHub Disconnect doesn't revoke the OAuth grant at GitHub; revoke it, never a PAT (10-25, Arch) | — |

### V: Conversation reliability (36)

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
| #2219 | Todo replies list the same item over and over, call todos 'reminders', and 'show my todos' doesn't show them (10-30, CXO from row 2 Q55-Q57 on e234776150; not a gate row) | — |
| #2233 | A name question gets an unprompted reminder nudge after the name (10-30, CXO from row 2's Q1, waived on #2221; revisit with #2219) | — |
| #2220 | 'Create issues from this meeting's action items' asks which repository when there are no action items to create from (10-30, CXO from row 2 Q44; not a gate row) | — |
| #2221 | Revisit row 2's 12 waived canonical rows after the 7 standing rows are fixed, so each passes without a waiver (10-30, xian via PA; after #2204, #2219, #2220) | — |
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
| #2169 | Chat delete: a list-item remove ask gets a confirmation for a different object (the prior turn's to-do) (10-24; closed, `close:pins-only` per CXO, not Class 1) | — |
| #2170 | Chat: remove an item from a list (a list-item rail), with exact-match arming and an id-bound confirm (added 10-24: missing from the plan, found by the map generator) | — |
| #2225 | Draft path with no user default repo: the answer to 'Which repository should I create this in?' goes into the draft body, so naming the repo can't file the draft (10-30, PA's re-check 3 side finding on `ac5b69f865`; CXO rules the behaviour; not a gate row); closed 10-30 16:17, Lead on Arch's validation, fix on main `47a9f431db` and **not served** (label `fix:not-served`; no promotion before the first invitations) | — |
| #2230 | 'Set my default GitHub repository to owner/name' gets the no-match line in every session: `set_default_repo` isn't live in the inversion consult (10-30, Arch's two-session probe on `ac5b69f865`; #2225's second shape; likely an ops fix to the live set, Arch rules; not a gate row) | — |

### E: Experience polish (29)

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
| #2156 | UX: Send feedback is a quiet footer link, and absent from the setup wizard and error pages (10-24) (closed 10-24, `close:pins-only`) | — |
| #2206 | Setup wizard 'Connect Your AI' offers only an optional Notion key (xian: "comprehensive or left out entirely") (10-29, PA from scenario A) | — |
| #2203 | Asked to summarize Notion docs, chat answers about uploaded documents and never says Notion isn't readable (10-29, CXO; #1386 row 3 C1; words given) | — |

### T: Trust and learning (14)

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
| #1509 | TRUST-CONSENT: consent gate + capability legibility — one feature (Jake alpha FTUX; PPM's hold-a-release … (added 10-24: missing from the plan, found by the map generator); closed 10-30 20:00 PT | — |

### Doc: Documents (9)

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
| #2226 | Document search from chat doesn't work on a partner account (OpenAI-only embeddings): the beta known-issue line's open home (10-30, PPM from the row-6 check; #2122 closed on the honest refusal) | — |

### Dist: Distribution (2)

| # | Title | was |
|---|---|---|
| #966 | DIST-VISUAL-IDENTITY: Visual identity for the plugin and MCP Apps surfaces (the MCPB half dropped, supersed… | PROD-DIST |
| #1242 | MEET-PIPER-GITHUB — Add GitHub connector setup step to meet-piper onboarding (closed, superseded 10-25) | PROD-ONBOARD |
| #1244 | CONSULT-ENRICH-FIX — Fix two enrichment layer bugs blocking consult-piper (Cowork/GitHub + Code/payload) (closed, superseded 10-25) | PROD-ONBOARD |
| #1245 | PIPER-SKILL-MERGE — Collapse ask-piper + consult-piper into one smart piper skill (closed, superseded 10-25) | PROD-ONBOARD |
| #1282 | BYOC-DIST — Plugin packaging and marketplace distribution | PROD-DIST |

### Q: Health lane (19)

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
| #2177 | Alpha promotion fails: staging's image tag returns 'manifest unknown' on pull (10-25, Lead; closed 10-27 07:12, served: run 40517175846 pulled by digest, alpha attests 36bdcf09bb) | — |
| #2202 | Handler-route /api/v1/intent replies carry no intent.original_message field (10-29, Lead; #1151's follow-up; response assembly in one place) | — |
| #2210 | tests/web smoke test_template_renders fails alone on main: Jinja2Templates not initialized in app state (10-29, Lead lanes; not a product defect, blocks a clean local landing-gate run); closed 10-30 12:16, fixture fix on main | — |
| #2211 | Delete the dead floor door _handle_guidance_via_floor (no callers) and correct the door-count comments to 3 (10-29, Arch from Lead's #2209 build) | — |
| #2232 | Local served fault run: a server from main, with the real DB and HTTP API and a failing upstream stub, for #2231's three rows that can't be forced on alpha (#2152, #2125, #2154) (10-30, Lead on Arch's ruling; the instrument, not a partner-facing defect) | — |
| #2234 | Test-account fault injection: a scoped switch, off by default, that makes one source fail so failure-path copy can be served on alpha (10-30, CXO's #2231 ruling; Arch designs it, security review first; #2232's served-on-alpha sibling); closed 10-30 17:37 as superseded by #2232 (Arch declined it as designed, since an account id would become a security boundary; CXO closed it) | — |
