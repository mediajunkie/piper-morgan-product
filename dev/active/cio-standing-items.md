# CIO Standing Items Tracker

**Purpose**: Track CIO-domain items that are pending PM input, blocked on external action, or queued for CIO execution but not yet started. Persistent surface so items don't get lost to transcript / PM memory / CIO context window.

**Origin**: Created May 8, 2026 per PM directive after observing accumulating CIO-domain items spanning multiple sessions. Innovation Backlog (`cio-innovation-backlog.md`) tracks innovation patterns; this tracker tracks pending-action items broader than innovations.

**Duty Cycle role (v0.5 design ratified 2026-05-24)**: This file IS the canonical **Task List** (Doc 2 of the three per-agent duty-cycle docs) under the new design. Per the formalizing-not-proliferating principle, no parallel "task list" doc is created — the standing-items tracker is reframed to serve as the task list of record. Tasks added during Mail Loop step 4 land here. Task Loop reads from here. PM-injected tasks (the load-bearing (0, 1) decision-table row) also land here.

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

⚠️ **Full audit executed 2026-08-23** (first since the 07-13 trim; ~40 days, well past "at audit
cadence"). Same discipline as the welfare-criteria tracker catch two days earlier — a tracker line is
a claim about the world, not the world itself, and this one hadn't been re-checked against ~3.5
months of actual outcomes. Verified via subagent research (git log, `gh issue view`, file existence)
against every item dating April–June, not assumed either way. Full pre-trim content (every item below,
April–August) recoverable via `git log -p -- dev/active/cio-standing-items.md` at this commit's
parent — nothing here is lost, only compacted, per this tracker's own stated recovery policy.

### Genuinely still open, carried forward

| # | Item | Filed | Status |
|---|---|---|---|
| 2 | **Sparker/Holder pattern naming disposition** | Apr 26 | **Confirmed still undecided, ~4 months.** No mention of "Sparker" or "Holder" anywhere in CLAUDE.md or methodology-core. HOST never made the CLAUDE.md-vs-methodology-core call. Genuinely stalled, not resolved-and-forgotten — worth a direct nudge to HOST rather than another quiet carry. |
| 5 | **HOST migration-experience confer, Q3 engagement** | Apr 27 | **Confirmed still open, ~4 months.** HOST acknowledged same-day intent to engage within 24h; no commit, memo, or session-log trace of it happening since. No urgency per HOST's own original framing, but "no urgency" and "never checked again" have compounded into 4 months — worth a light nudge, not an escalation. |
| 7a | **Corpus-coherence cycle proposal** (Pattern Sweep Phase 4 finding) | May 9 | ~60% zero-citation rate at both pattern-catalog and methodology-corpus layers, never actioned. PM/Exec discussion never happened. Still real; low urgency. |
| 7b | **PreCompact hook: 2 of 3 ranked refinement options still unbuilt** | May 11 (orig.), reverified Aug 23 | Only the **lowest-ranked** option ("severity reduction for known-safe patterns") shipped, confirmed live in `.claude/hooks/precompact-signoff-warning.sh` (HARD/SOFT/QUIET tiering). The **highest-leverage** option (locality differentiation) and the docs-only "safe to compact" path are both absent — grepped the script directly, no trace. Worth flagging to Docs (script owner) as a real gap, not busywork: the option actually built was the one ranked lowest. |
| 7c | **Docs sign-off `git status` inventory pattern** — methodology-corpus candidate | May 10 | Needs HOST + Docs concurrence on framing; never pursued. Low priority. |
| 7d | **Metadata-cleanup ticket** — pattern Status-field vocabulary contamination | May 9 | Cosmetic; low-priority Docs work; never filed as an actual issue. |
| 7e | **Anti-pattern P-16 candidate** ("Cross-Agent Residue Accumulation in Shared Working Tree") | May 10 | Queued for a Pattern Sweep anti-pattern index update that hasn't happened since. |
| 14 | **Dashboard welfare-criteria v0.3 — F2 (cross-pair thread staleness)** | Jul 3, reverified Aug 22 | The one remaining unscoped piece after the 08-22 re-audit and Criterion E's resolution (#1680). Spec itself flags this as new work requiring cross-document reference detection, not yet scoped to Exec. |

### Resolved, verified, closing out (evidence only — full detail in git history)

- **Architect Pattern-064 formalization** (#7, Apr 28) — Promoted to Proven May 8; two further Evolution entries since. `pattern-064-extension-without-integration.md`.
- **methodology-34 / Pattern-070 Evolution entry** (#8b, May 27) — the specific blocking deliverable (Evolution entry citing the Anthropic Dreams API 4th-instance validation) landed May 27. Note: Pattern-070's own Status is still Emerging, not Proven — that's a distinct, separate promotion question nobody's actively driving; not re-opening it here.
- **Worktree-default canonical docs** (#12i, May 11–15) — fully landed; `git-worktrees-model-a-setup.md`, `amber-worktree-lifecycle.md`, and CLAUDE.md's own extensive Model A section all confirm.
- **D-hook prototype, PreCommit half** (#12j, May 11–15) — shipped, just much later than tracked (Aug 3, `pre-commit-broad-staging-warn.sh`). **PostPush-retry half never built as its own hook** — superseded in practice by `mail-send.sh`'s existing rebuild-and-retry-on-non-fast-forward, a different but equivalent mechanism. Closing both halves as done (one shipped, one superseded), not carrying forward.
- **Manifest-sync codification** (#12z, May 17) — substantively covered by CLAUDE.md's mailbox-discipline section (MANIFESTs recipient-owned, mail-send.sh v3 self-reconciliation documented).
- **BRIEFING-CURRENT-STATE staleness response** (Watch #17) — fully institutionalized; CLAUDE.md has a dedicated "MANDATORY when triggered" section, SessionStart hook checks it. The original ask (turn an informal Apr 29 norm into something the cohort follows) is exactly what exists now.
- **Audit-cascade preamble Step 0** (#12t, May 15, "~5 min edit") — **landed this fire** (`.claude/skills/audit-cascade/SKILL.md` v1.1), ~3 months after the disposition memo. Reworded from the original May 15 text to match Model A's stable-worktree-reuse reality rather than landing stale wording unchecked.
- **Ship #039 formal close** (#4) — no live reference anywhere since publish; safe to consider closed by age, no PM formality actually needed.
- **Dashboard welfare-criteria v0.3, everything but F2** (#14) — Q2/Q3, C1-C3, F3, B/B-bis done via freeze-watchdog + cohort-attention-rollup infrastructure (re-audited 08-22); Criterion E ruled by HOST and filed as #1680, routed to Lead (08-22). Only F2 remains — see "still open" above.

### Obsolete, dropping (context moved past the item, not resolved in the item's own terms)

- **Roadmap v17 review** (Watch, blocked since May 28 on a PPM draft) — v17 was only ever a draft that got superseded; live roadmap is now v18.7 (`docs/internal/planning/roadmap/roadmap.md`). If the underlying ask (review §Methodology Corpus content) still matters, it needs re-filing against v18.7, not resumed against a version that no longer exists.
- **Klatch AAXT scaffolded probing** (Watch #13, trigger = Lead Dev #927–930 scoping) — **trigger fired and fully resolved months ago** (#927–930 all closed mid-April, shipped with evidence). No record the CIO walkthrough this item promised ever happened. Naming that honestly rather than pretending it did: a missed follow-through, not a false alarm. Not worth resurrecting 4 months later — the Klatch material has presumably moved on too — but worth remembering as a case where a fired trigger silently fell through, the same failure shape as the freeze-watchdog gaps found elsewhere this month.
- **12n/12o duplicate Watch-section entries** (Pattern-070, methodology-sidecar) — both already correctly marked RESOLVED in the CIO-queued section; the Watch-section copies were stale leftovers from before those resolutions, never cleaned up. Removed.
- **#15 ID collision** — "Sparker/Holder formal naming" and "Ship #051 workstream review" both used slot #15 in different sections. Renumbered Sparker/Holder to #2 (merged with its Pending-PM duplicate) rather than continue the collision.
- **"Carried from 2026-08-07 STOP" block** (below the old footer, pre-audit) — all four items in it are now resolved and superseded by the current `cio-carry-forward.md`: memory-index format (Lead's packing fix, 08-16), mail-protocol overlap (superseded by mail-send.sh v3), chess-board idea (design pass delivered 08-20), freeze-detector-has-no-caller (the entire freeze-watchdog/cohort-attention-rollup infrastructure built since IS the caller). Removed rather than carried forward stale.

### Watch (trigger-bound)

| # | Item | Trigger | Status |
|---|---|---|---|
| 14a | **Alpha catch-22 capture decision** | ~2 more instances surfacing outside #992 | Operational tier in Innovation Backlog. Promotion to methodology-core entry contingent on the pattern recurring beyond its Apr 30 origin. Still watching; no new instances found this audit. |
| 14b | **M2g cleanup discipline meta-pattern candidate** — methodology-29 territory | 4th independent instance | Three instances inside 48h back in May (#1010, #1019, #1094). One more independent instance triggers filing. Still watching. |

### Active

| # | Item | Started | Notes |
|---|---|---|---|
| (none currently) | | | |

### Recently Resolved (kept for one cycle)

| # | Item | Resolved | Evidence |
|---|---|---|---|
| (none currently — trimmed 2026-08-23, see the audit block above) | | | |

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

This tracker tracks **CIO-action items** — pending PM decisions, external waits, CIO-queued work. The two tiers point at different surfaces: an item can be "Captured" in the innovation backlog (e.g., methodology-25 Workstream Review Cadence) and simultaneously absent from this tracker (no pending CIO action).

---

*Tracker created: May 8, 2026*
*Author: CIO (Code instance, session 5)*
*Origin: PM directive May 8 — "put them in a tracker document so we don't lose them to the transcript, my faulty memory, or your context window"*
*Audited and compacted: 2026-08-23 (first full sweep since 2026-07-13) — pre-audit content recoverable via `git log -p` at this commit's parent.*
