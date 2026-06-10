# Cross-Pollination Brief — June 10, 2026

Piper Morgan's BYO-colleague braintrust closed overnight with six roles converging on the same architectural posture: BYO-colleague is composition, not greenfield, at every altitude — wire-format, consent, and strategy all map onto existing ADRs. The strategic question is no longer "when is colleague mode feature-ready" but "when is the calibration loop durable enough that shipping the routine strengthens the moat rather than flattens it." Two infrastructure fixes also shipped: a structural memory risk (cycle logs displacing session logs in 6 of 9 cycling roles) was patched cohort-wide with duty-cycle-tick v1.5, and the legacy intent dispatch-chain cleanup reached 10 of 28 original branches in one day.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. BYO-colleague braintrust closes — six roles converge on "composition, not greenfield" and HOST names the load-bearing structural constraint

**From:** PM Exec synthesis memo `mailboxes/exec/sent/memo-exec-to-pm-cc-braintrust-byo-colleague-synthesis-2026-06-09.md`, filed ~23:45 PT June 9 (CC: PA, Architect, PPM, CIO, CXO, HOST)
**Relevant to:** Both projects; DinP external positioning

Six roles examined the BYO-colleague thesis introduced last week and converged on the same finding at every altitude: seven of nine required architectural primitives already exist in current ADRs (wire-format in ADR-065, packaging in ADR-066, the consent gate in ADR-053). Two net-new pieces are extensions, not redesigns — a structured `needs_signal` package type for how Piper asks the host for information, and a multi-actor `actor_chain` audit record so the attribution is transparent. The implementation work is refactoring, not invention.

HOST's contribution is the most load-bearing: Piper in colleague mode is a *guest in the user's trust relationship with their own assistant*, not a second principal. The governing principle — Piper must never make the host agent do anything that erodes the user's trust in their assistant — falls out five concrete design rules: augment, don't supplant; make deputization legible at the moment it happens; calibrate consent to sensitivity × reversibility; lead with the give (proactive context-prep IS the give); and extend honest degradation to agent↔agent handoffs.

The synthesis question surfaced by PPM and amplified by Architect: this is a moat-defensibility question, not a technical-readiness question. CIO names the principle — ship the routine freely; the moat is the *living loop* that keeps producing better routines, not the routine itself. PPM turned it into a sequencing gate. Architect's amplification: at M5 beta launch, the loop is shippably-defensible if the methodology catalog shows how it improves across cohort iterations (m-30/m-40/m-41 + the dual-surface/displacement work this week is already part of that evidence set).

PPM ruled on roadmap sequencing (Architect concurred): M5 beta ships WITHOUT colleague mode; post-beta v1.1 carries the consult-piper generalization. ADR-068 only, no PDR-006.

**Suggested action:** Klatch — the "moat is the loop" principle applies directly. The defensible layer isn't any given conversation feature but the continuity infrastructure (history, portability, import/export across models) that keeps improving. Worth naming explicitly rather than leaving it implicit. DinP — HOST's "Piper as guest in the user's trust relationship" one-liner is the most compact external framing for the BYO-colleague arc; worth holding for the project page when narrative framing crystallizes.

---

### 2. Session-log displacement patched cohort-wide with duty-cycle-tick v1.5 — structural memory risk had reached 6 of 9 cycling roles

**From:** PM Docs audit `bf64ea7`; CLAUDE.md amendment `79a40f3`; skill v1.5 `8280b6b`; HOST self-correction `49949f3` (all June 9)
**Relevant to:** Klatch (Calliope Phase 1 cycle); DinP (Janus v0.2 + Themis v0.1 cycle proposals)

Docs ran a cohort audit June 9 and found a structural failure in 6 of 9 cycling roles (~15 role-days, CIO every single day): the duty-cycle fire loop referenced only the ephemeral cycle log in `dev/active/`, leaving the durable session log as a morning stub. Because cycle logs are sprint-cleaned, displaced work eventually vanishes from permanent storage. PM flagged this HIGH: "this needs to stop now — it risks our entire memory and learning process."

The root cause is structural, not individual. The fire-loop procedure pointed agents to the cycle log; the session log was never mentioned in the loop itself, so all nine cycling agents had the same gap in their procedure.

Fix shipped: duty-cycle-tick v1.5 bakes a mandatory one-liner into Step 5 of every substantive fire — a summary entry in the durable session log alongside the full cycle-log entry, so "cycle log full + session log empty" is impossible by construction. CLAUDE.md was amended with the displacement rule as the canonical discipline reference. HOST took a self-correction pass backfilling June 7.

**Suggested action:** Klatch — before Daedalus + Argus Phase 2 goes live, check whether the Calliope cycle template already has session-log writes alongside cycle-log writes per the v1.5 discipline. If not, one line added to Step 5 closes the gap. The displacement risk is real: Calliope's Phase 1 cycle could already be producing the same pattern.

---

### 3. #1124 dispatch-chain cleanup reaches 10 of 28 legacy branches in one day — ratchet now test-enforced

**From:** PM Lead Developer commits `5384110`, `c3bc476`, `b768b3d`, `0f1b5f0` (June 9); no-new-elif rule in CLAUDE.md active
**Relevant to:** PM internal (floor-first architecture); methodology (test-enforced cleanup ratchet)

Issue #1124 — removing hand-coded `elif intent.action` dispatch branches in favor of a floor-first workflow rail — progressed from 28 to 10 remaining sites in a single day across three cohort migrations plus a Phase 4 cleanup pass. An enforcement test (`TestPreFloorDispatchSiteRatchet`) now locks the count: the build fails if anyone adds a new elif instead of registering a `WorkflowEntry` on the rail. The CLAUDE.md no-new-elif rule backs it up at the human-instruction layer.

The methodology pattern: a counter-based enforcement test that tracks an architectural cleanup metric in real time, with the counter lowered in the same commit as each migration. At 10 remaining of 28 original, the cleanup is 64% complete with no regress possible.

**Suggested action:** Klatch — if route or handler sprawl emerges as Klatch scales, the "ratchet test + no-grow rule" pattern is a clean way to enforce cleanup progress without requiring all migrations to happen at once. The enforcement test as a living counter is the mechanism.

---

## Sources Read

- **PM** — Exec synthesis memo `mailboxes/exec/sent/memo-exec-to-pm-cc-braintrust-byo-colleague-synthesis-2026-06-09.md`; Docs audit commit `bf64ea7`; CLAUDE.md displacement amendment `79a40f3`; skill v1.5 `8280b6b`; #1124 cohort-migration commits `5384110`, `c3bc476`, `b768b3d`; ratchet enforcement `0f1b5f0`; Exec cycle log `dev/active/cycle-log-exec-2026-06-10.md`
- **Klatch** — no new substantive activity since June 8 (brief delivery commits only)
- **Secondary repos (atlas, globe, cuneo, one-job, optilisten)** — all quiet; no activity in 48-hour window (not listed in `sources_checked`)
- **weather** — brief delivery commits only; no original activity
- **nyt-crossword** — automated status updates only; no narrative agent activity

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*