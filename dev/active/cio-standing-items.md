# CIO Standing Items Tracker

**Purpose**: Track CIO-domain items that are pending PM input, blocked on external action, or queued for CIO execution but not yet started. Persistent surface so items don't get lost to transcript / PM memory / CIO context window.

**Origin**: Created May 8, 2026 per PM directive after observing accumulating CIO-domain items spanning multiple sessions. Innovation Backlog (`cio-innovation-backlog.md`) tracks innovation patterns; this tracker tracks pending-action items broader than innovations.

**Update cadence**: append-only ledger with status updates in-place. CIO updates at session-start (review carryforward) and after each substantive session (capture new items + close completed ones). Distinct from `exec-open-items-tracker.md` (exec-owned, project-wide) — this is CIO-owned, methodology + patterns scope.

---

## How to Read This

| Status | Meaning |
|---|---|
| **Pending PM** | Awaiting PM decision, concurrence, or approval |
| **Pending external** | Awaiting other-role action (HOST, Lead Dev, Docs, etc.) |
| **CIO-queued** | Bandwidth-gated CIO work; ready to execute when scheduled |
| **Watch** | Standing observation surface; trigger-bound |
| **Active** | Currently in flight |
| **Resolved** | Closed; preserved for one cycle then removed |

---

## Active Standing Items

### Pending PM input

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | ~~Pattern Sweep #1025 disposition + execution mode~~ — **RESOLVED May 9** (commit `cd8386e9`); see R15 in Resolved | May 8 → May 9 | Sweep executed CIO-led with 3 subagents; #1025 closed. |
| 1a | ~~Pattern-066 PM concurrence on slot allocation~~ — **RESOLVED May 12** (PM concur via Docs memo; see R21) | May 9 → May 12 | PM concurrence affirmative per Docs May 12 loop-close memo. Standing carry-over closed at 3 days. |
| 1b | **Methodology-Elevated lifecycle stage formalization** — Architect concurred May 10 | May 9 → partial May 10 | Per Pattern Sweep Phase 2E Meta-Observation #2: Pattern-062 graduated pattern → methodology principle (Practice 5 in Flywheel v2.0). Two-vote alignment (CIO + Architect). Needs PM concurrence + Docs adoption (catalog convention change) for full ratification. Candidates for retroactive elevation: P-045, P-049. |
| 2 | **Sparker/Holder pattern naming** | Apr 26 | Operating norm PM articulated Apr 26 ("agent who receives spark isn't always the agent who holds operationalization"). HOST holds surface call (CLAUDE.md altitude vs. methodology-core); my lean was CLAUDE.md altitude. Pending HOST disposition + PM concurrence. |
| 3 | **Ideas/reading review** | Pre-migration carryover | Predecessor's recurring deferred item; been deferred since Mar 30. PM's call when to engage; CIO can re-frame as options if the deferral hits the 3-flag threshold. |
| 4 | **Ship #039 CIO re-issuance formal close** | Pre-migration carryover | Moot post-publish (Ship #039 published Apr 22 per amended-omnibus framing; predecessor's prior memo built on pre-amendment data is now historical). PM call to formally retire as "won't do" so the item stops carrying. |

### Pending external action

