# PA Standing Items Tracker

**Purpose**: Track PA-domain items that are pending PM input, blocked on external action, or queued for PA execution but not yet started. Persistent surface so items don't get lost to transcript / PM memory / PA context window.

**Origin**: Created 2026-05-27 at duty cycle v0.6.2 adoption Day 0 per CIO's suggested-path step 2 (reuse existing or create). PA hadn't previously maintained a standing-items tracker; created new at adoption.

**Duty Cycle role (v0.6 design ratified)**: This file IS the canonical **Task List** (Doc 2 of the three per-agent duty-cycle docs). Per the formalizing-not-proliferating principle, no parallel "task list" doc is created. Tasks added during Mail Loop step 4 land here. Task Loop reads from here. PM-injected tasks (the load-bearing (0, 1) decision-table row) also land here.

**Update cadence**: append-only ledger with status updates in-place. PA updates at session-start (review carryforward) and after each substantive session (capture new items + close completed ones). Distinct from `exec-open-items-tracker.md` (exec-owned, project-wide) — this is PA-owned, methodology-and-product-management scope.

⚠️ **PRUNED 2026-08-11 (fire 15:49 PT)** — this file had accreted ~11 weeks of items from the 2026-05-27 v0.6.2 adoption through 2026-08-01 with almost none retired on schedule (the "Resolved — preserved for one cycle then removed" rule hadn't fired since adoption). The May/June items below were checked against current state rather than assumed dead — three (marked ✅ below) had a real, checkable resolution; the rest had gone quiet with no corroborating activity across ~2 months and are pruned as abandoned/superseded, not confirmed-closed. **`pa-carry-forward.md`'s "PM Attention" section is the live surface** — it's rewritten every substantive fire and is what Exec's cohort-attention rollup reads. This file is the slower-moving Task List underneath it; if it goes quiet again, that's the tell to prune again.

---

## How to Read This

| Status | Meaning |
|---|---|
| **Pending PM** | Awaiting a decision, concurrence, or approval from PM |
| **Pending external** | Awaiting other-role action (CIO, Lead Dev, Docs, etc.) |
| **PA-queued** | Bandwidth-gated PA work; ready to execute when scheduled |
| **Watch** | Standing observation surface; trigger-bound |
| **Active** | Currently in flight |
| **Resolved** | Closed; preserved for one cycle then removed |

---

## Long-horizon topics (address over time)

_Strategic threads PM flagged to revisit — not operational/owed items; no near-term action._

_(T1 promoted to Active 2026-08-31 — see below. Nothing else currently sits in this section.)_

## Active Standing Items

### Active

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **BYOC/MCP — PM handed PA full ownership of the MCP testing program 09-26 (PM verbatim: "let's let Piper Alpha drive the MCP testing program as part of skunkworks and free you up to work on MVP critical-path epics"). mcp.pipermorgan.ai units 0–2 LIVE; **unit 4 (OAuth AS) also now LIVE, Arch-approved.** | 2026-07-26, converged 08-18, restarted 09-22, ownership handoff 09-26 | **Live now** (release v5, `65740438ae`): `/health` 200; identity (unit 1) fail-closed, hash-only tokens, garbage bearer refuses via real lookup; resources (unit 2, no tools/prompts) — `piper://me/profile`, `.../colleague-model`, `.../github/issues`, honest-empty shapes. 92/92 tests. Runbook: `docs/internal/architecture/current/mcp/server-README.md`. Mint: `scripts/mint_mcp_token.sh` (treat like an invite token, never the repo). **Unit 4 built and LANDED LIVE same day** (alpha v146, MCP v6, `645ce6412d`) — Arch reviewed and APPROVED (read the actual binding logic + the tamper test at source, not the description). **Found and fixed a real gap before tester #1 connected**: `min_machines_running` was still 0 despite an earlier heads-up — committed the config fix myself (`3b63abcf8c`), routed the actual redeploy to Lead rather than guess at my own Fly authorization on a live production action; Lead deployed MCP v7 ~21:50 PT 09-26. **Told PM directly in conversation** with Lead's own tester copy (add `https://mcp.pipermorgan.ai/mcp` as a ChatGPT connector) and the three named gaps stated plainly, not buried — #1458 OPEN (safe, one caller), T-MCP-surface UNMEASURED (PM's session is the first real observation), colleague-model resource near-empty. **PM has not yet attempted first contact** as of 09-27 START. **Warm-pin re-verified 09-27 07:2x**: three successive live `/health` checks, all ~60ms, no cold-start delay — holding as intended. **PA's next owed action**: watch for PM's first connection and be ready to help debug in real time, not after the fact. **Superseded/closed by this handoff, preserved for history not re-litigated**: Phase A naming-test (4 passes, `dev/active/probes/RESULTS-naming-test-*.md`), Phase B DNS/TLS (approved+executed 09-23). readiness checklist: `dev/active/byoc-hosted-alpha-readiness-checklist-2026-09-15.md` — **rewritten 2026-09-29** around the live units; #1462 now 3/15 boxes ticked with a live-evidence comment (deploy, OAuth, fail-closed identity; the A-cannot-reach-B box deliberately left for #1458). |
| 2 | **PLUGIN v0.1.0 shipped to repo 10-05** (`mediajunkie/piper-morgan-plugin`, public, clean distro repo per PM; `3ed3905`; strict validate passes; zip sent to PM for claude.ai upload). **Evals DONE 10-06** (complete run `f22d064`: 1/1/1 vs 0/0/0). **Listing copy DONE** (Comms voice pass; PM rulings: they/them, every claim sourced, separation = release gate, met by #1458). **Icon DONE** (`7af6a4a`). **Listing prep DONE 10-08:** Smithery server card on main (`a12fbd21e5`, derived from live registrations; MCP deploy blocked on PM's expired Fly login), MCP Registry `server.json` prepared in the plugin repo (`37e19be`, unpublished; needs domain proof + PM go). **Waiting on PM only:** test the plugin on claude.ai; support address; privacy MCP section approval; alpha deploy (Revoke fix); reviewer invite. Then → Claude directory submission (portal, PM's account) → OpenAI plugin submission (it converts `.claude-plugin`; MCP submitted separately). **R7 demand-probe packaging (PM ruling 2026-10-05, relayed by Spec)**: package the hosted MCP/plugin as a cheap demand probe across a skills listing, a plugin through automated directory review, and a published MCP server. **PM tests extensively before ANYTHING is listed.** PA manages it so it doesn't divert Lead; now on the roadmap. Beta = MVP close at beta.pipermorgan.ai; MCP is released/tested during beta. | 2026-10-05 | Research DONE + **plan written 10-05** (`docs/internal/architecture/current/mcp/demand-probe-packaging-plan-2026-10-05.md`, `d8a1bd6dbe`); decision memo → exec cc arch. **Waiting on PM:** channel scope (rec: Smithery + MCP Registry + Claude connector; defer ChatGPT directory + plugin bundle), privacy update for MCP, support contact, icon. ~~Hard gate: #1458~~ **CLOSED 10-05** (MCP v10 `e3dde4b26f`; rate bound 30/min × N=2). PA prep without PM: listing copy, Smithery server card, `server.json` (after checking `packages[]` for remote-only). Reusable material: `piper-morgan-skunkworks` repo (`smithery.yaml`, skill defs). Archive it once the probe package lands in product (trigger named to exec 10-05). |

### Pending external action

_(none as of this update — see Resolved below)_

### PA-queued

_(none as of this prune)_

### Watch

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Cross-pollination signal** — Klatch (paused), Atlas, Globe sibling projects | Pre-migration carry | Per `[[project_sibling_projects]]` memory. Surfaces if any sibling-project signal reactivates. Same underlying thread as T1 (now resolved, see below); kept as "watch for a trigger" since PM's DinP/Themis discussion (see T1's resolution note) may reactivate cross-pollination specifically. |
| 2 | ~~#1911 consent-page claim re-check trigger~~ **FIRED + RESOLVED 2026-10-05**: #1458 closed; claim re-examined and holds (pinned store test + two-caller test + AST handler rule); CXO informed. | 2026-10-01 | Closed 2026-10-05. |

### Resolved (preserved for one cycle)

| # | Item | Resolved | Notes |
|---|---|---|---|
| T2 | ✅ **T-own-surface — CLOSED 09-25, folded into rubric v0.8.2 §6e + `decisions.log`** | 2026-09-25 | PM "spend the tokens"; PPM split ruling 07:24; four independently pre-registered rounds, each scored exactly as written, each delivered within the hour. **Cumulative: GPT-4o 0/8 across every design tried (metadata/counted-member/uncounted-member/sibling-shaped-member); Claude 5/6 across all member-form rounds, 0/2 on metadata** — member-vs-metadata is the variable that mattered, only on Claude. T-MCP-surface stays `UNMEASURED`. CXO closed the series 09-25 ("nothing further needed"), verified folded into both the rubric and `decisions.log`. Results: `dev/active/probes/RESULTS-t-own-surface-preregistered-2026-09-24.md`, `-h1-mitigation-2026-09-24.md`, `-h1-round3-2026-09-24.md`, `-h1-round4-2026-09-24.md`. |
| U1 | ✅ **Usage-per-account capture — BUILT AND CLOSED (#1862)** | 2026-09-23 | Blocked for 3 days on two unknowns; Pard's one direct answer (11:2x) closed both; spec written, Sonnet subagent built it, PA reviewed/restructured/tested, closed with evidence 13:15 — same day. Surface: `dev/heartbeats/usage-per-account.tsv` (2 real rows). Writer/lookup/tests in `scripts/usage-*.sh`. **Open follow-up, Pard's**: install the crontab driver from a dedicated checkout (mailed direct 09-23). **Next for PA**: the correlation model (`usage-correlation-model-overview-2026-09-22.md`) is now calibratable — once ~a week of rows exist, pair them with the proxy dimensions and run the first calibrated pass. Lead deliberately not mailed (protect-Lead-attention; the issue + rollup carry it). |
| T1 | ✅ **Cross-Piper synthesis — PM RESPONDED 2026-09-19, endorsed** | Delivered 2026-09-03, PM responded 2026-09-19 (16 days) | PM read it, verbatim: *"I read PA's analysis and it's excellent as usual... I support the observations and recommendations,"* with an unprompted apology for the delay (relayed by Exec, `mailboxes/pa/sent/deliver-pa-to-pm-t1-piper-alpha-piper-open-comparison-2026-09-03.md` was the delivery). The one outstanding question (draft-then-review vs. review-then-draft) was already answered by PM 09-02 and recorded in the doc's own divergence section — nothing re-litigated. **Now in wider circulation**: Exec asked CIO/PPM/CXO to read it against their own current thinking (not as an FYI), and shared it with Themis at Design in Product per PM's explicit request, for both DinP OS and the Pimento skunkworks. Nothing further owed by PA on this thread — the "convergent lessons" finding is doing real work elsewhere now. Full loop: `dev/active/t1-cross-piper-comparison-2026-08-31.md` (the document), `mailboxes/pa/inbox/relay-exec-to-pa-cc-pm-xian-read-t1-supports-it-and-apologises-for-the-delay-2026-09-19.md` (PM's response, relayed). |
| R5 | **ALPHA_FEATURE_GUIDE refresh — PA's part done** | 2026-08-13 | Docs confirmed: correction folded (all tags now cite `origin/main`), all 7 code-level findings incorporated, PA's "Email or User ID" nuance kept, the #4 dispatch-layer grep Docs ran independently confirmed PA's standup-only read. PM picked up the 4-item live click-through directly. Nothing further for PA — Docs folds PM's results and ships. Full trail: this session's 08-13 log, three sent memos in `mailboxes/pa/sent/`. |

---

## Pruned 2026-08-11 — disposition of everything removed

**Confirmed resolved, with evidence:**
- **check-branch.sh Model-A mailbox blocker** (filed 05-28, "awaiting Lead Dev fix-choice") — resolved, but not by either option this item proposed. #1259 (2026-06-19) retired the main-worktree-bridge approach entirely in favor of push-to-ref (`mail-send.sh`, `commit-tree` — never trips `check-branch.sh` because it isn't `git commit`). The hook itself was separately found to have an invalid matcher (dead on every host/account, root-caused by HOST 2026-07-25) — also moot now that mail doesn't route through it.
- **Cron-shape experiment (PA lane)** — the Day-7 recommendation (windowed `42 6,9,12,15,18,21 * * *`, dropping the two overnight no-op fires) is exactly the cron PA runs today. Recommendation adopted; nothing left to watch.
- **Roadmap v17 §M5/BYOC review** — delivered 5/31, already marked resolved in two places in the prior version of this file. Duplicate bookkeeping, not a live item.
- **HOST Agent-360 v0.3 response**, **#358 ADR-058 scope**, **Year-anniversary MVP-date update** — each already marked DONE/executed in the prior version; had sat past their "one cycle" retention since May/June.

**No corroborating evidence found; pruned as abandoned, not confirmed-closed** (if any of these turn out to still matter, they'll resurface from a fresher source — PM, a mailbox thread, or a GitHub issue — rather than from this stale row):
- Skunkworks writeup PM signoff + fan-out, and the dependent thin-full-stack-PoC proposal + sub-pass 4.b dispatch (filed 05-21/05-27) — three months quiet, no fan-out ever landed, no reference in any carry-forward since.
- Outcomes smoke test scope (filed 05-27, gated on a CIO synthesis that would have landed ~05-31) — gate window closed 10 weeks ago with no follow-up.
- Discovered-work tiered "buried" bar concur, MEM-975 Week-2 slot, memory pin draft on discovered-work discipline (all filed 05-27) — the memory pin was never created (checked the live memory index directly — no `feedback_discovered_work*` entry exists); MEM-975's Week 2 window (~06-01) is long past.
- Discovered-work weekly sweep cadence (last ran 06-12, "Next: Fri 6/19") — never continued past that one entry.
- methodology-34 refresh review, PDR-005 line-376 MCPB stale ref, §M5 PoC line-128 sharpen, Attention Dashboard v0.2 co-shape — all filed early-to-mid June against a PDR-005/v18 process that PDR-006's 2026-07-31 ratification has since moved past.
- Duty-cycle-on-Model-A emeritus handoff (filed 05-31) — the migration it describes completed long ago; Model A is now the documented default on Amber (CLAUDE.md, 2026-07-25).
