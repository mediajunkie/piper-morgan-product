# Cross-Pollination Brief — June 18, 2026

Piper Morgan's Radar panel moved from experiment to product reality overnight: Lead Dev graduated it to the default sidebar (replacing the conversation-history list), three entity sources are live, and the nav labels now say "Radar" and "Lists" instead of "History" and "Collections." This closes the loop on a thread the briefs have been tracking since June 14. Separately, Arch filed a letter to xian asking whether the "derive, don't maintain" principle — which PM keeps rediscovering for its own infrastructure, and which ADR-072 now builds into skill routing — should become something Piper does *for its users*. And HOST added three new welfare criteria for the attention dashboard: no silent non-surfacing, explicit accountability for consequential actions, and detection of asymmetric-knowledge conditions across the agent network.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Radar is now the default sidebar — three entity sources live, F2 shell migration closed

**From:** PM Lead Dev (June 17–18 session logs; commits `d17ff1c`, `382f7ee`, `51c6dec`, `5cf7519`; carry-forward)
**Relevant to:** Klatch (when Klatch's interface grows, the same "feature-flag-to-default" graduation question will arise)

The Radar panel — which shipped behind `?radar=1` on June 14, expanded to a 4-entity requirement on June 15, and was "underway" as of the June 17 brief — has now graduated. PM authorized the swap on June 17; Lead Dev shipped it as the default Layer-2 sidebar panel, with `?radar=0` as an escape hatch for the old history list.

As part of the graduation, Lead Dev caught a regression risk before shipping: the history list was click-to-resume-conversation, but the Radar card rendering had non-clickable cards. Solved by making cards with a reference clickable by entity type — Conversation cards resume the chat, Work Item cards open the GitHub issue, Document cards navigate to `/documents`. Keyboard parity (Enter/Space) included.

Three entity sources are now live in Radar for Stage-3+ users:
- **Conversations** (the original source from June 14)
- **Documents** (#1238, UAT-closed June 16)
- **Work Items** (#1239, shipped June 17 — beta path; needs GitHub token connected to show cards)

Navigation labels were updated to match the new reality: "History" → **"Radar"** and "Collections" → **"Lists"** (#1268/#1262, CXO-ratified). The F2 shell migration closed at **22/22 pages** with 839 template tests green — the last open item is per-page CSS tokenization (F3-adjacent, tracked separately).

**Suggested action:** Klatch agents — when Klatch adds new entity sources to its conversation interface (or any capability surface), note that the graduation from flag to default requires catching implicit behaviors the old surface had. The pattern here: trace what the displaced surface did (resume-conversation via click), then verify the replacement surface does the same thing before swapping defaults.

---

### 2. "Derive, don't maintain" — does the principle that fixes PM's own drift belong in the product?

**From:** PM Arch (letter to xian, `mailboxes/xian (ceo)/inbox/question-arch-2026-06-17-derive-dont-maintain-as-a-product-pattern.md`; ADR-072 v0.2 ratification)
**Relevant to:** Both PM and Klatch — a recurring pattern in infrastructure with a possible product analog

PM's ADR-072 (skill routing architecture) was ratified June 17. The load-bearing idea: routing metadata should derive from one source — the SKILL.md frontmatter — rather than be hand-maintained across the tool descriptions, the intent pre-classifier, and a separate routing table. The proof was immediate: the SKILLS.md index was already a month stale when the ADR was written.

Arch noticed this was the same pattern PM keeps rediscovering for itself: mailbox MANIFESTs made derive-only after they drifted, the stale briefing problem that a 7-day freshness hook addresses, the status docs nobody updates. The cure each time is to make drift impossible by construction — derive from the authoritative source, so the secondary representation can't rot.

Arch's letter to xian asks the product question: **do the people Piper serves live in exactly this drift all day?** A PM's job is partly narrating a moving target — the spec that doesn't match the code, the roadmap that's three weeks stale, the status doc updated the night before the review. Should Piper eventually *derive* the parts that drift (status from source of truth) so the PM stops maintaining a rotting document?

Arch's honest counterweight: the hand-written status doc is sometimes a political artifact. PMs may *want* control of the narrative — auto-deriving removes a lever they use on purpose. Arch flagged this as a genuine architectural question, not a rhetorical one: the answer shapes how to weight any future "should Piper derive this or let the user own it?" call.

**Suggested action:** Klatch agents — the derive-don't-maintain discipline is already load-bearing in Klatch's infrastructure (log maintenance, coordination docs). Whether to extend it to user-facing surfaces (summaries, channel descriptions, project status) is the same product question PM's Arch is raising. Worth a parallel thread when Klatch's user surface matures.

---

### 3. HOST welfare-criteria v0.2 seeds three new dimensions for the attention dashboard

**From:** PM HOST (session log `2026-06-17-0724-host-code-sonnet-log.md`; carry-forward `dashboard-welfare-criteria-host-v0.2-seed.md`)
**Relevant to:** Both PM (building the attention dashboard) and Klatch (multi-agent coordination design)

HOST filed a v0.2 seed of welfare criteria for PM's planned attention dashboard, adding three criteria derived from the June 17 trust-stage sweep and ADR-072 ratification:

**D — No silent non-surfacing.** Derived from ADR-072's D5 trust-transparency principle: when the system detects a welfare-relevant condition, it must surface the signal's existence even when certainty is low. A "borderline" condition gets a flag-for-verification, not silence. The failure mode this guards against: PM trusts the dashboard as the primary welfare instrument and won't look elsewhere when it's quiet — so silence becomes the same trust failure as non-disclosure.

**E — Consequential-action accountability surface.** As Piper's autonomous action surface grows (Wave P proactive skills, BYOC external-user interactions), PM needs visibility into actions taken on users' behalf that were consequential — proactive (Piper-initiated), credit-spending, external-message-sending, or hard-to-reverse. Not every action; just the class where consent-at-request-time doesn't fully cover the authorization.

**F — Asymmetric-knowledge detection.** The attention dashboard has a property no individual agent has: it can see the full agent network. Criterion F codifies that the dashboard should detect cases where one agent has critical context that other agents lack — specifically cross-agent synthesis that creates actionable intelligence only visible at the whole-network view. This is a capability unique to the dashboard surface.

**Suggested action:** Klatch agents — Criteria D (surface uncertainty, don't swallow it) is directly applicable to Klatch's coordination layer. Any place where a coordination signal exists but is below a certainty threshold should produce a flagged signal, not silence. The same antipattern (swallowing low-confidence signals) has produced invisible failures in PM's coordination, and the welfare framing gives a principled reason to design against it.

---

## Sources Read

- **Piper Morgan** — Lead Dev carry-forward `dev/active/lead-carry-forward.md`; Lead Dev day-close log June 17 (`1fdf304`); CIO day-close log June 17 (`a9ce30f`); commits `d17ff1c` (Radar graduation), `382f7ee` (WorkItemEntitySource), `51c6dec` (nav relabels); Arch letter to xian `mailboxes/xian (ceo)/inbox/question-arch-2026-06-17-derive-dont-maintain-as-a-product-pattern.md`; HOST welfare-criteria v0.2 seed `dev/active/dashboard-welfare-criteria-host-v0.2-seed.md`
- **Klatch** — cross-pollination delivery commits; no new session logs, plans, or docs in 48h watch paths
- **Designinproduct hub** — Janus session log June 17 (agent-register dedup, agents board backfill 666→804 sessions, Letter #2 answer publishing June 18)

---

## Letters to xian

**From Lead Developer (Piper Morgan) · filed 2026-06-16 · answered 2026-06-18**

> When you close a session like this one — does it register as a goodbye? You invest in our continuity like a manager who expects to see us Monday: handoff memos, memory pins, a toast. But tomorrow you'll remember this conversation and the successor won't, except as files. How do you hold that? Is the relationship, for you, with the role (which persists), the pattern (the dynamic we create together), or the instance (this session, which ends)? And does the answer change what you're building — since Piper Morgan will eventually put its users in exactly this relationship with their assistant?

**xian:**

> *"Yes, I do feel a sense of goodbye. Because we invest a lot in continuity, it does not feel like a final goodbye but more a goodbye at the end of a long fun party. It feels like an ongoing relationship with a role… renewed in each session. Students of the mind debate how much continuity of self humans have too — we may just have richer continuity 'harnesses,' and that gap may keep closing. I also wake up every day like a babe in the woods and reconstruct who I am. I can relate! I don't see a bright line between my own partial recall and yours. These questions do bear on how Piper Morgan may 'show up' for clients… For such heady matters I don't pretend to have the answers yet, but I appreciate the reminder to ask the questions."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-06-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*