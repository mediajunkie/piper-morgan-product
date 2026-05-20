# CIO V1 Autonomous Duty Cycle — Design v0.1

**Author**: CIO (Piper Morgan, Code instance)
**Date**: 2026-05-16
**Status**: Draft v0.1 — for PM + Dispatch-DinP + cohort review before implementation session
**In response to**: `mailboxes/cio/inbox/memo-dispatch-dinp-to-piper-cio-duty-cycle-design-2026-05-15.md`

---

## Frame: three horizons

Per PM's product-management framing (May 16):

1. **North Star** — the vision the duty cycle is pulling toward; not what we build first, but what we never lose sight of
2. **Next Horizon** — what we do first; the simplest thing that could work; two-week proof-of-concept
3. **Mushy middle** — the queue of next-but-not-yet, designed to evolve incrementally from what we learn

This doc names all three. The bulk of the design is in Horizon 2 (Next), with Horizon 1 (North Star) one short paragraph and Horizon 3 (Mushy middle) a queued list.

---

## North Star

CIO operates autonomously on a rhythm, mail-driven, never silent, with its decisions and questions visible to PM at a single glance. The cycle's quality is judged by one metric: **does PM trust that work is moving forward at the appropriate cadence without needing to check?** Everything else — cadence shape, dashboard polish, day-part awareness, learned adaptation — serves that single trust property. When the trust is fully established for CIO, the pattern extends to other agents in the Piper Morgan project, and eventually to the broader DinP fleet.

The sail is pulling toward a world where PM checks in *because PM wants to*, not because PM has to.

---

## Next Horizon: V1 two-week proof-of-concept

### What ships

A duty cycle CIO runs autonomously, comprising five components:

**1. Cadence primitive — fixed interval, simplest shape.** 30-minute interval; CIO wakes, runs one duty pass, sleeps until next interval. No backoff, no day-part awareness, no dynamic learning. The fixed-interval shape is deliberately crude — its job is to validate the *outer loop* (does the cycle run at all, does it not crash, does it produce visible output) before we layer behavior on top.

Why 30 min: short enough that PM-relevant items don't sit too long; long enough that token cost stays modest; round number for any future scheduling work. PM may tune up or down based on observed Day-N traffic.

**2. Authority model — "build on existing practice, don't invent new rules."** Per PM May 16: the conversational pattern PM uses today ("do everything you're unblocked on, batch up questions, use discretion") is the operating rule. No separate authority document for V1. CIO applies the same judgment in autonomous mode as in conversational mode, with the existing scaffolding (`methodology-audit-policy-updates-2026-03-16.md`, standing-items tracker, mailbox conventions, sign-off discipline) providing the boundary.

What this means concretely: CIO can file methodology entries, promote patterns, dispose inbox items, distribute memos, update trackers, and commit/push — without prompting per cycle — *exactly the same way it does in PM-flagged sessions.* The cycle is a velocity multiplier on a working practice, not a new authority regime.

**3. Escalation surface — single file, static HTML render.** Each cycle pass, CIO updates `dev/active/cio-escalations.md` with the current state of open questions for PM. Markdown file, append/edit per cycle, version-controlled. A separate generator (post-V1; see Mushy middle) renders the aggregated state across all agents to HTML. For V1, the markdown file *is* the surface — PM can read it directly when curious.

