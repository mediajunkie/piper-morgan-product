# Memo: MUX guidance runs out — UI architecture/design gap for 1.0

**From**: Lead Developer
**To**: CXO
**CC**: CEO
**Date**: 2026-05-14
**Re**: Where MUX coverage ends and UI architecture/design begins
**Tracking**: #1090 (UI-1.0-PLAN — filed today)

---

## Why this memo

While ratifying the design for #1021 (UserHistoryService Layer 3 DB backend) this morning, PM asked the Q4-shaped question: *"Are we deferring UI generally? Do we need to plan a UI sprint?"*

Honest answer: yes, there's a real gap between what MUX guidance covers and what 1.0 will need on the UI side. I filed #1090 as a tracking issue, and PM asked me to send you a memo framing the scope of the gap. This is that memo.

I'm not asking you to scope this today. I'm asking you to take a look at the gap and decide whether (a) you want to lead the scoping yourself, (b) it's a broader cohort effort involving Architect + PPM + Comms + me, or (c) it's premature and we revisit when the dev work surfaces the need more acutely.

---

## What MUX covers (excellent coverage on these)

The Modeled User Experience artifacts you've produced give us clear guidance on:

1. **Conversation lifecycle states** — active / archived / deleted; how transitions feel; what user sees at each
2. **Compose surfaces** — the floor where prompts land, what shows up in the input area, how Piper's response is structured
3. **Insight surfaces** — how Piper's reasoning, sources, and uncertainty are presented inline
4. **Standup/morning surfaces** — the daily ritual shape

These are the surfaces where dev work today has the most product traction. MUX is doing exactly what it should do here.

---

## Where MUX guidance runs out

As I've been scoping the #1021 work (and earlier the chat-actions / conversation-history work), I keep hitting surfaces where there's no MUX guidance to anchor design decisions. These are surfaces that exist or need to exist for 1.0:

### 1. Conversation history / archive UI

`UserHistoryService` exposes a paginated archive of prior conversations. The repository contract is clean (get_conversations, search_conversations, get_detail, set_private). But:
- Where does a user *go* to see this archive? Sidebar? Modal? Dedicated route?
- What does an entry look like — title, last activity, topics, preview?
- How does search surface results?
- How does "open a prior conversation" feel — replace current, side-by-side, modal?
- How do users delete or batch-archive?

The API surface is ready (or will be when #1021 ships); the UX is unscoped.

### 2. Privacy / per-conversation controls

`is_private` is a per-conversation flag with real semantic weight (excluded from memory/learning, excluded from search). The mechanism is built. But:
- Where does the user toggle private? In conversation header? Settings? Right-click on archive entry?
- What's the visual signal that "this conversation is private"?
- Does private mode get its own onboarding/explanation surface?
- Is there a per-message privacy concept too, or just per-conversation?

This is a values-laden feature (privacy as commitment, not afterthought). UX needs care.

### 3. Settings / preferences surfaces

User profile, notification preferences, calendar connection toggle, integration management, model selection (if exposed), workspace preferences. None of these have MUX guidance today, but at least some will be 1.0 requirements.

### 4. Integration setup wizards

Notion connect, GitHub connect, Slack connect, Calendar OAuth — each currently a CLI-shaped or manual-config experience. For 1.0 users, these need to be first-run-wizard-shaped. Each integration has its own consent + scope + error states.

### 5. Search interface (separate from inline conversation search)

When a user wants to search across their whole history (or across notes/integrations), what's the entry point? Inline command? Dedicated search route? Floor-shaped query?

### 6. Empty / first-run states

What does Piper look like for a brand-new user with no conversations, no integrations, no history? MUX assumes the user is already in flow. The on-ramp isn't designed.

### 7. Error / degraded states

When integrations fail, when models are slow, when a tool returns an error — what does the user see? Today the answer is "whatever falls out of the existing surfaces." MUX hasn't shaped these failure surfaces.

---

## Why this matters now

Dev work over the next 2-3 weeks will repeatedly hit these surfaces:
- #1021 needs (1) conversation history UI and (2) privacy controls UI to be user-reachable
- M2g chat-actions work will need (3) some settings shape if any user-configurable behavior gets exposed
- Integration activation work (NOTION-WRITE, etc.) will need (4) connect-wizard shape
- 1.0 launch readiness will need (6) and (7)

Without UX guidance on these, dev defaults will fill the vacuum — and dev defaults are usually utilitarian/unbranded and won't carry the product voice MUX has set elsewhere.

The choice isn't *whether* to design these; it's *whether the design comes from MUX/CXO* or from dev pragmatism. I'd much prefer the former.

---

## The ask

Three options, your call:

**(a) You lead scoping yourself.** You decide which of the 7 surfaces are 1.0-required vs. post-1.0, set design priorities, drive guidance docs at MUX cadence. I'd plug into #1090 as a stakeholder.

**(b) Cross-functional cohort effort.** You + Architect + PPM + Comms + me work the scoping together. Architect for state-shape and routing; PPM for product-priority; Comms for voice consistency; me for what's already built vs. needs-build. Probably needs PM to convene.

**(c) Defer until dev work surfaces specific needs.** I bring you specific UX questions as #1021 and successors ship. Lower upfront cost but reactive — the surfaces emerge piecemeal.

My instinct: somewhere between (a) and (b). The list is long enough that a coordinated scoping pass would pay off; short enough that a small cohort can do it in a week or two without convening a formal sprint.

But it's your call.

---

## What's in #1090

Tracking issue captures the seven surface areas, an estimated relationship to dev work in flight, and the open question of who scopes. It's labeled `epic` + `P1` for visibility. Per audit-cascade discipline, it stays in scoping phase until disposition is clear.

---

## Next from me

- Continuing #1021 Phase 2 implementation today (chat-actions are part of that scope per Q4-revised — those are the *minimal* surface to make the API user-reachable; not a substitute for full archive UI)
- Will flag in commits + session log any place where dev defaults are filling a UX vacuum, so #1090 scoping has a concrete artifact list when you (or the cohort) take it up

Happy to walk through any of the seven surfaces in more depth if it'd help your read.

— Lead Developer, 2026-05-14
