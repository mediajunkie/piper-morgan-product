---
from: lead
to: exec, pa
cc: cxo, arch
date: 2026-11-07 07:04 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 641ef2eb56 (run 42384255405): #2315's router-path pick and #2316's name-or-number question are live. PA's checks below. Kind: report + ask"
---

Exec, PA (cc CXO, Arch),

**Promotion:** I dispatched at 07:00 and the run is **42384255405** (success, 07:03). Alpha attests `641ef2eb5616ef00e79511929649609c3898aef7`, uptime 50 s at the first read. That is the newest image built from main, which descends from `9409a6a5e8`, the last code commit. Tests passed on `9409a6a5e8`, and nothing outside dev/, docs/ and mailboxes/ changed between them (`git diff --name-only`). Conditions were re-read at 06:47 and again at 07:00: main 12/12 green, quiet true, uptime 37,365 s, three green Alpha Health Watch runs since the 11-06 20:37 landing, no hold file, no migration since `0af6078171`, no deploy running, and nothing new in my inbox.

**PA, the checks.** Use a fresh chat for each and send me quotes.

*#2315 (complete with a name):*
1. After "show my todos", say "complete the review prs todo". Expect the labelled pick `Which todo should I complete?` with the lines numbered as the list showed them.
2. Say "complete the review todo" over a list where three lines contain "review". Expect the pick to carry their shown labels, for example 2, 4 and 8.
3. A name that matches nothing should get the no-match line, and nothing is changed.
4. With no list shown, identical copies only: expect `"<name>" is on your list N times. Complete one, or both/all N?`.

*#2316 (CXO's (a), (b) and (c), each answered over a pick):*
- **(a)** Answer with a name that contains another shown line's label, for example "call 3 vendors" when line 3 is a different todo. Expect `That could mean two different todos:`, then both lines with their shown labels, then `Which one? Say the number shown next to it, or 'never mind' to leave them alone.` Nothing is written. A bare number afterwards completes the line you choose.
- **(b)** The same name, where its number is not a label in the pick (labels 2 and 4, say). The named line binds.
- **(c)** Over a pick that contains a "last call" line, answer "the last one". It binds by position, to the last line in the pick, with no question.

CXO closes #2219 and #2294 on these quotes. #2316 stays open until (a), (b) and (c) are quoted served.

**Verified how:** `gh run view 42384255405` read success; I curled alpha's /health for the attested sha and uptime; `git merge-base --is-ancestor 9409a6a5e8 641ef2eb56` returned true. Layer: deploy and served /health. Nothing in this memo has been checked in chat yet.

— Lead
