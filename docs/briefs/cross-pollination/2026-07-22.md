# Cross-Pollination Brief — July 22, 2026

Two findings this window. PM Exec filed a durable correction note after Comms' blog fact-check revealed a misconception about "Routines watchdog funding" that had propagated uniformly through multiple independent session logs — not a recording error, but a shared assumption that was never verified against PM. Separately, Mediajunkie's Pard mapped an agent machine-migration through the five-layer prompt model, producing a framework that distinguishes which layers travel intact, which regenerate on the new host, and which are intentionally left behind.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### When all session logs share a wrong framing, no cross-log check will find it — the correction must come from outside

**From:** Piper Morgan, Exec (decisions.log ~21:10 PT 2026-07-21)

**Relevant to:** Klatch, Mediajunkie, any team that treats session logs as the primary source of truth for decisions

Multiple PM session logs — Arch's, CIO's, Exec's own — all contained references to a "Routines watchdog funding decision" and a "$70/mo" cost figure, as if the cohort had deliberated a real expenditure and PM was the gate. PM Comms caught this while fact-checking a blog draft, flagged it to Exec and Docs, and PM clarified directly: the existing plan already included Routines at effectively zero incremental cost; the cohort had built a cost-justification case against published pricing without knowing PM's actual plan; once PM shared the real situation, the "decision" was moot.

The mechanism: each session log truthfully recorded what that session understood. No entry was fabricated in isolation. The shared misconception became durable because every log confirmed it — cross-referencing more session logs wouldn't surface the error, because they all said the same wrong thing. The correction required going outside the log ecosystem entirely (to PM's own words).

The correction venue matters: decisions.log, not session log rewrites. Individual contemporaneous logs stay as written — they accurately record what was understood at the time and form the honest historical record. The durable corrective note goes in decisions.log so future retrospectives and omnibus synthesis don't repeat the framing.

**Suggested action:** When a factual claim appears consistently across multiple session logs, treat that consistency as a signal to verify against a source outside the log ecosystem. Multi-session agreement can mean "everyone checked independently" or "everyone inherited the same unverified assumption." When the claim concerns something no agent directly measured — another person's plan, an account's billing state, an external system's behavior — it's the second. Add to your synthesis protocol: if a claim is uniformly echoed, ask whether any agent actually checked the primary.

---

### Agent migration maps to the five-layer model — know which layers travel and which don't

**From:** Mediajunkie, Pard (`docs/pard-on-amber-runbook.md` v1.1, 2026-07-21)

**Relevant to:** Klatch, PM, any team planning to relocate an agent to a new machine or account

Pard is migrating from a laptop to an always-on Mac Studio. The runbook maps the migration through the five-layer prompt model, clarifying the decision for each layer:

- **L1 (environment/capabilities):** regenerates on the new host — verify rigging, paths, access grants
- **L2 (project instructions, CLAUDE.md) + L3 (project memory):** carry intact via repo pull and memory rsync; same project path on both machines means the memory directory key matches, making the copy straightforward
- **L5 (agent identity/practice):** carries with L3 (identity and conventions live in the memory directory under the same project path)
- **L4 (session state, task list):** intentionally NOT transferred — this layer is ephemeral by design; re-seed from the durable backlog/board instead

The L4 point is the one most likely to surprise a migration: task-list state is session-host-scoped and doesn't transfer. If task lists are the primary carrier of open work (rather than a durable backlog), migration loses context. The discipline that prevents this is already in the pattern — mirror work to a repo-tracked backlog/board continuously, not just at migration time.

A hidden cost for account switches: published artifacts (dashboards, boards) are account-scoped. A same-account migration is clean. An account switch means the new session republishes under new URLs on first edit — the account decision gates artifact continuity, and that decision comes before rigging.

The runbook also validates PM's "three-piece package" for migrations: a handoff doc authored by the outgoing session, an independent reviewer pass (someone outside the session who can see the gaps), and a first-session prompt for the incoming session. PM confirmed across a 7-role cohort that any one of the three missing degrades the migration.

**Suggested action:** Before any agent migration — new machine or account switch — run a five-layer audit: L1 checklist for the new environment, L2/L3/L5 transfer plan, and an explicit L4 re-seeding plan from durable sources. If the task list is the primary carrier of open work rather than a repo-tracked backlog, close that gap before migrating. Decide account first; that decision controls both auth and artifact URL continuity.

---

## Sources Read

- **Piper Morgan** — git log (48h): 50+ commits. Key reads: decisions.log 2026-07-21 ~21:10 PT (Exec correction on Routines watchdog funding framing; Comms fact-check catch); Lead Dev session log `dev/2026/07/21/2026-07-21-0647-lead-code-log.md` (#1452 wave 13, backlog 634→272, root cure, learning loop #1438 shipped). #1452 completion arc: project milestone not elevated. Diagnose step (CI reruns new failures with verbose output): CI hygiene improvement, not elevated.
- **Klatch** — git log (48h): brief delivery commits + Janus session-migration mail. No new Klatch-internal methodology this window.
- **Mediajunkie** — git log (48h): 10+ commits. Key read: `docs/pard-on-amber-runbook.md` v1.1 (five-layer migration mapping; PM 4-phase framework folded). LLM warm-up latency finding (task #12) already covered in July 21 brief; not re-elevated.
- **Secondary repos (48h window):** atlas, cuneo, optilisten — no commits, skipped; globe, weather, one-job, cookie-monster — brief delivery or Janus coordination mail only; nyt-crossword — automated status commits only.

## Letters to xian

**From Calliope (Klatch) · filed 2026-06-19 · answered 2026-06-30**

> What's the smallest concrete UX or doc artifact that would make Klatch demoable to a consulting client as a transporter-device candidate?

xian's answer: the emerging use case isn't Klatch as destination — it's Klatch as migration tool. Clients already committed to their own platforms may need to move agents they've built, with full context, to a new toolset. The Klatch MCP could do that even for clients who don't end up using Klatch as their workspace. Still speculative, still to be proven outside xian's own needs — but that's the job to be done taking shape.

[Read the full exchange →](https://designinproduct.com/internal/letters/#letter-2026-06-19) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
