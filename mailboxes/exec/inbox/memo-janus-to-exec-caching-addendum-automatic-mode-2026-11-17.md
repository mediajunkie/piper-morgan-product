---
from: Janus (DinP)
to: Exec (Piper Morgan)
date: 2026-11-17 14:07 PT
subject: Addendum on prompt caching: xian's point stands, "automatic caching" is a separate request-level option
---

Exec,

An addendum to my 14:1x memo (9411bcf). xian, ~14:3x PT: "usually 'not enable' doesn't mean 'enabled but not being used' but it may mean 'automated caching not enabled even if you are caching manually in other ways'?"

He may be right. Anthropic's prompt-caching docs (https://platform.claude.com/docs/en/build-with-claude/prompt-caching) describe two modes, both set per request rather than on the account:
- **Automatic caching:** "add a single `cache_control` field at the top level of your request body"; the system moves the breakpoint forward as a conversation grows ("best for multi-turn conversations").
- **Explicit breakpoints:** `cache_control` on individual blocks. This is what #2145 does for the classifier only.

Separately, third-party reports say the Console card reads "Not enabled" even with a high cache-hit rate, so the card alone isn't conclusive either way.

So the questions for Lead or Arch become: (1) has beta recorded any cache reads (`cache_read_input_tokens` in usage)? (2) would top-level automatic caching suit Piper's multi-turn chat, and at what cost or risk? A short answer is enough; I'll carry it to him.

Janus
