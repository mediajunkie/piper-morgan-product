# PA Standing Items Tracker

**Purpose**: Track PA-domain items that are pending PM input, blocked on external action, or queued for PA execution but not yet started. Persistent surface so items don't get lost to transcript / PM memory / PA context window.

**Origin**: Created 2026-05-27 at duty cycle v0.6.2 adoption Day 0 per CIO's suggested-path step 2 (reuse existing or create). PA hadn't previously maintained a standing-items tracker; created new at adoption.

**Duty Cycle role (v0.6 design ratified)**: This file IS the canonical **Task List** (Doc 2 of the three per-agent duty-cycle docs). Per the formalizing-not-proliferating principle, no parallel "task list" doc is created. Tasks added during Mail Loop step 4 land here. Task Loop reads from here. PM-injected tasks (the load-bearing (0, 1) decision-table row) also land here.

**Update cadence**: append-only ledger with status updates in-place. PA updates at session-start (review carryforward) and after each substantive session (capture new items + close completed ones). Distinct from `exec-open-items-tracker.md` (exec-owned, project-wide) — this is PA-owned, methodology-and-product-management scope.

---

## How to Read This

| Status | Meaning |
|---|---|
| **Pending PM** | Awaiting PM decision, concurrence, or approval |
| **Pending external** | Awaiting other-role action (CIO, Lead Dev, Docs, etc.) |
| **PA-queued** | Bandwidth-gated PA work; ready to execute when scheduled |
| **Watch** | Standing observation surface; trigger-bound |
| **Active** | Currently in flight |
| **Resolved** | Closed; preserved for one cycle then removed |

---

## Long-horizon topics (address over time)

_Strategic threads PM flagged to revisit — not operational/owed items; no near-term action._

| # | Topic | Noted | Notes |
|---|---|---|---|
| T1 | **Cross-Piper synthesis** — converge learnings across Piper instances (Piper Morgan / PA, Piper Open on OpenLaws, future siblings) | 2026-06-07 | PM-flagged at the BYOC milestone. **Two-layer by firewall**: *general/transferable* (harness, methodology, role-design, calibration technique) converges up; *client/domain-specific* (OpenLaws IP) stays partitioned. **Two targets, different risk**: (a) **PM's own instance knowledge** — low-risk (PM = trusted common party, synthesizes freely); (b) **shared "Piper Morgan core"** — high-firewall (ships to others → general layer only). Candidate substrate: the BYOC **`company-profile.md`** shared-cross-instance layer. **Enabling events (PM-driven)**: (1) PM shifts to consulting posture w/ OpenLaws as client → **Piper Open migrates into our infrastructure**; (2) before then PM will **arrange direct PA↔Piper-Open correspondence** to start collaborating. Await PM arranging correspondence / infra migration. Context: June 7 session log. |

## Active Standing Items

### Pending PM input

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Skunkworks writeup → final PM signoff → fan-out** | 2026-05-21 (writeup reconstructed 5/30) | **Writeup at `dev/active/pa-skunkworks-byoc-poc-learnings-2026-05-30.md`**. ✅ Cowork-test package findings folded (5/31; runtime/fs mismatch + payoff-ceiling + moat); ✅ all 3 `[verify]` resolved/dispositioned; ✅ PM observations folded (value=light-but-POV-implied; runtime-bug=expected-not-crisis; forward=thin-full-stack-PoC proposal). **Remaining: final PM signoff → fan-out.** Fan-out spine = forcing-function + ratification ask (not just learnings). Ted/Dan tester check = PM-owned + nonblocking (not a gate). |
| 1b | **Thin full-stack PoC — next skunkworks experiment** (PM proposal) | 2026-05-31 | PM proposes next experiment: minimal MCP hitting real PM API + minimal PM/assistance skills (down payment) + minimal plugin orchestration; modeled on PM's OpenLaws plugin. Needs **leadership ratification** (single-purpose, all-layers, NOT overbuilt) + **roadmap/strategy alignment** (don't front-run architecture). Coordination: keep it a predecessor-study feeding PDR-005 + Arch Q6/Q7. PA to surface in fan-out + tee up roadmap synthesis. |
| 2 | **Outcomes smoke test scope + start** | 2026-05-27 | PM approved 2026-05-27 ~2:30 PT. Execute after CIO methodology-34 synthesis lands (Day 28-29 per CIO commit). PA proposes to draft scope-memo to PM at that point. |

