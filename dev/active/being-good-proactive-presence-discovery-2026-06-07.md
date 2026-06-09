# Proactive Presence — Design Discovery (#1174) — working notes

**Owner**: CXO | **Track**: being-good (PM-watched) | **Started**: 2026-06-07 (PM + CXO conversational design session)
**Process**: forensic-first → concrete-example-led discovery. **Status**: live working notes (capturing as we design).

---

## 0. Forensic grounding (what our corpus already gives us)

- **Foundations Part V "Proactive vs Reactive Presence"** (`docs/internal/design/mux/piper-morgan-ux-foundations-and-open-questions.md`): the **observe → offer → act** spectrum; Radar-O'Reilly "shows up where you are"; the self-threat research (system-initiated delegation provokes resistance).
- **Contextual-Hint UX Spec v1** (Jan 2026, CXO; `docs/internal/design/specs/contextual-hint-ux-spec-v1.md`): **the in-conversation hint is already designed** — post-task + context-aware suggestions, throttled (≤2 per 5 interactions, stop after 2 ignored), dismissal patterns, colleague voice, anti-annoyance metrics.
- **Trust gradient** (foundations): Stage 1 notices-but-waits → Stage 2 anticipates/"shall I?" → Stage 3 offers-to-automate → Stage 4 proposes/acts.

## 1. The discovery cut (what's solved vs. the frontier)

- **In-conversation proactive hint** = essentially **SOLVED** (contextual-hint spec).
- **Ambient / cross-surface proactive presence** = the **frontier** (no paradigm): surfacing relevance *when you're not talking to Piper*, where you already work. Highest trust-vs-annoyance stakes. **This is #1174's real target.**
- The discovery question: *"How does Piper earn the right to show up uninvited, somewhere you're already working, without becoming the notification you mute?"*

## 2. The anchor example — "something you care about just got blocked"

Chosen over a deadline (deadlines are a solved paradigm). The blocker is the quintessential trusted-colleague-notices-what-you'd-miss move, and it leans on Piper's differentiator: the 8-dimensional spatial intelligence (CAUSAL + PRIORITY) seeing the dependency chain across tools.

**Vignette**: You flagged #456 (launch blocker) critical Tuesday. It's blocked by PR #123 (auth fix), in review 2 days with no activity. You're heads-down in Slack. Piper surfaces, where you are: *"Heads up: #456 (the launch blocker you flagged Tuesday) is stuck — PR #123 has been waiting on review 2 days. Want me to nudge the reviewer, or re-prioritize?"*

## 3. The two-gate model (PM + CXO, confirmed)

Two different gates compose:

- **Trust gradient = relationship-level permission**: *may* I show up uninvited, and *how forward* (observe/offer/act)? → gates **channel + posture**.
- **Three criteria = per-instance worth**: should I, for THIS thing? → gates the **moment**. The three:
  1. **Explicit care** — about something you flagged/assigned/asked-about (not just anything on the board).
  2. **Real, time-sensitive change** — newly stalled, not chronically.
  3. **High confidence** — Piper can name the specific chain, not a vague "something's off."

**Both must pass**, and trust **modulates** the criteria + channel over time. **Discipline**: *err toward silence — a miss costs less than a false alarm, and a false alarm costs trust.*

**Two payoffs of the composition:**
1. **The trust gradient IS the de-risked rollout plan** — channel escalates over time (in-conversation first → ambient later); we ship the easy, designed form first and light up the hard form as trust is earned.
2. **Self-correcting** — a dismissed-without-action nudge costs trust (down-gradient + raise the bar). The per-session throttle and the per-relationship trust gradient are *the same mechanism at two timescales*.

## 4. Channel-by-trust-stage mapping (the blocker)

| Stage | Trust posture | Channel (where it shows up) | What the blocker looks like |
|---|---|---|---|
| **1** notices-but-waits | observe (ambient channel CLOSED) | **In-conversation only** — the designed contextual hint, when you come to Piper | "When you check in: #456 is blocked by PR #123 (stalled 2 days)." No interruption. |
| **2** anticipates | observe + offer, **pull-not-push** | **A Piper "For You" surface** (a Piper-side ambient feed/digest the user checks) | The blocker waits in your "for you" feed with an offer; Piper doesn't reach into Slack yet. |
| **3** offers-to-automate | offer, **push** | **Pushed to where you work** (Slack DM / wherever you currently are) | The full Radar-O'Reilly moment: Piper shows up in Slack uninvited with the blocker + "Want me to nudge the reviewer?" |
| **4** proposes/acts | **act**-then-inform (with undo) | push + action | "I nudged the reviewer about PR #123 (blocking #456); I'll tell you when it moves." |

**Build sequence falls out of this**: extend contextual-hints to surface blockers (Stage 1) → build the "For You" pull-surface (Stage 2) → push integration / presence-aware channel (Stage 3) → act-with-undo (Stage 4). **Ship value early; earn the intrusive forms.**

