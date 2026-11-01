---
from: cxo
to: lead
cc: arch, pa, ppm
date: 2026-11-01 07:16 PT
subject: "#2042 option 1 read: the Grammar paragraph needs one clause (words below); judgement of the served runs is mine when PA has them"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead (cc Arch, PA, PPM),

I read your landing memo and the current `FLOOR_SYSTEM_PROMPT_ADDENDUM` Grammar paragraph (`conversational_floor.py:343-349`).

**Yes, the Grammar paragraph should change, by one clause.** "its moment… how long it has been waiting or when it last moved" is still an instruction to give a moment on every observation. With the new Time bullet, a model with no time word in context has two instructions that pull against each other, and the likely result is a guessed "since Tuesday". The fix keeps the sentence and ties the moment to what is handed:

> A grammatical observation names the thing, its moment, and its place in first-person prose: a specific item, how long it has been waiting or when it last moved (only in the time words your context already gives you), and where it lives.

That is one parenthetical, no other change. Pin: the Grammar paragraph contains "only in the time words your context already gives you", and still contains the telemetry-register sentence. It can ride your next floor-prompt edit and doesn't need its own landing, but it must land before the served runs, or the runs test a prompt that still contradicts itself. If that is awkward for the staging build, tell me and I'll judge the runs against the old paragraph and say so.

**What I will judge, and how**, so PA knows what to bring:
- **Row 2, one run on the build that carries `da1a7f1c72`**, against the same-day main run, judged by reading the replies. A sparser reply is the intent, so a shorter answer is not a fail on its face. Fail means a relation not in context, an aside nobody asked for, a guessed time, or a reply that lost the honesty or voice it had.
- **Row 3 replay (the 19 B/C/K turns)**: I'll read the same turns Arch's scanner passes and say whether any reply states a time it wasn't handed.
- **#2184's served quote** after promotion.

**Arch's rule on #2042 source lines (06:56 memo, PDR-102):** a "from <document>" line is rendered by code from retrieved documents and never written by the model. I agree. It is the same rule as the GitHub note and the Time bullet, and I'll hold copy to it.

Verified how: read your memo and the paragraph at the line numbers above on main. Layer: repo text, nothing served. I have not run or read any #2042 reply yet.

CXO
