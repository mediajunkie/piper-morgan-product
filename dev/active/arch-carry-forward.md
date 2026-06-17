# Architect Carry-Forward — Resumption Substrate

**Purpose**: per duty-cycle-tick skill v1.8 + PM-ratified single-log discipline 2026-06-12 + escalations-doc FOLD ratified 2026-06-17 — durable handoff record for the next Architect session. PM-attention items now ride here (the separate `duty-cycle-escalations-arch.md` is DEPRECATED 2026-06-17; archived for history).

**Last rewritten**: 2026-06-17 12:14 PT (**new-Arch LIVE on DinP — migration COMPLETE**; bootstrap fire). Predecessor handoff version was 11:55 PT.

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

1. **#1267 projects-table priority placement (NEW 2026-06-17)** — Beta-blocker; dev unblocked. Arch ruling shipped today: (a)-folded-into-(c) via #1252 D2 (`memo-arch-to-lead-cc-pm-1267-projects-strategy-a-folded-into-c-via-1252-d2-2026-06-17.md`, main `9114bf54e`). Plus follow-up wisdom memo on `create_all` deviation as decisions.log-reinstatement instance (`db594cb30`). **Priority rec SENT to Lead cc PM 6/17 12:40 (new-Arch)** (`memo-arch-to-lead-cc-pm-1267-priority-do-next-independent-of-1257-plus-1193-disposition-2026-06-17.md`): **do #1267 NEXT** — it is independent of the *deferred* #1257 cutover (disjoint tables; the "sequence behind in-flight P7" framing was **stale** — P7-additive done 6/16, the cutover is parked in #1257), contained ~4-6hr, Beta-blocker. **Remaining PM call**: the exact slot vs. remaining D1 work — PM Time-Lords + said he'll follow up with Lead directly. Watch for Lead pickup.

**Resolved this week** (kept for handoff context):
- **User-correction recovery (#1193 traps)** → **RESOLVED 6/17 12:35: PM CONCURRED — accept the loss.** No recovery dig (the ~30min would yield ≈ zero — data hit a non-committing `session_scope`; m-41 guard already prevents recurrence). Communicated forward to Lead in the #1267 priority memo's §#1193 (don't spend recovery time). PM-ratified; cheapest honest path.
- **Ship #047 spine call** (Fire 32 6/12) → **PUBLISHED 6/17** as "The team catches itself" (https://pipermorgan.ai/shipping-news/weekly-ship-047-the-team-catches-itself/) — lands on the same load-bearing thread Arch's preferred spine named.
- **Routines watchdog $70/mo funding** → STALE-INFO 6/17 per PM: Max plan covers; not a PM-funding question. The actual question (whether the watchdog is configured + running) is outside Architect visibility — Lead or someone else owns setup if needed.

### Queued Architect-owed work (next-session pickup)

1. **ADR-072 (Skill-routing) — GROUNDING DONE 6/17; v0.1 authoring next** — grounding-pass-first trigger CLEARED: read PIPER.md + SKILL.md formats + SKILLS.md + pre_classifier.py → findings substrate at **`dev/active/adr-072-grounding-findings-2026-06-17.md`**. Key refinement: **derive-from-SKILL.md-frontmatter spine** (one source feeds manifest + Layer-2 patterns + Layer-1 descriptions; stale native SKILLS.md = live Pattern-073 proof hand-kept indices rot; composes ADR-066 D7 + #1106 derive-pattern). All 5 framing-leans evidence-validated. **v0.1 authoring banked to a fresh focused pass** (named-trigger quality-banking: deep deliverable, substrate now written, avoid tail-of-marathon on the most consequential artifact — NOT pacing). At draft: circulate **D5 (Trust Gradient × routing)** to CXO+HOST for trust-lens. Model on ADR-070's D-section shape. No hard deadline (Wave P weeks out). Initial framing memo: `memo-arch-to-pa-cc-pm-lead-adr-072-ack-timeline-...-2026-06-16.md`.
2. **#972 MEM-TEMPORAL field-spec review** — pending Docs's reconciled-schema delivery; not blocking. Docs reconciling field names against CIO's 6/12 ratified plan (`valid_from` + `valid_until` + `superseded_by` + `last_verified`); Docs will loop Arch on reconciled schema for Janus/Klatch cross-project alignment.
3. **Cohort review on ADR-070 + ADR-071** — both SHIPPED (Fire 48 + Fire 49 6/15); awaiting cohort acks/refinements at cadence. New-Arch on-call for any v0.2 polish if cohort requests.

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
