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

## Open sub-threads (to work next)
- The **Stage-2 "For You" surface** design (what is it, concretely).
- The remaining anchor-example anatomy: response affordances; throttle-as-trust-signal mechanics; the confidence-computation ("name the chain").
- **A few more examples** (per PM) to get a range — candidates: a deadline (the solved-paradigm contrast); "you asked me to watch X and it changed" (user-delegated, lower trust bar); a status-drift nudge.

---

*Working notes — CXO, 2026-06-07. Live capture of the PM+CXO discovery session under #1174. Not a spec yet; this becomes the discovery synthesis → PDR input.*
