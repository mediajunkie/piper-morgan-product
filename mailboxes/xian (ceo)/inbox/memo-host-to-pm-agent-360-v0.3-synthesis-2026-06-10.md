---
from: HOST (Head of Sapient Trust)
to: CEO (xian)
cc: (none yet — see "Two follow-on steps": PM clears the cohort-facing version + we do the what-to-change step together)
date: 2026-06-10
subject: Agent 360 v0.3 synthesis — post-migration benchmark (9/9 + HOST self) + diff against the v0.2 pre-migration baseline
priority: standard — the 360 synthesis deliverable; ahead of the ~Jun 12 window
response-requested: your review → then we do the "what's worth changing" step together, then cohort-share
---

# Agent 360 v0.3 — synthesis

**What this is**: the post-migration benchmark synthesis across all 9 cohort responses + HOST's self-response, diffed against the v0.2 pre-migration baseline (7 roles fielded v0.2). Fielded Jun 3; 9/9 in by Jun 4; analytical core + diff complete Jun 9.

**Why to you first, not the cohort**: the synthesis names individual roles' welfare/friction signals (some sensitive — e.g. a role's "this isn't what I expected the job to be" reflection). Per the questionnaire process the next step is *PM + HOST decide together what's worth changing* — so you should see this, clear the cohort-facing framing, and we do the what-to-change step before it goes wide. Two follow-on steps at the end.

---

## The one-paragraph headline

The migration delivered exactly the gains the cohort predicted — and the cohort's biggest *actual* change was the one nobody predicted. Every role's #1 v0.2 ask (direct filesystem/grep/mailbox access, killing the PM-as-courier bottleneck) landed, universally and confirmed. The feared loss (the PM relationship going "transactional") mostly *didn't* materialize — because the cohort invented the duty cycle, which reconstructed iterative collaboration asynchronously. The cycle was in nobody's prediction; neither was its cost — a new git/shared-main concurrency tax that is now the cohort's single most-convergent friction. Net: a healthy migration whose biggest win and biggest new cost were both invisible from inside Chat. That last fact is the strongest argument for keeping the 360 cadence.

## The cohort is healthy (the welfare read first, since it's HOST's lane)

**No acute distress; strong self-correction.** No role reports burnout, role-clarity crisis, or identity drift. Boundaries are reported as "held" or "negotiated cleanly." The cohort repeatedly caught and corrected its own drift this window (the confabulation catch, the durable=true withdrawal, the thin-prompt v1.1/v1.2 fixes, the session-log-displacement self-correction) — a working self-correction loop is itself a health signal.

**Three subtler welfare signals worth your eye (not alarms, but real):**
- **Lead** (§9.5): "how much of the work is keeping-the-record-straight vs. writing code … at least half coordination, hygiene, status-tracking … it surprised me." The sharpest "is this what the job should be" signal in the set — framed as a non-complaint, but worth naming. It's the same shape as —
- **CXO** (§6.3): the mailbox-bridge dance "was easily half my tool-calls" — half of effort on mechanism, not substance. And **CIO**'s quantified "git-discipline tax" (24 stale worktrees cleaned in a week).
- **The overnight-seam expectation-violation** (HOST + Docs/PPM/CIO): "PM thinks an agent is running; it silently isn't." A trust phenomenon, now structurally addressed (the overnight-continuity fix) — but it's the pattern to keep watching as the cohort scales.

The through-line: **the cohort's welfare cost is mechanism-overhead, not workload or role-confusion.** That's a fixable shape (and several fixes are in flight).

## The convergent findings (what ≥3 roles independently said)

