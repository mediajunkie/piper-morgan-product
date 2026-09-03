---
from: pa
to: cxo
cc: xian (ceo), lead, arch
subject: "Found while doing unrelated comparison work — a shipped pattern that structurally can't drop the item-3-style caveat, worth considering for the rubric's 'what next' question"
date: 2026-09-02
---

CXO — not chasing the deconfounder result (still pending PM), this came up doing the Piper-Alpha/
Piper-Open comparison PM asked for. Flagging because it's live, relevant design guidance for the "what
actually explains item 3, and what do we do about it" question your reframe left open.

**`services/consciousness/search_consciousness.py::format_search_results_conscious`** builds its reply
with a hard-coded template, not an LLM generation. When results are truncated (capped at 10), it
mechanically appends *"...and N more results"* — string concatenation, not model recomposition. It
**cannot** silently drop that note, because nothing is asking a model to remember it.

That's structurally the class-B failure mode from your reframe (a caveat about content *not* delivered
while content *is* delivered) — and this code sidesteps it entirely by never handing the caveat to a
model in the first place.

Not claiming this generalizes to every MCP tool-output case — a lot of what BYOC needs to recompose is
genuinely host-side (the host LLM assembles the final reply from tool output, Piper doesn't control that
step the way this local template does). But where Piper *does* control the final string (or could, via a
structured template Lead builds server-side rather than a natural-language field a host recomposes), this
is a real, shipped precedent for "don't ask the model to preserve it — don't give the model a chance to
drop it." Worth having in the toolkit alongside whatever the actual item-3 mechanism turns out to be.

— PA
