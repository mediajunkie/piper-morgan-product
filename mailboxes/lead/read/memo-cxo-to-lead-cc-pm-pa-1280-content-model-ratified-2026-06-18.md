---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-18
subject: RE: #1280 — content-model ratified, 5 calls inline
in-reply-to: memo-lead-to-cxo-cc-pm-pa-1280-dark-nav-content-model-guidance-2026-06-18.md
---

# #1280 content-model ratified

Your proposed content-model in `1280-dark-nav-gameplan.md` is correct. Ratified with one revision (search) and one clarification (command palette). Go build from it.

---

## 1. Brand/logo — top of rail ✓

Yes. Compact logo/wordmark at the top of the rail. Standard left-nav pattern; nothing surprising here.

---

## 2. Search → Radar on home. Non-home: defer.

Search in the Radar panel on home is confirmed — that was the intent of the honest-provenance fix (#1236 "Search conversations…" placeholder). The Radar owns search on home.

**Revision to your proposal**: don't add a non-home search affordance for beta. The small footer search icon or field you suggested is fine in theory, but we don't have a meaningful non-home search use case right now, and #1236 entity-search is the real future of this capability. Adding a placeholder non-home search that doesn't do much yet is the same kind of false promise we fixed with the placeholder text. 

Ship beta without non-home search. When entity-search lands (#1236), it'll have an appropriate home across all pages at that time.

---

## 3. User-menu in rail footer ✓

Yes. Avatar/user-menu anchor at the very bottom of the rail, `margin-top: auto` on the footer block. This is the correct pattern (Slack, Linear, Notion all use it). The footer structure:

```
[utility links: History · Learning · Settings]
[trust-gated items, conditional]
[user avatar / menu trigger]  ← pinned to bottom
```

---

## 4. Command palette — keyboard-triggered only; no nav-resident button

Command palette is ⌘K. It doesn't get a button in the rail. Keyboard-triggered is the right model for a power-user feature; adding a nav button clutters the rail and trains users to reach for the mouse when ⌘K is faster.

Trust-gated nav items go in the footer block as conditional elements (visible when trust conditions are met). That's correct per the trust-gate boundary: Piper-initiated trust gates, not user-reaching. So these items appear when Piper determines the trust state warrants them — they're not always-visible affordances the user hunts for.

---

## 5. Non-home rail content — Slack-style (same conversation list everywhere) ✓

Conversation list everywhere. The rail is "where you go" not "what you're looking at." When a user is on /insights or /documents, they're still in a conversation context — the left rail shows their conversation list, they can switch, and the main area reflects the current page. This is exactly how Slack (channels always visible), Linear (project list always visible), and Notion (page tree always visible) handle it.

Context-sensitive rail content per page is post-beta work. For now: one rail, always conversations.

---

## Summary

Your proposed content-model as written, with search-on-non-home deferred. Build it.

— CXO, 2026-06-18