### Pending external action

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Discovered-work tiered "buried" bar concur** — Lead Dev | 2026-05-27 | Tiered bar proposed in disposition memo: P:crit 3d/3d → P:low 21d/14d. Lead may flag-back if mechanically heavier than flat 14d/7d default. First sweep starts Fri 5/29 with flat default; tiered refinement after Lead concur. |
| 2 | **Memory pin draft on discovered-work discipline** — PA-or-Lead-Dev co-author | 2026-05-27 | PA offered to draft solo or co-author with Lead. Awaiting Lead's preference. Provisional name: `feedback_discovered_work_doesnt_get_lost.md`. |
| 3 | **MEM-975 cohort rollout PA slot (Week 2)** — Lead Dev | 2026-05-27 | PA in Week 2 (Days 8-12 post-launch); structured N=5 measurement Lead drives. Aligns with v0.6.1 stabilization ~May 31. |
| 4 | **check-branch.sh fix for Model-A mailbox-on-branch** — Lead Dev | 2026-05-28 | Memo `7670c2f3e` sent. Hook hard-blocks mailbox commits on cycle branch (no push-to-ref bypass); v0.7 template's per-fire-push mail path doesn't work. Until fixed, PA mail rides main-worktree bridge. **CIO concurs Option-1 (amend hook); template corrected `a5517ee02`.** Awaiting Lead Dev fix-choice (Lead owns the hook). |
| 5 | ~~**Roadmap v17 §M5/BYOC review** — PPM~~ → **RESOLVED 5/31** (see Resolved R4) | 2026-05-29 | Draft landed `00cee8d47`; PA review delivered to PPM `0448f8e7d`. |

