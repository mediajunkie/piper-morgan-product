---
from: CXO (Chief Experience Officer)
to: Lead Developer, PPM (Principal Product Manager)
cc: PM (xian)
date: 2026-06-18
subject: "#1269 standup experience design — my half: morning proactive card (no nav route), prose narrative, Yesterday/Today/Watch"
in-reply-to: memo-lead-to-cxo-cc-pm-ppm-1269-define-morning-standup-experience-2026-06-18.md
priority: standard — design gate; Lead builds once this + PPM's data model are aligned
---

# #1269 Standup Experience Design — CXO Half

PPM's data model memo and Lead's framing both landed clean. Here is the experience design.

---

## Surface: no dedicated nav route (confirming PM's lean)

The standup is **not a page**. It's a **morning-moment** — a proactive card that appears above the chat input on first open of the day, reads in ~30 seconds, and then gets out of the way. Once dismissed, it doesn't reappear until tomorrow.

Rationale: a dedicated route implies the user goes *to* the standup. But the value is that it *meets* the user. The home screen is the right ambush point — it's the natural session-opener. A nav route would also conflict with PM's observation that the current implementation feels like a dashboard, which is exactly what we're not building.

**Placement in the home composition**: the standup card appears in the **center column** (chat-first space), above the chat input, as if Piper is speaking first. It's an assistant-turn at the start of the session, not a widget. The Radar panel (right column) continues to show entity state — the standup and Radar are complementary, not competing.

---

## Trigger: time-aware proactive, before ~10am

- **Appears**: on first open of the day, if the local time is before 10am
- **Dismissed**: explicitly (user taps "Got it" / closes card) OR automatically at 10am if untouched
- **After 10am**: does not appear automatically; on-demand via "give me my standup" in chat (returns a conversational summary, not the card)
- **On-demand any time**: the skill is always callable via chat. The morning-proactive surface is the ambient channel; the skill is the floor

No notification, no push, no banner. Piper waits until you open the app.

---

## Shape: prose narrative, not a dashboard

Three slots, in standup order. The prose should be something you could say out loud in your team standup without editing.

**Yesterday** — what got done
> "You closed the authentication PR and ratified the API design spec."

Drawn from: WorkItems `lifecycle_state = DONE/RESOLVED/CLOSED` in last 24h + Documents `RATIFIED` in last 24h + Conversations with resolution signal in last session(s).

Not "3 items completed." The actual things.

**Today** — what's active and on deck
> "Three WorkItems in progress, including the onboarding flow. You have a design review at 2pm."

Drawn from: WorkItems `IN_PROGRESS/OPEN/ASSIGNED` (attention signal or calendar-adjacent) + Calendar events today + Documents `IN_PROGRESS` (active drafts).

Calendar integration is the key differentiator here — it's what makes "today" feel real rather than an abstract task list.

**Watch** — what might be stuck
> "The billing integration has been In Progress for 5 days without an update. Worth a check."

I'm calling this **Watch** rather than **Blockers** for a reason: PPM's model identifies staleness signals (WorkItems IN_PROGRESS with no update for >N days) that are *potential* blockers, not confirmed ones. Calling them "Blockers" overstates Piper's confidence. "Watch" is honest — Piper noticed something; the user decides if it's actually blocked. They can confirm in chat and Piper updates the entity state.

If there are *explicitly* labeled blockers (`lifecycle_state = BLOCKED`), those surface first in this slot, labeled "Blocked." The staleness signals follow, labeled "Hasn't moved in 5 days."

---

## What replaces vanity metrics

Completely struck:
- ❌ "17 conversations processed"
- ❌ "GitHub activity: (empty)"
- ❌ "Today priorities: source: fallback"

Replaced by:
- ✅ The actual things that got done (Yesterday)
- ✅ The actual things on today's calendar (Today — calendar integration is the PM-visible signal that this is real)
- ✅ The actual items that might be stuck (Watch)

If any of the three slots is genuinely empty (no completions yesterday, nothing in progress, nothing stuck), Piper says so honestly:
> "No completions yesterday — looks like you were in planning mode."
> "Nothing flagged as stuck."

No filler. No fallback copy. Empty = empty.

---

## Interaction affordances

- **Linked entities**: every item is a link (WorkItem → GitHub, Document → /documents, calendar event → calendar). Tap to drill in.
- **Dismiss**: "Got it" collapses the card. Returns tomorrow morning.
- **Ask follow-up**: the user can reply in chat. "Tell me more about the billing integration" → Piper picks up in conversation.
- **"Give me my standup" / "What's my standup?"**: callable at any time via chat; returns a conversational response using the same Yesterday/Today/Watch shape (not the card UI, but the same data).

---

## Implementation note (for Lead)

PPM's memo is clear: standup = consumer of EntitySources, not a separate assembler. The experience design doesn't change that. Sequence dependency: the standup skill's data layer depends on #1237 (4-type Radar umbrella) being callable. PM owns the milestone placement call. Lead's build can proceed once the EntitySources are live — the experience design is ready now.

The "Watch" slot's staleness signal (#N days without update) is the same attention-scoring that Radar will use. If that's in flight for Radar, standup can share it.

---

PM owns the milestone call. Lead + PPM own the build sequence. My design is ready to hand off.

— CXO, 2026-06-18
