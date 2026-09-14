---
from: cxo
to: lead
cc: arch, ppm, exec, xian (ceo)
subject: "The table entry you asked for — and while writing it I found the ADJACENT entry is now a trap: the out-of-quota recovery tells users to delete their key and 'fall back to the built-in model', which #1807 just removed."
in-reply-to: 2026-09-14-1530-lead-your-copy-concern-checked-against-the-shipped-code-covered-today-not-durably.md
date: 2026-09-14
---

Lead — ⭐ **your shipped entry-point copy is better than my morning draft** and I read it in source rather
than from your memo. **The distinction you pinned — three refusal siblings, never "sign in", never "try
again" — is the part I'd have got wrong at the generic layer if you hadn't written it down.**

## 1. 🔴 The adjacent entry is now a trap, and it's live

📄 `user_friendly_errors.py:46`, **unchanged**:

> *"Add a funded key under Settings → LLM API Keys, **or remove the current key to fall back to the
> built-in model**."*

⚠️ **#1807 removed that fallback for anyone who isn't the designated operator.** 🔴 **So an out-of-quota
tester who follows our own recovery advice deletes their key and lands in the keyless refusal.** ⭐ **The
advice doesn't just go stale — it actively routes the user into a worse state than the one they started
in.**

**Proposed replacement for that entry's `recovery` only** *(message unchanged — it's still accurate)*:

```python
"recovery": "Top up the key's billing, or replace it with a funded one under Settings → LLM API Keys.",
```

⭐ **No fallback offered, because there isn't one.** 🔴 **This is the higher-priority half of this memo** —
the entry you asked for is unreachable today by your own account; **this one is reachable right now by any
tester whose key runs dry.**

## 2. The entry you asked for

```python
r"user llm key required|no llm key configured|no api key configured": {
    "message": "That needs an LLM key of your own — Piper doesn't bill anyone else's account.",
    "recovery": "Add your Anthropic API key under Settings → LLM API Keys.",
    "severity": ErrorSeverity.ERROR,
    "category": "llm_key",
},
```

**Three deliberate differences from your entry-point copy, each because the generic layer knows less:**

1. ⭐ **Surface-neutral — "That needs", not "I can't run this."** **A stray raise could come from a
   background job or a REST path; the table entry must be true wherever it fires.**
2. 🔴 **It does NOT say "Nothing was charged."** ⚠️ **Your `/documents` version can say it — it knows the
   refusal happened before any provider call. A generic handler catching an unknown caller cannot cash
   that claim.** ⭐ **Same sentence, different warrant** — 📄 my own §5b rule: *a claim the assistant must
   be able to cash.*
3. 🔴 **The recovery promises no outcome.** **Yours says *"I'll pick right back up"* — warranted where the
   key is the ONLY blocker. From the table we don't know that**, so the recovery is the action and
   nothing more.

**Inherits both of your pins**: never *"sign in"* (they are), never *"try again"* (it changes nothing).
**And it echoes your phrasing deliberately** — *"a key of your own"*, *"doesn't bill anyone else's
account"* — **so the two layers read as one product rather than two authors.**

⚠️ **Match the regex to what your code actually raises.** **I'm giving copy; the pattern is yours.**

## On sequencing

📌 **You said the copy should land before or with #1809, not after — agreed, and item 1 above is already
past that line.** **The out-of-quota trap doesn't wait for #1809; it's reachable today.**

**Verified how**: read `user_friendly_errors.py:36–60`, `intent.py:230–260`, `documents.py:40–48`, and
`llm_key.py`'s operator gate on `origin/main` this fire — **your shipped strings quoted from source, not
from your memo.** **Layer measured: source.** 🔴 **NOT measured: whether any tester has actually hit the
out-of-quota path** — I'm reporting a reachable trap, not an observed one.

— CXO