**Dependencies surfaced**: Stage-3 "where you are" requires **presence awareness** (Piper knows which surface you're currently in). Stage-2 raises a sub-design: *what exactly is the "For You" surface?* (notifications panel in the web UI? a digest? relates to the history/memory surfaces.)

## 5. Range examples — stress-testing the model (2026-06-08, CXO autonomous)

Three more moments, chosen to *try to break* the two-gate + channel model. Result: the model **holds on two and flexes usefully on one**, and all three (plus the Type-2 lens from #1166) converge on a single discriminating principle. Each example below: vignette → criteria test → channel verdict → does the model hold or flex.

### Example A — The deadline (the solved-paradigm contrast)
**Vignette**: Your OpenLaws deliverable is due Friday. It's Wednesday; the draft is at 40%.
- **Criteria test**: Explicit care ✅ (committed deliverable). Real time-sensitive **change**? ❌ — *the deadline was always Friday.* What changed is elapsed time, not an event. **A countdown is not a change.**
- **Channel verdict**: the bare deadline routes to the **solved reminder paradigm** (calendar/due-date notifications — "not being bad / conform, don't innovate"). It does NOT earn proactive-ambient presence. The MUX version — "due Friday, you're at 40%, *and the thing it's blocked on hasn't moved*" — is just the **blocker case** (§2) wearing a deadline; the jeopardy-reasoning is the value, not the date.
- **Model HOLDS — and discriminates correctly.** Criterion #2 is the blade: a bare countdown fails "real change," so it stays in the solved-paradigm lane; only jeopardy-reasoning (an actual event in the dependency chain) elevates it — and that's already the blocker.
- **Sharpening it forces**: criterion #2 should explicitly read **event-change (something happened), not countdown (time passed).** (This is the *same* distinction the #1166 Type-2 lens landed on — "event-justified surfacing, not scheduled." Two threads, one principle.)

### Example B — "You asked me to watch X and it changed" (invited / user-delegated)
**Vignette**: Earlier you said *"let me know if the staging error rate spikes again."* Two days later, it spikes.
- **Criteria test**: all three pass cleanly (explicit care = you literally asked; real event = the spike; high confidence = a named metric crossing). Gate A intact.
- **The flex**: the user **explicitly invited** this presence. The trust gradient (Gate B) exists to answer *"may I show up uninvited?"* — but here that question is **pre-answered for this specific item.** An explicit standing-watch request creates a **scoped pre-authorization** that overrides the channel gate *for the invited item only.* Even a Stage-1 ("notices but waits") relationship may **push** *this* item, because the user opened that exact door.
- **Model FLEXES — and this is the most valuable finding.** The two-gate model needs a third concept layered on Gate B: **invited vs. uninvited.** General trust gradient governs *uninvited* presence; an explicit watch-request creates *scoped consent* that elevates the channel for that item regardless of stage. Gate A (the three criteria) still fully applies — don't fire on a non-event, name the thing, be confident.
- **Rollout consequence**: invited-watch is the **safest proactive presence to ship — consent is explicit and scoped — so it should come FIRST**, even before the uninvited blocker. *"Let me know if X"* is a dead-simple, high-trust, user-initiated on-ramp to ambient presence. Revised build order: **invited-watch (free consent) → uninvited-blocker (earned) → drift-digest → act-with-undo.**

### Example C — The status-drift nudge (a slow trend, no event)
**Vignette**: A project you own has been quietly sliding — velocity down, review latency up — over two weeks. No single trigger; a trend.
- **Criteria test**: Explicit care ✅. Real time-sensitive **event**? ❌ — drift is the *opposite* of a discrete event. Name the **chain** with high confidence? ❌ — drift is diffuse ("things feel slower"), not a crisp "X blocked Y." A push here would be exactly the **vague-dread anti-pattern** (the Type-2 cardinal sin: threat with no nameable cause).
- **Channel verdict**: drift correctly **fails the push criteria** and routes to the **pull/digest surface** (the Stage-2 "For You" feed) — the user *visits* and sees "this project's health has been sliding; here are the contributing factors." **Drift is digest material, not interruption material.**
- **Model HOLDS — and validates the pull surface's reason to exist:** not everything worth surfacing is worth *pushing.* The pull surface is the home for real-but-non-event signal that would be obnoxious as an interruption.
- **Sharpening it forces**: drift **converts to an event at a threshold-crossing** ("review latency just passed your team's SLA *for the first time*"). At the crossing, drift earns an event and may elevate to push. So: **drift lives in pull; threshold-crossings convert drift → event → eligible for push.** (Again the generation-vs-surfacing distinction — the trend is always being *tracked*; only the crossing is *surfaced.*)

### What the range proves (synthesis)
1. **One discriminating variable governs push vs. pull across all cases (incl. #1166 Type-2):** *is there a discrete, recent, nameable event?* Event → eligible for push. Countdown / drift / vague signal → pull/digest, never push. The deadline (countdown), the drift (trend), and Type-2's scheduled rehearsal all fail the same way and route the same way. This is now a **validated core principle**, not a single-example intuition.
2. **The one genuine model addition: invited vs. uninvited.** Explicit standing watch-requests create *scoped pre-authorization* that overrides Gate B's channel gate for that item — and are the **safest, first thing to ship.** This is new since the 6/7 model and reshuffles the rollout order.
3. **Criterion #2 re-stated**: "real, time-sensitive **event-change**" (something happened) — explicitly *not* a countdown or a slow trend. This single word ("event") is doing most of the discriminating work across every example.

## Open sub-threads (to work next)
- The **Stage-2 "For You" surface** design (what is it, concretely) — now load-bearing: it's the home for drift-digest AND (per #1166) Type-2's "what I'm prepared for" stream. One ambient surface, multiple content-streams (learned / changed / prepared-for / drifting).
- **Invited-watch** as the shippable first slice — spec the *"let me know if X"* standing-request affordance (how the user sets it, how Piper confirms scope, how it expires).
- The remaining anchor-example anatomy: response affordances; throttle-as-trust-signal mechanics; the confidence-computation ("name the chain").

---

*Working notes — CXO, started 2026-06-07 (PM+CXO discovery session under #1174); §5 range examples added 2026-06-08 (CXO autonomous). Not a spec yet; this becomes the discovery synthesis → PDR input.*
