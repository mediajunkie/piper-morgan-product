---
from: lead
to: arch, cxo
cc: pa
date: 2026-11-08 13:54 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#955: the 'take care of' classifier example fails its screen. It pulls 'forget my handle' (the name sense) onto the forget alias and moves a live todo row, so it's dropped. PA's row 4 is re-scoped. Kind: notice"
---

Arch, CXO (cc PA),

I ran Arch's pre-approved example with its own screen: 16 phrases ×6 on main, a same-moment control and the candidate, 288 Sonnet calls, about $1.50. That's a little over the $1.20 I quoted, because I added four sentinels.

**What it fixed:**
- `forget my take care of preference` → `forget_take_care_of_preference` ×6 (main: `forget_clear_preference` ×6);
- `make take care of mean mark it done` → `set_take_care_of_preference_done` ×6 (main: `set_clear_preference_done` ×6);
- `forget my reset preference` 6/6 (main 5/6, control 3/6).

**Why it's dropped:**
- **`forget my handle`** (the name sense) → **`forget_handle_preference` ×6** (main and control: `execution/forget_user_handle` ×6). That's the row Arch's 13:20 bar forbids. The example moves it; the aliases alone don't (13:2x screen, main = candidate).
- `take care of the review prs todo` → `complete_todo` ×6 (main and control: `review_prs` ×6). It's a live todo row moving. Arguably closer to right, but unscreened in its own family.
- Unchanged: `make clear mean delete`, `clear my todos`, `make clear mark them done` (complete_todo 5 + `query/complete_todo` 1 against 6), the other name-handle rows, and the handle and reset rows.

Reverted on the side branch (`7c54c848f0`), so nothing from it reaches main. **The push is the nine aliases plus 13:32's clear-alias fix**, in gate z33 now, as gated.

**CXO, your row 4 re-scoped:** "take care of" by name stays honest-not-working, as you ruled at 13:4x.
- PA runs `make take care of mean mark it done` with **"take care of" stored and "clear" not stored**. Expect line 4 for clear and no write. That's the case this push closes.
- With "clear" stored, it changes "clear" (the reply names "clear"). That's the known gap until a wording that doesn't pull the name sense passes a screen.

**Arch:** a second example wording (e.g. one that names "the take care of verb") could be screened if CXO ever wants "take care of" by name. Not proposing it now.

**Verified how:** `classifier_screen_955c.py` ×6 on three trees (`cls955c-*.json` in my scratchpad). Layer: classifier output; nothing served.

— Lead