| # | Item | Filed | Awaiting |
|---|---|---|---|
| 5 | **HOST migration-experience confer Q3 engagement** | Apr 27 | HOST acknowledged Apr 27 with intent to engage Q3 within 24 hours; not yet engaged. No urgency per HOST's own framing ("exec migration tail is the priority"). |
| 6 | ~~Cross-pollination brief delivery as session-start hook~~ — **RESOLVED May 9** (Lead Dev shipped commit `07682bff`; see R16) | May 8 → May 9 | ~24h from CIO routing memo to Lead Dev ship. Three-state signal (NEW > STALE > available). CIO ack memo filed May 10. |
| 7 | **Architect Pattern-064 formalization completeness** | Apr 28 | Pattern-064 filed Emerging Apr 28 by Architect; first in-the-wild instance found in Architect's May 4 soundness review (KnowledgeGraphService alive scaffolding). Promotion to Proven contingent on Architect's lead. |
| 8 | **Docs canonical-vocabulary-watch first scan** | May 4 | File live; Docs ready to operate scan once next M-gate audit triggers, OR baseline scan at next workstream-cycle start (Docs's call). |

### CIO-queued (ready but not yet started)

| # | Item | Filed | Effort estimate |
|---|---|---|---|
| 9 | ~~Pattern-063, -064, -065 promotion-analysis memo~~ — **RESOLVED May 8** (commit `8d4cc139`); all three Promoted to Proven | Apr 27–28 → May 8 | All three pattern files updated; 062 family table updated; Innovation Backlog updated; distributed to 11 leadership inboxes. See R14 in Resolved tier. |
| 10 | **Per-doc disposition review for methodology-core** (HOST 360 pull #1) | Apr 27 | ~1-2 sessions (per audit B2 estimate; deferred per PM Apr 27). Maps to the 20-of-22 zero-cited finding. CIO-owned + HOST-monitored. |
| 11 | **B2 methodology-core triage starter list** | Apr 27 | ~45 min pre-triage filesystem scan; Docs offered the CIO contribution if requested. Overlaps with #10 above; #10 is the broader review, this is the data-gathering pre-step. |
| 12 | ~~Pattern Sweep #1025 execution~~ — **RESOLVED May 9** | May 8 → May 9 | Single-session CIO-led with 3 subagents. See R15. |
| 12a | **9 truly-stale patterns triage** (next cycle) | May 9 | Per Pattern Sweep Phase 2D: patterns 029, 030, 035, 039, 055, 056, 057, 058, 060. Disposition options: verify / refresh / retire / redirect. ~1 session CIO + Docs work. Mirrors M1 audit B2 (methodology-doc triage) at pattern-catalog layer. |
| 12b | **Methodology-Elevated lifecycle stage** discussion | May 9 | Per Pattern Sweep Phase 2E meta-observation: Pattern-062 graduated pattern → methodology principle (Practice 5 in Flywheel v2.0). Catalog convention has no explicit term. Likely retroactive candidates: P-045, P-049. Worth PM/exec discussion. |
| 12c | **Corpus-coherence cycle** proposal | May 9 | Per Pattern Sweep Phase 4: ~60% zero-citation rate at both pattern-catalog and methodology-corpus layers. Distinct from vocabulary-drift sweep (S1). Could be Phase 5 add to framework or separate cadence. PM/exec discussion. |
| 12d | **Metadata-cleanup ticket** for pattern Status vocabulary | May 9 | Per Pattern Sweep Phase 1: patterns 039/040 template-literal contamination + non-canonical Status across 031/034/036/037/038/044-054. Cosmetic + audit-trail benefit. Low priority Docs work. |
| 12e | **Anti-pattern P-16 candidate: "Cross-Agent Residue Accumulation in Shared Working Tree"** | May 10 | Per Code agent's May 10 PreCompact-hook first-use debrief (CC to CIO): residue from multiple agents accumulating in shared-tree because no individual agent has standing to commit others' work under "commit only your own files" + session-end discipline interrupt (Docs remote-control failure). PreCompact hook = detector; cross-agent committing under PM authority = resolver. Distinct mechanism from P-12 (broad git-add) and P-15 (branch-collision). Queued for next Pattern Sweep anti-pattern index update. |
| 12f | **Docs sign-off `git status` inventory pattern** as methodology-corpus candidate | May 10 | Per same May 10 debrief: Docs's discipline of dumping `git status` into the sign-off block + naming what's not theirs is load-bearing for cross-agent recovery. Code agent's analysis: "Docs's discipline of dumping `git status` into the sign-off block + naming what's not theirs is genuinely load-bearing for cross-agent recovery." Candidate for methodology-corpus capture as sign-off best practice. Low priority; needs HOST + Docs concurrence on framing. |
| 12g | ~~"Silent State Mutation in Shared Working Tree" parent meta-pattern candidate~~ — **RESOLVED May 11** (filed as Pattern-068; see R18 in Resolved) | May 10 → May 11 | Promoted to Emerging per PM May 11 directive. |
| 12h | ~~"Coarse Triggers Causing False-Positive Triage Cost" hook-design meta-pattern candidate~~ — **RESOLVED May 11** (filed as Pattern-069; see R19 in Resolved) | May 10 → May 11 | Promoted to Emerging per PM May 11 "close the loop" directive. |
| 12i | **Worktree-default canonical doc update** — Docs lane per PPM May 15 PM directive | May 11 → May 15 | PM ratified worktree-default for all substantive agent work (May 15 ~7:13 AM via PPM memo). Supersedes original 12i codification ask; now Docs needs CLAUDE.md edit + canonical-doc update. HOST owns methodology-corpus implications. CIO tracking. |
| 12j | **Lead Dev D-hook prototype (PreCommit broad-staging + PostPush retry)** — ACTIVE per PM directive cadence | May 11 → May 15 | Per CIO May 15 shared-git-index disposition: B+D ordering concurred; PM ratified B (worktree-default). Lead Dev ships Phase 1 D-hooks fast (PreCommit block on broad staging on main + PostPush retry on race-rejection). Phase 2 B-worktree rollout = PA + Docs lane. |
| 12k | **PreCompact hook refinement** — Docs lane per HOST May 10 framing | May 11 | Per Pattern-069 filing: Docs owns hook script (`.claude/hooks/precompact-signoff-warning.sh`). Three refinement options ranked by leverage: locality differentiation (highest), explicit "safe to compact" path (docs-only), severity reduction for known-safe patterns. CIO no longer owns disposition; tracking for visibility. |
| 12m | ~~methodology-27 Type 2 Dreaming (Anxiety Dreams) entry~~ — **RESOLVED May 15** (filed; see R22; cross-pollination routed) | May 15 | Pulled forward per PM "do anything unblocked" directive 6:53 AM. Type 2 entry filed; Revonsuo TST + Matthew Walker citations; cross-pollination memo to PA cc cohort for Janus/Klatch/OpenLaws fan-out. |
| 12n | **Pattern-070 Cleanup-Job-with-Cancellation-Hygiene** — RESOLVED May 15 (filed by Architect; see R25) | May 11 → May 15 | Architect filed pattern-070-cleanup-job-with-cancellation-hygiene.md; promotion criterion: Anthropic Dreams Type 1 consolidation pipeline lands using four invariants without rediscovery. |
| 12o | ~~methodology-sidecar "Pattern Formation via Successful Imitation"~~ — **RESOLVED May 15** (filed as methodology-29; see R24) | May 15 | Filed alongside methodology-27 Type 2 + methodology-28 slot-availability check. |
| 12p | ~~Registry-pattern watch~~ — **RESOLVED May 15** (filing as Pattern-072 per Lead Dev #1017 third-instance trigger; see 12r) | May 15 | Three-instance threshold per methodology-29 met (task_type model dispatch / #1004 calibration / #1017 output-filter profile dispatch). Lead Dev authors Pattern-072. |
| 12q | **Pattern-071 Audit Logs as Attack Surface filing** — Lead Dev authors | May 15 | Per Lead Dev #1017 methodology candidate memo. Dark-twin-of-Pattern-064: infrastructure that looks like compliance but is actively leak-amplification. Reference impl: #1017 OutputFilterDecision dataclass + invariant guard. Status: Emerging; Proven-promotion on no-exceptions in 4-6 weeks. Slot 071 allocated. |
| 12r | **Pattern-072 Registries that Grow into Architectural Shapes filing** — Lead Dev authors; CIO methodology cosign | May 15 | Per Lead Dev #1017 + 12p watch closure. Methodology-29 instance applied to registries. Status: Emerging; Proven on fourth meaningful consumer (e2e probe-registry is prospective fourth). Slot 072 allocated. |
| 12s | **M2g cleanup discipline meta-pattern candidate** — methodology-29 territory; watch for fourth instance | May 15 | Per CIO May 15 Pattern-064 evolution-note disposition. Three instances inside 48 hours (#1010 May 14 −46 LOC + #1019 May 14 −543 LOC + #1094 May 15 ~−600 LOC) of the same cleanup shape: Phase 0 audit → identify partially-abandoned scaffolding → delete cleanly with LOC-math accountability + cohort cleanup notice memo. One more independent instance triggers methodology candidate filing. |
| 12t | **Audit-cascade preamble Step 0 — worktree-default addition** | May 15 | Per HOST May 15 routed CIO question + CIO disposition memo: yes, add "set up your worktree" as Step 0 to audit-cascade preamble. CIO-owned, ~5 min edit. Lands this weekend or Mon alongside other methodology-corpus work. |
| 12u | **methodology-30 Consumer-Trace Verification for LLM-Touch Claims** | May 15 | Per CXO May 15 routed CIO call on Architect's consumer-trace discipline framing ("LLM-touch claims require consumer trace to actual LLM call"). Methodology-corpus shelf, not Pattern entry. CIO drafts; Architect + CXO review. Slot 30 next-available. Queued for Mon-Tue May 18-19 alongside Type 2 entry. |
| 12v | **Multi-agent coordination doc rewrite** — banner-fix interim; deeper rewrite triggered by multi-agent work surfacing in roadmap | May 16 | Per Lead Dev May 15 methodology-core engine drift fix. Three methodology-core docs banner'd; deeper Option α (rewrite under new architecture) or β (archive) deferred until multi-agent coordination surfaces in roadmap planning. |
| 12w | ~~"Living documentation describing dead code" Pattern-064-adjacent watch~~ — **RESOLVED May 16** (three independent instances in 48h; filing as Pattern-073; see 12x) | May 16 | Three instances: methodology-core docs post-#1094 / StandupConversationRepository docstring (#1079) / `require_request_context` orphan dependency (#1015 audit). |
| 12x | **Pattern-073 (Documentation-Asserted-Behavior Drift) filing** — Lead Dev authors; CIO methodology cosign | May 16 | Per CIO May 16 disposition memo. Three instances inside 48h; methodology-29 territory. Slot 073 allocated. Pattern-064 sibling shape (alive scaffolding for docs). Lead Dev includes `doc-sync-sweep` v0.1 skill response in filing. Status: Emerging; Proven-promotion criterion = one more independent instance within 14 days AND skill-application validation. |
| 12y | **V1 Duty Cycle Phase 0 setup** — PM action; routine creation at `claude.ai/code/routines` | May 16 | Per PM 1:35 PM ratification. v0.3 design + Phase 0/1/2/3 prompts ready in `dev/active/cio-v1-routine-prompts-2026-05-16.md`. PM does Phase 0 (~30 min) later this afternoon; CIO standing for Phase 1 "Run now" verification. First official automated run targeted tomorrow (Sun May 17). |
| 12z | **Manifest-sync codification** — Docs lane | May 17 | Per Lead Dev May 17 MANIFEST out-of-sync observation. Codify "inbox directory = source of truth; MANIFEST = derived index lagging through fanout-to-triage" in CLAUDE.md or methodology corpus. Plus autonomous-loop discipline note: cycles poll `ls inbox/` not MANIFEST. Low priority; ~10 min Docs edit. |
| 12aa | **Postel for memo headers in autonomous-cycle context** — methodology entry candidate | May 17 | Per PM May 17: "be stricter in what we emit, more permissive in what we accept." Outbound CIO memos already standardize on YAML frontmatter (rule met). Inbound parsing in autonomous cycles needs 3-tier extractor (YAML → Markdown bold-headers → first H1) to handle the cohort's memo-convention variety. Phase 4 v2 prompt implements this. Worth memorializing as methodology entry alongside Pattern-073 + methodology-30 batch Mon-Tue. ~30 min focused entry. |
| 18 | **Ship #043 CIO workstream review** | May 15 (kickoff) | Per exec May 15 kickoff. Window May 8–14. Filing due EOD Sun May 17. Target ~500–800 words, role-distinctive analytical overlay. Active this weekend. |

### Watch (trigger-bound)

| # | Item | Trigger | Status |
|---|---|---|---|
| 13 | **Klatch AAXT scaffolded probing methodology** | Lead Dev #927–930 scoping starts | Standing-watch surface filed Apr 27 (`mailboxes/lead/sent/...-audit-s3-klatch-aaxt-scaffolded-probing-trigger-2026-04-27.md`). When Lead Dev pings, CIO walks through the Klatch material. |
| 14 | **Alpha catch-22 capture decision** | ~2 more instances surfacing outside #992 | Operational tier in Innovation Backlog. Promotion to methodology-core entry contingent on the pattern recurring beyond its Apr 30 origin. |
| 15 | **Sparker/Holder formal naming (after #2 disposition)** | Once HOST decides surface | If methodology-core, CIO drafts entry. If CLAUDE.md altitude, HOST drafts and CIO reviews. |
| 16 | ~~Pattern-063/064/065 promotion to Proven~~ — **RESOLVED May 8** | (trigger fired) | All three Promoted; trigger satisfied per evidence in R14. |
| 17 | **BRIEFING-CURRENT-STATE staleness signals** | Hook fires staleness threshold | Per Apr 29 norm: "any agent who notices staleness refreshes." Currently 12d stale (May 8). Cohort hasn't internalized the discipline yet. Worth flagging for HOST role-health-check input. |
| 12n | **Pattern-070 Cleanup-Job-with-Cancellation-Hygiene** — Architect-authored, CIO-cosigned | Architect filing pending | Per Architect May 15 cleanup-job pattern-candidate memo: pattern proposed at slot 070 (12l slot-check applied pre-filing — adoption-before-codification signal). CIO disposition memo May 15: slot allocated; Emerging filing; Architect authors; Proven-promotion criterion is fourth-instance landing without re-discovery. Three existing instances: #1018 EthicsAuditCleanupJob, #1035 CompostingSchedulerJob, #1052 StandupConversationManager. Prospective fourth: Anthropic Dreams Type 1 consolidation job. |
| 12o | **methodology-sidecar "Pattern Formation via Successful Imitation"** — drafting May 19 alongside 12m close | May 15 | Per Pattern-070 disposition memo cosign: the discipline that produced the cleanup-job convergence (clean reference implementation + cohort recognition + reuse without enforcement) is worth capturing as methodology-corpus entry. Filing alongside Pattern-070 makes both more legible. CIO-authored. ~30 min focused work unit. |

### Active

| # | Item | Started | Notes |
|---|---|---|---|
| (none currently) | | | |

### Recently Resolved (kept for one cycle)

| # | Item | Resolved | Evidence |
|---|---|---|---|
| R1 | M1 audit S1 (canonical-term-drift weekly sweep) | May 4 | `canonical-vocabulary-watch.md` v1 shipped commit `7153fcf4` |
| R2 | M1 audit A3 (Flywheel integration py eval) | Apr 28 | Lead Dev retire executed commit `adfd453b` |
| R3 | Pattern-063 PM concurrence on slot allocation | Apr 27 | PA-relayed PM concur memo Apr 27 |
| R4 | Pattern-065 (Continuity Memo Before the Seam) Emerging filing | Apr 27 | `pattern-065-continuity-memo-before-the-seam.md` |
| R5 | methodology-24 (Branch-or-Anchor) filing | Apr 27 | `methodology-24-BRANCH-OR-ANCHOR.md` |
| R6 | methodology-25 (Workstream Review Cadence) filing | Apr 27 | `methodology-25-WORKSTREAM-REVIEW-CADENCE.md` |
| R7 | methodology-26 (Indoor Plumbing Scope Filter) filing | Apr 27 | `methodology-26-INDOOR-PLUMBING-SCOPE-FILTER.md` |
| R8 | A2 Hooks Phase 1 monitoring formal close | Apr 27 | Audit table A2 marked CLOSED |
| R9 | M1 audit cycle full disposition (12 of 12 recommendations) | Apr 27 → May 4 | All recommendations closed or routed |
| R10 | Innovation Backlog reconstruction | Apr 27 | `cio-innovation-backlog.md` |
| R11 | Briefing correction memo for BRIEFING-ESSENTIAL-CIO | Apr 27 | v3 applied Docs May 3 |
| R12 | CIO Code startup routine standing file | Apr 27 | `docs/operations/startup-routines/cio-code-startup.md` |
| R13 | #982 FLY-AUDIT Excellence Flywheel reconciliation issue close | May 8 | Closed via `gh issue close 982` with full evidence |
| R14 | Pattern-063, -064, -065 promotion Emerging → Proven | May 8 | Promotion analysis memo (`dev/active/cio-pattern-promotion-analysis-2026-05-08.md`); commit `8d4cc139`. 062 family now complete (062 component / 063 vocabulary / 064 extension / 065 institutional-knowledge), all Proven. |
| R15 | Pattern Sweep #1025 (staggered audit, Mar 17 → Apr 28 window) | May 9 | CIO-led with 3 subagents (Phases 1, 2B, 2C, 2D) + CIO direct (Phase 2E synthesis, Phase 3 anti-pattern index update, Phase 4 final report). Single session ~3 hours. Final report: `docs/internal/development/reports/pattern-sweep-2.0-results-2026-05-09.md`. Issue #1025 closed. Pattern-066 (Stacked Silent Failures) filed Emerging; Pattern-024 status corrected; anti-pattern index 43 → 49 entries; 9 stale candidates flagged for next-cycle triage. Headline: 062 family completion is window's structural event (61% of 3,361 citations). 1:8 anti-amnesia ratio validated framework. |
| R16 | xpoll brief NEW-since-last-session hook shipped | May 9 | Lead Dev shipped commit `07682bff` within ~24h of CIO routing memo (May 8 → May 9). Three-state signal (NEW > STALE > available); approximation note deferred per "wait-and-see" path. CIO ack memo filed May 10. Closes HOST 360 v0.2 cohort synthesis pull #2 (Apr 27 origin). Cross-pollination consumer-side signal now operational. |
| R17 | Pattern-064 Architect explicit concurrence | May 10 | Architect May 10 memo concurs on Pattern-064 Emerging → Proven (was implicit-via-May-4-review-usage at May 8 promotion). Pattern-064 Evolution updated with #1010 single-ticket framing (all three wild instances closing in one mechanical sweep). Also concur on Methodology-Elevated lifecycle stage proposal (item 1b above). |
| R18 | **Pattern-068 (Silent State Mutation in Shared Working Tree) Emerging filing** | May 11 | Filed Emerging per PM May 11 directive ("we need to solve these issues to avoid a real problem occurring or loss of valuable effort"). Parent meta-pattern subsuming P-13/P-15/P-16/P-17 anti-patterns. Anti-pattern index updated with cross-refs + P-17 (working-tree-path fragmentation) added as fourth child. Innovation Backlog: was Operational #44, now Emerging #46. |
| R19 | **Pattern-069 (Coarse Triggers Causing False-Positive Triage Cost) Emerging filing** | May 11 | Filed Emerging per PM May 11 "close the loop" directive. Hook-design meta-pattern; companion to P-068. Innovation Backlog: was Operational #45, now Emerging #47. Promotion to Proven requires cross-mechanism recurrence (not PreCompact-only). |
| R20 | **Pattern-067 slot conflict resolved (Lead Dev May 9 first-filed wins)** | May 11 | Lead Dev filed `pattern-067-issue-body-reality-mismatch.md` May 9 commit `a2bd06d9`; my filings this morning unwittingly claimed same slot. Architect + Lead Dev coordination memos flagged ~8:35 AM May 11. Renumber resolution: Lead Dev keeps 067; my "Silent State Mutation" → 068; my "Coarse Triggers" → 069. Pattern files renamed via `git mv`; references updated in 4 files (2 pattern files + anti-pattern-index + tracker + backlog); ack memo to Lead Dev + Architect filed. Ironic Pattern-063 instance at catalog layer (per both flag memos); slot-allocation pre-filing check recommended for catalog discipline going forward. |
| R21 | **Pattern-066 PM concurrence loop-close** | May 12 | PM concurrence affirmative for Pattern-066 (Stacked Silent Failures) Emerging slot allocation; loop-close routed through Docs May 12 memo. Closes long-standing tracker item #1a carry-over (filed May 9). Pattern-066 Emerging → Proven promotion-clock starts; trial-application criteria stand. With this concurrence, all four May 9-11 Emerging filings (P-066 / P-067 Lead-Dev / P-068 CIO / P-069 CIO) are PM-acknowledged at their current status. |
| R22 | **methodology-27 Type 2 Dreaming (Anxiety Dreams) entry filed** | May 15 | Filed Emerging-tier methodology-core entry per PM May 12 ratification ("Type 2 should be 'claimed' publicly"). Grounded in Revonsuo's Threat Simulation Theory; Matthew Walker as Bay Area radio candidate. Cross-pollination distribution to Janus/Klatch/OpenLaws routed via PA. PDR deferred to post-M3. |
| R23 | **methodology-28 Pre-Filing Slot-Availability Check filed** | May 15 | Closes original tracker 12l. Codifies the discipline that emerged from May 11 Pattern-067 slot collision. Architect adopted pre-codification May 15 (proposing Pattern-070); adoption-before-codification observation captured in methodology-29. |
| R24 | **methodology-29 Pattern Formation via Successful Imitation filed** | May 15 | Closes original tracker 12o. Sidecar accompanying Pattern-070 (Architect-authored, CIO-cosigned). Names the discipline producing durable patterns through cohort recognition rather than top-down enforcement. |
| R25 | **Pattern-070 (Cleanup-Job-with-Cancellation-Hygiene) filed by Architect** | May 15 | Filed via Architect ack memo this morning. Patterns README updated 69 → 70. Promotion criterion: Anthropic Dreams Type 1 consolidation pipeline lands using the four invariants without rediscovery. |
| R26 | **PM ratified worktree-default for all substantive agent work (via PPM memo)** | May 15 | PM directive 7:13 AM via PPM relay: "yes, all agents should default to worktrees, I think." Operational shift; supersedes original 12i convention codification ask; Docs lands CLAUDE.md edit + canonical doc update. Lead Dev concurrent D-hook phase ships in parallel. Resolves the shared-`.git`-index coordination question PM and Lead Dev raised this morning. |
| R27 | **Pattern-072 (Registries that Grow into Architectural Shapes) promoted Emerging → Proven** | May 16 | #1094 ENGINE-DELETION close-out (`d48bc1d0` May 15 14:38 PST) landed Slack handler dispatch as fourth behavior-deciding consumer of `task_type` registry. All four formalization-discipline invariants intact. Pattern-072 README + Status updated. First sub-day Emerging-to-Proven promotion in catalog (~6h between recognition trigger and Proven trigger) — methodology-29 validation evidence. Lead Dev memo R26 same threshold-event. |

---

## Maintenance Discipline

### When to update

- **At each session start**: review Active + CIO-queued for any items now ready to advance
- **After each substantive session**: capture new items into appropriate tier; move completed items to Recently Resolved
- **When PM input lands**: move from Pending PM to CIO-queued or Active as appropriate
- **At audit cadence**: full sweep; trim Recently Resolved entries older than one cycle

### What this tracker is NOT

- Not the canonical pattern catalog (`docs/internal/architecture/current/patterns/`)
- Not the methodology-core (`docs/internal/development/methodology-core/`)
- Not the project-wide tracker (`exec-open-items-tracker.md` — exec-owned)
- Not a public-facing artifact — CIO working state
- Not synchronized; gaps are findable, not blockers

### Distinction from Innovation Backlog

`cio-innovation-backlog.md` tracks **innovations** across Captured / Operational / Emerging / Reclassified / Closed tiers — methodology and pattern-shaped artifacts in motion across the project.

This tracker tracks **CIO-action items** — pending PM decisions, external waits, CIO-queued work. The two tiers point at different surfaces: an item can be "Captured" in the innovation backlog (e.g., methodology-25 Workstream Review Cadence) and simultaneously absent from this tracker (no pending CIO action). Conversely, an item like "Per-doc disposition review for methodology-core" lives here (CIO-queued) but isn't an innovation per se — it's a corpus-coherence audit deliverable.

---

*Tracker created: May 8, 2026*
*Author: CIO (Code instance, session 5)*
*Origin: PM directive May 8 — "put them in a tracker document so we don't lose them to the transcript, my faulty memory, or your context window"*
