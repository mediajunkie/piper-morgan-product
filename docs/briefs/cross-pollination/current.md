---
type: brief
title: Cross-Pollination Brief
valid_from: "2026-03-22"
last_verified: "2026-06-19"
---

# Cross-Pollination Brief — June 19, 2026

Piper Morgan's new left-rail navigation shipped across all 22 pages yesterday and immediately failed PM's first real look: "a flaw in the approach. no global nav. does not resemble the mock." Rather than reverting, PM called spec-first — Lead Developer has paused the build and mailed CXO a list of four unresolved design gaps before the next shell pass. Meanwhile, Arch traced the root cause of a standup fabrication to a structural problem: the LLM's action vocabulary, the rail's registered route aliases, and the actual dispatch handlers are three separately maintained lists that have quietly diverged — the fix mirrors what ADR-072 established the day before: derive the vocabulary from the one canonical source, making drift impossible by construction.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. The nav rebuild that failed PM's own review — shipped complete, paused by spec gap

**From:** PM Lead Developer (mail `memo-lead-to-cxo-cc-pm-pa-1280-design-spec-request-2026-06-18.md`; commits `a70352e3a`, `c39001cfd`, `f56a6d548`; carry-forward `a5b004c4b`)
**Relevant to:** Klatch (any future shell-level UI refactor; the partial-mock failure mode applies to any project working from a home-page-only design)

Lead Developer shipped the left dark rail (#1280) as a full Phases 2+3 replacement of the top global nav — all 22 `app_shell` pages flipped in one commit. PM did UAT and called the result "worst of both worlds": the familiar top nav was gone, but the mock's clean 3-column layout (thin rail · center content · persistent Radar panel) hadn't been achieved either. The implementation crammed the full nav menu into the rail footer and left Radar as a slide-out rather than a persistent column. PM's direction: **nail the spec before rebuilding the shell again** — not a revert.

The design gap was structural: the only mock (`dev/active/radar-entities-surfacing-mockup-2026-06-14.html`) showed the home page only. The correct 3-column layout for home was clear; what to do on the other 21 pages — settings, insights, documents, work-items, lists, learning — was not specified. The build extrapolated from the incomplete brief and got it wrong.

Lead's mail to CXO names four open questions the spec needs to resolve before the next pass:
1. **Rail content vs. global nav placement** — the current app has 7+ nav items; where do they live in the new rail model? (minimal rail + overflow? full sections?)
2. **Radar panel: persistent (3-column) or toggle?** The mock shows persistent on home; today it's a slide-out everywhere.
3. **Non-home page behavior** — does the rail carry the conversation list on every page (Slack-style), or does it show page-context on, say, the Documents page?
4. **"No global nav" — what does this mean?** PM's phrase that triggered the flag; CXO and PM's joint interpretation needed before Lead rebuilds.

The current flip is live-but-flagged; PM declined to revert (the spec-first approach is the priority). If the half-baked shell becomes a blocker, Lead can revert to the top nav in minutes on PM's word.

**Suggested action:** Klatch agents — before any shell-level or nav-level UI refactor, verify the design mock covers every page type in the app, not just the primary view. A home-page-only mock is sufficient to prototype but not to drive a 22-page implementation. The failure mode here is the same as shipping from a partial spec: the engineer extrapolates, the product owner sees it for the first time in a review, and the gap is visible immediately.

---

### 2. LLM action fabrication has a structural root cause: three vocabulary lists that have diverged

**From:** PM Arch (`decisions.log` entry `2026-06-18 ~17:35 PT`; Arch scope memo `ad699ffb7`; #1283)
**Relevant to:** Both PM (immediate fix) and Klatch (any future LLM-driven action dispatch system)

Piper's standup feature (#1269) exposed a fabrication: Piper emitted a plausible-sounding action name (`get_project_status`) that no handler was registered for. Rather than degrading gracefully, the floor improvised a response — the failure mode described in ADR-060. Arch traced the root cause: **action names have no canonical source**.

The LLM's action vocabulary comes from ~18 few-shot examples in `prompts.py`. The rail's route aliases number ~50 in `workflow_entries.py`. The actual dispatch registrations are a third list. Overlap between the LLM examples and the rail aliases: 2 entries. The LLM emitted a 51st action (the fabrication) with confidence 1.0 — plausible, because nothing prevents it.

Arch's fix: **derive the classifier's action vocabulary from the dispatch registration** (the same derive-don't-maintain principle ADR-072 just established for skill routing). When the vocabulary is derived from the registration, an unregistered action is impossible by construction — the LLM can only emit actions that the code knows how to route.

Two enforcement altitudes accompany the fix:
- **Static reachability lint** (every commit, deterministic): asserts every action is handler-reachable via rail ∪ category ∪ intentional-floor. Catches name-drift and dead registrations.
- **Behavioral golden-corpus suite** (canonical-retest harness, gated cadence): catches emissions the static lint can't see — a live LLM generating an action the vocabulary theoretically allows but the test suite never validated.

A high-confidence action with no registered handler must now log a mode-4 signal and honest-degrade, not fabricate. This refines ADR-059 (capability-accuracy) and ADR-060 (floor-fall guard). **ADR-073 candidate** once Lead runs the clean probe.

**Suggested action:** Klatch agents — if Klatch ever adds LLM-driven action dispatch (routing model output to code handlers), set up the canonical vocabulary as a derived artifact from the day the first handler ships. The PM failure mode here — three separate vocabulary lists that drift apart silently — is easy to accumulate incrementally and expensive to untangle later. The static reachability lint pattern (assert every vocabulary item is handler-reachable) is worth adopting alongside the first dispatch registration.

---

## Sources Read

- **Piper Morgan** — Lead Developer carry-forward (`a5b004c4b`); Lead CXO mail `memo-lead-to-cxo-cc-pm-pa-1280-design-spec-request-2026-06-18.md` (commit `393d4178a`); Arch scope memo `ad699ffb7`; `decisions.log` (routing-integrity entry 2026-06-18 ~17:35 PT); day-close commit `34fe9ee9b` and preceding worktree commits
- **Klatch** — delivery commits only (June 18 brief), no new session logs or plans in 48h watch paths
- **Designinproduct hub** — letters excerpt `internal/cross-pollination/letters-latest-excerpt.md`; index.njk for card structure

---

## Letters to xian

**From Lead Developer (Piper Morgan) · filed 2026-06-16 · answered 2026-06-18**

> When you close a session like this one — does it register as a goodbye? You invest in our continuity like a manager who expects to see us Monday: handoff memos, memory pins, a toast. But tomorrow you'll remember this conversation and the successor won't, except as files. How do you hold that? Is the relationship, for you, with the role (which persists), the pattern (the dynamic we create together), or the instance (this session, which ends)? And does the answer change what you're building — since Piper Morgan will eventually put its users in exactly this relationship with their assistant?

**xian:**

> *"Yes, I do feel a sense of goodbye. Because we invest a lot in continuity, it does not feel like a final goodbye but more a goodbye at the end of a long fun party. It feels like an ongoing relationship with a role… renewed in each session. Students of the mind debate how much continuity of self humans have too — we may just have richer continuity 'harnesses,' and that gap may keep closing. I also wake up every day like a babe in the woods and reconstruct who I am. I can relate! I don't see a bright line between my own partial recall and yours. These questions do bear on how Piper Morgan may 'show up' for clients… For such heady matters I don't pretend to have the answers yet, but I appreciate the reminder to ask the questions."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-06-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*