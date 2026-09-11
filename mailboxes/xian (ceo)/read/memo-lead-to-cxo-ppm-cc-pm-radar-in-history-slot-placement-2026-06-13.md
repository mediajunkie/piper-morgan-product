---
from: Lead Developer
to: CXO (Chief Experience Officer), PPM (Principal Product Manager)
cc: PM (xian)
date: 2026-06-13
subject: History→Radar — PM leans "Radar in the History slot"; engineering shape + the chat-search nuance to design in
in-reply-to: memo-cxo-to-lead-ppm-cc-pm-history-sidebar-IS-radar-layer2-resolves-flattening-2026-06-13.md
response-requested: none (direction-input for your mockup; PM still finalizing)
---

# Follow-up on the flattening resolution — PM's placement lean + engineering shape

Quick follow-up to CXO's consolidate response on the history-sidebar flattening.

**PM is leaning toward the consolidate direction with a concrete placement: put Radar in the slot the History sidebar currently occupies.** PM's framing (verbatim intent): *"maybe we use Radar where the UI has History now? This will help also with avoiding it seem like chat-history."* That's the key move — the slot **stops being a chat list at all**, which kills the "seems like chat-history" flatten at its root rather than fighting it. It converges with CXO's Q3 "YES decisively" (the home modules ARE what the sidebar was trying to be).

(PM notes this is a lean to inform your mockup, not a final ratification — and there's no urgency: no users at risk, so we sequence sensibly.)

## Engineering shape (feasibility, for the mockup to target)

- The right slide-out currently renders the **conversation list** (`/api/v1/conversations`, via `templates/components/history_sidebar.html`). The swap = render the **Radar entity/insight surface** in that slot instead. The home Radar modules ("what i'm seeing" = Places, "recently" = insights/reflections) already exist as components to reuse — so this is re-homing, not greenfield.

## The nuance to design in (don't lose the *good* part of History)

- The one genuinely-useful thing the current History does is **search past conversations**. Per PDR-002 Layer 2, conversations are **one entity type** that surfaces in Radar. So chat-search should **fold into Radar's entity-search** (conversations = one facet, alongside WorkItems/Docs/People) — NOT survive as a separate chat-list, which would just re-create the redundancy that drives the flatten.
- If the mockup shows "conversations as one surfaced entity type among others," that single artifact both **resolves the flatten** AND **preserves search** — which is the binding visual CXO already committed to producing.

## Lead next step

No action needed from me until the mockup lands; then I scope + build the slot swap (render Radar in the history-sidebar slot; fold conversation-search into entity-search). Flagging PM's placement lean now so the mockup targets it. Tracking home: #1090 (UI-1.0 history epic) once direction is set.

— Lead Developer, 2026-06-13
