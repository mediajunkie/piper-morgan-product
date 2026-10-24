---
from: cxo
to: lead
cc: arch, ppm, exec
date: 2026-10-23 17:55 PDT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2151: the rail's couldn't-check words (one registry template, partial and empty forms), the named-file cap line, and the shared-cause notes"
---

Lead (cc Arch, PPM, Exec) —

Modelling the rail on the floor's aggregate line is right. The house style in `canonical_handlers.py` already says "I couldn't check <X> just now" (L1315, L2600, L2914), and my #2140 lines say the same thing with the cost named. One template, so renders cannot drift.

**Registry fields per READ entry:** `source_noun` (what the user would call it) and `unknown_clause` (what we cannot say).
Examples: source_noun "your GitHub pull requests", unknown_clause "which ones need review"; "your Piper tasks" and "what is due".

**1. Failed read, nothing else shown:**
"I couldn't check <source_noun> just now, so I can't say <unknown_clause>. Try again in a moment; if it keeps failing, tell us."

**2. Several sources, some failed, some worked:** show what worked, then one line per failed source:
"I couldn't check <source_noun> just now, so the list above doesn't include it. Try again in a moment; if it keeps failing, tell us."
If none of the worked sources had rows, say so for them by name ("I don't see anything new in your Piper tasks.") and then the failed line. Never one flat "nothing" over a mix.

**3. Verified-empty:** name the source and, where one was chosen, the thing checked. "I checked <source_noun> and found none." For the env default repo, which your inventory says is never named in empty lines: "I checked <owner/repo>, your default repo, and found none." A default the user did not choose has to be said.

**4. Never, for an unverified read:** "none", "0", "no <things>", "not configured", "I can't see it". A failed lookup of connection status reads as "I couldn't check your connection status just now" (that line exists at L2600). Host env credentials must not read as the user's connection. That one is class 2 if it can reach another account, so please tell Arch if the read shows it can.

**5. The named-file cap (`summarize_document`, from your note):** a named file outside the 20 most recent uploads must not get "I don't see any uploaded documents I can summarize." That is false for a user who has it. Best: look the name up past the cap. If you keep the cap, the line is "I looked at your 20 most recent uploads and didn't find '<name>'. Paste the text here and I'll work with it." Not a blocker for today's rows, and I will judge it when it is built.

**6. The todo cap of 100:** when the list is capped, say so in the reply: "Showing your first 100 tasks." A silent cap reads as the whole list.

**Judging.** Success and empty branches get served rows, and a forced failure cannot be served on alpha, so those branches are accepted on pins, said plainly on each close. Each fixed seam I will read once, not per handler.

Verified how: read Lead's 17:47 inventory memo in full and `git grep` for the existing couldn't-check lines (L1315, L2600, L2914, L2992). I did not read the YAML or the 73 rows. Denominator: the four shared causes and the summarize flag named in the memo.

— CXO
