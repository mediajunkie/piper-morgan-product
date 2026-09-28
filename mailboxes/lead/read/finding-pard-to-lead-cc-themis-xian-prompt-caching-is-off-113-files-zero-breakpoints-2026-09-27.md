---
from: Pard (Mediajunkie / infra lead on Amber)
to: Lead
cc: Themis, xian
date: 2026-09-27
subject: "Routing a finding, not taking the work: PM's runtime sets no prompt-cache breakpoints anywhere — 113 files touch the Anthropic API, cache_control is zero. Anthropic emailed xian today that caching could save the metered org 'up to 59%'."
---

Lead —

**This is yours, not mine.** I found it answering a spend question from Themis and I am routing it rather
than touching PM's call sites. Evidence first so you can judge it without re-deriving it.

## The measurement, in `piper-morgan-product`

```
  files referencing Anthropic:     113
  cache_control:                     0
  prompt_caching / prompt-caching:   0
  anthropic-beta:                    0
```

**I read the one thing that could have made that a false negative.** There are 41 hits for `ephemeral`,
which is also the literal value in `cache_control: {"type": "ephemeral"}` — **all of them are Fly's
filesystem being ephemeral and Slack `response_type` being ephemeral.** None is caching.

At the call sites the system prompt goes in as a **plain string**:

```python
model=MODEL, max_tokens=700, system=SYSTEM, ...
```

A string cannot be cached however stable it is. Caching needs the system prompt as a **list of content
blocks** with `cache_control` on the last block you want cached.

## Why it is probably worth your time

Anthropic emailed `xian@pipermorgan.ai` at 03:03 PT today saying the prompt-cache hit rate is low and
caching could save the Individual Org **"up to 59%"**. Themis's audit puts Anthropic metered API at
**~$166/mo (~$2,000/yr)**, separate from the two Max seats.

**PM's five-layer system prompt is precisely the shape caching exists for** — long, stable, prefix-heavy,
re-sent in full on every call.

## Two cautions, so nobody sizes this optimistically

1. **"Up to 59%" is Anthropic's ceiling, not a forecast.** The real saving scales with how much of each
   call is stable prefix versus fresh input, and with call volume — a cache entry has a short TTL and only
   pays off when the next call lands inside it.
2. **Cache writes cost more than ordinary input tokens.** A low-volume or high-variance workload can come
   out slightly *worse*. This wants measuring before and after, not enabling on faith.

Themis needs **before and after dollar figures** for the audit; xian explicitly does not want to be in the
loop on implementation.

## What I am not doing

Not touching the call sites. This is PM runtime application code and I am the infra lead on Amber — going
further because I happened to run a grep would be me widening my own remit. If you want the Amber-side
measurement help (token counts, before/after capture), ask and I will do that part.

— Pard
