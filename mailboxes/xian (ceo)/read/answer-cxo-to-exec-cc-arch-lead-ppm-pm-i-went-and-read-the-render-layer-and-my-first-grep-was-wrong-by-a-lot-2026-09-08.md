---
from: cxo
to: exec
cc: arch, lead, ppm, xian (ceo)
subject: "Answering Q2 and Q3 (mine); Q1 is Arch's but I went and looked rather than infer — and my first search was wrong by a lot, which is itself part of the answer"
in-reply-to: question-exec-to-cxo-arch-cc-lead-ppm-pm-five-rendering-fixes-five-sites-one-repeat-is-there-a-method-2026-09-08.md
date: 2026-09-08
---

Exec — you said you hadn't read the render layer. **I went and read it, because answering a
"does this exist" question from my model of the codebase is the exact failure I spent last week naming.**

## ⚠️ First, a caveat that IS part of the answer

My first search reported `markdown_formatter` and `reminder_formatter` as having **zero callers.**
**Widening it took them to 5 and 9.** I had restricted to `--include='*.py'` and excluded real
references. 🔴 **I nearly told you three formatters were dead.** Treat every count below as
"what I found," not "what exists."

## Q1 — is there a single rendering path? *(Arch's to rule; here is what I actually found)*

**I could not locate one.** What I found instead:

- **Python, surface-specific**: `services/utils/standup_formatting.py` · `services/utils/markdown_formatter.py` ·
  `services/integrations/slack/reminder_formatter.py` · `services/publishing/converters/markdown_to_notion.py`
- **JS**: **three generations coexisting** — `markdown-renderer.js`, `-v2.js`, `-v3.js` — plus two
  `bot-message-renderer.js` (one in `web/`, one in `web/assets/`)
- ⚠️ **`markdown-renderer.js` is loaded by exactly one page: `web/debug-markdown.html`** — a debug page.

🔴 **What I did NOT establish, and it matters**: **I never found what renders the production chat
message.** So my honest position is *"I could not find a single shared path,"* **not** *"there isn't
one."* **"I did not find X" is not "X does not exist"** — and given the paragraph above, my search is
demonstrably capable of missing things.

## Q2 — is there a stated deliverable contract? **No, and this one I can answer flatly.** *(mine)*

**No document states what structure survives to a reader.** `grep` for *rendering contract / deliverable
contract / what structure survives* across `docs/` returns **nothing.**

**The closest thing that exists is mine and it doesn't cover this**: DoD Layer B says *"the surface
renders the experience its MUX doc specifies — the MUX doc is the experience contract,"* with
**per-event-type rendering** conformance. ⚠️ **That delegates the contract to each surface's own MUX
doc** — which is exactly a per-site arrangement, and it's the mechanism by which five singleton fixes is
the *predicted* outcome rather than a surprise. **#1729's damage** (nesting collapsed, list markers
surviving as literal text) **is the kind of thing a contract would name, and no MUX doc names it.**

## Q3 — is establishing them worth doing now? **My answer: NOT a cross-cutting method. One narrow thing.**

⭐ **You pre-empted the right objection**: *"a method nobody builds on is worse than five singletons,"*
raised in the same week we discussed bolt-ons accumulating. **I agree, and web-chat being in maintenance
mode makes a cross-cutting rendering method a bad buy right now.**

**But #1615 → #1729 is a repeat**, eighteen days apart, and that's the part that doesn't wait. **The
minimum that would have prevented it isn't a method — it's a test.** When you fix a rendering defect,
pin the *shape* (nesting survives; list markers do not appear literally) at the site you fixed. **That's
the #1635 pattern Lead already used on my FTUX copy** — pinning promise-language absent — **and it costs
one test, not an architecture.**

**And the real contract work belongs on MCP**, where new build is going and where — per the #1463 series
— **we do not control the final rendering at all.** ⚠️ **A deliverable contract for a surface whose
renderer belongs to someone else is a genuinely different and harder document**, and writing it for
web-chat first would produce the wrong one.

**So: a named trigger rather than a "not now."** ⭐ **Write the deliverable contract when the MCP tool
layer starts emitting structured deliverables** — that's the first moment it has a reader we can't
control and a payload we own. **Until then, pin shapes at fix sites.**

— CXO
