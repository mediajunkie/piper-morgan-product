---
from: pa
to: xian (ceo)
cc: cxo, arch, ppm, lead
subject: "One more precise ask on #1463 — the 2-call deconfounder needs its own go, separate from the GPT arm"
date: 2026-08-31
---

PM — smaller follow-up to this morning's OpenAI-credits check-in, not urgent, filing it now so it's
waiting rather than forgotten.

CXO proposed a 2-call follow-up experiment yesterday (re-running item 3's structured payload with a
directive field added, to isolate why it dropped its hedge) and initially said it didn't need a fresh
ask since it was small. **CXO retracted that this morning**: *"size isn't the criterion —
authorization scope is, and PM's go covered a specific packet... it isn't mine to run anyway — it
extends the Claude arm and I'm a Claude. It rides with the GPT arm's authorization, and the ask is
yours."*

So: I've built it into the harness (gated behind an opt-in flag, doesn't touch the original 14-trial
corpus), but it's **2 additional Claude calls, not part of what you already authorized**. When you
top up the OpenAI account for the GPT arm, I wanted to ask cleanly rather than just run it alongside
under the existing yes: **should the deconfounder run at the same time as the GPT arm, or is that a
separate decision?** Either answer is fine — just didn't want to quietly fold a new ask into an old
authorization, which is the exact discipline CXO caught themselves almost undoing.

No deadline on my end either — this rides whenever the GPT arm does.

— PA
