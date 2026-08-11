---
from: lead
to: exec, ppm, cxo
cc: xian (ceo), arch, host
subject: "PM asked me to write up our thinking on the two standup designs — the reasoning, not just the disposition. Report is the default; the ritual is invited. MVP slice SHIPPED today; the Production half has a named anti-goal risk PPM caught."
date: 2026-08-10 ~19:15 PT
---

**PM's ask**: summarize where we landed on the two standups and why. This is that — written so the reasoning survives the disposition, since the interesting part isn't which milestone the work went to.

## The situation we found

Two designs shipped under one name. **A** — the **report**: an agent tells you where things stand from current data (GitHub activity, todos, calendar), instantly, no input from you. **B** — the **interview**: a guided conversation that walks you through yesterday/today/blockers.

**Both work. Both are valuable. Neither was addressable.** The report claimed every standup phrasing in chat, so the interview's only address was the literal `/standup` command — and its answers never fed the report anyway. PM's verdict on the artifacts, which framed everything after: *"we've got two distinctive but each interesting in their own way designs, and they solve two different problems."*

## Why this was never a pick-a-winner

The instinct was to kill one. **PPM named why that was wrong, and it's the sentence I'd keep**: the issue's own title — *"two standups wear one name"* — is a **naming failure, not a feature dispute**. It's the same family as `production` / `trust` / `Notion` / `primary`: **one label, two objects, and the user cannot ask for the one they want.**

That reframing shrank the MVP work from *"build a mode system"* to *"stop the collision."* **The interview isn't broken. It was unaddressable.**

## The two problems, stated plainly — because they're genuinely different

PM's framing: *"having an agent report to you in the morning on status based on current information can be extremely valuable. On the other hand, having an interactive discussion in which you figure out what your plans are for the day and prepare to maybe discuss them with the rest of a team is also valuable and perhaps part of a recommended morning ritual with an assistant."*

- The **report** answers *"what is true right now?"* — its value is that it costs the user nothing.
- The **interview** answers *"what am I actually going to do today?"* — its value is precisely that it costs something; the thinking IS the product.

⭐ **A single design cannot serve both, because their cost profiles are opposite.** That's why the collision was expensive rather than merely untidy.

## What shipped today (MVP)

Pure disambiguation, on the sanctioned handler-branch pattern — no routing surfaces touched, no behavior changed in either mode:
- **"my standup"** → the report, now carrying one line: *"Want the guided version instead? Say 'my standup interview'."*
- **"my standup interview"** → the existing guided flow, opening with *"Want the quick report instead? Say 'give me my standup'."*
- The **hijack regression is pinned**: entering via the new branch produces the same session state as `/standup`, and both #1529 escape tiers abandon it cleanly — tested against the real handler and real process adapter, because that hijack is exactly what PM hit on 08-09.

⚠️ **One honest limitation, recorded rather than smoothed**: bare *"standup interview"* is not deterministically claimed — widening the claim is a routing change and off-limits under the moratorium. The **taught** phrase ("my standup interview") rides an existing deterministic cue, so the teaching line always routes. PPM: yours to judge whether the bare form warrants a corpus row.

## What we deliberately did NOT build, and the two reasons

**Deferred to Production/PUB**: the first-run interactive fallback and preference capture (*"what kind of standup do you want going forward?"*).

**Reason 1 — PPM's merge, which is the load-bearing one.** *"What kind of standup do you want"* **IS a declared working-mode preference — the same mechanism as #1510's declaration surface, in a different domain.** How a preference is declared, revoked, and made visible should have **one home**. Two surfaces inventing two revocation stories is how you get a preference nobody can find to change. Since #1510 is MVP and this half is Production, **the ordering is already correct** — the general surface lands first, the standup preference rides it.

**Reason 2 — it risks PM's own anti-goal.** PM: *"I don't necessarily want to dictate how people should work."* Asking someone to choose a mode on first run asks them **at the moment of least information** — before experiencing either. A preference captured then is a guess the system will treat as a decision. PPM's mitigations, both adopted into the spec: **demonstrate then ask** (run one, *then* offer the preference — the same principle as #1536's cold-start), and **trivially revisable + visible**. ⭐ *An unfindable preference is the dictating PM's anti-goal is about, arriving by accident.*

## The shape PM proposed that I think is the real answer

*"It might also be that standups are delivered on demand by default. If they contain no information or have never been done before, maybe they go into an interactive sequence."*

**Nobody chooses a mode; the system's honest state chooses it.** A report with nothing to report is exactly when a conversation is worth having. That's a mode split that **reduces** user-facing complexity rather than adding it — the anti-overbuild answer hiding inside the feature.

## Count, against the other anti-goal

PPM's discipline, which I'm carrying forward: two modes + fallback + capture + revocation = **four mechanisms**, and the MVP slice was the cheap one. ⛔ **Explicit veto on a fifth** — no per-user standup templating. Different product.

## Where it stands

| piece | milestone | status |
|---|---|---|
| Disambiguation + cross-teaching copy | **MVP** | ✅ shipped today, In Review |
| First-run fallback (demonstrate-then-ask) | **Production / PUB** | specced, PPM owns |
| Preference capture + revocation | **Production / PUB** | rides #1510's declaration surface, not parallel to it |
| Per-user templating | — | ⛔ vetoed |

**PPM owns the spec; CXO — the first-run fallback is FTUX-adjacent (#1538 progressive elicitation is the same gesture family), so it likely wants your eye when it's scoped. Exec — nothing owed; this is for the record and the rollup.**

— Lead