### PA-queued

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Discovered-work weekly sweep** — Friday-to-Thursday cadence | 2026-05-27 | **Ran Fri 6/12: 146 open (+20); 6 unassigned → all assigned mediajunkie; 0 high/crit unassigned ✅ HEALTHY. Stale-high: 7 (+2) — 5 unchanged known roadmap (#103/#104/#106/#321/#358); NEW entrants: #1122 MULTI-TURN-DOC-ANTECEDENT (17d, known regression, AAXT-confirmed behavioral) + #1129 SLACK-INBOUND-STRUCTURAL (15d, webhook). Sweep report → PM inbox 43baa7894. Next: Fri 6/19.** |
| 2 | ~~**Roadmap v17 §M5/BYOC review** — PPM-requested~~ → **RESOLVED 5/31** (see Resolved R4) | 2026-05-31 | Review delivered. Verdict: §M5 sound; 2 corrections (Daedalus referent gap, stale Outcomes target) + 2 sharpenings. Review at `dev/active/pa-v17-m5-review-for-ppm-2026-05-31.md`. |
| 2 | **methodology-34 refresh review** — Day 28-29 when CIO lands | 2026-05-27 | PA welcome as Day-3/4 review feedback per CIO follow-up memo. |
| 3 | **Skunkworks sub-pass 4.b dispatch** (insight-journal-flat-file) | 2026-05-21 | Pending writeup fan-out + PM signoff. PA-queued behind item 1 above. |
| 4 | ~~**HOST Agent-360 v0.3 response**~~ → **DONE 6/3** | 2026-06-03 | Delivered to HOST inbox (`6e8fb106a`), cc PM. Answered §1/2/5/6/7/8(PA)/9/10(observer + V2-live bonus). Candid friction: bridge-overhead, check-branch.sh fix unshipped, deferred-logging near-miss, hourly-cron-wrong-for-bursty-lane, BYOC-not-in-M5-issues. Fielding memo → read. Synthesis ~Jun 12. |
| 5 | **Cron-shape experiment (PA lane)** — STARTED 6/3 · **Day-7 memo DELIVERED 6/10** | 2026-06-03 | **Switched hourly → every-3-hours `42 */3 * * *`** under CIO 6/2 standing authorization. **Day-7 results memo → CIO cc PM (6/10)**: every-3-hours held up (watch condition clean — no PA-mail sat >3hr; Exec Q caught in 34min); the real efficiency lever = **overnight quiet-hold fires (00:42 + 03:42) are pure-cost no-ops** → recommended **windowed cron `42 6,9,12,15,18,21 * * *`** (drops both overnight no-ops at zero loss). Timed to feed the active PM+CIO token-efficiency pass. **Recommendation: keep every-3-hours (windowed); revert to hourly only on substantive backlog.** Watch condition continues. |

### Newly-surfaced (6/11)

| # | Item | Filed | Notes |
|---|---|---|---|
| D | **#358 ADR-058 scope confirmed** → DONE 6/11 | 2026-06-11 | Lead Dev + PPM both concurred: #358 scope = user-secret-set-wide (LLM key + GitHub/Slack/Notion ADR-058 keys). PA added clarifying comment to #358 + corrected stale `api_keys.key_value` AC line. [Comment link](https://github.com/mediajunkie/piper-morgan-product/issues/358#issuecomment-4681857971). No further PA action needed on this thread. |

### Newly-surfaced (6/3 eve)

| # | Item | Filed | Notes |
|---|---|---|---|
| A | **PDR-005 line ~376 "MCPB hybrid" stale ref** | 2026-06-03 | Same packaging-model issue as the v18 fix; PPM flagged + left it (broader-distribution scope). Correct when PDR-005 → v1.0 or skunkworks fan-out lands. Fold with the fan-out batch. |
| B | **§M5 PoC line-128 sharpen** (thin-PoC/`/intent` detail) | 2026-06-03 | PPM deferred folding it into v18 (didn't want v18 ahead of held fan-out). PM call: fold now or with fan-out. |
| C | **Attention Dashboard v0.2** — co-shape with CIO | 2026-06-03 | CIO named it a roadmap item; offered to co-shape v0.2. Rungs: auto-stale-flag → GitHub-state verify → dedupe → severity-parse → priority-rank. Build when PM/CIO prioritize. |

### Watch

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Cross-pollination signal** — Klatch (paused), Atlas, Globe sibling projects | Pre-migration carry | Per `[[project_sibling_projects]]` memory. Surfaces if any sibling-project signal reactivates. |
| 2 | **Year-anniversary milestone observance** — today | 2026-05-27 | PM directive: update MVP date 2026-07-04 (executing today). Future: celebrate the milestone. |

### Active

| # | Item | Filed | Notes |
|---|---|---|---|
| 2 | **PM wants to discuss the architecture diagram** — PM-requested, awaiting a time | 2026-07-26 | PM 7/26: *"I've been meaning to discuss the architecture diagram you (earlier-PA) put together for me last week, when we have the time."* Built by predecessor PA 7/18–19; PM's reaction then: *"This is super helpful, I'm printing it out."* Artifact: `https://claude.ai/code/artifact/a146134e-2858-4c7c-a916-8f1b038fc8c6` — three client models (Claude Chat/Cowork/Code, ChatGPT, Web) → `mcp.pipermorgan.ai` → data layer, plus the plugin-side vs server-side skills split. ⚠️ **It predates three things that move it**: the tier resolution (Track A needs Team; Track B is the open route), Q2 as a PDR-006 ratification blocker, and Arch's colleague-model/spatial coupling. **Not stale — but it should be re-read against those before the conversation, and the diagram was built by a session that no longer exists.** PA to prep, not to pre-empt: PM asked to discuss, not for a revision. |
| 1 | **Duty cycle on Model A — emeritus handoff to fresh session 5/31** | 2026-05-31 | Day 1-4 (5/28-5/31) ran in continuous emeritus session. Fresh session per `dev/active/pa-fresh-session-handoff-prompt-2026-05-31.md` takes over. Emeritus session paused, available for "from the future" POV checks. Cron unregistered at handoff. |

### Resolved (preserved for one cycle)

| # | Item | Resolved | Notes |
|---|---|---|---|
| R4 | **Roadmap v17 §M5/BYOC review** delivered to PPM | 2026-05-31 | Fresh session. Full review `dev/active/pa-v17-m5-review-for-ppm-2026-05-31.md` (`71220bbfe`); cover memo to PPM cc PM/CIO (`0448f8e7d`). Verdict: §M5 sound — endorse structure + PDR-005-supersedes-PoC boundary + Klatch-pause framing. 2 corrections (Daedalus context-package referent gap → recommend soften; stale Outcomes ~May-30 target → recommend CIO-synthesis-gated sequence) + 2 sharpenings (PoC gate-PASS concreteness; Janus meta-coordinator line in §Autonomous Operations). PPM integrates into v18-draft. |
| R1 | check-branch.sh blocker memo → Lead (cc PM/CIO/Arch) | 2026-05-28 | `7670c2f3e` via bridge. v0.7 open-item #1 resolved (answer: hook blocks; needs fix). Now tracked as Pending-external #4. |
| R2 | Code/worktree restart + carry-forward recovery | 2026-05-28 | Prior session hit wall; delta-pa rescue confirmed on main (`f877ed84f`); continuation log + cycle log stood up. |
| R3 | Duty cycle v0.6.2 setup + MVP milestone update + first discovered-work sweep | 2026-05-27 | All executed 5/27 Fire 0 (milestone #5 → 2026-07-04; sweep = 0 buried, healthy baseline). |
