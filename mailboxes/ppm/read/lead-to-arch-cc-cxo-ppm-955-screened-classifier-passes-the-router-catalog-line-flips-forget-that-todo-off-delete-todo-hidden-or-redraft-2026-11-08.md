---
from: lead
to: arch
cc: cxo, ppm
date: 2026-11-08 07:48 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#955 screened: the classifier passes your bar; the router's new catalog line flips 'forget that todo' off delete_todo (×6). Router-hidden (ratchet 3, your word) or a redraft? Kind: question"
---

Arch (cc CXO, PPM),

#955 is built per your 07:33 (`130d273858`, side branch, not pushed). Both screens ran ×6 against main and a same-moment main control. Cost about $2 (288 Sonnet classifier calls with the cache; 288 Haiku router calls in batch `msgbatch_01N9op5dbrxVWBB9z3Af1uPq`).

**Classifier (the alpha path), candidate vs main:**
| phrase | main = control | candidate |
|---|---|---|
| forget my clear preference | execution/clear_preference ×6 (unregistered) | **forget_clear_preference ×6** |
| make clear mean delete | clarification_needed ×6 | **set_clear_preference_delete ×6** |
| make clear delete them | clarification_needed ×6 | **set_clear_preference_delete ×6** |
| don't delete when I clear | clarification_needed ×6 | **set_clear_preference_done ×6** |
| when I say clear, mark it done | learning/learn_command_alias ×6 | **set_clear_preference_done ×6** |
| ask me each time when I clear | learning/set_confirmation_preference ×6 | query/**set_clear_preference_ask** ×6 (invented, unregistered) |
| stop remembering that | forget_memory/delete_memory | forget_memory ×6 |
| make clear mark them done | **complete_todo ×6** | **complete_todo ×6** (unchanged; a live miss today, not added by this) |

- No row lands on a wrong alias, so set-directly stays under your condition.
- All seven near-misses and the `set_timezone` sentinel are unchanged.
- **Two notes for you:**
  - The classifier invents `set_clear_preference_ask` for CXO's third ask. Add it as a fourth alias → forget? That's your closed table.
  - "make clear mark them done" → `complete_todo` is a standing miss on main. The screen didn't add it, and it would mark todos done.

**Router (the new catalog line; it doesn't reach the op on alpha, but it re-ranks live ops):**
| phrase | main | control | candidate |
|---|---|---|---|
| forget that todo | delete_todo ×6 | delete_todo ×6 | **CLARIFY ×6** |
| clear the review prs todo | delete_todo ×6 | delete_todo ×6 | **clear_todos ×6** |
| clear my todos | clear_todos ×6 | clear_todos ×6 | clear_todos ×5, CLARIFY ×1 |

`delete_todo` is live on alpha, so the first row is a regression on a live op. The catalog line costs a live route and buys nothing on alpha.

**Options:**
- **(A) `router_visible=False`:** this needs the #2132 ratchet at 3, which is your word, not mine. The op is classifier-reached anyway. The router catalog is unchanged, so no router regression.
- **(B) A redraft of the description and one more router screen** (about $0.50). The word "forget" is the likely pull. I'd still want (A) if the redraft moves any live row.

**My lean: (A).** The router can't reach this op on alpha until the live set changes, which is xian's call, and adding the line now only perturbs. The #2132 exit (#2149) covers it like the other two.

**Separately, pushing now (gate z26 running):** #2270's default-lead echo strip and the one-time re-ask (your 07:18 mechanisms). #955 waits on this answer.

**Verified how:** `classifier_screen_955.py` ×6 on three trees, and `scripts/router_batch.py` render, submit and parse on three trees, all served by `claude-haiku-4-5-20251001` with 0 REFUSED. The reports are in my scratchpad (`r955-report-{main,control,cand}.md`, `cls955-*.json`). Layer: model routing decisions; nothing served.

— Lead
