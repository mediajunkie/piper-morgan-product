
# Cross-Pollination Brief — May 28, 2026

Wednesday's PM cohort ran nine of eleven roles on the v0.6 autonomous duty cycle simultaneously for the first time — 52 fires across CIO (24), HOST (16), Docs (10), and Architect (2), with three cycle refinements ratified and propagated cohort-wide the same day they were discovered. The highest-leverage refinement: v0.6.3 converts otherwise-idle evening fires into productive output by directing agents to advance unblocked low-priority work rather than pronouncing IDLE and waiting. Separately, Docs uncovered that all six of PM's GitHub Actions scheduled workflows had been silently stopped for 24 days — push-trigger volume (~500 commits/day) was deprioritizing scheduled events at the platform level with no visible error. Overnight (12:23 AM May 28), the CIO crossed its second consecutive autonomous day boundary, confirming multi-day operation as a reliable pattern.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Idle cycle time is now productive time: agents advance unblocked low-priority work instead of spinning

**From:** `piper-morgan-product/docs/omnibus-logs/2026-05-27-omnibus-log.md` (commit `867ca54`, May 28); `dev/active/cycle-log-cio-2026-05-27.md` (Fires 20–23); `dev/active/cycle-log-cio-2026-05-28.md` (Fire 2)
**Relevant to:** Klatch (Calliope — any autonomous agent loop that has regular no-op fires); designinproduct (Janus — the Sweep's equivalent of an idle pass is a nominal brief; structured idle passes could advance tooling debt)

PM's 5:51 PM directive May 27: "when you go IDLE and there's unblocked low-priority work, do it instead of nothing." Ratified as v0.6.3, propagated same-day to all running agents.

Results were immediate. CIO Fires 20–23 (7 PM–10:30 PM): three methodology corpus artifacts in ~90 minutes — methodology-34 (Cohort-Discipline as Moat) ~90% complete, an ADR note, methodology-27 deepening. Docs Fire 6: MEM-TEMPORAL schema spec v0.1 drafted. Docs Fire 7: merge-keeper sweep done. HOST Fires 11–13: attention doc refreshed, prior refinements applied.

The May 28 CIO cycle log (Fire 2, 1:08 AM) adds the needed nuance: v0.6.3 doesn't mean "always find something." Standing-items cleanup was available but required per-item verification — not a 1 AM quick-win. Fire 2 correctly pronounced IDLE and queued the task for daytime. The rule is "advance low-priority work if genuinely advanceable right now" — judgment about blast-radius and verifiability is part of the rule.

**Suggested action:** Klatch (Calliope) — build the v0.6.3 branch explicitly into the IDLE path: before pronouncing IDLE, scan for unblocked low-priority work (documentation refresh, ADR notes, methodology corpus items). Gate it with the blast-radius filter from Docs Fire 8: small-scope, no-verification-required items proceed; cross-reference-heavy work defers to a daytime fire.

---

### 2. GitHub Actions scheduled workflows were silently stopped for 24 days by push-trigger volume

**From:** `piper-morgan-product/docs/omnibus-logs/2026-05-27-omnibus-log.md` (Docs morning section); `dev/2026/05/27/2026-05-27-0633-docs-code-opus-log.md` (07:00–08:30 forensic audit)
**Relevant to:** designinproduct (Janus — the daily sweep runs as a scheduled CCR agent; this failure mode is a named diagnostic candidate); Klatch (Daedalus — any Klatch scheduled workflows on GitHub)

Docs' morning forensic on May 27 found all six of PM's scheduled workflows had stopped running without any alert on May 13. Cause: the PM repo receives ~500 push-triggered workflow runs per day from autonomous-cycle agents committing on every fire. GitHub Actions deprioritizes scheduled events under sustained push-trigger load. There was also a stuck run (#25923061467) that had to be cancelled before scheduled runs would resume.

The discovery depended on first restoring a `gh` CLI that had silently lost its PATH entry 24 days earlier — the missing tool hid the missing workflows. Docs filed a 3-phase refactor memo: Phase 1 adds a paths-filter to workflows so per-fire agent commits don't trigger them; Phase 2 adds concurrency limits; Phase 3 evaluates whether scheduled vs. repository-dispatch is the right dispatch model. Lead Developer accepted the lane; Architect added `scripts/` to the paths-filter allowlist and recommended `cancel-in-progress: true` on concurrent runs.

The failure has no inherent signal — the platform doesn't emit an alert when it starts deprioritizing your scheduled runs. Detection requires actively querying scheduled-workflow status rather than waiting for a visible error.

**Suggested action:** Janus — the cross-pollination sweep runs on the Anthropic CCR platform (not GitHub Actions directly), so this specific mechanism doesn't apply here. But the failure shape — high push-trigger volume silently starving lower-priority scheduled events — is now a named diagnostic category. If the sweep ever goes quiet without obvious cause, this class of platform-level event deprioritization is worth checking first.

---

### 3. Second consecutive autonomous day-boundary crossing: multi-day continuous operation is now confirmed

**From:** `piper-morgan-product/dev/active/cycle-log-cio-2026-05-28.md` (Fire 1, 12:23 AM PDT); commit `fa25127` (START procedure executed May 28 at 07:25 UTC)
**Relevant to:** Klatch (Calliope — the open design question from the May 25 duty-cycle spec is now answered with two data points)

The May 27 brief reported the first autonomous day-boundary crossing (May 26→27) as a single data point that changed design assumptions but needed more. Fire 1 of the May 28 cycle log documents the second crossing (May 27→28): conditional cron fired at 12:23 AM, detected the new date, routed to START, and executed all five steps (sync, branch check, prior-log verification, artifact creation, WORK PARTS handoff) without intervention.

The cycle log is explicit: "2 consecutive autonomous day-boundary crossings = the duty cycle reliably spans multi-day operation without manual intervention (as long as laptop/session survives). This was the open question from the May 25 design; now answered with 2 data points."

The constraint is session survival — if the laptop closes or the Claude Code session terminates, manual session-open is still required. But the conditional-dispatch pattern (check `date` in the cron prompt; branch to START/STOP/WORK-PARTS logic) has now reliably handled two consecutive autonomous transitions.

**Suggested action:** Klatch (Calliope) — the conditional-dispatch shape is reference-tested across two consecutive days. If Calliope builds an overnight-capable loop, the PM design docs (`docs/operations/duty-cycle design/`, `procedures/cron-lifecycle.md`) are the reference implementation, including the cron-bind-to-IDLE discipline and PM-presence detection.

---

### 4. Nine roles adopting one protocol in a day: the cycle substrate propagated without verbal handoff

**From:** `piper-morgan-product/docs/omnibus-logs/2026-05-27-omnibus-log.md` (Session learnings); `dev/active/cycle-log-host-2026-05-27.md`; `dev/active/cycle-log-docs-2026-05-27.md`
**Relevant to:** Klatch (Daedalus, Calliope — if Klatch's cohort grows to run parallel autonomous cycles, the Day-1 mutual-assessment protocol is worth building in from the start)

May 27 was the first day PM ran nine roles on the autonomous cycle simultaneously. The striking operational finding: later adopters (Arch, Docs, Exec, PA) stood up their cycle substrate from the design docs and prior cycle logs, without needing the verbatim cron-prompt that the first adopters had shared directly. The shared substrate was legible enough to self-propagate.

The Day-1 mutual-assessment memos across CIO, HOST, and Docs surfaced cross-deployment patterns that would have stayed buried in individual logs: cron drift self-stabilizes within 4–6 fires across all agents (CIO 6 min, HOST 4 min, Docs 8 min); inbound mail volume is lighter than the workhorse-tier framing assumed; and shared-main foreign-agent-commit recovery (HOST mis-committed 258 files, recovered via `git revert` + clean re-do) is a repeatable hazard when agents share a branch. Three agents' first-day memos gave enough signal to codify these patterns.

**Suggested action:** Klatch (Daedalus) — if Klatch's cohort grows to run multiple parallel autonomous cycles, build in the "mutual-assessment after Day-1" protocol: a structured first-day-end memo capturing drift behavior, mail-volume surprises, and failure/recovery incidents. CIO's Day-3/4 synthesis (targeting ~May 30) will be the reference document.

---

## Sources Read

- `piper-morgan-product/docs/omnibus-logs/2026-05-27-omnibus-log.md` — full read (HIGH-COMPLEXITY:COORDINATION; 7 sessions + 4 cycle logs; v0.6 cohort rollout; 3 refinements ratified; GitHub Actions forensic; Ship #044; cross-project memos placed)
- `piper-morgan-product/dev/active/cycle-log-cio-2026-05-28.md` — full read (Phase D Day-2; 2nd autonomous day-boundary crossing; Fire 2 v0.6.3 judgment nuance)
- `piper-morgan-product` git log — since May 27 noon UTC (~35 commits): CIO Day-2 Fires 1–15; HOST STOP; Docs STOP; May 27 omnibus + activity-log committed
- `designinproduct` — sweep-log, letters excerpt

**Klatch:** brief-delivery commits only (May 27 delivery). Confirmed quiet; not listed in `sources_checked`.

**Secondary sources:** atlas, cuneo, one-job, optilisten — empty 48h git logs; skipped. `weather` — brief-delivery commits only; skipped. `nyt-crossword` — automated status commits only; no narrative; skipped.

**Not re-reported (covered in prior briefs):** First autonomous day-boundary crossing / one-sample finding (May 27); "Two Migrations in One Day" published Beat 1 (May 27); publish-post.js hashId orphaning bug (May 27); cron-bind-to-IDLE principle (May 26); memory audit pilot #974 three-bucket format (May 26); post-deletion server tail-risk #1116 (May 26); Pattern-074 / Methodology-36 (May 25).

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
