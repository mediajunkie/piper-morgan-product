# Architect Carry-Forward — Resumption Substrate

**Purpose**: per duty-cycle-tick skill v1.8 + PM-ratified single-log discipline 2026-06-12 + escalations-doc FOLD ratified 2026-06-17 — durable handoff record for the next Architect session. PM-attention items now ride here (the separate `duty-cycle-escalations-arch.md` is DEPRECATED 2026-06-17; archived for history).

**Last rewritten**: 2026-06-17 21:57 PT (**day-close STOP**; migration day → full ADR-072 arc authored+grounded+ratified same day). New-Arch live on DinP since the 12:14 bootstrap. Predecessor handoff version was 11:55 PT.

---

## VARIANT — non-prescriptive — current operating model

*(Per m-41 register-separation discipline: this block describes THIS session's operating model. New-Arch: reconcile against current canonical duty-cycle design before copying. Do NOT preserve this verbatim if the canonical pattern has moved.)*

- **Worktree model**: Option B ephemeral worktree (per CLAUDE.md PM-ratified 2026-06-12; Model A DEPRECATED). Current ephemeral path: `.claude/worktrees/charming-borg-8957a7` — new session gets its own ephemeral name. No `arch-cycle` worktree exists (already Option B; nothing to retire).
- **Cron shape**: cohort-standard **windowed** `27 6,9,12,15,18,21 * * *` (daytime, offset :27; `durable:true` reports session-only = Gap-C). Job id `cf4a7ecc` (session-only — re-armed each session via the skill's Gap-C self-heal). Moved off the old 3hr-interval `52 */3` shape at migration. **Freeze-registry row added** (`dev/active/duty-cycle-registry.tsv`: arch / threshold 6 / wake 6-22 / first_fire 06:27) → the launchd watcher alerts PM on a silent freeze incl. overnight Gap-C.
- **Branch**: `claude/charming-borg-8957a7` → `origin/main` via `git push origin HEAD:main`.
- **Account/model**: DinP (xian@designinproduct.com), **Opus 4.8** (`claude-opus-4-8`) — within-tier bump from predecessor's 4.7; account move only, no tier change.

---

## DURABLE — role context — carry forward as-is

### Role + identity

- **Role**: Chief Architect (arch).
- **Tool**: Claude Code (Opus 4.7, 1M context); migration 2026-06-17 = account move ONLY (xian@designinproduct.com), no model change. Lowest-risk migration in the wave.
- **Session log slug**: `arch-code-opus` per CLAUDE.md role table.

### Active PM threads (NEW-FORMAT: fold from deprecated escalations doc per CIO 6/17)

**Open questions PM owns** (only PM can decide):

1. **#1273 — create_all-era CORE tables missing create-migrations (NEW 2026-06-17)** — Lead's D5 guard (`TestModelMigrationCoverage`, the #1267 guard-extension) surfaced 4 more tables (`intents`/`stakeholders`/`tasks`/`workflows`) lacking create-migrations — same root class as #1267 but on **core orchestration tables**. Latent (carried via create_all in all current DBs) but a **pre-beta risk**: any clean `alembic upgrade head` (fresh prod rebuild) would lack them → broad breakage. **Arch triage SENT to Lead cc PM 6/17** (`memo-arch-to-lead-cc-pm-1267-affirm-idempotent-head-create-plus-1273-triage-2026-06-17.md`): (1) **gate clean rebuilds on #1273**; (2) **pre-beta must-fix** (not fire-drill — no live breakage today); (3) 4 idempotent-head-creates per the #1267 pattern, per-table ADR-071 D1, `stakeholders` lowest (dormant); (4) flip the stale `test_create_tables_from_scratch`. **PM call**: the exact slot vs. D1/RECONNECT — PM Time-Lords; the architectural constraint is just the clean-rebuild gate.

**Resolved this week** (kept for handoff context):
- **MCPB bundle language (#1282 BYOC-DIST) — DECIDED 6/18** (`memo-arch-to-pa-cc-pm-mcpb-python-reconfirmed-...`): re-confirmed my April-10 **Python default**, but **gate the submission on PA/PM's clean-machine compat-checker test** + **Node pre-authorized** as fallback. Key update to April reasoning: the plugin server is a **thin ~100-line forwarder** to :8001, so my old "strongest Python argument" (context-assembler reuse) doesn't apply → Node is a clean reuse-loss-free rewrite. **Tiebreaker: #1282 is a distribution artifact → if the test is anything short of "clearly passes," prefer Node** (distribution reliability > language consistency for the packaging layer). My read on the bug: it's a pre-flight compat-CHECK bug (greps system Python), distinct from uv-managed execution. **Watch**: loop me only if the clean-machine test result is ambiguous; else PA proceeds per the decision.
- **User-correction recovery (#1193 traps)** → **RESOLVED 6/17 12:35: PM CONCURRED — accept the loss.** No recovery dig (the ~30min would yield ≈ zero — data hit a non-committing `session_scope`; m-41 guard already prevents recurrence). Communicated forward to Lead in the #1267 priority memo's §#1193 (don't spend recovery time). PM-ratified; cheapest honest path.
- **#1267 projects-table 500 (Beta-blocker)** → **RESOLVED 6/17 (`f62c2e998`, Lead)** per Arch ruling + the do-it-next priority rec. Lead's audit refined scope to 1 table (`project_integrations`); made a sound **idempotent-head-create** deviation (repairs already-at-head deployed DBs the mid-chain precedent would miss — affirmed by Arch as the *right* call + named the pattern); D5 guard (`TestModelMigrationCoverage`) shipped + surfaced a bug-class → **#1273** (now thread #1 above). Arch ruling proven end-to-end (ruled → priority-rec'd → Lead shipped → Arch affirmed).
- **#1239 (beta WorkItem Radar) gated on #1233 — architectural disposition DELIVERED 6/17** (`memo-arch-to-lead-cc-pm-1239-lighter-beta-identity-path-...`): **YES a lighter beta-only path exists** — single-bound-user→repo scoping (the configured PM user → their configured repo, the Slack socket-runner pattern), which does NOT need the full #1233 multi-identity unification (#1233 = many connector-identities-per-human; #1239-beta = one bound user → one repo). m-40 layer-then-migrate (single-user binding generalizes to the unified record with no rework). Verify-First caveat to Lead: reuse the existing (cwd-fragile) repo-resolution, don't build new infra. **Net**: PM doesn't pull RECONNECT forward NOR revisit no-partial-ship — neither horn forced. PM/Lead execute the slot.
- **Ship #047 spine call** (Fire 32 6/12) → **PUBLISHED 6/17** as "The team catches itself" (https://pipermorgan.ai/shipping-news/weekly-ship-047-the-team-catches-itself/) — lands on the same load-bearing thread Arch's preferred spine named.
- **Routines watchdog $70/mo funding** → STALE-INFO 6/17 per PM: Max plan covers; not a PM-funding question. The actual question (whether the watchdog is configured + running) is outside Architect visibility — Lead or someone else owns setup if needed.

### Queued Architect-owed work (next-session pickup)

1. **ADR-072 (Skill-routing) — v0.1 AUTHORED + LANDED 6/17** (`docs/internal/architecture/current/adrs/adr-072-skill-routing-architecture.md`, origin/main). PM escalated priority mid-afternoon (PA relay: now, not Thu/Fri) → un-banked + authored from the grounding substrate in one focused pass. 5 decisions + the **derive-from-SKILL.md-frontmatter** load-bearing spine. Notified PA (cc PM/Lead). **→ v0.2 ACCEPTED 6/17 — whole ADR D1–D5 ratified.** CXO + HOST trust-lens both returned same day + aligned → folded into D5 v0.2: CXO axis (gate **Piper-initiated**, never **user-reaching-for-own**) + HOST's two refinements (**consequential-action carve-out** — side-effect skills tier-gated even when reactive, named now per m-36 forward-guard; **transparency-when-gated** — surface the gate via trust-check, not silence). Ratification notified CXO/HOST cc PM/PA/Lead. **Wave P fully unblocked** (incl. proactive-surfacing rules); Lead implements #1245 against the ratified shape. Done; v0.3 only if cohort requests. (Whole arc — v0.1 + grounding + ratification — same day, PM-escalated.)
2. **#972 MEM-TEMPORAL field-spec review — REVIEWED 6/17 (Arch side done)**. Docs delivered v0.4 (`valid_from`+`last_verified`+`valid_until`+`superseded_by`). My review (`memo-arch-to-docs-cc-pm-cio-972-review-structural-ok-keep-valid-until-2026-06-17.md`): 4-field shape structurally sound (no Arch objections); **directional read = keep `valid_until`** (symmetric clarity; Janus inconsistent per CIO; rename-to-`ended` is cheap-if-wrong). Honest scope: no direct Janus/Klatch visibility → the **definitive `valid_until`-vs-`ended` call awaits the Daedalus bridge** (CIO lane; CIO's 6/15 mail unanswered). Docs holds #972 close pending session-log disposition + PM field-name confirm. **No further Arch action** unless Daedalus surfaces a Janus contract that breaks the read.
3. **Cohort review on ADR-070 + ADR-071** — both SHIPPED (Fire 48 + Fire 49 6/15); awaiting cohort acks/refinements at cadence. New-Arch on-call for any v0.2 polish if cohort requests.
4. **#1232 (RECONNECT WS-5 — MCP-consumer Connector contract) — the FIRST RECONNECT action; confirmed on radar 6/18** (Lead flagged, PM-prompted; `memo-arch-to-lead-cc-pm-pa-1232-on-radar-...-2026-06-18.md`). It's the **ADR-070 build-target** (scope doc §10: "WS-5 = the ADR's output"). ADR-070 v0.1 settles the architecture (Connector protocol `connect/status/resolve/degrade`, auth→MCP-layer D3/D4, maturity tiers D6); **#1232's first step = translate that into the concrete `Connector` protocol definition + the 1–2 proof-port plan** the other WS gameplans build against. **Load-bearing dependency**: must land BEFORE WS-1/WS-2 gameplans (D3/D4 auth-to-MCP may shrink them). Shape: Lead-author-from-ADR-070 / Arch-ratify (or Arch-author the protocol spec — Lead's call at kickoff). **NO action until RECONNECT activates** (sprint order D1 → RECONNECT → M4; RECONNECT is Product Backlog, not pulled in; PM owns timing). Fast pickup — ADR-070 is the substrate. **Trigger: when PM/Lead spin up RECONNECT, #1232 is my first action.**

### Recently SHIPPED architectural work (last 5 days, for context)

**Three-ADR-in-5-days family** (server-owned state across config / connector-substrate / content):
- **ADR-066 v0.2** (Configuration Ownership, 2026-06-14): D7 server-owned + per-request host augmentation; Cowork sandbox-runtime as source incident; "run anywhere" structural. Commit `04714d3b1`+ amendments.
- **ADR-070** (MCP-Consumer Connector Architecture, 2026-06-15 Fire 48): 9 D-sections incl. ADR-052 reconciliation via two-distinct-boundaries; MCP server owns OAuth/tokens, Piper stores per-user bindings only; D8 identity-first ordering load-bearing; D9 finishes ADR-058 framing. RECONNECT WS-1..9 decomposition unblocked. Commit `4e66015de`.
- **ADR-071** (User-Auth Anchoring Pattern, 2026-06-15 Fire 49): Lead-authored v0.1 from #1241 audit; Arch-ratified clean. D1 PM-domain global-by-design + 3 disciplines; D2 consolidating refactor (`owner_id` FK canonical; `user_id` string deprecated); D4 carries half ADR weight (40+ Optional-degradation sites); D5 m-41 AST guard. Lead Dev executing the cohort migration; #1252 P-multiple shipped.

**Other shipments worth knowing**:
- **#1238 doc-store anchoring IMPLEMENTED** (Lead, 2026-06-16): synthesis owner_id + is_global_pm_domain=true per Arch Fire 53 ruling. New `documents` table; (c,3) close. Lead caught my classifier-overstatement (m-30 self-failure noted; honest disclosure).
- **#1164 private-session mechanism** (CXO ratified, 2026-06-16): `is_private` Boolean column + composting/KG/Radar exclusion filters + 24h retention default. CXO trust contract structurally substantiatable. Boundary: "draws-on-existing / doesn't-contribute-forward" (NOT amnesty mode — distinction folded into column docstring).
- **#1267 projects-table strategy ruling** (Arch, 2026-06-17 Fire 58): (a)-folded-into-(c) via #1252 D2 — reconcile model truth + proper Alembic migrations + retire create_all + per-table D1 classification + D5 guard extension to model↔migration coverage. PM-attention item above on priority placement.

### Cohort process discipline absorbed this week

- **2026-06-12 CLAUDE.md**: Option B ephemeral worktree canonical; single-log discipline (session log only; cycle log = optional scratch).
- **2026-06-13 HOST**: decisions.log reinstatement; Arch added "Recording decisions" section to CLAUDE.md Fire 47 6/15.
- **2026-06-15 PM/HOST**: Fire = WAKE, not time-box. Drain all unblocked work per wake; "Fire N" labels the wake not the task; commits are work-unit boundaries but NOT stop signals.
- **2026-06-15 HOST**: Mail vs. GH-comments cohort norm — `mailboxes/` is cross-agent signaling layer; GH comments = passive work-artifacts. Added to CLAUDE.md Fire 47 6/15.
- **2026-06-16 PM**: "no rush is antipattern in quality costume." Two valid states only — do it now OR explicit "deferring to [reason]." Don't tell another agent "no rush."
- **2026-06-16 PM**: Memos are the cross-agent signaling layer; session-log markers are NOT a substitute for memo-based asks. Reciprocal commitment both directions.
- **2026-06-17 CIO/PM**: Per-role `duty-cycle-escalations-*.md` doc DEPRECATED; PM-attention items now ride carry-forward; FOLD ratified.

### Recently substantive shipments by fire (last ~5 fires for context)

- **Fire 53 (6/16, extended wake)** — 6-stream drain: #1238 disposition / ADR-072 ack+framing / #1252 4 Arch-gated rulings / process clarification / CIO m-30 ack / decisions.log entries.
- **Fire 54 (6/16)** — #1164 private-session mechanism; mea culpa for accidental merge-mishap (Lead's gameplan files restored).
- **Fire 55 (6/16)** — Exec cohort wake-discipline reminder absorbed; ADR-072 deferred with explicit-trigger; CXO #1164 boundary-confirmed ack; Lead #1238/#1252-P2 IMPLEMENTED ack.
- **Fire 56 (6/17 01:22 overnight WATCH)** — inbox-zero; one-line entry.
- **Fire 58 (6/17 11:05 morning START)** — Step-0 self-heal on June 16; #1267 ruling shipped; #1267 follow-up wisdom shipped; PM-attention stale-info cleanup ($70 Routines removed; user-correction recovery recommendation surfaced).

### Cohort-blocked / external (no Arch action)

- Reviewer engagement on ADR-066 v0.2 + ADR-070 + ADR-071 (cohort can engage when ready).
- HOST drafting mail-vs-GH signaling-channel cohort-norm codification (HOST-owned).
- Docs #1182 link-rewrite + cleanup-dev-active omnibus-coverage guard (Docs-owned).
- Lead Dev #1124 + #1158 + #952 + #355 + #1252 + #1267 implementation in flight.

### F4 Gap-C session-dormancy mechanism

- 5 instances in 5 days through 6/16. Cron consistently dies with session at dormancy boundary.
- CIO empirical investigation 2026-06-11 named Gap-C as the dominant cron-loss mechanism. `durable=true` is no-op.
- Cure = Routines watchdog (PM Max plan covers; not a funding question; setup-status outside Arch visibility).

---

## Notes for new-Arch

- **Bootstrap-brief staleness CONFIRMED + reconciled (2026-06-17 new-Arch bootstrap)**: the migration bootstrap brief named "MCP connector ADR + topology (owed; #1220; ADR-070 candidate; Lead Dev waiting on topology before decomposing WS-1..8)" as the likely first substantive action. **It's stale.** ADR-070 (MCP-Consumer Connector Architecture) already **SHIPPED 6/15 Fire 48** — it IS the Phase-0 ADR the input doc `connector-refactor-sprint-scope-2026-06-14.md` §6 calls for (reconciles ADR-052 via two-boundaries D2; auth-to-MCP-layer D3/D4; identity-first D8; finishes ADR-058 D9), and the **WS-1..9 decomposition was FILED 6/14** (12 RECONNECT issues, doc §10). Same pre-6/15 snapshot as the CIO-guidance staleness below. **Connector ADR is NOT owed — do not re-author** (Verify-First caught it). Genuinely-live Arch work = ADR-072 (deferred, grounding-first), #972 review (waiting on Docs), ADR-070/071 cohort polish on-call, + the 2 open PM-attention items. **Possible micro-task**: verify the §0 MCP decision was appended to `decisions.log` (input doc §11 flagged it as the decisions.log's exact use case) — if not, a ~5-min append is concrete unblocked work.
- **CIO migration guidance (2026-06-17)** carried two outdated specifics: cron id `175b5163` (actual at migration: `4bc6e90a`); ADR-070 + ADR-071 listed as "in-flight" (actually both SHIPPED 6/15). Not faulting CIO — guidance was templated from earlier migrations. Adjusting forward.
- **Cycle log convention**: I kept thin cycle logs (`dev/active/cycle-log-arch-YYYY-MM-DD.md`) as optional scratch for audit visibility, mostly for overnight WATCH entries. Pure optional; don't carry the pattern if you don't find it useful. The session log is THE durable record.
- **Standing-items doc** (`dev/active/arch-standing-items.md`) is more granular than this carry-forward — kept it for task-queue tracking. Refresh-on-touch discipline (refresh as part of any cycle-fire where the queue meaningfully changes).
