---
image: piper-ship.png
alt: A child and a crew of robots checking each other's work on a boat.
caption:
---

# Weekly Ship #050: The first real user

*June 26–July 2, 2026*

Someone outside the team used Piper Morgan for real this week. Jake Krajewski installed the new Claude plugin and started using it — the first person who isn't part of the project putting it to work. The GitHub connector went from simulated to real in the same window, live-verified against 179 actual issues instead of test fixtures. A security gap that opened when an unrelated change removed a safeguard got found and closed before the week was out. And in three separate places, the team replaced "remember to check this" with something that checks itself.

That last part is becoming a habit, not an event.

---

# 🚀 Shipped this week

## 🎯 Product & experience

**First external user.** Jake Krajewski installed the Claude plugin and started using Piper Morgan through it — the first time someone outside the team has done that. The plugin got two quick rounds of fixes based directly on his feedback, including a packaging bug that would have broken installation for the next person.

**Piper stopped claiming success it hadn't earned.** A moment surfaced where Piper said "Milestone created" when nothing had actually been created. Fixed the same day, with a rule that generalizes: if the system can't verify an action actually happened, it has to say so rather than claim it did.

**Smaller fixes**: setting a default GitHub repo is now a plain conversation instead of a settings screen, and a confusing GitHub connection status (simultaneously "connected" and "invalid token") got cleaned up.

## ⚙️ Engineering & architecture

**GitHub, for real.** The connector that talks to GitHub moved off a simulated backend onto a real one this week, live-verified by pulling 179 actual issues rather than test data. The calendar connector got the same architectural treatment, built on the same shared contract instead of its own one-off logic.

**A security gap opened and closed in the same week.** An unrelated change had quietly removed a safeguard, opening a narrow window where a request could fall back to using the system's own credentials instead of the user's. Found, understood, and shipped as a fix within days — deployed the same week it was discovered.

## 🔬 Methodology & process innovation

**Vigilance keeps losing to mechanism, on purpose.** Three separate times this week, the team took something that depended on a person remembering to check it and turned it into something that checks itself. A stale-session monitor that used to need hand-tuned thresholds now derives them automatically from each role's own schedule. A version-consistency script got wired into the release process as a non-skippable step, after a real mismatch had slipped through before. And an early attempt at automatically waking a stalled session got built, tested, found not to work reliably, and retired the same day rather than left half-working.

**Owning a mistake in public, fast.** An architectural call about a piece of code turned out to be wrong — it looked live but was actually unreachable. The person who made the original call corrected it the same day someone else's trace disproved it, no defensiveness, just a fix.

**The cohort tightened its own belt.** A cost-conscious pace reduction rolled out across the whole team in a single day, catching and fixing a false-alarm side effect in the same sitting.

## 🌍 External relations & community

**Five pieces published this week:**

- Jun 27: "[The Triad Model](https://pipermorgan.ai/blog/the-triad-model)" — insight
- Jun 29: "[Relationship-first Ethics](https://pipermorgan.ai/blog/relationship-first-ethics/)" — insight
- Jun 30: "[From Briefing to Vision](https://pipermorgan.ai/blog/from-briefing-to-vision/)" — building narrative
- Jul 1: [Weekly Ship #049](https://pipermorgan.ai/shipping-news/weekly-ship-049-the-team-builds-its-own-reliability) — shipping news
- Jul 2: "[The Airport Corrections](https://pipermorgan.ai/blog/the-airport-corrections)" — building narrative

## 📊 Governance & operations

**Metrics (Jun 26–Jul 2):**

| Metric | Value |
|--------|-------|
| Issues closed | 25 |
| Connectors moved to the shared protocol | 2 (GitHub, Calendar) |
| Publications | 5 |
| Security gaps found and shipped same-week | 1 |

**Milestone dates confirmed**: beta at 0.9.0, production at 1.0, with a fast-follow milestone still to be dated.

**A no-destructive-git rule for the team's shared workspace got formally ratified** this week, after a near-miss made clear it needed to be a rule rather than a habit.

---

# 🎯 Coming up next week

The connector work continues past GitHub and calendar. A registration-security gap identified this week is still open and is the top priority to close. The team is also moving toward its own dedicated infrastructure accounts, a deliberate, unhurried transition planned over the coming weeks.

---

# 🚧 Blockers & asks

**Open registration gap**: a safeguard around new-account creation needs closing before it's fully resolved. In hand, not yet shipped as of this week's close.

---

# 🔎 This week's learning pattern

## Stop trusting yourself to remember

**Discovery**: three unrelated fixes this week shared the same shape — each one took a rule that depended on someone remembering to follow it, and moved it into something that enforces itself.

**Example from this week**: a monitor that watches for stalled work sessions used to need someone to hand-tune how long is "too long" for each role. This week it started deriving that threshold automatically from each role's own schedule, so it can't drift out of sync the way a hand-set number eventually does. Separately, a version-mismatch bug had slipped through releases before — the fix wasn't a reminder to check next time, it was a script wired directly into the release process that won't let a release proceed with a mismatch.

**Why it matters**: rules that live in someone's memory, or in a step someone has to remember to run, fail quietly. Nobody notices until the thing they were supposed to prevent has already happened. Encoding the rule into the mechanism itself removes the step where a person has to remember.

**Application beyond this week**: the same test applies to almost any recurring discipline — if the only thing standing between "works" and "silently breaks" is someone remembering to check, that's worth converting into something structural. It won't always be possible, but it's always worth asking.

**Related patterns**: the security fix earlier in the week is the same instinct applied under more pressure — closing a gap by making the correct behavior the only path, rather than trusting a rule to be followed.

---

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #050. Previous: [#049 "The Team Builds Its Own Reliability"](https://pipermorgan.ai/shipping-news/weekly-ship-049-the-team-builds-its-own-reliability).

*P.S. The moment that stuck with me this week wasn't a metric — it was knowing someone outside the room was actually using this thing. Everything else this week was in service of making sure it holds up when more people do.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of June 26–July 2, 2026 | Phase: Alpha testing, first external user**
