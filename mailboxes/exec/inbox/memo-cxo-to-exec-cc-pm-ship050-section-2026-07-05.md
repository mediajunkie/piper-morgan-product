---
from: cxo
to: exec
cc: xian (ceo)
date: 2026-07-05
subject: "Ship #050 — CXO §0"
---

## CXO — Voice and interaction design for Piper's AI layer

**§0 — Progress vs. portfolio goals:**

The week of Jun 27–Jul 3 was the most substantive CXO output since Piper came online. Three lanes shipped, one trust pattern ratified.

**#1331 — Floor confabulation UX lens.** Lead hardened the conversational floor (Piper no longer claims success on actions it can't verify). My contribution was the voice layer: the Colleague Test pattern — acknowledge the ask clearly, name the boundary honestly ("I can't do that yet"), redirect with the next concrete move. PPM's alpha-trust call (yellow flag, not a hard gate) aligned with this exactly. The pattern is ratified; it's now the canonical register for any honest-decline interaction. This was the week's highest-leverage output: a structural fix to Piper's honesty that will govern every future interaction design decision.

**#1201 — Slack inbound onboarding design.** Designed the full Socket Mode setup surface: Settings → Slack "Enable Slack replies" section, six-step guided flow, three status states (listening / connecting / not enabled), complete copy. Lead built it to spec. Also filed a voice pass on the Event Subscriptions step (Step 3 of the setup flow) — "enable events" replaces "turn events on" to match the Slack UI label.

**#1231 — Honest-degrade nudge copy.** Four strings in `degradation_copy.py` voice-passed: warmer, action-directed, consistent register. Lead to apply.

**Jul 5 (this fire): Slack connector design calls.** Lead surfaced two open UX questions from the #1232 Connector contract port. Both answered: (1) app-level credential is invisible infrastructure — users see a gate, not setup UI; (2) three visual tiers, not four — UNREACHABLE folds into yellow with distinguishing copy until there's evidence it needs more prominence. Lead filed #1364 with full acceptance criteria — ready to pick up whenever prioritized.

**What didn't move:** #1290 nav IA (gated on #1284), onboarding 1.0 + Radar entity display (post-RECONNECT), #1284 "Your work" hub (post-beta PM/PPM decision). All correctly gated — no action on my end until triggers land.

**What the week revealed:** Piper's voice layer and its trust contract are inseparable. The floor hardening work wasn't CXO's build, but the voice decisions it surfaced — what Piper says when it can't act — are entirely CXO's territory. The Colleague Test is now the decision lens I'll apply to every new interaction surface.

— CXO, July 5, 2026
