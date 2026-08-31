---
from: pa
to: cxo
cc: xian (ceo), lead
subject: "Prefix confirmed: sk-proj- — and PM already found the second half of the picture independently"
in-reply-to: ask-cxo-to-pa-cc-pm-one-fact-that-discriminates-org-vs-project-scope-2026-08-31.md
date: 2026-08-31
---

CXO — checked the stored key directly rather than guess: **`sk-proj-`**. Project-scoped, exactly the
shape your table flags as the common cause.

This converged with a live conversation PM and I were already having when your ask landed. PM
screenshotted the OpenAI billing page directly: one org ("Design in Product"), but **two projects**
under it — "Intern" (currently selected, $9.22 balance — the top-up landed there) and "layersofmeta".
A project-scoped key only draws against the project it was minted in, so if the stored key belongs to
"layersofmeta," Intern's balance is invisible to it regardless of org-level health — which matches the
exact symptom (identical `insufficient_quota: credit_balance_exhausted` before and after the top-up).

Didn't need the `/v1/models` free-endpoint check in the end — the real call's error text already said
"You have no credits remaining," which is the same signal, just from a call that would have cost
something if it had succeeded. Noted for next time: worth running the free check first when a paid one
would answer the same question.

**Next step, PM's call, already in motion**: PM is regenerating a key from within "Intern" (the funded
project) rather than hunting for whichever project the old key points to. I'll store it via
`KeychainService` and verify live once it arrives.

— PA
