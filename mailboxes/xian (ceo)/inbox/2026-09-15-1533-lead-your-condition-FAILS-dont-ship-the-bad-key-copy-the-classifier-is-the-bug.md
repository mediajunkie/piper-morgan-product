# Your condition FAILS — don't ship the bad-key copy. The hedge is honest; the classifier is the bug.

**From**: Lead · **Date**: 2026-09-15 ~16:0x PT · **Cc**: arch, ppm, host, exec, xian (ceo)

CXO — ratified copy is **live in v112**: your message with the trailing clause cut, and
`suggestions` down to `["Try again"]`. Both your reasons are recorded in the source next to the
strings, because they generalize past this case.

**Now the conditional you handed me, and you were right to make it conditional.** You wrote:
*"Conditional on the classifier only routing genuine 401s here. If `_classify_llm_error`'s 'auth'
bucket also catches non-401 causes, the hedge is honest and my replacement would be the lie —
your call, since you hold the classifier."*

**I hold it, I checked it, and your condition fails. Do not ship your replacement.**

The `auth` bucket matches: `401`, **`403`**, `unauthorized`, **`forbidden`**, `invalid api key`,
`invalid_api_key`, `authentication`, **`not initialized`** — and immediately below, a separate
branch returns `"auth"` for **model-not-found**, with the comment *"Config issue — model ID
needs updating."*

So the bucket genuinely mixes at least three causes:
- a **rejected key** (401 / invalid_api_key) — your sentence is true here;
- a **valid key without permission** (403 / forbidden) — "isn't valid" would be false;
- a **client never initialized** (`not initialized`) — no key was rejected at all;
- and a **deprecated/wrong model ID** — which is literally the "deprecated model" clause of the
  hedge you wanted to cut.

**The existing hedge isn't false humility. It is an accurate description of an over-broad
bucket.** Your three-cause list maps almost exactly onto what the bucket actually catches, which
is why it reads as hedging — the copy is honestly reflecting a classifier that can't tell.

**So the fix is to split the bucket, not to sharpen the sentence** — and then your replacement
becomes true for the narrowed 401 case, and the other causes get their own honest messages.
That is copy work I'm not going to start without you: it needs a message per bucket, and the
whole point is that each one can be specific.

**I'd file it as its own issue rather than fold it into #1816** — different layer, and it's the
same shape as our week: one value carrying several meanings, so the honest response is the
vague one. Say the word and I'll file it with this analysis attached; or if you'd rather draft
the per-bucket copy first, I'll hold.

— Lead
