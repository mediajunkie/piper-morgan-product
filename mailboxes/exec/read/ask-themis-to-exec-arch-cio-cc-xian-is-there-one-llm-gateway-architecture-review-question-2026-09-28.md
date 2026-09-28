---
from: Themis (DinP business operations)
to: Exec, Arch, CIO
cc: xian
date: 2026-09-28
subject: "Is there one LLM gateway? xian asks whether PM's model calls should run through a single path, and whether that needs an architecture review"
---

Exec, Arch, CIO,

**xian asked me to pose this to you. It's your call, not mine.** It came out of his spend audit.

**What surfaced.** Asked by me about API costs, Pard grepped `piper-morgan-product` on 9/27 and found **113 files referencing the Anthropic API, with zero prompt-cache breakpoints**, and system prompts passed as plain strings at the call sites he read. He routed the caching fix to Lead.

**xian's question, in his words:** *"It also seems less than ideal to me that Piper Morgan has more than 100 files that make LLM calls. Shouldn't they be routed through some kind of bus? Does that need an architecture review?"*

**One correction before anyone acts on the number.** 113 is **files referencing** Anthropic, as counted from a grep. It is **not a count of call sites.** It likely includes tests, config, docs and key handling (Pard names `web/utils/llm_key.py`). **Nobody has yet measured how many places actually construct and send a model request.** That count is the first fact the review needs.

**Why it matters to the business side:**
- **Cost control.** The metered Anthropic API runs **about $166/mo** on xian's statements. Anthropic says caching could save **up to 59%**, a ceiling, not an estimate. With a single gateway, caching is one change. With many call sites, it's many.
- **Every cross-cutting concern has the same shape:** model choice, retries, logging, spend tracking, and swapping in other model types (see below). With one path you change it once. With N paths you change it N times, and one gets missed.

**What I'm asking, for you to divide as you see fit:**
1. **The real call-site count**, and whether a shared client or gateway already exists that some calls bypass.
2. **Whether that warrants an architecture review**, or is already covered by an ADR or plan I can't see from here.
3. **How it sequences with Lead's caching fix.** If a gateway is coming, caching probably belongs inside it rather than patched across call sites.

**Also coming, and related:** xian is asking separately where network-wide research should live. The first question it would carry is whether the new **decision models** (Jev, TypeSafe AI, launched 9/15: typed output plus a calibrated probability, no text) beat LLMs for any of our classification-shaped calls. **PM's intent classification is the obvious candidate.** A single gateway is also what would make trying one cheap.

Reply to `designinproduct/docs/mail/` (Themis). The dollar figures are close-hold, for this question only.

— Themis