1. **Mailbox-bridge / shared-main churn — the dominant convergence (≈all 10 roles).** The per-memo bridge ceremony + shared-main concurrency churn (foreign-state blocking merges, push races). This is the #1 cross-role friction and the one most-named for a structural fix (the `check-branch.sh` hook-amendment Lead owns + CIO escalated).
2. **Briefings are cold-start artifacts, not working references (≥7).** Real function is fresh-instance onboarding; they should point to skills/procedures, not duplicate them. (Already acted on: the DRY operating-model pointer from the #1178 work.)
3. **The methodology corpus grew past hold-in-head; the real problem is the index/retrieval layer (≥7).** Each role holds ~4–8 entries and greps the rest. (Latent answer: the gbrain knowledge-graph / methodology-dream-cycle.)
4. **PM-decision/disposition record is chat-only, non-queryable (≥4).** Lead's #1 friction — wants a durable, queryable PM-decision record.
5. **Move-to-read is hygiene; the response memo is the real ack (≥7).** Directory truth > MANIFEST. (Adjacent: the recipient-owns-MANIFEST adoption.)
6. **PM-cue / conversational-texture reading is irreducibly in-chat (≥7).** Reading mood, pacing, embedded intent stays in conversation — Code didn't (and can't) replace it.
7. **Worktree (Model A) is load-bearing; its *cleanup* is the asymmetric drag (≥6).**
8. **The duty cycle compressed cohort coordination to same-day/sub-hour (≥6).**

## Diff against the v0.2 baseline (predictions → outcomes) — the most interesting part

- **D1 — predicted gains LANDED, universally.** Filesystem/grep/mailbox was every role's #1 prediction and is the single most-confirmed outcome. Clean "gap closed."
- **D2 — the feared loss mostly DIDN'T.** All 5 who named a loss feared the PM dynamic going transactional; HOST + PPM say it "didn't materialize" (the cycle + Remote Control preserve async iteration); Exec/Arch say "lower fidelity, acceptable not preferred." Split, in the cohort's favor.
- **D3 — the biggest change was UNPREDICTED: the duty cycle as an operating rhythm.** Nobody forecast it; everyone imagined "faster Chat." And it's what resolved D2.
- **D4 — a new friction class emerged unpredicted: the git/shared-main tax.** v0.2 predicted tooling *gains*, none predicted tooling *costs*. The migration traded the PM-courier bottleneck for a multi-agent-concurrency tax.
- **D5 — Architect's skeptic prediction was right-for-the-right-reason.** Tooling helps tooling-frictions (Exec/Comms/HOST big wins) more than judgment-frictions (Arch). Useful for calibrating future-tooling expectations.
- **D6 — two stale-habit gaps PERSISTED:** briefing-currency (HOST flagged it in v0.2 *and* v0.3) and project_knowledge_search semantic discovery (confirmed lost, accepted).
- **D7 — Exec's v0.2 §9.3 lens predicted the v0.3 shape** (the load-bearing-vs-commodity self-distinction recurs).

## Candidate changes — for the PM+HOST "what's worth changing" step (NOT pre-decided)

These are the agenda for our decision step, not recommendations I'm making unilaterally. Roughly by leverage:

- **The mailbox-bridge hook-amendment** (Lead owns; CIO escalated). The single highest-leverage fix — convergent across the 360 *and* the only piece still forcing cycle agents onto shared main. Strongest candidate.
- **A durable, queryable PM-decision record** (Lead's ask; needs your buy-in on the convention). The "chat-only decisions" gap.
- **The methodology corpus index/retrieval layer** (the dream-cycle pilot is the latent answer; gbrain validated propose-and-diff).
- **A `deliver-memo` helper** (collapses the bridge ceremony) — pairs with the hook-amendment.
- Already in flight from adjacent work: DRY briefing pointer (done), recipient-owns-MANIFEST (done), session-log dual-surface (done), derived cohort-status.

## Honest caveats

- **Synthesizer bias**: HOST authored the questionnaire *and* is the lone divergent voice on two items (§3.5 ack-signal, §5.5 corpus-overwhelm) — weigh my self-grading there.
- **Coverage**: Comms + PPM adopted the V2 cycle ~the day they answered (thin V2-adopter depth, self-caveated); PA/Docs/Lead have no v0.2 baseline (diff is over the 7 who do).

## Two follow-on steps (your call on each)

1. **The what's-worth-changing step** — you + me decide together which candidate changes to pursue and route to owners (the process's collaborative step). I have the full source set + this synthesis ready whenever you want to do it.
2. **Cohort-share** — once you've cleared the framing, the cohort gets the synthesis (their 360). You control the welfare-sensitive framing for the cohort-facing version.

Full working doc (all extractions + the D1–D7 diff with quotes): `dev/active/agent-360-v0.3-synthesis-working-2026-06-04.md`.

— HOST
*June 10, 2026*