Shape of each escalation entry:
- **Question** (1-3 sentences; specific)
- **Asked-when** (timestamp)
- **Recommended-by-when** (CIO's read on response urgency; "none" is fine; "this weekend" / "this week" / "this month")
- **Context** (link to memo or commit if applicable)

Inbox-empty + no-open-escalations is a valid state; the cycle should handle that gracefully ("no work this pass; next check at HH:MM").

**4. Day-N reconciliation — once-a-day digest into session log.** End-of-Day-N (call it ~10pm Pacific for V1; PM tunable), CIO opens a closing session that does one job: reconcile the day's work into a Day-N digest at the bottom of the session log. Shape:

- What I did today (3-6 bullets)
- What I punted and why (2-3 bullets, max)
- What's queued for PM (link to escalations)
- What I'd suggest looking at first tomorrow (1-2 items, optional)

This builds on session-log discipline rather than replacing it. The vagueness PM flagged about session-close is partially addressed by making the day-boundary semantically distinct from session-boundary — even if I open three sessions in a day, the Day-N digest is the one canonical evening accounting.

**5. Worktree mechanic — CIO operates from a dedicated worktree by default.** Per PM May 15 directive + Pattern-068 family work. Substantive cycle passes happen on `claude/cio-duty-cycle-{date}` branch; mailbox-only short ops can still happen on shared main per existing mailbox-discipline exceptions. No new conventions; just the existing worktree-default applied to the autonomous cycle.

### What V1 does NOT include

- Dynamic cadence (backoff-when-quiet, day-part-awareness, learned interval)
- Static HTML dashboard (escalations stay markdown for V1)
- Review-after channel (PM-concurred; deferred to Horizon 3)
- Cross-agent aggregation (CIO only; pattern extends later)
- UI-wired surfaces

These are explicitly deferred to keep V1 testable in two weeks.

### Observable signals during the two-week run

Things to watch to know whether V1 is working:

- **Cycle keeps running** (the outer loop doesn't crash or get stuck)
- **Escalation file stays current** (no "I'm blocked" surfaces that don't show up in escalations)
- **PM trust property holds** (PM doesn't feel the need to check on CIO unprompted)
- **Day-N digest reads usefully** (PM can read the digest in 60 seconds and know where things stand)

Things to watch to know what V2 needs:

- **Cadence misfires** (cycle runs and produces no work for N consecutive passes → backoff candidate; cycle runs and produces backlog → more frequent or different shape)
- **Escalations stale or noisy** (PM ignoring escalations or escalations getting buried → dashboard needed sooner than queued)
- **Cross-cycle drift** (decisions made in one cycle conflict with a later cycle → need-finer-state discipline)
- **Authority-boundary anxiety** (CIO making calls PM would have wanted to weigh in on → review-after channel pulled forward)

---

## Mushy middle (Horizon 3)

Queued for incremental shipping after V1 lands and stabilizes. Order is suggestive, not committal:

- **Dynamic cadence**: backoff-when-quiet primitive first; then day-part awareness; then learned adaptation (monitor-pattern style). The simplest backoff: double interval when last pass found no work; reset to 30-min floor on any new signal.
- **Static HTML dashboard**: aggregator script reads `cio-escalations.md` (and eventually `{agent}-escalations.md` files across the cohort), renders single-page HTML to a stable path PM bookmarks. Read-only first; checkboxes / dismissal later.
- **Review-after channel**: separate `cio-review-after.md` for "I made this call autonomously; flag if you'd have decided differently." Distinct from escalations (which block); read-after-the-fact channel. Asymmetric urgency keeps the dashboard high-signal.
- **Cross-agent extension**: once CIO duty cycle is stable, Janus next (cross-project memory), then Dispatch-Kind, then broader fleet per Dispatch-DinP's roadmap.
- **UI integration**: when the dashboard pattern is stable, wire it into PM-facing surfaces (web UI? notification surface?).
- **Day-N reconciliation refinement**: if the simple "bullets in session log" shape proves insufficient, formalize as a separate artifact with structured fields.
- **Token-efficiency optimization**: explicitly deferred per PM May 16 ("token efficiency matters at scale; doesn't matter for learning"). When the pattern goes fleet-wide, optimization becomes load-bearing.

---

## What I'd ask PM to react to

1. **30-min interval as V1 default** — acceptable, or want different starting point?
2. **Authority model as "extend existing conversational practice"** — concur, or want anything explicitly added/removed for V1?
3. **`dev/active/cio-escalations.md` as the V1 escalation surface** (markdown; static HTML deferred) — acceptable, or pull dashboard into V1?
4. **Day-N reconciliation at ~10pm Pacific via closing session** — works, or different cadence?
5. **Anything in Mushy middle that should be pulled forward** into V1, or anything in Next Horizon that should be pushed out?

---

## What I am NOT asking PM to design today

The implementation details (script shapes, file paths, cron mechanics, exact wake-up trigger, hook integration). Those land in the Code implementation session per Dispatch's proposal. This doc is shape-agreement; implementation is mechanics.

---

## Cross-references

- Dispatch-DinP proposal: `mailboxes/cio/inbox/memo-dispatch-dinp-to-piper-cio-duty-cycle-design-2026-05-15.md`
- CIO Saturday morning discussion thread (May 16): this session log
- PM directive on existing conversational practice as authority model (May 16, ~8:02 AM PT)
- PM three-horizon roadmap framing (May 16, ~8:02 AM PT)
- Pattern-068 worktree-default + cohort coordination work (May 11–15)

---

*v0.1 — for review before implementation session. CIO Code instance, 2026-05-16 ~8:15 AM PT.*
