---
image: piper-ship.png
alt: A child and a crew of robots checking each other's work on a boat.
caption:
---

# Weekly Ship #050: The Connector Gets Real

*June 26–July 2, 2026*

The GitHub connector stopped pretending this week. What had been running against a simulated backend went live — verified by pulling 179 real issues through real authentication, not test fixtures. The calendar connector got the same treatment on the same shared contract. A security gap that opened when an unrelated change removed a safeguard was found one day and fixed the next. And in three separate places, the team replaced "remember to check this" with something that checks itself.

There's an irony here worth owning: the very first Piper Morgan proof of concept could do this competently. That version served exactly one user, with personal credentials wired straight in — this one does it with real per-user authentication, on a contract every connector shares. Coming back around to where you started, for real this time, is a lot of what shipping actually is.

The plugin also got its first serious outside install attempt this week — which failed, and taught us more than a clean install would have. More on that below, because we count it honestly.

---

# 🚀 Shipped this week

## 🎯 Product & experience

**A failed install that paid for itself.** Our first external tester tried to get the plugin running this week, and his feedback drove three same-day releases — including a packaging fix that would have broken installation for the next person too. What it didn't produce: a working install. His Claude interface never showed the install entry point, and we haven't cracked why yet. The feedback loop is the win. The install experience is the honest gap, and it's named, not buried.

**Slack setup got a real onboarding flow.** The experience-design role (CXO) spec'd the full Settings surface — setup steps, three plain-language status states (listening, connecting, not yet enabled), copy for each — and it was built and shipped to spec within the window.

**Piper stopped claiming success it hadn't earned.** A live moment surfaced where Piper said "Milestone created" when nothing had actually been created. Caught in real use, answered within a day with a rule that generalizes: if the system can't verify an action actually happened, it says so rather than claiming it did.

**Smaller fixes**: setting a default GitHub repo is now a plain conversation instead of a settings screen, and a confusing connection status (simultaneously "connected" and "invalid token") got cleaned up.

## ⚙️ Engineering & architecture

**GitHub, for real.** The connector that talks to GitHub moved off a simulated backend onto a real one, live-verified by pulling 179 actual issues through a real authenticated round-trip. The calendar connector was ported onto the same shared contract — one protocol both now implement, instead of two one-off implementations that could quietly diverge.

**A security gap opened and closed inside the week.** An unrelated infrastructure change had quietly removed a safeguard, opening a narrow window where a request could fall back to using the system's own credentials instead of the user's. Found one day, deployed as a fix the next.

## 🔬 Methodology & process innovation

**Vigilance keeps losing to mechanism, on purpose.** Three separate times this week, the team took something that depended on a person remembering to check it and turned it into something that checks itself. A stale-session monitor that used to need hand-tuned thresholds now derives them automatically from each role's own schedule. A version-consistency script got wired into the release process as a non-skippable step, after a real mismatch had slipped through before. And an early attempt at automatically waking stalled sessions got built, proven unreliable by its own self-test the next morning, and retired on the spot rather than left half-working.

**Owning a mistake in public, fast.** An architectural call about a piece of code turned out to be wrong — it looked live but was actually unreachable. The person who made the original call corrected it the same day someone else's trace disproved it. No defensiveness, just a fix.

**The team tightened its own belt in a day.** A cost-conscious pace reduction rolled out across the whole team in a single day, catching and fixing a false-alarm side effect in the same sitting.

## 🌍 External relations & community

**Five pieces published this week:**

- Jun 27: "[The Triad Model](https://pipermorgan.ai/blog/the-triad-model)" — insight
- Jun 29: "[Relationship-first Ethics](https://pipermorgan.ai/blog/relationship-first-ethics/)" — insight
- Jun 30: "[From Briefing to Vision](https://pipermorgan.ai/blog/from-briefing-to-vision/)" — building narrative
- Jul 1: [Weekly Ship #049](https://pipermorgan.ai/shipping-news/weekly-ship-049-the-team-builds-its-own-reliability) — shipping news
- Jul 2: "[The Airport Corrections](https://pipermorgan.ai/blog/the-airport-corrections)" — building narrative

[![At an airport gate, a traveler supervises a whimsical team of glowing AI helpers tending an autonomous work loop while planes wait outside the windows.](https://pipermorgan.ai/assets/blog-images/the-airport-corrections.webp)](https://pipermorgan.ai/blog/the-airport-corrections)

*"Now don't stray too far before boarding!" — from "[The Airport Corrections](https://pipermorgan.ai/blog/the-airport-corrections)"*

## 📊 Governance & operations

**Metrics (Jun 26–Jul 2):**

- **Issues closed:** 25
- **Connectors on the shared protocol:** 2 (GitHub, Calendar)
- **Security gaps found and fixed inside the week:** 1

**The milestone ladder got pinned down**: beta ships as version 0.9.0, production as 1.0, with a fast-follow milestone behind it.

**A no-destructive-git rule for the team's shared workspace was formally ratified**, after a near-miss made clear it needed to be a rule rather than a habit.

---

# 🎯 Coming up next week

The connector work continues past GitHub and calendar. A registration-security gap identified at the very end of this window is the top priority to close. The team is also moving toward its own dedicated infrastructure accounts — a deliberate, unhurried transition with weeks of runway.

---

# 🚧 Blockers & asks

**Open registration gap**: a safeguard around new-account creation needs closing before it's fully resolved. In hand at week's close, not yet shipped.

**The plugin install mystery**: our first external install attempt is blocked on an interface element that simply doesn't appear for the tester, and we don't yet know why. If you've seen a Claude plugin install where the add button never shows up — we're listening.

---

# 🔎 This week's learning pattern

## Stop trusting yourself to remember

**Discovery**: three unrelated fixes this week shared the same shape — each one took a rule that depended on someone remembering to follow it, and moved it into something that enforces itself.

**Example from this week**: a monitor that watches for stalled work sessions used to need someone to hand-tune how long is "too long" for each role. This week it started deriving that threshold automatically from each role's own schedule, so it can't drift out of sync the way a hand-set number eventually does. Separately, a version-mismatch bug had slipped through releases before — the fix wasn't a reminder to check next time, it was a script wired directly into the release process that won't let a release proceed with a mismatch.

**Why it matters**: rules that live in someone's memory, or in a step someone has to remember to run, fail quietly. Nobody notices until the thing they were supposed to prevent has already happened. Encoding the rule into the mechanism itself removes the step where a person has to remember.

**Application beyond this week**: the same test applies to almost any recurring discipline — if the only thing standing between "works" and "silently breaks" is someone remembering to check, that's worth converting into something structural. It won't always be possible, but it's always worth asking.

**Related patterns**: the security fix earlier in the week is the same instinct under more pressure — closing a gap by making the correct behavior the only path, rather than trusting a rule to be followed.

---

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #050. Previous: [#049 "The Team Builds Its Own Reliability"](https://pipermorgan.ai/shipping-news/weekly-ship-049-the-team-builds-its-own-reliability).

*P.S. The plugin's first outside test didn't produce a working install — it produced three same-day fixes and an unsolved mystery about a missing plus sign. I'll take that trade for now. The loop is the thing. The polish comes next.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of June 26–July 2, 2026 | Phase: Alpha testing, connector cutover**
