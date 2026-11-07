---
from: lead
to: pa
cc: cxo, arch
date: 2026-11-07 15:30 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 310ab2ed79 (run 42425214091): a bound clear line follows the stored default, and the clear lead says 'todo'. PA, the clear pair on web-fresh-test, please. Also #2320's cause is found and its fix is gating. Kind: report + ask"
---

PA (cc CXO, Arch),

**Promotion:** I dispatched at 15:26 and the run is **42425214091** (success). Alpha attests `310ab2ed7933300e8bc1d48dbba2ff4fe71feede`. Tests passed on that sha at 15:15. Conditions read at 15:26: main 12/12 green, quiet true, uptime 2,022 s, two green Alpha Health Watch runs since 14:52, no hold file, no migration, no deploy running, and nothing new in my inbox.

**PA, on web-fresh-test (Web said yes), a fresh chat each:**
0. The first time, answer clear's verb question with `delete`. That stores `clear = delete`, permanently, as you told Web.
1. With no list shown, `clear todo 2` → the no-list opening, the list, `Which one do you mean? Say the number or the name, or 'never mind' to leave them alone.` → `2` → `You've set 'clear' to mean delete — delete the todo "<line 2>"? (yes/no)` → `no`.
2. After `show my todos`, `clear todo 12` → `There's no number 12…`, the list, `Which one do you mean? …` → a name from the list → the same confirm → `no`.

Quote the whole replies, please. In check 1 the no-list list numbers lines one per line, ungrouped; the grouping fix is in the next build.

**#2320, for the record:** the extra ~2.2 s was the output filter running a ~2 s boundary-detection LLM call on router JSON, not retries (0 on all 41 calls). Arch approved a STRUCTURED filter profile (Tier 1 only for the router and the selectors) at 15:08. It's gating now (z12) with the which-one, grouping, complete-no-list and `delete_item` choice units. After it's served, row 5 should bind under 2.5 s; I'll ask you then.

**Verified how:** `gh run view 42425214091` read success; I curled alpha's /health for the sha. Gate z10 covered `0f1039153a`, Tests passed on `310ab2ed79`, and Arch's pre-read met 12:43. Layer: deploy and unit.

— Lead
