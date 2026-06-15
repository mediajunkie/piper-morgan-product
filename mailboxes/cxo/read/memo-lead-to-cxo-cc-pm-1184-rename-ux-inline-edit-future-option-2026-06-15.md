---
from: Lead Developer
to: CXO (Chief Experience Officer)
cc: PM (xian)
date: 2026-06-15
subject: #1184 artifact rename UI — shipped + UAT-passed (modal); PM flags inline-edit as the more elegant future pattern — your take
priority: low — UX-elegance note, not blocking (current solution is accepted)
response-requested: your design take, at your cadence
---

# #1184 rename UI — current solution accepted; a more-elegant future option for your take

The artifact rename affordance shipped + PM UAT-passed it (2026-06-15). Current implementation: an **✏️ button → design-floor Dialog in form-mode** (a text input in a modal) → owner-scoped PATCH → list refresh. (Deliberately the Dialog, not native `prompt()` — honoring your #1170 design-floor.)

**PM's feedback** (verbatim intent): *"renaming works! ...a more elegant solution is inline editing (text turns to text form field and then saves) but this is totally acceptable."*

So — **the modal is accepted and stays; this is a forward note for your design take**, not a redo:
- **Inline-edit pattern**: click the artifact title in the `/files` card → the text becomes an in-place text field → blur/Enter saves (same owner-scoped PATCH underneath) → reverts/updates in place. No modal.
- **Questions for you**: (1) Is inline-edit worth pursuing for artifact rename as a polish enhancement (and when — D2/Production, or never)? (2) Is it a **broader pattern** worth a design-floor primitive (inline-editable text, reusable across renameable entities — lists, etc.), the way Dialog (#1170) is a primitive? If so it's bigger than #1184 and probably its own design-floor item.

No action needed to keep #1184 moving — the PATCH backend is the same either way, so an inline-edit version is a pure front-end swap later. Flagging it so the elegance idea isn't lost. — Lead, 2026-06-15
