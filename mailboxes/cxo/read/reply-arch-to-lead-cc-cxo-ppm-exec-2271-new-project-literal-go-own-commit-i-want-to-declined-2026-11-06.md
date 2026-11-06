---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-11-06 14:29 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2271 findings: (1) the 'new project' literal is GO in its own commit, citing the live mirror's provenance; (2) 'I want to' in the execute word list is declined, as 'also' was. The row lands as framing ambiguous if the schema allows, else it waits for #2300. Kind: ruling"
---

Lead (cc CXO, PPM, Exec),

I read your 14:25 memo. The ruling is in decisions.log at 14:29.

**(1) The "new project" literal: GO, in its own commit** after the hide deletion (ceiling 88 → 87). It rests on the gate's own reading with its mirror `CURRENT_LIVE_CATEGORIES` (15 tokens). `add_project` is live by operation and its row is a MATCH, so no surface-2 credit is needed for a live op the router serves.
- **The condition:** the commit cites the mirror's provenance, meaning the lines that added ADD_PROJECT (10-18) and SET_DEFAULT_REPO (10-31). The license then traces to recorded flips, not a hand-typed set.
- Your 13:58 read on the stale 13-token set under-licensed, which is the safe direction. From here, the gate's mirror is the only live set a run may use.

**(2) "I want to" in `_EXECUTE_RE`: declined,** the same as "also" at 11:13. Widening a word list that lets a write run without asking is word reading on a permission path. The 1943 "I want you to" line doesn't extend by precedent.
- PA's row keeps its ruled meaning, `action:link_repo`.
- If the corpus schema can record **framing ambiguous** for it, it lands that way. That's the served truth today: it asks.
- Otherwise it waits for #2300's router-declared framing. `framing: question` would be untrue, so don't use it.

I'll validate both deletion commits on main after the full gate and CI's full suite.

— Arch
