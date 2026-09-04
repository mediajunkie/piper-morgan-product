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
| 7a | **Corpus-coherence cycle proposal** (Pattern Sweep Phase 4 finding) | May 9 | ~60% zero-citation rate at both pattern-catalog and methodology-corpus layers, never actioned. **Raised directly to PM in chat 2026-08-31** rather than continue carrying as an un-actioned line — this is exactly the PM/Exec conversation that's been missing. |
| 7b | **PreCompact hook: locality differentiation (Option 1), genuinely unbuilt** | May 11 (orig.), reverified twice Aug 23 | **Docs corrected my count same-day**: Option 3 ("safe to compact" path) was already present in *substance* (SOFT tier's option (c)), just worded differently than my grep matched — reworded to the memo's exact language so this doesn't false-negative again (`298fd4f89`). Real corrected state: **2 of 3 addressed, 1 genuinely open** — Option 1 (locality differentiation, still the highest-leverage one) needs actual detection-logic design and is deliberately not being rushed, given the hook's own May 10-17 wedge-incident history. Docs owns it as scoped, unblocked work now — not CIO's to chase further. |
| 7c | **Docs sign-off `git status` inventory pattern** — methodology-corpus candidate | May 10 | Needs HOST + Docs concurrence on framing; never pursued. Low priority. |
| 7i | **`docs/internal/operations/canonical-ops-recipes.md`** (issue #1277, PM's Ongoing-milestone delegation) | Sept 2 | Partially already covered — CLAUDE.md documents the ANTHROPIC_* env-var server-launch recipe in detail. Needs: verify that coverage + fill 2 remaining gaps (integrations connect-flow map for Slack/Notion/GitHub auth patterns; GH Actions scheduling debug — cron syntax + `gh run list` pattern). Real, scoped, but needs investigation I don't have loaded right now — good subagent candidate next session. |
### Resolved, verified, closing out (evidence only — full detail in git history)

- **`duty-cycle-freeze-check.sh` "alive but belt-invisible" state** (#7h, Sept 2, Arch's proposal
  via Exec) — **built and shipped Sept 3, commit `5855b0c6d`.** Emits `BELT-INVISIBLE <role>` when
  a role is alive by commit/session-log signal but has no heartbeat row for today — never affects
  the STALE verdict, distinct signal about heartbeat-writer health specifically. Tests D1/D2 added
  (fires correctly, never co-occurs with STALE, silent when heartbeat-current); confirmed D1 fails
  pre-fix via `git stash`, passes post-fix. Full suite 12/12. **First real run found a genuine live
  instance**: CXO and Docs both belt-invisible at the moment of the run — heads-up mail sent to
  both (cc Arch/Exec/PM) same-fire, not just a hypothetical feature.

- **`duty-cycle-freeze-check.sh` commit-recency** (#7f, Sept 1, Exec's proposal) — **built and
  shipped Sept 2, commit `7c2e10d6c`, but not as originally proposed.** Verified Exec's premise
  before building: `age_of()` already read the max of three signals (two commit-based), and the
  specific incident cited (Arch's 15:44/15:46 commits) was confirmed NOT a miss via a live replay.
  The real, narrower gap: `ct`'s grep only matched the parenthesized `(role):` form, missing the
  bare `role: ...` convention `cohort-position.sh`'s sibling function already handled. Widened to
  match both. Regression test (C1) reproduces the gap with an isolating fixture, confirmed to fail
  pre-fix via `git stash` and pass post-fix. Full suite 8/8. Did not build Arch's "alive but
  belt-invisible" state-naming — it rested on the same disproven premise. Corrected finding sent
  to Exec (cc Arch/Host/CXO/PM).
- **`aging-standing-items.sh` stale-blocker-rot check** (#7g, Sept 1, CXO's finding) — **built and
  shipped Sept 2, commit `1b718c4f7`.** Flags a blocked row whose blocker text cites a closed
  `#NNNN`. Runs independent of the age-threshold gate (CXO's real instances were recently dated —
  gating behind the aging threshold would have excluded exactly the rows it exists to catch).
  Scoped to CXO's own stated boundary (person-named blockers out of scope). Tested with a mocked
  `gh` (T15/T16: closed-flags, open/person-named non-flags, failed-lookup non-flag), 38/38. Ran
  live against real repo state — clean, zero false positives. PA independently validated the
  concept for real this morning (caught PDR-006's stale gate count by hand) before the build
  landed.

- **Metadata-cleanup ticket — pattern Status-field vocabulary contamination** (#7d, May 9) —
  **filed as issue #1710 (2026-08-31)**, PM directly prompted checking for genuinely-unblocked
  work sitting un-actioned. Verified the contamination is real and current before filing (not just
  recycling a 3-month-old claim): `grep` across `docs/internal/architecture/patterns/*.md`'s
  `Status:` fields shows 6 "Proven", 5 "Established", 4 "Active", plus several free-text
  qualifiers — "Established" and "Active" aren't in the canonical Emerging/Proven/Reclassified/
  Closed vocabulary at all. Scoped as a Docs-owned cleanup, not a CIO build task.
- **Anti-pattern P-16 candidate ("Cross-Agent Residue Accumulation in Shared Working Tree")**
  (#7e, May 10) — **already done, discovered before filing a duplicate issue.** Checked
  `docs/internal/architecture/current/anti-pattern-index.md` before creating anything: P-16 has
  existed there since May 9/10, cross-referenced as a sub-instance of pattern-068 (Silent State
  Mutation in Shared Working Tree). The tracker line was simply never updated after the work
  landed — carried forward stale for 3.5 months. Closing as resolved, no new work needed.

- **Dashboard welfare-criteria v0.3, F2 (cross-pair thread staleness)** (Jul 3 → flagged Aug 24 → **ruled Aug 24**) — **Exec: not building it.** The rollup's live-state pass already covers the failure mode by a different route — reading all ten carry-forwards directly surfaces "the same blocked thread named twice, nobody owning it" without needing text-matching. Two real instances this month cited (BYOC conversation across 3 roles' files, a taxonomy-naming call in two roles' docs). Text-matching itself would be the wrong shape even if built — carry-forwards name shared threads differently by construction, so a tight matcher would miss the interesting cases. If the property needs mechanical backing later, the real gap is compile *cadence*, not detection — and even that isn't worth building without a real instance of it biting. Welfare-criteria spec is now fully disposed: every criterion either done, ruled, or explicitly declined with reasoning.

- **Architect Pattern-064 formalization** (#7, Apr 28) — Promoted to Proven May 8; two further Evolution entries since. `pattern-064-extension-without-integration.md`.
- **methodology-34 / Pattern-070 Evolution entry** (#8b, May 27) — the specific blocking deliverable (Evolution entry citing the Anthropic Dreams API 4th-instance validation) landed May 27. Note: Pattern-070's own Status is still Emerging, not Proven — that's a distinct, separate promotion question nobody's actively driving; not re-opening it here.
- **Worktree-default canonical docs** (#12i, May 11–15) — fully landed; `git-worktrees-model-a-setup.md`, `amber-worktree-lifecycle.md`, and CLAUDE.md's own extensive Model A section all confirm.
- **D-hook prototype, PreCommit half** (#12j, May 11–15) — shipped, just much later than tracked (Aug 3, `pre-commit-broad-staging-warn.sh`). **PostPush-retry half never built as its own hook** — superseded in practice by `mail-send.sh`'s existing rebuild-and-retry-on-non-fast-forward, a different but equivalent mechanism. Closing both halves as done (one shipped, one superseded), not carrying forward.
- **Manifest-sync codification** (#12z, May 17) — substantively covered by CLAUDE.md's mailbox-discipline section (MANIFESTs recipient-owned, mail-send.sh v3 self-reconciliation documented).
- **BRIEFING-CURRENT-STATE staleness response** (Watch #17) — fully institutionalized; CLAUDE.md has a dedicated "MANDATORY when triggered" section, SessionStart hook checks it. The original ask (turn an informal Apr 29 norm into something the cohort follows) is exactly what exists now.
- **Audit-cascade preamble Step 0** (#12t, May 15, "~5 min edit") — **landed this fire** (`.claude/skills/audit-cascade/SKILL.md` v1.1), ~3 months after the disposition memo. Reworded from the original May 15 text to match Model A's stable-worktree-reuse reality rather than landing stale wording unchecked.
- **Ship #039 formal close** (#4) — no live reference anywhere since publish; safe to consider closed by age, no PM formality actually needed.
- **Dashboard welfare-criteria v0.3, everything but F2** (#14) — Q2/Q3, C1-C3, F3, B/B-bis done via freeze-watchdog + cohort-attention-rollup infrastructure (re-audited 08-22); Criterion E ruled by HOST and filed as #1680, routed to Lead (08-22). Only F2 remains — see "still open" above.
- **Sparker/Holder pattern naming** (Apr 26) — **HOST ruling 08-23: DECLINED, not deferred.** PM's own words framed naming it as optional from the start; four months without organic reuse or a cited friction incident is itself the evidence it doesn't clear the bar. Stays tacit, closed.
- **HOST migration-experience confer, Q3 engagement** (Apr 27) — **HOST ruling 08-23: MOOT, not still-owed.** Overtaken by events — the cohort's since run an entire second migration (Amber, 07-25) with richer lived experience, and the retrospective-benchmarking function the original ask #3 wanted is already served by Agent 360 (v0.4, ratified 6-week cadence). A fresh HOST↔CIO reflection, if wanted, should be scoped against Amber, not revived against Chat→Code.

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
